import time

import requests
from fastapi import HTTPException, UploadFile

from smart_cart.schemas.response import ResponseSchema
from smart_cart.utils.settings import settings


class ReceiptProcessor:
    def __init__(self, image: UploadFile):
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

    def process_and_get_result(self):
        try:
            token = self.call_process()
            return self.call_result(token)
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            # Convert other exceptions to 500 errors
            raise HTTPException(status_code=500, detail=str(e))
