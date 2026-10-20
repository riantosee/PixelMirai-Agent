<div align="center">

# 👾 PixelMirai Agent
### Deterministic Pixel Art Engine & AI Agent Skill
**"Pixel art will never fade with time."**  
*Pixel art tak akan luntur oleh zaman. | ドット絵は時代に色褪せない。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/riantosee/PixelMirai-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/riantosee/PixelMirai-Agent/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![No AI Slop](https://img.shields.io/badge/AI%20Slop-0%25%20Pure%20Grid-success)](https://github.com/riantosee/PixelMirai-Agent)
[![Custom Format](https://img.shields.io/badge/Format-.pxm%20(FNV--1a)-ff007f)](docs/pxm-format-spec.md)
[![Creator](https://img.shields.io/badge/Creator-Rian-8a2be2)](https://github.com/riantosee)

<br/>

**[ 🇬🇧 English ](#-english)** &nbsp;|&nbsp; 
**[ 🇮🇩 Bahasa Indonesia ](#-bahasa-indonesia)** &nbsp;|&nbsp; 
**[ 🇯🇵 日本語 ](#-日本語)**

</div>

---

## 🎨 Gallery & Live Renders (Zero AI Slop)

Every sprite showcased below is rendered using the **PixelMirai Engine** through explicit code and discrete integer grid mathematics — zero diffusion blur, zero anti-aliasing artifacts:

| 🐱 Royal Calico Cat (64×64) | 📺 64×64 CRT Retro Edition |
|:---:|:---:|
| <img src="assets/cat-64.gif" width="256" alt="Royal Calico Cat 64x64 GIF" /> | <img src="assets/cat-64-crt.png" width="256" alt="Royal Calico Cat CRT Scanline" /> |
| *2-Frame Idle + Blink & Tail Movement* | *CRT Phosphor Scanlines + Radial Vignette* |

| ⚔️ 8-Bit Knight (32×32) | 🐱 Classic Cat (32×32) | 🪙 Gold Coin (16×16) |
|:---:|:---:|:---:|
| <img src="assets/knight-32.gif" width="200" alt="Knight 32x32 Walk Cycle" /> | <img src="assets/cat-32.gif" width="200" alt="Classic Cat 32x32" /> | <img src="assets/coin-16.gif" width="200" alt="Spinning Coin 16x16" /> |
| *4-Frame Walking Animation* | *2-Frame Idle & Eye-Blink Animation* | *4-Frame 3D Spin Cycle (Transparent)* |

---

# 🇬🇧 English

### 🌟 Philosophy: Pure Grid, Zero AI Slop
Generative diffusion models often produce pixel-art-style images with blurry edges, inconsistent pixel sizes, unwanted anti-aliasing, and muddy palettes that break the retro aesthetic.

**PixelMirai Engine** takes a code-first approach to pixel art: define drawing operations explicitly and render them through a deterministic pixel-grid workflow.

1. **100% Integer Grid** — Work with discrete `(x, y)` coordinates to maintain crisp pixel placement without subpixel blur.
2. **Curated Retro Palettes** — Strict palettes inspired by classic gaming hardware, including PICO-8, Endesga32, Game Boy, and CGA.
3. **Custom `.pxm` Format** — Lightweight JSON project format with a documented FNV-1a 32-bit checksum mechanism.
4. **AI Agent Native** — Out-of-the-box instructions (`SKILL.md`) enabling LLM coding agents (Antigravity, Claude, Cursor, Copilot) to generate structured pixel-art assets.

---

### ✨ Core Features
- 📜 **PixelMirai DSL** — Declarative scripting language with drawing commands: `pixel`, `pixels`, `rect`, `hline`, `vline`, `circle`, and `fillcircle`.
- 🎬 **Multi-Frame Animation** — Define timeline frames and export supported sequences as smooth loopable animated GIFs.
- 📺 **CRT Retro Filter** — Optional horizontal scanline darkening and radial vignette effects replicating classic arcade monitors.
- 💎 **True Alpha Transparency** — Declaring `background transparent` generates authentic 32-bit RGBA PNGs and transparent animated GIFs.
- 📦 **`.pxm` Project Standard & Round-Trip** — Store project data in a custom JSON format with FNV-1a checksum validation. Supports both exporting and reloading via `load_pxm()`.
- 🛡️ **Strict Syntax & Resource Bounds** — Validates syntax, canvas dimensions, scales, and coordinates with line-accurate error reporting.
- 🛠️ **Python CLI Compiler** — Compile DSL scripts into images and project files directly from the command line.
- 🤖 **Universal AI Agent Skill** — Standard `SKILL.md` frontmatter for seamless LLM integration.

---

### 🚀 Quick Start Guide

#### 1. Requirements & Installation
Requires Python 3.10 or newer and Pillow:
```bash
git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent
pip install -r requirements.txt
```

To install development and testing dependencies:
```bash
pip install -r requirements-dev.txt
```

#### 2. Compiling DSL via CLI
Convert any `.pxm.dsl` file into PNG, GIF, CRT renders, and `.pxm` containers:
```bash
# Compile the 32x32 knight example (strict mode by default)
python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

# Render the 64x64 cat with a CRT filter and 8x scaling
python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

# Export only the animated GIF
python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif

# Lenient mode (skips invalid lines without terminating)
python scripts/pixelmirai_compiler.py my_sprite.pxm.dsl --lenient
```

#### 3. PixelMirai DSL Syntax Example (`examples/coin-16.pxm.dsl`)
```dsl
canvas 16 16
palette pico8
background transparent
scale 16
fps 10

frame 0
  layer "coin"
    fillcircle 8 8 6 #ffec27
    circle 8 8 6 #ab5236
    fillcircle 8 8 4 #ffa300

frame 1
  layer "coin"
    rect 5 2 6 12 #ffec27
    vline 5 2 13 #ab5236

export png "coin-16.png"
export gif "coin-16.gif"
export pxm "coin-16.pxm"
```

#### 4. Python API Usage
You can also use the engine programmatically in Python applications:
```python
from scripts.pixelmirai_compiler import PixelMiraiEngine

# Initialize 32x32 canvas
engine = PixelMiraiEngine(width=32, height=32)
engine.set_palette("pico8")
engine.set_background("transparent")  # True RGBA transparency

# Draw on frame 0
frame = engine.new_frame(0)
layer = frame.new_layer("character")
layer.rect(10, 10, 12, 12, "#ffa300")
layer.pixel(14, 14, "#00e436")

# Export formats
engine.export_png("output.png", scale=12)
engine.export_pxm("output.pxm")

# Load and verify existing .pxm project file
loaded = PixelMiraiEngine.load_pxm("output.pxm", verify_checksum=True)
print(f"Loaded {loaded.name} with {len(loaded.frames)} frame(s)!")
```

#### 5. Running Automated Tests
Run the comprehensive test suite covering parser edge cases, validation, transparency, exports, and CLI behavior:
```bash
pytest tests/ -v
```

---

### 🧠 Design Principles

- **Explicit over ambiguous** — Sprite construction is represented by clear, deterministic drawing instructions.
- **Consistency over randomness** — The exact same input script produces identical results every time.
- **Pixel precision over artificial smoothness** — Preserve the sharp, authentic character of a discrete pixel grid.
- **Automation over repetitive work** — Enable scripts and AI coding agents to create and reproduce assets programmatically.
- **Open tooling over lock-in** — Keep the project inspectable and extensible through standard Python and documented formats.

---

# 🇮🇩 Bahasa Indonesia

### 🌟 Filosofi: Murni Grid, Bebas AI Slop
Dalam era di mana model difusi generatif sering menghasilkan "AI Slop" (pixel kabur, subpixel tidak rata, warna pecah, tepi anti-aliasing yang merusak estetika retro), **PixelMirai Engine** hadir membawa filosofi keaslian berbasis kode:
1. **100% Integer Grid** — Setiap piksel terikat pada koordinat `(x, y)` bulat untuk menjaga penempatan piksel tetap presisi.
2. **Palet Retro Terkurasi** — Palet konsol retro otentik terkurasi (PICO-8, Endesga32, GameBoy, CGA).
3. **Format Asli `.pxm`** — Format proyek berbasis JSON dengan validasi checksum FNV-1a 32-bit untuk integritas data.
4. **Siap untuk AI Agent** — Dilengkapi panduan `SKILL.md` agar coding agent (Antigravity, Claude, Cursor, Copilot) dapat memproduksi aset game pixel art murni secara otonom.

---

### ✨ Fitur Utama
- 📜 **PixelMirai DSL** — Bahasa scripting deklaratif sederhana (`pixel`, `pixels`, `rect`, `hline`, `vline`, `circle`, `fillcircle`).
- 🎬 **Animasi Multi-Frame** — Pembuatan animasi sprite frame-by-frame yang langsung diekspor menjadi GIF berulang mulus (*seamless loop*).
- 📺 **CRT Retro Filter** — Efek opsional scanlines CRT horizontal dan vignette sudut layar gaya monitor arcade tahun 80-an.
- 💎 **Transparansi Alpha Sejati** — Mendukung `background transparent` untuk menghasilkan PNG 32-bit RGBA dan GIF transparan.
- 📦 **Format `.pxm` & Round-Trip** — Format project berbasis JSON tervalidasi checksum FNV-1a 32-bit, mendukung export maupun import via `load_pxm()`.
- 🛡️ **Validasi Ketat & Batas Resource** — Melaporkan error baris secara presisi untuk sintaks atau perintah yang tidak valid.
- 🤖 **AI Agent Skill (`SKILL.md`)** — Panduan terstruktur bagi coding agent yang kompatibel.

---

### 🚀 Panduan Memulai Cepat

#### 1. Prasyarat & Instalasi
Membutuhkan Python 3.10 atau lebih baru dan library Pillow:
```bash
git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent
pip install -r requirements.txt
```

Untuk instalasi dependensi pengujian & pengembangan:
```bash
pip install -r requirements-dev.txt
```

#### 2. Menjalankan CLI Compiler
Compile file DSL menjadi PNG, GIF, CRT, dan file project `.pxm`:
```bash
# Compile contoh sprite kesatria 32x32
python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

# Export kucing 64x64 dengan CRT filter dan scale 8x
python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

# Hanya export format GIF animasi
python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif

# Mode lenient (melewati baris error tanpa membatalkan proses)
python scripts/pixelmirai_compiler.py my_sprite.pxm.dsl --lenient
```

#### 3. Menjalankan Unit Test
Jalankan pengujian otomatis:
```bash
pytest tests/ -v
```

---

# 🇯🇵 日本語

### 🌟 開発理念：純粋なグリッド、AIスロップの排除
現代の生成AI（拡散モデル）が生成する「ドット絵風画像」には、サブピクセルのにじみ、混濁したカラーパレット、不自然なアンチエイリアスなどの「AIスロップ（粗悪なAI生成物）」が頻繁に見られます。  
**PixelMirai Engine** は、明示的なコードと離散的なピクセルグリッドを使って、再現性のあるドット絵制作を目指します：
1. **完全な整数グリッド (100% Integer Grid)** — `(x, y)` の整数座標を使い、ピクセルの配置を明確にします。
2. **厳格なレトロパレット** — PICO-8、Endesga32、ゲームボーイ、CGA など時代を彩った名機のカラーパレットのみを使用。
3. **独自プロジェクト形式 `.pxm`** — 改ざん防止と整合性のための FNV-1a 32ビットチェックサムを搭載。
4. **AIエージェント対応スキル** — `SKILL.md` により、AIコーディングエージェントが自律的に本物のドット絵を生成可能。

---

### ✨ 主な機能
- 📜 **PixelMirai DSL** — 直感的でわかりやすい宣言型スクリプト言語。
- 🎬 **マルチフレームアニメーション** — 複数フレームを記述するだけで、スムーズにループするGIFアニメーションを出力。
- 📺 **CRTレトロフィルター** — アーケード筐体やブラウン管テレビのスキャンラインと周辺減光をシミュレート。
- 💎 **完全透過アルファ対応** — `background transparent` で透過PNGおよび透過GIFを正確に出力。
- 📦 **`.pxm` プロジェクト仕様** — レイヤー構造やパレットを保持し、`load_pxm()` による読み込み・検証に対応。

---

### 🚀 クイックスタート

#### 1. インストール
Python 3.10以上とPillowが必要です：
```bash
git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent
python -m pip install -r requirements.txt
```

#### 2. CLIコンパイラの使用例
```bash
# 32x32 ナイト（歩行ループ）のビルド
python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

# 64x64 ネコ（CRTスキャンライン付き）
python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

# アニメーションGIFのみを出力
python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif
```

---

## 📁 Project Structure

```
PixelMirai-Agent/
├── .agents/
│   └── skills/
│       └── pixelmirai/
│           ├── SKILL.md                 # Agent Skill definition & instructions
│           ├── examples/                # Sample DSL scripts for agent training
│           └── references/              # Color palettes & format specifications
├── assets/                              # High-resolution showcase GIFs and renders
│   ├── cat-64.gif
│   ├── cat-64-crt.png
│   ├── cat-32.gif
│   ├── knight-32.gif
│   └── coin-16.gif
├── docs/                                # Technical specifications
│   ├── dsl-specification.md
│   ├── palette-endesga32.md
│   └── pxm-format-spec.md
├── examples/                            # Ready-to-compile DSL sprite samples
│   ├── cat-64.pxm.dsl
│   ├── cat-32.pxm.dsl
│   ├── knight-32.pxm.dsl
│   └── coin-16.pxm.dsl
├── scripts/
│   ├── pixelmirai_compiler.py           # Core CLI and Python compilation engine
│   ├── generate_cat_art.py              # Procedural 32x32 generator
│   └── generate_cat_64.py               # Procedural 64x64 generator
├── tests/                               # Comprehensive automated test suite (pytest)
│   ├── test_cli.py
│   ├── test_dsl_parser.py
│   ├── test_examples.py
│   ├── test_exports_and_pxm.py
│   ├── test_transparency.py
│   └── test_validation.py
├── SKILL.md                             # Root Agent Skill entrypoint
├── requirements.txt                     # Runtime dependencies (Pillow)
├── requirements-dev.txt                 # Dev & Test dependencies (pytest)
├── LICENSE                              # MIT License
└── README.md                            # Documentation & showcase
```

---

## 👨‍💻 Creator & Socials

Created with passion by **Rian (@riantosee / @RianFix)**  
- 🐙 **GitHub**: [@riantosee](https://github.com/riantosee) & [@RianFix](https://github.com/RianFix)
- 📸 **Instagram**: [@bisarianbisaryan](https://www.instagram.com/bisarianbisaryan/)

*"Pixel art will never fade with time. Timeless in every era, precise in every grid."*

---

## 📄 License
This project is open-source software released under the terms of the [MIT License](LICENSE).
