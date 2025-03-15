import json
import time
import requests
from pathlib import Path
from smart_cart.utils.settings import settings
from smart_cart.schemas.response import ResponseSchema


class Processor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.receipt_image = (Path(__file__).parent.parent / "smart_cart/parser/img" / file_name).with_suffix(".jpg")
        self.results_path = (Path(__file__).parent.parent / "smart_cart/parser/results" / file_name).with_suffix(
            ".json"
        )
        self.endpoint = "https://api.tabscanner.com/api/2/process"
        self.result_url = "https://api.tabscanner.com/api/result/"
        self.headers = {"apikey": settings.tabs_scanner_api_key}

    def validate_image(self):
        if not self.receipt_image.exists():
            raise FileNotFoundError(f"Receipt image not found: {self.receipt_image}")

    def call_process(self):
        self.validate_image()
        payload = {"documentType": "receipt"}

        with self.receipt_image.open("rb") as image_file:
            files = {"file": image_file}
            response = requests.post(self.endpoint, files=files, data=payload, headers=self.headers)

        result = response.json()

        if result.get("status") == "success" and result.get("token"):
            return result["token"]
        raise Exception(f"Error processing receipt: {result}")

    def call_result(self, token):
        url = f"{self.result_url}{token}"

        while True:
            response = requests.get(url, headers=self.headers)
            result = response.json()

            if result.get("status") == "done" and "result" in result:
                return result
            elif result.get("status") == "error":
                raise Exception(f"Error retrieving result: {result}")

            time.sleep(1)

    def process_and_get_result(self):
        try:
            token = self.call_process()
            result = self.call_result(token)

            self.results_path.parent.mkdir(parents=True, exist_ok=True)
            with self.results_path.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)

            return result
        except Exception as e:
            return None


if __name__ == "__main__":
    processor = Processor("IMG6")
    processor.process_and_get_result()
