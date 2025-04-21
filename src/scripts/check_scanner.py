import json
from pathlib import Path

from smart_cart.schemas.response import ResponseSchema
from smart_cart.services.receipts.scanner import ReceiptScanner

receipts_path = Path(__file__).parent.parent / "tests" / "services" / "receipts" / "results"


for receipt_file in receipts_path.glob("*.json"):
    print(f"Processing receipt: {receipt_file.name}")
    with open(receipt_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        response = ResponseSchema(**data)

        scanner = ReceiptScanner(image=None)
        result = scanner.parse_response_to_receipt(response, user_id="test-user")

        result_dict = result.model_dump()

        print("Parsed receipt data:")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))

print("✅ All receipts parsed successfully.")
