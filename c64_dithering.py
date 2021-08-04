import argparse

import cv2
import numpy as np

FLOYD_STEINBERG = {
    "weight": 1.0 / 16.0,
    "pattern": [
        (0, 1, 7.0),
        (1, -1, 3.0),
        (1, 0, 5.0),
        (1, 1, 1.0),
    ]
}

JARVIS_JUDICE_NINKE = {
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
    "weight": 1.0 / 4.0,
    "pattern": [
        (0, 1, 2.0),
        (1, -1, 1.0),
        (1, 0, 1.0)
    ]
}

BLACK = (0.0, 0.0, 0.0)
WHITE = (255.0, 255.0, 255.0)
RED = (43.0, 55.0, 104.0)
CYAN = (178.0, 164.0, 112.0)
PURPLE = (134.0, 61.0, 111.0)
GREEN = (67.0, 141.0, 88.0)
BLUE = (121.0, 40.0, 53.0)
YELLOW = (111.0, 199.0, 184.0)
ORANGE = (37.0, 79.0, 111.0)
BROWN = (0.0, 57.0, 67.0)
LIGHT_RED = (89.0, 103.0, 154.0)
DARK_GREY = (68.0, 68.0, 68.0)
GREY = (108.0, 108.0, 108.0)
LIGHT_GREEN = (132.0, 210.0, 154.0)
LIGHT_BLUE = (181.0, 94.0, 108.0)
LIGHT_GREY = (149.0, 149.0, 149.0)

COLORS = [BLACK, WHITE, RED, CYAN,
          PURPLE, GREEN, BLUE, YELLOW,
          ORANGE, BROWN, LIGHT_RED, DARK_GREY,
          GREY, LIGHT_GREEN, LIGHT_BLUE, LIGHT_GREY]

color_map = []
color2_map = []


def init_colors():
    print("Initialize colors #1")
    for y in range(25):
        row = []
        for x in range(40):
            row.append(COLORS)
        color_map.append(row)


def get_nearest_color(colors, bgr: (float, float, float)):
    (bs, gs, rs) = bgr
    pd = None
    (bt, gt, rt) = (0, 0, 0)
    (be, ge, re) = (0, 0, 0)
    for color in colors:
        (bc, gc, rc) = color
        d = pow(bs - bc, 2) + pow(gs - gc, 2) + pow(rs - rc, 2)
        if pd is None or pd > d:
            (bt, gt, rt) = color
            (be, ge, re) = (bs - bt, gs - gt, rs - rt)
            pd = d
    return (bt, gt, rt), (be, ge, re)


def init_colors2(background, dithered1):
    print("Initialize colors #2")
    for cy in range(25):
        row = []
        color2_map.append(row)
        for cx in range(40):
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
            row.append(color_list)


def get_background_color(orig, dithered):
    print("Get background colors: ", end="")
    colors = {}
    for cy in range(200):
        for cx in range(160):
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
        min(max(bc + be * weight, 0.0), 255.0),
        min(max(gc + ge * weight, 0.0), 255.0),
        min(max(rc + re * weight, 0.0), 255.0)
    )


def dithering2(model, cm, image, p):
    print(f"Dithering pass #{p} ", end="")
    dithered = image.copy()
    for y in range(200):
        if (y % 20) == 0:
            print(".", end='')
        if (y % 2) == 0:
            for x in range(160):
                colors = cm[int(max(y, 0) / 8)][int(max(x, 0) / 4)]
                (new_pixel, error) = get_nearest_color(colors, dithered[y, x])
                dithered[y, x] = new_pixel
                w0 = model["weight"]
                for (dy, dx, w) in model.get("pattern"):
                    if -1 < (x + dx) < 160 and -1 < (y + dy) < 200:
                        dithered[y + dy, x + dx] = add_error(dithered[y + dy, x + dx], error, w0 * w)
        else:
            for x in range(159, -1, -1):
                colors = cm[int(max(y, 0) / 8)][int(max(x, 0) / 4)]
                (new_pixel, error) = get_nearest_color(colors, dithered[y, x])
                dithered[y, x] = new_pixel
                w0 = model["weight"]
                for (dy, dx, w) in model.get("pattern"):
                    if -1 < (x - dx) < 160 and -1 < (y + dy) < 200:
                        dithered[y + dy, x - dx] = add_error(dithered[y + dy, x - dx], error, w0 * w)

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
                print(cx)
                print(cy)
                print(colors)
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
    resized_image = cv2.resize(image, (160, 200), interpolation=cv2.INTER_LANCZOS4)
    resized_image = resized_image.astype(np.float32)

    init_colors()

    dithered1 = dithering2(SIERRA, color_map, resized_image, 1)

    background = get_background_color(resized_image, dithered1)

    init_colors2(background, dithered1)

    dithered2 = dithering2(SIERRA, color2_map, resized_image, 2)

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
