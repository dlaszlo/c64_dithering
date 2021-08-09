import argparse

import cv2
import numpy as np

from c64_palette import get_palette
from c64_palette import palettes
from dithering_models import dithering_models
from dithering_models import get_dithering_model

color_map = []
color2_map = []


def init_colors(palette):
    print("Initialize colors #1")
    for y in range(25):
        row = []
        for x in range(40):
            row.append(palette)
        color_map.append(row)


def get_nearest_color(colors, bgr: (float, float, float)):
    (bs, gs, rs) = bgr
    pd = None
    (bt, gt, rt) = (0, 0, 0)
    (be, ge, re) = (0, 0, 0)
    for color in colors:
        (bc, gc, rc) = color
        # https://www.compuphase.com/cmetric.htm
        rmean = (rs + rc) / 2
        d = ((767 - rmean) * pow(bs - bc, 2) / 256) + 4 * pow(gs - gc, 2) + ((512 + rmean) * pow(rs - rc, 2) / 256)
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


def dithering(model, cm, image, p):
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


def save_kla(kla_name, background, dithered, palette):
    address = bytearray()
    address.append(0x00)
    address.append(0x60)

    bitmap = bytearray()

    screenmem = bytearray()
    colormem = bytearray()

    bgmem = bytearray()
    bgmem.append(palette.index(background))

    print("Check colors and convert to KLA")
    for cy in range(25):
        for cx in range(40):
            colors = {}
            for yy in range(8):
                for xx in range(4):
                    px = cx * 4 + xx
                    py = cy * 8 + yy
                    c = tuple(dithered[py, px])
                    if c not in palette:
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

            s1 = palette.index(list(colors.keys())[0]) if len(colors) > 0 else 0
            s2 = palette.index(list(colors.keys())[1]) if len(colors) > 1 else 0
            c1 = palette.index(list(colors.keys())[2]) if len(colors) > 2 else 0
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


def convert(input_file, output_file, kla_name, model_name, palette_name):
    model = get_dithering_model(model_name)
    print(f"Model: {model['name']}")
    palette = get_palette(palette_name)
    print(f"Palette: {palette['name']}")
    print(f"Read file: {input_file}")

    image = cv2.imread(input_file)
    resized_image = cv2.resize(image, (160, 200), interpolation=cv2.INTER_LANCZOS4)
    resized_image = resized_image.astype(np.float32)

    init_colors(palette["colors"])

    dithered1 = dithering(model, color_map, resized_image, 1)

    background = get_background_color(resized_image, dithered1)

    init_colors2(background, dithered1)

    dithered2 = dithering(model, color2_map, resized_image, 2)

    resized_dithered = cv2.resize(dithered2, (320, 200), interpolation=cv2.INTER_NEAREST)

    save_kla(kla_name, background, dithered2, palette["colors"])

    print(f"Save file: {output_file}")
    cv2.imwrite(output_file, resized_dithered)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Original image")
ap.add_argument("-k", "--kla", required=True, help="KLA image")
ap.add_argument("-o", "--output", required=True, help="Output PNG image")

ap.add_argument("-m", "--model", required=False, default="sierra",
                help=f"Dithering models: {dithering_models()}, Default: sierra")

ap.add_argument("-p", "--palette", required=False, default="Pepto",
                help=f"Palettes: {palettes()}, Default: Pepto")

args = vars(ap.parse_args())

convert(args["image"], args["output"], args["kla"], args["model"], args["palette"])
