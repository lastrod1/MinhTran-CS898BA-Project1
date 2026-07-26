import os
import numpy as np
import matplotlib.font_manager as fm
from PIL import Image, ImageDraw, ImageFont

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "font_digits.npz")

RENDER_SIZE = 20
# I have 242 on my system so since mnist is 70000, I did 120 so the datasets wouldn't be too skewed
AUGS_PER_FONT_DIGIT = 120


def get_system_fonts():
    candidates = fm.findSystemFonts(fontext="ttf")
    good = []

    bad = ["symbol", "emoji", "icon", "awesome", "wingding", "webding",
           "dingbat", "material", "glyphicon", "brands", "fontawesome",
           "bootstrap", "octicon"]

    for path in candidates:
        name = os.path.basename(path).lower()
        if any(kw in name for kw in bad):
            continue

        try:
            font = ImageFont.truetype(path, RENDER_SIZE)

            renders = []
            for d in range(10):
                img = Image.new("L", (28, 28), 0)
                draw = ImageDraw.Draw(img)
                bbox = draw.textbbox((0, 0), str(d), font=font)
                if bbox[2] - bbox[0] == 0 or bbox[3] - bbox[1] == 0:
                    raise ValueError("empty glyph")
                x = (28 - (bbox[2] - bbox[0])) / 2 - bbox[0]
                y = (28 - (bbox[3] - bbox[1])) / 2 - bbox[1]
                draw.text((x, y), str(d), font=font, fill=255)
                renders.append(np.array(img).tobytes())

            if len(set(renders)) < 8:
                continue

            good.append(path)
        except Exception:
            continue

    return good


def render_digit(digit, font_path):
    img = Image.new("L", (28, 28), color=0)  # black bg
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, RENDER_SIZE)

    bbox = draw.textbbox((0, 0), str(digit), font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (28 - w) / 2 - bbox[0]
    y = (28 - h) / 2 - bbox[1]

    draw.text((x, y), str(digit), font=font, fill=255)  # white digit
    return np.array(img, dtype=np.uint8)


def center_by_mass(arr):
    ys, xs = np.nonzero(arr)
    if len(xs) == 0:
        return arr
    cy, cx = ys.mean(), xs.mean()
    shift_y, shift_x = int(28 / 2 - cy), int(28 / 2 - cx)
    return np.roll(np.roll(arr, shift_y, axis=0), shift_x, axis=1)


def jitter(arr, rng):
    # This is just so we have variation
    shift_y = rng.integers(-2, 3)
    shift_x = rng.integers(-2, 3)
    return np.roll(np.roll(arr, shift_y, axis=0), shift_x, axis=1)


def main():
    font_paths = get_system_fonts()
    if not font_paths:
        raise SystemExit(
            "No Fonts"
        )
    print(f"{len(font_paths)} Fonts")

    random = np.random.default_rng(67)
    images, labels, font_ids = [], [], []

    kept_fonts = 0
    for font_idx, font_path in enumerate(font_paths):
        try:
            bases = [render_digit(d, font_path) for d in range(10)]
        except Exception as e:
            print(f"skipping {font_path}: {e}")
            continue

        # skipping anything thats bascially black
        if any(b.sum() == 0 for b in bases):
            continue

        kept_fonts += 1
        for digit, base in enumerate(bases):
            base = center_by_mass(base)
            for _ in range(AUGS_PER_FONT_DIGIT):
                images.append(jitter(base, random))
                labels.append(digit)
                font_ids.append(font_idx)

    images = np.stack(images).astype(np.uint8)
    labels = np.array(labels, dtype=np.uint8)
    font_ids = np.array(font_ids, dtype=np.int32)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    np.savez_compressed(OUT_PATH, images=images, labels=labels, font_ids=font_ids)


if __name__ == "__main__":
    main()