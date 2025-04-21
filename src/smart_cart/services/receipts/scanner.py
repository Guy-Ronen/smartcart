import datetime
import time
import uuid
from typing import List, Optional

import requests
from fastapi import HTTPException, UploadFile

from smart_cart.schemas.receipt import Category, Currency, Item, Market, ReceiptSchema
from smart_cart.schemas.response import LineItem, ResponseSchema
from smart_cart.services.receipts.categorizer import CATEGORY_MAP
from smart_cart.utils.settings import settings


class ReceiptScanner:
    def __init__(self, image: Optional[UploadFile] = None):
        self.image = image
        self.process_endpoint = settings.tabs_scanner.process_endpoint
        self.result_endpoint = settings.tabs_scanner.result_endpoint
        self.headers = {"apikey": settings.tabs_scanner.api_key}

    def call_process(self):
        payload = {"documentType": "receipt", "decimalPlaces": "2", "region": "de"}

        files = {"file": (self.image.filename, self.image.file, self.image.content_type)}
        response = requests.post(self.process_endpoint, files=files, data=payload, headers=self.headers)
        result = response.json()

        if result.get("status") == "success" and result.get("token"):
            return result["token"]
        raise HTTPException(status_code=400, detail=f"Error processing receipt: {result}")

    def call_result(self, token):
        url = f"{self.result_endpoint}/{token}"

        while True:
            response = requests.get(url, headers=self.headers)
            result = response.json()

            if result.get("status") == "done" and "result" in result:
                return ResponseSchema(**result)
            elif result.get("status") == "error":
                raise HTTPException(status_code=400, detail=f"Error retrieving result: {result}")

            time.sleep(1)

    def process_and_get_result(self, user_id: Optional[str] = None) -> ReceiptSchema:
        try:
            token = self.call_process()
            result = self.call_result(token)
            receipt = self.parse_response_to_receipt(result, user_id)
            return receipt
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def parse_response_to_receipt(self, response: ResponseSchema, user_id: Optional[str] = None) -> ReceiptSchema:
        result = response.result

        return ReceiptSchema(
            receipt_id=str(uuid.uuid4()),
            user_id=user_id or "",
            items=self._parse_items(result.lineItems),
            total=result.total,
            date=self._parse_date_to_timestamp(result.dateISO),
            currency=Currency(result.currency) if result.currency else Currency.EUR,
            market=self._map_market(result.establishment),
        )

    def _parse_date_to_timestamp(self, date_str: datetime.datetime) -> int:
        return int(date_str.timestamp())

    def _parse_items(self, line_items: List[LineItem]) -> List[Item]:
        items = []
        for item in line_items:
            name = item.descClean or item.desc or "Unknown"
            total = item.lineTotal or 0.0
            price = item.price or 0.0
            quantity = item.qty or 1

            if price == 0.0 and quantity > 0:
                price = total / quantity

            category = self._detect_category(name)

            items.append(
                Item(
                    name=name,
                    price=round(price, 2),
                    quantity=quantity,
                    total=round(total, 2),
                    category=category,
                )
            )
        return items

    def _detect_category(self, name: str) -> Category:
        lower_name = name.lower()

        for keyword, category in CATEGORY_MAP.items():
            if keyword.lower() in lower_name:
                return category

        return Category.OTHER

    def _map_market(self, name: Optional[str]) -> Market:
        name = (name or "").upper()

        for market in Market:
            if market.name in name:
                return market

        return Market.OTHER
