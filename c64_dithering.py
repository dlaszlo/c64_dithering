import argparse

import cv2

W1 = 7 / 16.0
W2 = 3 / 16.0
W3 = 5 / 16.0
W4 = 1 / 16.0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (43, 55, 104)
CYAN = (178, 164, 112)
PURPLE = (134, 61, 111)
GREEN = (67, 141, 88)
BLUE = (121, 40, 53)
YELLOW = (111, 199, 184)
ORANGE = (37, 79, 111)
BROWN = (0, 57, 67)
LIGHT_RED = (89, 103, 154)
DARK_GREY = (68, 68, 68)
GREY = (108, 108, 108)
LIGHT_GREEN = (132, 210, 154)
LIGHT_BLUE = (181, 94, 108)
LIGHT_GREY = (149, 149, 149)

COLORS = [BLACK, WHITE, RED, CYAN,
          PURPLE, GREEN, BLUE, YELLOW,
          ORANGE, BROWN, LIGHT_RED, DARK_GREY,
          GREY, LIGHT_GREEN, LIGHT_BLUE, LIGHT_GREY]

color_map = []
color2_map = []


def init_colors():
    print("Initialize colors #1")
    for x in range(40):
        col = []
        for y in range(25):
            col.append(COLORS)
        color_map.append(col)


def get_nearest_color(colors, bgr: (int, int, int)):
    (bs, gs, rs) = bgr
    pd = None
    (bt, gt, rt) = (0, 0, 0)
    (be, ge, re) = (0, 0, 0)
    for color in colors:
        (bc, gc, rc) = color
        d = pow((int(bs) - int(bc)), 2) + pow((int(gs) - int(gc)), 2) + pow((int(rs) - int(rc)), 2)
        if pd is None or pd > d:
            (bt, gt, rt) = color
            (be, ge, re) = (int(bs) - int(bt), int(gs) - int(gt), int(rs) - int(rt))
            pd = d
    return (bt, gt, rt), (be, ge, re)


def init_colors2(background, dithered1):
    print("Initialize colors #2")
    for cx in range(40):
        col = []
        color2_map.append(col)
        for cy in range(25):
            colors = {}
            for xx in range(4):
                for yy in range(8):
                    px = cx * 4 + xx
                    py = cy * 8 + yy
                    c = tuple(dithered1[py, px])
                    if c != background:
                        if c in colors:
                            colors[c] += 1
                        else:
                            colors[c] = 1
            colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))
            color_list = list(colors.keys())
            cl = [background]
            cl.extend(color_list)
            color_list = cl[:4]
            col.append(color_list)


def get_background_color(orig, dithered):
    print("Get background colors: ", end="")
    colors = {}
    for cx in range(160):
        for cy in range(200):
            c = tuple(dithered[cy, cx])
            if c in colors:
                colors[c] += 1
            else:
                colors[c] = 1
    colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))
    background = list(colors.keys())[0]
    print(background)

    return background


def add_error(color, error, weight):
    (bc, gc, rc) = color
    (be, ge, re) = error
    return (
        min(max(bc + be * weight, 0), 255),
        min(max(gc + ge * weight, 0), 255),
        min(max(rc + re * weight, 0), 255)
    )


def dithering(cm, image, p):
    print(f"Dithering pass #{p} ", end="")
    dithered = image.copy()
    for x in range(161):
        if (x % 20) == 0:
            print(".", end='')
        for y in range(201):
            colors = cm[int(max(x - 1, 0) / 4)][int(max(y - 1, 0) / 8)]
            (new_pixel, error) = get_nearest_color(colors, dithered[y, x])
            dithered[y, x] = new_pixel
            dithered[y + 1, x] = add_error(dithered[y + 1, x], error, W1)
            dithered[y - 1, x + 1] = add_error(dithered[y - 1, x + 1], error, W2)
            dithered[y, x + 1] = add_error(dithered[y, x + 1], error, W3)
            dithered[y + 1, x + 1] = add_error(dithered[y + 1, x + 1], error, W4)

    dithered = dithered[1:201, 1:161]
    print("")
    return dithered


def save_kla(kla_name, background, dithered):
    address = bytearray()
    address.append(0x00)
    address.append(0x60)

    bitmap = bytearray()

    screenmem = bytearray()
    colormem = bytearray()

    bgmem = bytearray()
    bgmem.append(COLORS.index(background))

    print("Check colors and convert to KLA")
    for cy in range(25):
        for cx in range(40):
            colors = {}
            for yy in range(8):
                for xx in range(4):
                    px = cx * 4 + xx
                    py = cy * 8 + yy
                    c = tuple(dithered[py, px])
                    if c not in COLORS:
                        raise ValueError("Invalid color")
                    if c != background:
                        if c in colors:
                            colors[c] += 1
                        else:
                            colors[c] = 1

            if len(colors) > 3:
                raise ValueError("Color constraint error.")

            colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))

            s1 = COLORS.index(list(colors.keys())[0]) if len(colors) > 0 else 0
            s2 = COLORS.index(list(colors.keys())[1]) if len(colors) > 1 else 0
            c1 = COLORS.index(list(colors.keys())[2]) if len(colors) > 2 else 0
            screenmem.append(((s1 << 4) & 0xf0) | (s2 & 0x0f))
            colormem.append(c1)

            for yy in range(8):
                b = 0
                for xx in range(4):
                    px = cx * 4 + xx
                    py = cy * 8 + yy
                    c = tuple(dithered[py, px])
                    i = 0 if c == background else list(colors.keys()).index(c) + 1
                    b = (b << 2) & 0xff
                    b = (b | (i & 3)) & 0xff
                bitmap.append(b)

    print(f"Save file: {kla_name}")
    with open(kla_name, "wb") as f:
        f.write(address)
        f.write(bitmap)
        f.write(screenmem)
        f.write(colormem)
        f.write(bgmem)
        f.flush()


def convert(inputfile, outputfile, klaname):
    print(f"Read file: {inputfile}")
    image = cv2.imread(inputfile)
    resized_image = cv2.resize(image, (162, 202), interpolation=cv2.INTER_LANCZOS4)

    init_colors()

    dithered1 = dithering(color_map, resized_image, 1)

    background = get_background_color(resized_image, dithered1)

    init_colors2(background, dithered1)

    dithered2 = dithering(color2_map, resized_image, 2)

    resized_dithered = cv2.resize(dithered2, (320, 200), interpolation=cv2.INTER_NEAREST)

    save_kla(klaname, background, dithered2)

    print(f"Save file: {outputfile}")
    cv2.imwrite(outputfile, resized_dithered)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Original image")
ap.add_argument("-k", "--kla", required=True, help="KLA image")
ap.add_argument("-o", "--output", required=True, help="Output PNG image")
args = vars(ap.parse_args())

convert(args["image"], args["output"], args["kla"])
