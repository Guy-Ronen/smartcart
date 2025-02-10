import enum
from typing import List

from pydantic import BaseModel


class Currency(str, enum.Enum):
    EUR = "EUR"


class Market(str, enum.Enum):
    ALDI = "ALDI"
    LIDL = "LIDL"
    NETTO = "NETTO"
    REWE = "REWE"
    EDEKA = "EDEKA"
    KAUFLAND = "KAUFLAND"
    PENNY = "PENNY"
    REAL = "REAL"


class Category(str, enum.Enum):
    FRUITS = "FRUITS"
    VEGETABLES = "VEGETABLES"
    MEAT = "MEAT"
    FISH = "FISH"
    DAIRY = "DAIRY"
    BREAD = "BREAD"
    SWEETS = "SWEETS"
    DRINKS = "DRINKS"
    ALCOHOL = "ALCOHOL"
    CANNED = "CANNED"
    FROZEN = "FROZEN"
    OTHER = "OTHER"


class Item(BaseModel):
    name: str
    price: float
    quantity: int
    total: float
    category: Category


class ReceiptSchema(BaseModel):
    receipt_id: str
    user_id: str
    items: List[Item]
    total: float
    date: int
    currency: Currency
    market: Market
