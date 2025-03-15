from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class LineItem(BaseModel):
    qty: int
    desc: str
    unit: Optional[str] = ""
    price: float
    symbols: List[str]
    discount: float
    lineType: Optional[str] = ""
    descClean: str
    lineTotal: float
    productCode: Optional[str] = ""
    customFields: Dict[str, str]


class AddressNorm(BaseModel):
    city: Optional[str] = ""
    state: Optional[str] = ""
    number: Optional[str] = ""
    street: Optional[str] = ""
    suburb: Optional[str] = ""
    country: Optional[str] = ""
    building: Optional[str] = ""
    postcode: Optional[str] = ""


class CustomFields(BaseModel):
    URL: Optional[str] = ""
    Country: Optional[str] = ""
    StoreID: Optional[str] = ""
    Currency: Optional[str] = ""
    VATNumber: Optional[str] = ""
    ExpenseType: Optional[str] = ""
    PaymentMethod: Optional[str] = ""
    CardLast4Digits: Optional[str] = ""


class ReceiptResult(BaseModel):
    establishment: str
    validatedEstablishment: bool
    date: str
    total: float
    url: Optional[str] = ""
    phoneNumber: Optional[str] = ""
    paymentMethod: Optional[str] = ""
    address: Optional[str] = ""
    cash: float
    change: float
    validatedTotal: bool
    subTotal: float
    validatedSubTotal: bool
    tax: float
    tip: float
    taxes: List
    serviceCharges: List
    discount: float
    rounding: float
    discounts: List
    lineItems: List[LineItem]
    summaryItems: List[LineItem]
    subTotalConfidence: float
    taxesConfidence: List
    serviceChargeConfidences: List
    discountConfidences: List
    totalConfidence: float
    dateConfidence: float
    establishmentConfidence: float
    tipConfidence: float
    cashConfidence: float
    changeConfidence: float
    roundingConfidence: float
    customFields: CustomFields
    documentType: str
    currency: str
    barcodes: List
    dateISO: datetime
    addressNorm: AddressNorm
    expenseType: str
    otherData: List


class ResponseSchema(BaseModel):
    message: str
    status: str
    status_code: int
    result: ReceiptResult
    success: bool
    code: int
