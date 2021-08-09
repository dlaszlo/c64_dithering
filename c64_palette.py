# https://github.com/Hammarberg/pixcen/blob/master/C64Col.cpp

def rgb(val):
    return (
        float(val & 255),
        float((val >> 8) & 255),
        float((val >> 16) & 255)
    )


PALETTE = [
    {
        "name": "default",
        "colors": [
            rgb(0x000000),
            rgb(0xffffff),
            rgb(0x894036),
            rgb(0x7abfc7),
            rgb(0x8a46ae),
            rgb(0x68a941),
            rgb(0x3e31a2),
            rgb(0xd0dc71),
            rgb(0x905f25),
            rgb(0x5c4700),
            rgb(0xbb776d),
            rgb(0x555555),
            rgb(0x808080),
            rgb(0xacea88),
            rgb(0x7c70da),
            rgb(0xababab)
        ]
    },
    {
        "name": "Pepto",
        "colors": [
            rgb(0x000000),
            rgb(0xFFFFFF),
            rgb(0x68372B),
            rgb(0x70A4B2),
            rgb(0x6F3D86),
            rgb(0x588D43),
            rgb(0x352879),
            rgb(0xB8C76F),
            rgb(0x6F4F25),
            rgb(0x433900),
            rgb(0x9A6759),
            rgb(0x444444),
            rgb(0x6C6C6C),
            rgb(0x9AD284),
            rgb(0x6C5EB5),
            rgb(0x959595)
        ],
    },
    {
        "name": "c64hq",
        "colors": [
            rgb(0x0A0A0A),
            rgb(0xFFF8FF),
            rgb(0x851F02),
            rgb(0x65CDA8),
            rgb(0xA73B9F),
            rgb(0x4DAB19),
            rgb(0x1A0C92),
            rgb(0xEBE353),
            rgb(0xA94B02),
            rgb(0x441E00),
            rgb(0xD28074),
            rgb(0x464646),
            rgb(0x8B8B8B),
            rgb(0x8EF68E),
            rgb(0x4D91D1),
            rgb(0xBABABA)
        ]
    },
    {
        "name": "c64s",
        "colors": [
            rgb(0x000000),
            rgb(0xFCFCFC),
            rgb(0xA80000),
            rgb(0x54FCFC),
            rgb(0xA800A8),
            rgb(0x00A800),
            rgb(0x0000A8),
            rgb(0xFCFC00),
            rgb(0xA85400),
            rgb(0x802C00),
            rgb(0xFC5454),
            rgb(0x545454),
            rgb(0x808080),
            rgb(0x54FC54),
            rgb(0x5454FC),
            rgb(0xA8A8A8)
        ]
    },
    {
        "name": "ccs64",
        "colors": [
            rgb(0x101010),
            rgb(0xFFFFFF),
            rgb(0xE04040),
            rgb(0x60FFFF),
            rgb(0xE060E0),
            rgb(0x40E040),
            rgb(0x4040E0),
            rgb(0xFFFF40),
            rgb(0xE0A040),
            rgb(0x9C7448),
            rgb(0xFFA0A0),
            rgb(0x545454),
            rgb(0x888888),
            rgb(0xA0FFA0),
            rgb(0xA0A0FF),
            rgb(0xC0C0C0)
        ]
    },
    {
        "name": "frodo",
        "colors": [
            rgb(0x000000),
            rgb(0xFFFFFF),
            rgb(0xCC0000),
            rgb(0x00FFCC),
            rgb(0xFF00FF),
            rgb(0x00CC00),
            rgb(0x0000CC),
            rgb(0xFFFF00),
            rgb(0xFF8800),
            rgb(0x884400),
            rgb(0xFF8888),
            rgb(0x444444),
            rgb(0x888888),
            rgb(0x88FF88),
            rgb(0x8888FF),
            rgb(0xCCCCCC)
        ]
    },
    {
        "name": "godot",
        "colors": [
            rgb(0x000000),
            rgb(0xFFFFFF),
            rgb(0x880000),
            rgb(0xAAFFEE),
            rgb(0xCC44CC),
            rgb(0x00CC55),
            rgb(0x0000AA),
            rgb(0xEEEE77),
            rgb(0xDD8855),
            rgb(0x664400),
            rgb(0xFE7777),
            rgb(0x333333),
            rgb(0x777777),
            rgb(0xAAFF66),
            rgb(0x0088FF),
            rgb(0xBBBBBB)
        ]
    },
    {
        "name": "pc64",
        "colors": [
            rgb(0x212121),
            rgb(0xFFFFFF),
            rgb(0xB52121),
            rgb(0x73FFFF),
            rgb(0xB521B5),
            rgb(0x21B521),
            rgb(0x2121B5),
            rgb(0xFFFF21),
            rgb(0xB57321),
            rgb(0x944221),
            rgb(0xFF7373),
            rgb(0x737373),
            rgb(0x949494),
            rgb(0x73FF73),
            rgb(0x7373FF),
            rgb(0xB5B5B5)
        ]
    },
    {
        "name": "colodore",
        "colors": [
            rgb(0x000000),
            rgb(0xffffff),
            rgb(0x813338),
            rgb(0x75cec8),
            rgb(0x8e3c97),
            rgb(0x56ac4d),
            rgb(0x2e2c9b),
            rgb(0xedf171),
            rgb(0x8e5029),
            rgb(0x553800),
            rgb(0xc46c71),
            rgb(0x4a4a4a),
            rgb(0x7b7b7b),
            rgb(0xa9ff9f),
            rgb(0x706deb),
            rgb(0xb2b2b2)
        ]
    },
    {
        "name": "PALette",
        "colors": [
            rgb(0x000000),
            rgb(0xd5d5d5),
            rgb(0x72352c),
            rgb(0x659fa6),
            rgb(0x733a91),
            rgb(0x568d35),
            rgb(0x2e237d),
            rgb(0xaeb75e),
            rgb(0x774f1e),
            rgb(0x4b3c00),
            rgb(0x9c635a),
            rgb(0x474747),
            rgb(0x6b6b6b),
            rgb(0x8fc271),
            rgb(0x675db6),
            rgb(0x8f8f8f)
        ]
    }
]


def palettes():
    ret = ""
    for m in PALETTE:
        ret += "" if len(ret) == 0 else ", "
        ret += m["name"]
    return ret


def get_palette(name: str):
    ret = None
    for m in PALETTE:
        if m["name"].lower() == name.lower():
            ret = m
            break
    if ret is None:
        raise ValueError(f"Invalid palette: {name}. Valid palettes: {palettes()}. Default model: Pepto")
    return ret
