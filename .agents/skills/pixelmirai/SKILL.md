---
name: pixelmirai
description: >
  Generate deterministic pixel art (sprites, scenes, animations) using the
  PixelMirai Engine. Supports DSL scripting, CRT filter, multi-frame GIF
  animation, and the native .pxm project format with FNV-1a checksum.
  Zero AI slop — every pixel is placed on an integer grid by code.
version: 1.0.0
author: RianFix
tags: [pixel-art, sprite, animation, crt, pxm, retro, game-art]
entry_script: scripts/pixelmirai_compiler.py
---

# PixelMirai Engine — AI Agent Skill

> **Filosofi Inti:** Pixel art murni adalah seni integer. Setiap piksel
> berada tepat di koordinat (x, y) pada grid diskrit. Tidak ada anti-alias,
> tidak ada gradient blur, tidak ada AI upscaling. Hanya kode + matematika.

---

## Kapan Gunakan Skill Ini

- User meminta **sprite pixel art** (karakter, item, tile, icon)
- User meminta **scene pixel art** (latar belakang, landscape, interior)
- User meminta **animasi pixel art** (walk cycle, idle, attack, blink)
- User ingin **export ke format** PNG, GIF (animasi), atau `.pxm` (project)
- User ingin **CRT retro filter** pada hasil render
- User meminta **konversi DSL script** ke gambar

---

## Alur Kerja (Workflow)

```
DSL Script → pixelmirai_compiler.py → PNG + GIF + CRT + .pxm
```

1. **Tulis DSL Script** — definisikan canvas, palette, layer, frames
2. **Jalankan compiler**: `python scripts/pixelmirai_compiler.py <script.pxm.dsl>`
3. **Output** tersimpan di `public/exports/` secara otomatis
4. **Tampilkan hasilnya** ke user (PNG statis atau GIF animasi)

---

## DSL Syntax Reference

### Header Block

```dsl
canvas 64 64          # ukuran canvas (width height) — harus integer
palette pico8         # preset: pico8 | endesga32 | gameboy | cga | custom
background #0d1117    # warna background (hex) atau "transparent"
scale 8               # multiplier output PNG (1-16, default: 8)
crt on                # aktifkan CRT scanline filter (opsional)
fps 6                 # frame rate untuk GIF animasi
```

### Layer & Pixel Commands

```dsl
layer "base"          # buat layer baru (nama bebas, tapi unik)

# Format: pixel x y #rrggbb
pixel 10 10 #ff6600
pixel 11 10 #ff6600

# Shorthand fill rectangle: rect x y w h #rrggbb
rect 0 0 64 64 #1a1c2c

# Horizontal/vertical line
hline y x1 x2 #rrggbb
vline x y1 y2 #rrggbb

# Circle (outline only)
circle cx cy radius #rrggbb

# Fill circle
fillcircle cx cy radius #rrggbb

# Copy region: copy src_layer x y w h → dst_x dst_y
copy "base" 0 0 32 32 → 32 0
```

### Frame & Animation Block

```dsl
# Frame 1 (frame index mulai dari 0)
frame 0
  layer "body"
    pixel 32 20 #ff9900
    # ... pixels ...

# Frame 2 — state berbeda (animasi blink, dll)
frame 1
  layer "body"
    pixel 32 20 #ff9900
    # ... pixels (bisa beda dari frame 0) ...
  layer "eyes"
    # mata tertutup (blink frame)
    hline 28 24 26 #1a1c2c
```

### Export Commands

```dsl
export png "cat-64.png"          # PNG statis (frame 0)
export gif "cat-64.gif"          # GIF animasi semua frame
export crt "cat-64-crt.png"      # PNG + CRT filter
export pxm "cat-64.pxm"          # Project file (binary JSON + checksum)
```

---

## Palette Presets

### PICO-8 (16 warna)
| Name | Hex | Usage |
|------|-----|-------|
| black | `#000000` | outline, shadow |
| dark-blue | `#1d2b53` | deep shadow, sky |
| dark-purple | `#7e2553` | shadow, accent |
| dark-green | `#008751` | grass, foliage |
| brown | `#ab5236` | skin, wood |
| dark-grey | `#5f574f` | stone, metal |
| light-grey | `#c2c3c7` | highlights |
| white | `#fff1e8` | bright highlights |
| red | `#ff004d` | danger, health |
| orange | `#ffa300` | fire, warm tones |
| yellow | `#ffec27` | gold, light |
| green | `#00e436` | lush foliage |
| blue | `#29adff` | sky, water |
| lavender | `#83769c` | magic, UI |
| pink | `#ff77a8` | cute, healing |
| light-peach | `#ffccaa` | skin highlights |

### Endesga32 Extensions (untuk 64×64+)
Tersedia 16 warna tambahan via `palette endesga32`. Lihat
`references/palette-endesga32.md` untuk daftar lengkap.

---

## Format File `.pxm`

`.pxm` adalah format project PixelMirai — JSON terenkripsi dengan checksum
FNV-1a 32-bit. Dapat di-load langsung oleh PixelMirai Studio (web app).

### Struktur Internal

```json
{
  "version": "1.0",
  "format": "PixelMirai",
  "name": "nama-project",
  "width": 64,
  "height": 64,
  "palette": ["#000000", "#ff6600", ...],
  "frames": [
    {
      "index": 0,
      "layers": [
        {
          "name": "base",
          "pixels": [[x, y, paletteIndex], ...]
        }
      ]
    }
  ],
  "fps": 6,
  "checksum": "9d43519a"
}
```

### Validasi Checksum

```js
// Dari lib/project-file.js
import { validateProjectData } from './lib/project-file.js';
const result = validateProjectData(projectObj);
// { valid: true, errors: [] }  ✅
```

```python
# Dari Python engine
def fnv1a_32(data: bytes) -> str:
    h = 2166136261
    for b in data:
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF
    return format(h, '08x')
```

---

## Aturan Grid Integer (WAJIB)

> ⚠️ **JANGAN PERNAH MELANGGAR ATURAN INI**

1. **Semua koordinat HARUS integer** — tidak ada `x=10.5`, tidak ada float
2. **Semua warna HARUS dari palette** — tidak ada warna di luar daftar
3. **Scale HARUS integer** — `scale 8` bukan `scale 7.5`
4. **Tidak ada anti-aliasing** — setiap piksel solid, tidak ada opacity
5. **Tidak ada gradient** — kecuali dinyatakan explisit via step bertingkat
6. **Outline hitam** — sprite harus punya outline `#000000` atau `#1d2b53`

---

## Menjalankan Compiler

### Basic Usage

```bash
# Generate dari DSL script
python scripts/pixelmirai_compiler.py scripts/my_sprite.pxm.dsl

# Dengan output directory kustom
python scripts/pixelmirai_compiler.py my_sprite.pxm.dsl --out public/exports/

# Mode verbose (debug tiap pixel)
python scripts/pixelmirai_compiler.py my_sprite.pxm.dsl --verbose

# Hanya export PNG (skip GIF & CRT)
python scripts/pixelmirai_compiler.py my_sprite.pxm.dsl --only png
```

### Python API (Direct)

```python
from scripts.pixelmirai_compiler import PixelMiraiEngine

engine = PixelMiraiEngine(width=64, height=64)
engine.set_palette('pico8')
engine.set_background('#0d1117')

# Frame 0
frame = engine.new_frame()
layer = frame.new_layer('body')
layer.rect(0, 0, 64, 64, '#1a1c2c')
layer.pixel(32, 20, '#ff9900')

# Render
engine.export_png('output.png', scale=8)
engine.export_gif('output.gif', fps=6)
engine.export_crt('output-crt.png', scale=8)
engine.export_pxm('output.pxm')
```

---

## HTTP API Endpoint

PixelMirai Studio menyediakan REST API untuk generate pixel art:

```
POST /api/generate
Content-Type: application/json

{
  "dsl": "canvas 32 32\npalette pico8\n...",
  "format": ["png", "gif", "pxm"]
}

Response:
{
  "png": "data:image/png;base64,...",
  "gif": "data:image/gif;base64,...",
  "pxm": { ...project object... },
  "checksum": "9d43519a"
}
```

---

## Contoh Lengkap — Sprite Karakter

Lihat `examples/` untuk referensi sprite siap pakai:

| File | Deskripsi |
|------|-----------|
| `examples/cat-32.pxm.dsl` | Royal Calico Cat 32×32, 2-frame blink |
| `examples/cat-64.pxm.dsl` | Royal Calico Cat 64×64, detail tinggi |
| `examples/knight-32.pxm.dsl` | 8-bit Knight, 4-frame walk cycle |
| `examples/coin-16.pxm.dsl` | Gold coin, 4-frame spin |

---

## CRT Filter Spec

Saat `crt on` diaktifkan:
- **Scanlines**: garis hitam horizontal setiap 2 piksel (opacity 40%)
- **Vignette**: sudut gelap melingkar (gradient radial)
- **Background**: hitam (`#0d1117`) menggantikan putih
- **Glow**: subtle green/amber phosphor glow (opsional, via `crt phosphor green`)
- **Tidak mengubah grid** — CRT hanya di compositing layer, piksel asli intact

---

## Batasan & Tips

| Batas | Nilai | Keterangan |
|-------|-------|-----------|
| Canvas min | 8×8 | Terlalu kecil untuk detail |
| Canvas max | 256×256 | Di atas ini pakai scene split |
| Frame max | 60 | Untuk GIF; RAM heavy di atas 30 |
| Palette max | 256 warna | Biasanya cukup 16-32 |
| Scale max | 16× | 256px × 16 = 4096px PNG |
| FPS range | 1–30 | GIF optimal: 6–12 FPS |

**Tips:**
- Mulai dari **outline** dulu, lalu fill, baru shadow/highlight
- Gunakan **odd pixel counts** untuk simetri (31 bukan 32 untuk tengah di 16)
- Untuk animasi walk cycle: minimal 4 frame (stand-step-stand-step)
- CRT filter paling bagus di canvas kecil (16-64px), di-scale besar (8-16×)
- `.pxm` files bisa di-drag-drop langsung ke PixelMirai Studio

---

## Output Files

Semua file output tersimpan di `public/exports/` (accessible via `/exports/`):

```
public/exports/
├── nama-project.png         # PNG statis frame 0
├── nama-project.gif         # GIF animasi
├── nama-project-crt.png     # PNG + CRT filter
└── nama-project.pxm         # Project file (loadable di Studio)
```

---

## Integrasi dengan PixelMirai Studio

File `.pxm` yang di-generate bisa langsung dibuka di PixelMirai Studio:

1. Buka `http://localhost:3000/studio`
2. Klik **"Buka Project"** (atau drag-drop `.pxm` file)
3. Edit langsung di canvas — semua layer tetap terpreservasi
4. Export ulang via Studio UI atau API

---

*PixelMirai Engine — Pixel art tak akan luntur oleh zaman.*  
*Dibuat oleh [@RianFix](https://github.com/RianFix)*
