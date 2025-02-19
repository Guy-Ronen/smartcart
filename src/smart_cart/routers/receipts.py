from typing import List

from fastapi import APIRouter, HTTPException, Request, status

from smart_cart.repositories.receipts import ReceiptRepository
from smart_cart.schemas.receipt import ReceiptSchema

router = APIRouter()


@router.post("/receipts", response_model=ReceiptSchema, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: ReceiptSchema, request: Request):
    receipt.user_id = request.state.user.sub
    try:
        return ReceiptRepository.create_receipt(receipt)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create receipt")


@router.get("/receipts/{receipt_id}", response_model=ReceiptSchema)
def get_receipt(receipt_id: str, request: Request):
    user_id = request.state.user.sub

    receipt = ReceiptRepository.get_user_receipt(user_id, receipt_id)
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    return receipt


@router.get("/receipts", response_model=List[ReceiptSchema])
def get_receipts(request: Request):
    user_id = request.state.user.sub
    receipts = ReceiptRepository.get_receipts_by_user(user_id)
    return receipts


@router.put("/receipts/{receipt_id}", response_model=ReceiptSchema)
def update_receipt(receipt_id: str, receipt: ReceiptSchema, request: Request):
    user_id = request.state.user.sub

    existing_receipt = ReceiptRepository.get_user_receipt(user_id, receipt_id)
    if not existing_receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    updated_data = existing_receipt.model_dump()
    updated_data.update(receipt.model_dump(exclude_unset=True))
    updated_data["user_id"] = user_id
    updated_data["receipt_id"] = receipt_id

    return ReceiptRepository.update_receipt(ReceiptSchema(**updated_data))


@router.delete("/receipts/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: str, request: Request):
    user_id = request.state.user.sub

    receipt = ReceiptRepository.get_user_receipt(user_id, receipt_id)
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    ReceiptRepository.delete_receipt(receipt_id)
