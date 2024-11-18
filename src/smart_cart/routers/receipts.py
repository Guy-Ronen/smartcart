from fastapi import APIRouter, HTTPException, status

from smart_cart.models.receipt import Receipt
from smart_cart.repositories.receipts import ReceiptRepository

router = APIRouter()


@router.post("/receipts", response_model=Receipt, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: Receipt):
    try:
        ReceiptRepository.create_receipt(receipt)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create receipt")
    return receipt
