from fastapi import APIRouter, HTTPException, status

from smart_cart.repositories.receipts import ReceiptRepository
from smart_cart.schemas.receipt import ReceiptSchema

router = APIRouter()


@router.post("/receipts", response_model=ReceiptSchema, status_code=status.HTTP_201_CREATED)
def create_receipt(receipt: ReceiptSchema):
    try:
        ReceiptRepository.create_receipt(receipt)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create receipt")
    return receipt
