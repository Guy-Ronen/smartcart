from typing import List, Optional

from fastapi import APIRouter, File, Query, Request, UploadFile, status

from smart_cart.parser.processor import ReceiptProcessor
from smart_cart.repositories.receipts import ReceiptRepository
from smart_cart.schemas.receipt import ReceiptSchema
from smart_cart.schemas.response import ResponseSchema

router = APIRouter()


@router.post("/receipts", response_model=ReceiptSchema, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: ReceiptSchema, request: Request):
    receipt = receipt.model_copy(update={"user_id": request.state.user.sub})
    return ReceiptRepository.create_receipt(receipt)


@router.get("/receipts/{receipt_id}", response_model=ReceiptSchema)
def get_receipt(receipt_id: str, request: Request):
    return ReceiptRepository.get_receipt(request.state.user.sub, receipt_id)


@router.get("/receipts", response_model=List[ReceiptSchema])
def get_receipts(
    request: Request,
    month: Optional[int] = Query(None, ge=1, le=12, description="Month (1-12)"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="Year (2000-2100)"),
):
    user_id = request.state.user.sub

    if month and year:
        return ReceiptRepository.get_receipts_by_month_and_year(user_id, month, year)

    return ReceiptRepository.get_receipts(user_id)


@router.put("/receipts/{receipt_id}", response_model=ReceiptSchema)
def update_receipt(receipt_id: str, receipt: ReceiptSchema, request: Request):
    return ReceiptRepository.update_receipt(request.state.user.sub, receipt_id, receipt)


@router.delete("/receipts/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: str, request: Request):
    ReceiptRepository.delete_receipt(request.state.user.sub, receipt_id)


@router.post("/process_receipt", response_model=ResponseSchema)
def process_receipt(file: UploadFile = File(...)):
    processor = ReceiptProcessor(file)
    return processor.process_and_get_result()
