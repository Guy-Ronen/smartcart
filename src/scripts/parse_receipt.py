from pathlib import Path

from fastapi import UploadFile

from smart_cart.parser.processor import ReceiptProcessor
from smart_cart.schemas.response import ResponseSchema

FILE_NAME = "IMG6.jpg"
receipt_image = Path(__file__).parent.parent / "smart_cart/parser/img" / FILE_NAME
results_path = (Path(__file__).parent.parent / "smart_cart/parser/results" / FILE_NAME).with_suffix(".json")

with open(receipt_image, "rb") as file:
    upload_file = UploadFile(file=file, filename=FILE_NAME, headers={"content-type": "image/jpeg"})
    processor = ReceiptProcessor(upload_file)

    print("Processing receipt...")
    result: ResponseSchema = processor.process_and_get_result()

    with open(results_path, "w", encoding="utf-8") as file:
        file.write(result.model_dump_json(indent=4))

    print(f"Receipt:\n{result.model_dump_json(indent=4)}")
    print(f"Results saved to: {results_path}")

    print("Done!")
