from typing import List

from fastapi import APIRouter, Request, status

from smart_cart.repositories.receipts import ReceiptRepository
from smart_cart.schemas.receipt import ReceiptSchema

router = APIRouter()


@router.post("/receipts", response_model=ReceiptSchema, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: ReceiptSchema, request: Request):
    receipt = receipt.model_copy(update={"user_id": request.state.user.sub})
    return ReceiptRepository.create_receipt(receipt)


@router.get("/receipts/{receipt_id}", response_model=ReceiptSchema)
def get_receipt(receipt_id: str, request: Request):
    return ReceiptRepository.get_user_receipt(request.state.user.sub, receipt_id)


@router.get("/receipts", response_model=List[ReceiptSchema])
def get_receipts(request: Request):
    return ReceiptRepository.get_receipts_by_user(request.state.user.sub)


@router.put("/receipts/{receipt_id}", response_model=ReceiptSchema)
def update_receipt(receipt_id: str, receipt: ReceiptSchema, request: Request):
    return ReceiptRepository.update_receipt(request.state.user.sub, receipt_id, receipt)


@router.delete("/receipts/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: str, request: Request):
    ReceiptRepository.delete_receipt(request.state.user.sub, receipt_id)
