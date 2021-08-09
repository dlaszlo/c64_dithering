# https://tannerhelland.com/2012/12/28/dithering-eleven-algorithms-source-code.html

FLOYD_STEINBERG = {
    "name": "floyd_steinberg",
    "weight": 1.0 / 16.0,
    "pattern": [
        (0, 1, 7.0),
        (1, -1, 3.0),
        (1, 0, 5.0),
        (1, 1, 1.0),
    ]
}

JARVIS_JUDICE_NINKE = {
    "name": "jarvis_judice_ninke",
    "weight": 1.0 / 48.0,
    "pattern": [
        (0, 1, 7.0),
        (0, 2, 5.0),
        (1, -2, 3.0),
        (1, -1, 5.0),
        (1, 0, 7.0),
        (1, 1, 5.0),
        (1, 2, 3.0),
        (2, -2, 1.0),
        (2, -1, 3.0),
        (2, 0, 5.0),
        (2, 1, 3.0),
        (2, 2, 1.0)
    ]
}

STUCKI = {
    "name": "stucki",
    "weight": 1.0 / 42.0,
    "pattern": [
        (0, 1, 8.0),
        (0, 2, 4.0),
        (1, -2, 2.0),
        (1, -1, 4.0),
        (1, 0, 8.0),
        (1, 1, 4.0),
        (1, 2, 2.0),
        (2, -2, 1.0),
        (2, -1, 2.0),
        (2, 0, 4.0),
        (2, 1, 2.0),
        (2, 2, 1.0)
    ]
}

ATKINSON = {
    "name": "atkinson",
    "weight": 1.0 / 8.0,
    "pattern": [
        (0, 1, 1.0),
        (0, 2, 1.0),
        (1, -1, 1.0),
        (1, 0, 1.0),
        (1, 1, 1.0),
        (2, 0, 1.0)
    ]
}

BURKES = {
    "name": "burkes",
    "weight": 1.0 / 32.0,
    "pattern": [
        (0, 1, 8.0),
        (0, 2, 4.0),
        (1, -2, 2.0),
        (1, -1, 4.0),
        (1, 0, 8.0),
        (1, 1, 4.0),
        (1, 2, 2.0)
    ]
}

SIERRA = {
    "name": "sierra",
    "weight": 1.0 / 32.0,
    "pattern": [
        (0, 1, 5.0),
        (0, 2, 3.0),
        (1, -2, 2.0),
        (1, -1, 4.0),
        (1, 0, 5.0),
        (1, 1, 4.0),
        (1, 2, 2.0),
        (2, -1, 2.0),
        (2, 0, 3.0),
        (2, 1, 2.0)
    ]
}

TWO_ROW_SIERRA = {
    "name": "two_row_sierra",
    "weight": 1.0 / 16.0,
    "pattern": [
        (0, 1, 4.0),
        (0, 2, 3.0),
        (1, -2, 1.0),
        (1, -1, 2.0),
        (1, 0, 3.0),
        (1, 1, 2.0),
        (1, 2, 1.0)
    ]
}

SIERRA_LITE = {
    "name": "sierra_lite",
    "weight": 1.0 / 4.0,
    "pattern": [
        (0, 1, 2.0),
        (1, -1, 1.0),
        (1, 0, 1.0)
    ]
}

DITHERING_MODELS = [
    FLOYD_STEINBERG, JARVIS_JUDICE_NINKE, STUCKI, ATKINSON, BURKES, SIERRA, TWO_ROW_SIERRA, SIERRA_LITE
]


def dithering_models():
    ret = ""
    for m in DITHERING_MODELS:
        ret += "" if len(ret) == 0 else ", "
        ret += m["name"]
    return ret


def get_dithering_model(name: str):
    ret = None
    for m in DITHERING_MODELS:
        if m["name"].lower() == name.lower():
            ret = m
            break
    if ret is None:
        raise ValueError(f"Invalid dithering model: {name}. Valid models: {dithering_models()}. Default model: sierra")
    return ret
