from smart_cart.schemas.receipt import Category

VEGETABLES = {
    "SUPPENGRUEN": Category.VEGETABLES,
    "Oliven": Category.VEGETABLES,
}

FRUITS = {
    "Saftorangen": Category.FRUITS,
    "Banane": Category.FRUITS,
    "Apfel": Category.FRUITS,
    "Pflaume": Category.FRUITS,
    "TRUE FRUITS": Category.FRUITS,
}

DAIRY = {
    "Milch": Category.DAIRY,
    "YOGHURT": Category.DAIRY,
}

BAKED = {
    "BROT": Category.BAKED,
    "WEIZENBROETCHEN": Category.BAKED,
}

SWEETS = {
    "Schok": Category.SWEETS,
    "Chips": Category.SWEETS,
}

COSMETICS = {
    "HAUTKLAR": Category.COSMETICS,
    "essence": Category.COSMETICS,
    "Nachfüll": Category.COSMETICS,
    "Tücher": Category.COSMETICS,
    "compact powder": Category.COSMETICS,
    "nailpol": Category.COSMETICS,
}

ALCOHOL = {
    "PILS": Category.ALCOHOL,
    "Krombacher": Category.ALCOHOL,
    "Bier": Category.ALCOHOL,
}

CANNED = {
    "Leergut": Category.CANNED,
}

SPICES = {
    "ESSIG": Category.SPICES,
}

CATEGORY_MAP = {
    **VEGETABLES,
    **FRUITS,
    **DAIRY,
    **BAKED,
    **SWEETS,
    **COSMETICS,
    **ALCOHOL,
    **CANNED,
    **SPICES,
}
