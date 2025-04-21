import json
from pathlib import Path

from smart_cart.parser.processor import ReceiptProcessor
from smart_cart.schemas.response import ResponseSchema

receipts_path = Path(__file__).parent.parent / "tests" / "parser" / "receipts"

for receipt_file in receipts_path.glob("*.json"):
    print(f"Processing receipt: {receipt_file.name}")
    with open(receipt_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        response = ResponseSchema(**data)

        processor = ReceiptProcessor(image=None)
        result = processor.parse_response_to_receipt(response, user_id="test-user")

        result_dict = result.model_dump()

        print("Parsed receipt data:")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))

print("✅ All receipts parsed successfully.")
