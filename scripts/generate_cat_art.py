import json
import os
import math
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFilter

SIZE = 32
SCALE = 16  # 32 * 16 = 512x512 crisp integer upscale

# Palette PICO-8
COLORS = {
    "black": "#000000",
    "dark_navy": "#1d2b53",
    "dark_purple": "#7e2553",
    "dark_green": "#008751",
    "brown": "#ab5236",
    "dark_gray": "#5f574f",
    "light_gray": "#c2c3c7",
    "white": "#fff1e8",
    "pure_white": "#ffffff",
    "red": "#ff004d",
    "orange": "#ffa300",
    "yellow": "#ffec27",
    "green": "#00e436",
    "blue": "#29adff",
    "lavender": "#83769c",
    "pink": "#ff77a8",
    "peach": "#ffccaa"
}

PICO_PALETTE = list(COLORS.values())

def hex_to_rgba(hex_str, alpha=255):
    if not hex_str or hex_str == "transparent":
        return (0, 0, 0, 0)
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return (r, g, b, alpha)

def create_cat_grid(blink=False, tail_up=False):
    grid = [None] * (SIZE * SIZE)
    
    def set_p(x, y, col):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            grid[y * SIZE + x] = col

    def set_rect(x1, y1, w, h, col):
        for y in range(y1, y1 + h):
            for x in range(x1, x1 + w):
                set_p(x, y, col)

    # 1. Dark Outline & Silhouette
    # Left Ear
    outline_col = COLORS["dark_navy"]
    fur_col = COLORS["orange"]
    fur_shade = COLORS["brown"]
    fur_light = COLORS["yellow"]
    white_fur = COLORS["pure_white"]
    pink_inner = COLORS["pink"]

    # Ears Outline
    set_p(9, 6, outline_col)
    set_p(8, 7, outline_col)
    set_p(7, 8, outline_col)
    set_p(7, 9, outline_col)
    set_p(7, 10, outline_col)
    set_p(8, 11, outline_col)
    set_p(9, 8, outline_col)
    set_p(10, 7, outline_col)
    set_p(11, 7, outline_col)
    set_p(12, 8, outline_col)

    # Right Ear Outline
    set_p(22, 6, outline_col)
    set_p(23, 7, outline_col)
    set_p(24, 8, outline_col)
    set_p(24, 9, outline_col)
    set_p(24, 10, outline_col)
    set_p(23, 11, outline_col)
    set_p(22, 8, outline_col)
    set_p(21, 7, outline_col)
    set_p(20, 7, outline_col)
    set_p(19, 8, outline_col)

    # Head top outline
    for x in range(13, 19):
        set_p(x, 8, outline_col)

    # Head Side & Cheek Outline
    for y in range(11, 19):
        set_p(6, y, outline_col)
        set_p(25, y, outline_col)
    set_p(7, 19, outline_col)
    set_p(24, 19, outline_col)

    # Body Outline
    for y in range(20, 28):
        set_p(8, y, outline_col)
        set_p(23, y, outline_col)
    for x in range(9, 23):
        set_p(x, 28, outline_col)

    # 2. Fill Ears (Inner pink & fur)
    set_p(9, 7, fur_col)
    set_rect(8, 8, 3, 3, fur_col)
    set_rect(8, 9, 2, 2, pink_inner)

    set_p(22, 7, fur_col)
    set_rect(21, 8, 3, 3, fur_col)
    set_rect(22, 9, 2, 2, pink_inner)

    # 3. Fill Head Base Fur (Orange ginger)
    for y in range(9, 19):
        for x in range(7, 25):
            if grid[y * SIZE + x] is None:
                grid[y * SIZE + x] = fur_col

    # Tabby Head Stripes (Brown)
    for y in range(9, 12):
        set_p(15, y, fur_shade)
        set_p(16, y, fur_shade)
    set_p(14, 10, fur_shade)
    set_p(17, 10, fur_shade)
    set_p(13, 11, fur_shade)
    set_p(18, 11, fur_shade)

    # Cheek Fluff (White)
    set_rect(7, 15, 3, 3, white_fur)
    set_rect(22, 15, 3, 3, white_fur)
    set_p(8, 18, white_fur)
    set_p(23, 18, white_fur)

    # 4. Eyes
    if blink:
        # Happy Blinking Eyes (^ ^)
        set_p(10, 14, outline_col)
        set_p(11, 13, outline_col)
        set_p(12, 13, outline_col)
        set_p(13, 14, outline_col)

        set_p(18, 14, outline_col)
        set_p(19, 13, outline_col)
        set_p(20, 13, outline_col)
        set_p(21, 14, outline_col)
    else:
        # Big Sparkling Emerald Eyes
        # Left Eye (x: 10..13, y: 13..14)
        set_rect(10, 13, 4, 2, COLORS["green"])
        set_p(11, 13, outline_col)  # Pupil
        set_p(11, 14, outline_col)
        set_p(10, 13, white_fur)    # Specular shine
        set_p(12, 14, fur_light)    # Iris reflection

        # Right Eye (x: 18..21, y: 13..14)
        set_rect(18, 13, 4, 2, COLORS["green"])
        set_p(19, 13, outline_col)  # Pupil
        set_p(19, 14, outline_col)
        set_p(18, 13, white_fur)    # Specular shine
        set_p(20, 14, fur_light)    # Iris reflection

    # 5. Muzzle & Nose & Whiskers
    set_p(15, 15, pink_inner)
    set_p(16, 15, pink_inner)
    set_p(15, 16, outline_col)
    set_p(16, 16, outline_col)
    set_p(14, 16, white_fur)
    set_p(17, 16, white_fur)
    set_p(14, 17, outline_col)
    set_p(17, 17, outline_col)
    set_p(15, 17, white_fur)
    set_p(16, 17, white_fur)

    # Whiskers (Left & Right 1px crisp lines)
    set_p(4, 15, white_fur)
    set_p(5, 15, white_fur)
    set_p(3, 17, white_fur)
    set_p(4, 17, white_fur)
    set_p(5, 16, white_fur)

    set_p(26, 15, white_fur)
    set_p(27, 15, white_fur)
    set_p(26, 16, white_fur)
    set_p(27, 17, white_fur)
    set_p(28, 17, white_fur)

    # 6. Collar & Golden Bell
    for x in range(9, 23):
        set_p(x, 19, COLORS["red"])
    set_rect(15, 20, 2, 2, COLORS["yellow"])  # Bell
    set_p(15, 21, fur_shade)                  # Bell hole

    # 7. Body Fur & White Bib
    for y in range(20, 28):
        for x in range(9, 23):
            if grid[y * SIZE + x] is None:
                grid[y * SIZE + x] = fur_col

    # Tabby body markings (Stripes)
    set_p(9, 22, fur_shade); set_p(10, 22, fur_shade)
    set_p(9, 25, fur_shade); set_p(10, 25, fur_shade)
    set_p(21, 22, fur_shade); set_p(22, 22, fur_shade)
    set_p(21, 25, fur_shade); set_p(22, 25, fur_shade)

    # White Chest/Bib
    for y in range(21, 27):
        for x in range(13, 19):
            set_p(x, y, white_fur)
    set_p(14, 20, white_fur); set_p(17, 20, white_fur)

    # Front Paws (White Mittens with paw lines)
    set_rect(11, 26, 3, 2, white_fur)
    set_p(12, 27, outline_col)
    set_rect(17, 26, 3, 2, white_fur)
    set_p(18, 27, outline_col)

    # 8. Tail
    if tail_up:
        # Frame 2: Tail swished higher & curved
        tail_coords = [
            (22, 26), (23, 26), (24, 25), (25, 24),
            (26, 23), (27, 21), (27, 20), (26, 18),
            (25, 17), (24, 17), (23, 18)
        ]
        for (tx, ty) in tail_coords:
            set_p(tx, ty, fur_col)
            # Outline
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if grid[(ty + dy) * SIZE + (tx + dx)] is None:
                    grid[(ty + dy) * SIZE + (tx + dx)] = outline_col
        # White tip
        set_p(24, 17, white_fur)
        set_p(23, 18, white_fur)
    else:
        # Frame 1: Tail resting curve
        tail_coords = [
            (22, 27), (23, 27), (24, 27), (25, 26),
            (26, 25), (27, 24), (27, 23), (26, 22),
            (25, 21)
        ]
        for (tx, ty) in tail_coords:
            set_p(tx, ty, fur_col)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if grid[(ty + dy) * SIZE + (tx + dx)] is None:
                    grid[(ty + dy) * SIZE + (tx + dx)] = outline_col
        # White tip
        set_p(26, 22, white_fur)
        set_p(25, 21, white_fur)

    # 9. Clean up outside outline
    return grid

def generate_dsl_script():
    lines = [
        "// PixelMirai DSL — 32x32 Royal Calico Cat (Anti-AI-Slop)",
        "size 32",
        "palette pico-8",
        "fps 4",
        "crt on",
        "",
        "// Frame 1: Cat Idle Resting Pose",
        "frame 1",
        "layer \"cat_base\"",
        ""
    ]
    grid1 = create_cat_grid(blink=False, tail_up=False)
    # Convert pixels to compact script
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
            if len(chunk) >= 12:
                lines.append(f"pixels {c} " + " ".join(chunk))
                chunk = []
        if chunk:
            lines.append(f"pixels {c} " + " ".join(chunk))

    lines.append("")
    lines.append("// Frame 2: Cat Happy Blinking & Tail Swish")
    lines.append("frame 2")
    lines.append("layer \"cat_base\"")
    grid2 = create_cat_grid(blink=True, tail_up=True)
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
            if len(chunk) >= 12:
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

def generate_pxm_project(grid1, grid2):
    frames = [
        {
            "id": "frame-1",
            "layers": [
                {
                    "id": "layer-cat-1",
                    "name": "Cat Sprite",
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
                    "id": "layer-cat-2",
                    "name": "Cat Sprite",
                    "visible": True,
                    "opacity": 1.0,
                    "blendMode": "source-over",
                    "pixels": grid2
                }
            ]
        }
    ]

    canonical_data = {
        "projectName": "32x32 Royal Calico Cat",
        "size": 32,
        "frames": frames,
        "palette": PICO_PALETTE,
        "settings": {
            "pixelPerfect": True,
            "soundEnabled": True,
            "crtFilter": True
        }
    }

    # Strict JSON without whitespace for canonical checksum
    canonical_json = json.dumps(canonical_data, separators=(',', ':'))
    checksum = compute_fnv1a_checksum(canonical_json)

    full_project = {
        "format": "PixelMirai",
        "version": 1,
        "generator": "PixelMirai Studio v3.0 (Anti-AI-Slop Engine)",
        "exportedAt": datetime.now(timezone.utc).isoformat(),
        "checksum": checksum,
        "projectName": "32x32 Royal Calico Cat",
        "size": 32,
        "paletteName": "PICO-8",
        "palette": PICO_PALETTE,
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

def apply_crt_filter(img):
    w, h = img.size
    crt_img = Image.new("RGBA", (w, h), (16, 14, 26, 255))
    
    # Backdrop vignette
    bg_draw = ImageDraw.Draw(crt_img)
    bg_draw.rectangle([0, 0, w, h], fill=(18, 16, 28, 255))
    
    # Alpha composite the cat
    crt_img.alpha_composite(img, (0, 0))

    # Apply 50% Horizontal Scanlines
    scanline_overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scanline_overlay)
    for y in range(0, h, 4):
        scan_draw.line([(0, y), (w, y)], fill=(0, 0, 0, 110), width=2)
    
    crt_img.alpha_composite(scanline_overlay, (0, 0))

    # CRT Curved Vignette
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for i in range(16):
        alpha = int((16 - i) * 6)
        vig_draw.rectangle([i, i, w - i, h - i], outline=(0, 0, 0, alpha), width=1)
    
    crt_img.alpha_composite(vignette, (0, 0))
    return crt_img

def main():
    out_dir = r"C:\Users\A\Downloads\pixelmirai-next\public\exports"
    os.makedirs(out_dir, exist_ok=True)

    grid1 = create_cat_grid(blink=False, tail_up=False)
    grid2 = create_cat_grid(blink=True, tail_up=True)

    # 1. Export DSL Script
    dsl_content = generate_dsl_script()
    dsl_path = os.path.join(out_dir, "cat-32.dsl")
    with open(dsl_path, "w", encoding="utf-8") as f:
        f.write(dsl_content)
    print(f"Saved DSL: {dsl_path}")

    # 2. Export .pxm Project File
    pxm_data = generate_pxm_project(grid1, grid2)
    pxm_path = os.path.join(out_dir, "cat-32.pxm")
    with open(pxm_path, "w", encoding="utf-8") as f:
        json.dump(pxm_data, f, indent=2)
    print(f"Saved .pxm: {pxm_path}")

    # 3. Export PNG (1x = 32x32, 16x = 512x512)
    img1_1x = grid_to_image(grid1, scale=1)
    img1_1x.save(os.path.join(out_dir, "cat-32-1x.png"))

    img1_16x = grid_to_image(grid1, scale=SCALE)
    img1_16x.save(os.path.join(out_dir, "cat-32.png"))
    print(f"Saved PNG: {os.path.join(out_dir, 'cat-32.png')}")

    # 4. Export CRT Edition PNG
    crt_img = apply_crt_filter(img1_16x)
    crt_path = os.path.join(out_dir, "cat-32-crt.png")
    crt_img.save(crt_path)
    print(f"Saved CRT PNG: {crt_path}")

    # 5. Export 2-Frame Looping Animated GIF
    img2_16x = grid_to_image(grid2, scale=SCALE)
    gif_path = os.path.join(out_dir, "cat-32.gif")
    # 350ms per frame
    img1_16x.save(
        gif_path,
        save_all=True,
        append_images=[img2_16x],
        duration=350,
        loop=0,
        disposal=2
    )
    print(f"Saved Animated GIF: {gif_path}")

    # Also copy to brain artifacts directory for easy embedding
    brain_dir = r"C:\Users\A\.gemini\antigravity\brain\d9703ca7-69c6-466b-8834-640f7dc6a023"
    import shutil
    shutil.copy(os.path.join(out_dir, "cat-32.png"), os.path.join(brain_dir, "cat-32.png"))
    shutil.copy(crt_path, os.path.join(brain_dir, "cat-32-crt.png"))
    shutil.copy(gif_path, os.path.join(brain_dir, "cat-32.gif"))
    print("Copied all outputs to brain artifact directory!")

if __name__ == "__main__":
    main()
