import json
import os
import math
from datetime import datetime, timezone
from PIL import Image, ImageDraw

SIZE = 64
SCALE = 8  # 64 * 8 = 512x512 crisp integer upscale

# Extended PICO-8 & Endesga rich palette for 64x64
COLORS = {
    "black": "#000000",
    "dark_navy": "#1d2b53",
    "deep_purple": "#7e2553",
    "dark_brown": "#4f2b1d",
    "brown": "#ab5236",
    "light_brown": "#d77643",
    "orange": "#ffa300",
    "amber": "#f77622",
    "gold": "#ffec27",
    "peach": "#ffccaa",
    "warm_white": "#fff1e8",
    "pure_white": "#ffffff",
    "dark_green": "#008751",
    "emerald": "#00e436",
    "lime": "#63c74d",
    "red": "#ff004d",
    "dark_red": "#a22633",
    "soft_pink": "#ff77a8",
    "deep_pink": "#b55088",
    "gray": "#5f574f",
    "light_gray": "#c2c3c7",
    "shadow_purple": "#2b1e3a"
}

PALETTE_LIST = list(COLORS.values())

def hex_to_rgba(hex_str, alpha=255):
    if not hex_str or hex_str == "transparent":
        return (0, 0, 0, 0)
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return (r, g, b, alpha)

def create_cat_64_grid(blink=False, tail_swish=False):
    grid = [None] * (SIZE * SIZE)

    def set_p(x, y, col):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            grid[y * SIZE + x] = col

    def set_rect(x1, y1, w, h, col):
        for y in range(y1, y1 + h):
            for x in range(x1, x1 + w):
                set_p(x, y, col)

    out = COLORS["dark_navy"]
    fur = COLORS["orange"]
    fur_shade = COLORS["brown"]
    fur_deep = COLORS["dark_brown"]
    fur_light = COLORS["gold"]
    fur_amber = COLORS["amber"]
    white = COLORS["pure_white"]
    cream = COLORS["warm_white"]
    pink = COLORS["soft_pink"]
    deep_pink = COLORS["deep_pink"]

    # 0. Cozy Floor Ambient Shadow
    for y in range(56, 59):
        for x in range(16, 48):
            set_p(x, y, COLORS["shadow_purple"])
    for x in range(20, 44):
        set_p(x, 59, COLORS["shadow_purple"])

    # 1. Ears
    # Left Ear Outline & Shape
    left_ear_pts = [
        (18, 8), (17, 9), (16, 10), (15, 11), (14, 12), (13, 13), (12, 14), (12, 15), (12, 16),
        (19, 9), (20, 10), (21, 11), (22, 12), (23, 13), (24, 14), (24, 15)
    ]
    for (ex, ey) in left_ear_pts:
        set_p(ex, ey, out)

    # Right Ear Outline & Shape
    right_ear_pts = [
        (45, 8), (46, 9), (47, 10), (48, 11), (49, 12), (50, 13), (51, 14), (51, 15), (51, 16),
        (44, 9), (43, 10), (42, 11), (41, 12), (40, 13), (39, 14), (39, 15)
    ]
    for (ex, ey) in right_ear_pts:
        set_p(ex, ey, out)

    # Fill Left Ear
    for y in range(9, 16):
        for x in range(13, 24):
            if 14 <= x <= 22 and 10 <= y <= 15:
                set_p(x, y, fur)
    # Inner Left Ear Pink
    set_rect(15, 11, 4, 4, pink)
    set_rect(16, 12, 2, 2, deep_pink)
    # Ear tuft white
    set_p(14, 14, white); set_p(14, 15, white); set_p(15, 15, white)

    # Fill Right Ear
    for y in range(9, 16):
        for x in range(40, 51):
            if 41 <= x <= 49 and 10 <= y <= 15:
                set_p(x, y, fur)
    # Inner Right Ear Pink
    set_rect(44, 11, 4, 4, pink)
    set_rect(45, 12, 2, 2, deep_pink)
    # Ear tuft white
    set_p(49, 14, white); set_p(49, 15, white); set_p(48, 15, white)

    # 2. Head Dome & Contours
    for x in range(24, 40):
        set_p(x, 15, out)
    for y in range(16, 36):
        set_p(11, y, out)
        set_p(52, y, out)
    set_p(12, 36, out); set_p(13, 37, out)
    set_p(51, 36, out); set_p(50, 37, out)

    # Fill Head Base Fur
    for y in range(16, 37):
        for x in range(12, 52):
            set_p(x, y, fur)

    # Shading on Head (Amber & Fur Light)
    for x in range(20, 44):
        set_p(x, 16, fur_light)
    for y in range(17, 21):
        set_p(13, y, fur_shade)
        set_p(50, y, fur_shade)

    # Tabby Forehead Stripes (Symmetrical crown marks)
    # Center stripe
    set_rect(31, 16, 2, 6, fur_shade)
    set_rect(31, 17, 2, 4, fur_deep)
    # Flanking stripes
    set_rect(27, 18, 2, 4, fur_shade)
    set_rect(35, 18, 2, 4, fur_shade)
    set_rect(23, 20, 2, 3, fur_shade)
    set_rect(39, 20, 2, 3, fur_shade)

    # Cheek Fluff (White fur tufts)
    for y in range(29, 36):
        for x in range(12, 19):
            set_p(x, y, white)
        for x in range(45, 52):
            set_p(x, y, white)
    # Fluff tips
    set_p(10, 31, white); set_p(10, 32, white); set_p(9, 32, out)
    set_p(53, 31, white); set_p(53, 32, white); set_p(54, 32, out)

    # 3. Eyes (Rich Emerald Gradient 6x5 pixels each)
    if blink:
        # Happy Blinking Closed Eyes (^ ^)
        for x in range(20, 28):
            set_p(x, 26, out)
        set_p(19, 27, out); set_p(28, 27, out)
        set_p(23, 25, out); set_p(24, 25, out)

        for x in range(36, 44):
            set_p(x, 26, out)
        set_p(35, 27, out); set_p(44, 27, out)
        set_p(39, 25, out); set_p(40, 25, out)
    else:
        # Left Eye (x: 20..27, y: 23..28)
        # Eye socket outline
        for x in range(20, 28):
            set_p(x, 23, out)
            set_p(x, 28, out)
        set_p(19, 24, out); set_p(19, 25, out); set_p(19, 26, out); set_p(19, 27, out)
        set_p(28, 24, out); set_p(28, 25, out); set_p(28, 26, out); set_p(28, 27, out)

        # Iris Green Gradient
        set_rect(20, 24, 8, 4, COLORS["emerald"])
        set_rect(20, 24, 8, 1, COLORS["dark_green"])
        set_rect(20, 27, 8, 1, COLORS["lime"])
        # Lower golden rim reflection
        set_p(22, 27, COLORS["gold"]); set_p(23, 27, COLORS["gold"]); set_p(24, 27, COLORS["gold"])

        # Pupil (Slit-oval midnight navy)
        set_rect(23, 24, 2, 4, out)
        set_p(23, 25, COLORS["black"]); set_p(24, 25, COLORS["black"])
        set_p(23, 26, COLORS["black"]); set_p(24, 26, COLORS["black"])

        # Specular Highlights (Sparkling primary & secondary)
        set_rect(21, 24, 2, 2, white)
        set_p(25, 26, cream)

        # Right Eye (x: 36..43, y: 23..28)
        for x in range(36, 44):
            set_p(x, 23, out)
            set_p(x, 28, out)
        set_p(35, 24, out); set_p(35, 25, out); set_p(35, 26, out); set_p(35, 27, out)
        set_p(44, 24, out); set_p(44, 25, out); set_p(44, 26, out); set_p(44, 27, out)

        set_rect(36, 24, 8, 4, COLORS["emerald"])
        set_rect(36, 24, 8, 1, COLORS["dark_green"])
        set_rect(36, 27, 8, 1, COLORS["lime"])
        set_p(38, 27, COLORS["gold"]); set_p(39, 27, COLORS["gold"]); set_p(40, 27, COLORS["gold"])

        # Pupil
        set_rect(39, 24, 2, 4, out)
        set_p(39, 25, COLORS["black"]); set_p(40, 25, COLORS["black"])
        set_p(39, 26, COLORS["black"]); set_p(40, 26, COLORS["black"])

        # Highlights
        set_rect(37, 24, 2, 2, white)
        set_p(41, 26, cream)

    # 4. Muzzle & Nose & Mouth
    # Pink cute nose
    set_rect(30, 29, 4, 2, pink)
    set_rect(31, 30, 2, 1, deep_pink)
    set_p(31, 31, out); set_p(32, 31, out)

    # White Muzzle Pad
    set_rect(26, 31, 4, 3, cream)
    set_rect(34, 31, 4, 3, cream)
    set_rect(27, 32, 3, 2, white)
    set_rect(34, 32, 3, 2, white)
    # Whisker dots
    set_p(27, 32, fur_shade); set_p(29, 33, fur_shade)
    set_p(36, 32, fur_shade); set_p(34, 33, fur_shade)

    # Mouth lips curve
    set_p(30, 33, out); set_p(33, 33, out)
    set_p(29, 34, out); set_p(34, 34, out)
    set_p(31, 34, cream); set_p(32, 34, cream)

    # 5. Whiskers (Long sweeping 1px white lines)
    # Left Whiskers
    left_whiskers = [
        # Top
        (8, 28), (9, 28), (10, 29), (11, 29), (12, 30),
        # Mid
        (6, 31), (7, 31), (8, 31), (9, 32), (10, 32), (11, 32),
        # Bottom
        (7, 34), (8, 34), (9, 34), (10, 33), (11, 33)
    ]
    for (wx, wy) in left_whiskers:
        set_p(wx, wy, white)

    # Right Whiskers
    right_whiskers = [
        # Top
        (55, 28), (54, 28), (53, 29), (52, 29), (51, 30),
        # Mid
        (57, 31), (56, 31), (55, 31), (54, 32), (53, 32), (52, 32),
        # Bottom
        (56, 34), (55, 34), (54, 34), (53, 33), (52, 33)
    ]
    for (wx, wy) in right_whiskers:
        set_p(wx, wy, white)

    # 6. Royal Collar & Golden Bell
    for x in range(18, 46):
        set_p(x, 37, COLORS["red"])
        set_p(x, 38, COLORS["dark_red"])
        set_p(x, 36, out)
        set_p(x, 39, out)
    # Collar gold highlights
    set_p(22, 37, COLORS["gold"]); set_p(41, 37, COLORS["gold"])

    # Golden Bell (Detailed 6x6 sphere)
    set_rect(29, 39, 6, 6, COLORS["gold"])
    set_rect(30, 40, 4, 4, fur_amber)
    set_rect(30, 40, 2, 2, white)  # Gold shine
    set_rect(31, 42, 2, 2, out)    # Bell slit
    # Bell outline
    for x in range(29, 35):
        set_p(x, 39, out); set_p(x, 44, out)
    for y in range(39, 45):
        set_p(29, y, out); set_p(34, y, out)

    # 7. Body & Calico/Tabby Fur
    for y in range(39, 56):
        set_p(15, y, out)
        set_p(48, y, out)
    for x in range(16, 48):
        set_p(x, 56, out)

    # Fill body
    for y in range(39, 56):
        for x in range(16, 48):
            set_p(x, y, fur)

    # Tabby Stripes on Flanks
    # Left flank stripes
    set_rect(16, 42, 5, 2, fur_shade)
    set_rect(16, 47, 6, 2, fur_shade)
    set_rect(16, 52, 4, 2, fur_shade)
    # Right flank stripes
    set_rect(43, 42, 5, 2, fur_shade)
    set_rect(42, 47, 6, 2, fur_shade)
    set_rect(44, 52, 4, 2, fur_shade)

    # White Chest Bib / Apron
    for y in range(41, 53):
        for x in range(26, 38):
            set_p(x, y, cream)
    for y in range(43, 51):
        for x in range(28, 36):
            set_p(x, y, white)
    # Fluffy edge of chest bib
    set_p(25, 45, white); set_p(25, 48, white)
    set_p(38, 45, white); set_p(38, 48, white)

    # 8. Front Paws (Soft White Mittens with Toes)
    # Left Paw (x: 23..29, y: 52..55)
    set_rect(23, 52, 7, 4, white)
    for x in range(23, 30):
        set_p(x, 56, out)
    set_p(22, 53, out); set_p(22, 54, out); set_p(22, 55, out)
    set_p(30, 53, out); set_p(30, 54, out); set_p(30, 55, out)
    # Toe separation lines
    set_p(25, 54, out); set_p(25, 55, out)
    set_p(27, 54, out); set_p(27, 55, out)

    # Right Paw (x: 34..40, y: 52..55)
    set_rect(34, 52, 7, 4, white)
    for x in range(34, 41):
        set_p(x, 56, out)
    set_p(33, 53, out); set_p(33, 54, out); set_p(33, 55, out)
    set_p(41, 53, out); set_p(41, 54, out); set_p(41, 55, out)
    # Toe lines
    set_p(36, 54, out); set_p(36, 55, out)
    set_p(38, 54, out); set_p(38, 55, out)

    # 9. Tail
    if tail_swish:
        # Frame 2: Tail swished high and curving inward gracefully
        tail_path = [
            (47, 53), (48, 52), (49, 51), (50, 49), (51, 47),
            (52, 45), (53, 42), (54, 39), (55, 36), (55, 33),
            (54, 30), (53, 28), (51, 27), (49, 27), (47, 28)
        ]
        for (tx, ty) in tail_path:
            set_rect(tx - 1, ty - 1, 3, 3, fur)
            set_p(tx, ty, fur_amber)
        # Tabby rings on tail
        set_rect(50, 48, 3, 2, fur_shade)
        set_rect(53, 41, 3, 2, fur_shade)
        set_rect(54, 34, 3, 2, fur_shade)
        # White tip
        set_rect(46, 27, 4, 3, white)
        set_p(48, 28, cream)
    else:
        # Frame 1: Resting majestic S-curve tail
        tail_path = [
            (47, 54), (49, 54), (51, 53), (53, 51), (55, 48),
            (56, 45), (57, 41), (57, 37), (56, 34), (54, 32),
            (52, 31), (50, 32)
        ]
        for (tx, ty) in tail_path:
            set_rect(tx - 1, ty - 1, 3, 3, fur)
            set_p(tx, ty, fur_amber)
        # Tabby rings on tail
        set_rect(52, 52, 3, 2, fur_shade)
        set_rect(55, 46, 3, 2, fur_shade)
        set_rect(56, 39, 3, 2, fur_shade)
        # White tip
        set_rect(49, 31, 4, 3, white)
        set_p(51, 32, cream)

    return grid

def generate_dsl_64():
    lines = [
        "// PixelMirai DSL — 64x64 Royal Masterpiece Calico Cat (Anti-AI-Slop)",
        "size 64",
        "palette pico-8",
        "fps 4",
        "crt on",
        "",
        "// Frame 1: 64x64 Royal Cat Resting Pose",
        "frame 1",
        "layer \"cat_sprite_64\"",
        ""
    ]
    grid1 = create_cat_64_grid(blink=False, tail_swish=False)
    color_map = {}
    for y in range(SIZE):
        for x in range(SIZE):
            c = grid1[y * SIZE + x]
            if c:
                color_map.setdefault(c, []).append((x, y))
    
    for c, pts in color_map.items():
        chunk = []
        for (px, py) in pts:
            chunk.append(f"{px},{py}")
            if len(chunk) >= 16:
                lines.append(f"pixels {c} " + " ".join(chunk))
                chunk = []
        if chunk:
            lines.append(f"pixels {c} " + " ".join(chunk))

    lines.append("")
    lines.append("// Frame 2: 64x64 Royal Cat Eye Blink & High Tail Swish")
    lines.append("frame 2")
    lines.append("layer \"cat_sprite_64\"")
    grid2 = create_cat_64_grid(blink=True, tail_swish=True)
    color_map2 = {}
    for y in range(SIZE):
        for x in range(SIZE):
            c = grid2[y * SIZE + x]
            if c:
                color_map2.setdefault(c, []).append((x, y))
    
    for c, pts in color_map2.items():
        chunk = []
        for (px, py) in pts:
            chunk.append(f"{px},{py}")
            if len(chunk) >= 16:
                lines.append(f"pixels {c} " + " ".join(chunk))
                chunk = []
        if chunk:
            lines.append(f"pixels {c} " + " ".join(chunk))

    return "\n".join(lines)

def compute_fnv1a_checksum(canonical_str):
    hash_val = 0x811C9DC5
    for ch in canonical_str:
        hash_val ^= ord(ch)
        hash_val = (hash_val * 0x01000193) & 0xFFFFFFFF
    return f"{hash_val:08x}"

def generate_pxm_project_64(grid1, grid2):
    frames = [
        {
            "id": "frame-1",
            "layers": [
                {
                    "id": "layer-cat-64-1",
                    "name": "Royal Cat 64x64",
                    "visible": True,
                    "opacity": 1.0,
                    "blendMode": "source-over",
                    "pixels": grid1
                }
            ]
        },
        {
            "id": "frame-2",
            "layers": [
                {
                    "id": "layer-cat-64-2",
                    "name": "Royal Cat 64x64",
                    "visible": True,
                    "opacity": 1.0,
                    "blendMode": "source-over",
                    "pixels": grid2
                }
            ]
        }
    ]

    canonical_data = {
        "projectName": "64x64 Royal Calico Cat",
        "size": 64,
        "frames": frames,
        "palette": PALETTE_LIST,
        "settings": {
            "pixelPerfect": True,
            "soundEnabled": True,
            "crtFilter": True
        }
    }

    canonical_json = json.dumps(canonical_data, separators=(',', ':'))
    checksum = compute_fnv1a_checksum(canonical_json)

    full_project = {
        "format": "PixelMirai",
        "version": 1,
        "generator": "PixelMirai Studio v3.0 (Anti-AI-Slop Engine)",
        "exportedAt": datetime.now(timezone.utc).isoformat(),
        "checksum": checksum,
        "projectName": "64x64 Royal Calico Cat",
        "size": 64,
        "paletteName": "Custom Retro 22",
        "palette": PALETTE_LIST,
        "settings": {
            "pixelPerfect": True,
            "soundEnabled": True,
            "crtFilter": True
        },
        "frames": frames
    }
    return full_project

def grid_to_image(grid, scale=1):
    img = Image.new("RGBA", (SIZE * scale, SIZE * scale), (0, 0, 0, 0))
    for y in range(SIZE):
        for x in range(SIZE):
            c = grid[y * SIZE + x]
            if c:
                rgba = hex_to_rgba(c)
                for sy in range(scale):
                    for sx in range(scale):
                        img.putpixel((x * scale + sx, y * scale + sy), rgba)
    return img

def apply_crt_filter_64(img):
    w, h = img.size
    crt_img = Image.new("RGBA", (w, h), (16, 14, 26, 255))
    
    bg_draw = ImageDraw.Draw(crt_img)
    bg_draw.rectangle([0, 0, w, h], fill=(18, 16, 28, 255))
    
    crt_img.alpha_composite(img, (0, 0))

    # Fine 50% Horizontal Scanlines (every 2px on 512x512)
    scanline_overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scanline_overlay)
    for y in range(0, h, 3):
        scan_draw.line([(0, y), (w, y)], fill=(0, 0, 0, 85), width=1)
    
    crt_img.alpha_composite(scanline_overlay, (0, 0))

    # CRT Curved Vignette
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for i in range(20):
        alpha = int((20 - i) * 5)
        vig_draw.rectangle([i, i, w - i, h - i], outline=(0, 0, 0, alpha), width=1)
    
    crt_img.alpha_composite(vignette, (0, 0))
    return crt_img

def main():
    out_dir = r"C:\Users\A\Downloads\pixelmirai-next\public\exports"
    os.makedirs(out_dir, exist_ok=True)

    grid1 = create_cat_64_grid(blink=False, tail_swish=False)
    grid2 = create_cat_64_grid(blink=True, tail_swish=True)

    # 1. Export DSL Script
    dsl_content = generate_dsl_64()
    dsl_path = os.path.join(out_dir, "cat-64.dsl")
    with open(dsl_path, "w", encoding="utf-8") as f:
        f.write(dsl_content)
    print(f"Saved 64x64 DSL: {dsl_path}")

    # 2. Export .pxm Project File
    pxm_data = generate_pxm_project_64(grid1, grid2)
    pxm_path = os.path.join(out_dir, "cat-64.pxm")
    with open(pxm_path, "w", encoding="utf-8") as f:
        json.dump(pxm_data, f, indent=2)
    print(f"Saved 64x64 .pxm: {pxm_path}")

    # 3. Export PNG (1x = 64x64, 8x = 512x512)
    img1_1x = grid_to_image(grid1, scale=1)
    img1_1x.save(os.path.join(out_dir, "cat-64-1x.png"))

    img1_8x = grid_to_image(grid1, scale=SCALE)
    img1_8x.save(os.path.join(out_dir, "cat-64.png"))
    print(f"Saved 64x64 PNG: {os.path.join(out_dir, 'cat-64.png')}")

    # 4. Export CRT Edition PNG
    crt_img = apply_crt_filter_64(img1_8x)
    crt_path = os.path.join(out_dir, "cat-64-crt.png")
    crt_img.save(crt_path)
    print(f"Saved 64x64 CRT PNG: {crt_path}")

    # 5. Export 2-Frame Looping Animated GIF
    img2_8x = grid_to_image(grid2, scale=SCALE)
    gif_path = os.path.join(out_dir, "cat-64.gif")
    img1_8x.save(
        gif_path,
        save_all=True,
        append_images=[img2_8x],
        duration=350,
        loop=0,
        disposal=2
    )
    print(f"Saved 64x64 Animated GIF: {gif_path}")

    # Copy to brain artifact directory
    brain_dir = r"C:\Users\A\.gemini\antigravity\brain\d9703ca7-69c6-466b-8834-640f7dc6a023"
    import shutil
    shutil.copy(os.path.join(out_dir, "cat-64.png"), os.path.join(brain_dir, "cat-64.png"))
    shutil.copy(crt_path, os.path.join(brain_dir, "cat-64-crt.png"))
    shutil.copy(gif_path, os.path.join(brain_dir, "cat-64.gif"))
    print("Copied all 64x64 outputs to brain directory!")

if __name__ == "__main__":
    main()
