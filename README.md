<div align="center">👾 PixelMirai Agent

Deterministic Pixel Art Engine & AI Agent Skill

"Pixel art never fades with time."

""License: MIT" (https://img.shields.io/badge/License-MIT-yellow.svg)" (https://opensource.org/licenses/MIT)
""CI" (https://github.com/riantosee/PixelMirai-Agent/actions/workflows/ci.yml/badge.svg)" (https://github.com/riantosee/PixelMirai-Agent/actions)
""Python 3.10+" (https://img.shields.io/badge/python-3.10+-blue.svg)" (https://www.python.org/downloads/)
""No AI Slop" (https://img.shields.io/badge/AI%20Slop-0%25%20Pure%20Grid-success)" (https://github.com/riantosee/PixelMirai-Agent)
""Custom Format" (https://img.shields.io/badge/Format-.pxm%20(FNV--1a)-ff007f)" (docs/pxm-format-spec.md)
""Creator" (https://img.shields.io/badge/Creator-Rian-8a2be2)" (https://github.com/riantosee)

<br/>" 🇬🇧 English " (#-english)  | 
" 🇮🇩 Bahasa Indonesia " (#-bahasa-indonesia)  | 
" 🇯🇵 日本語 " (#-日本語)

</div>---

🎨 Gallery & Live Renders (Zero AI Slop)

Every sprite showcased below is rendered using the PixelMirai Engine through explicit code and integer-based drawing operations on a discrete pixel grid.

🐱 Royal Calico Cat (64×64)| 📺 64×64 CRT Retro Edition
<img src="assets/cat-64.gif" width="256" alt="Royal Calico Cat 64x64 GIF" />| <img src="assets/cat-64-crt.png" width="256" alt="Royal Calico Cat CRT Scanline" />
2-frame idle animation with blinking and tail movement| CRT phosphor scanlines and radial vignette

⚔️ 8-Bit Knight (32×32)| 🐱 Classic Cat (32×32)| 🪙 Gold Coin (16×16)
<img src="assets/knight-32.gif" width="200" alt="Knight 32x32 Walk Cycle" />| <img src="assets/cat-32.gif" width="200" alt="Classic Cat 32x32" />| <img src="assets/coin-16.gif" width="200" alt="Spinning Coin 16x16" />
4-frame walking animation| 2-frame idle and eye-blink animation| 4-frame spinning animation

---

🇬🇧 English

🌟 Philosophy: Pure Grid, Zero AI Slop

Generative image models can produce pixel-art-style images with blurry edges, inconsistent pixel sizes, unwanted anti-aliasing, and colors that do not follow a coherent retro palette.

PixelMirai Engine takes a code-first approach to pixel art: define drawing operations explicitly and render them through a predictable pixel-grid workflow.

1. 100% Integer Grid — Work with discrete "(x, y)" coordinates to maintain crisp pixel placement.
2. Curated Retro Palettes — Use palettes inspired by classic gaming systems, including PICO-8, Endesga32, Game Boy, and CGA.
3. Custom ".pxm" Format — Use a JSON-based project format with a documented FNV-1a 32-bit checksum mechanism.
4. AI Agent Ready — Provide compatible coding agents with project instructions through "SKILL.md" to help create structured pixel-art assets.

✨ Core Features

- 📜 PixelMirai DSL — A declarative scripting language with drawing commands such as "pixel", "rect", "hline", "vline", "circle", and "fillcircle".
- 🎬 Multi-Frame Animation — Define frame-by-frame sprite animations and export supported sequences as animated GIFs.
- 📺 CRT Retro Filter — Apply optional horizontal scanlines and vignette effects inspired by classic arcade monitors.
- 🎨 Retro Palette Support — Work with curated color palettes for consistent pixel-art aesthetics.
- 📦 ".pxm" Project Format — Store project data in a custom JSON-based format with an FNV-1a checksum for integrity verification.
- 🛠️ Python CLI Compiler — Compile DSL scripts into supported image and project formats from the command line.
- 🤖 AI Agent Skill ("SKILL.md") — Give compatible coding agents a structured guide for working with PixelMirai.

---

🚀 Quick Start Guide

1. Requirements & Installation

Requires Python 3.10 or newer and Pillow.

git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent
python -m pip install -r requirements.txt

2. Compile a Sprite Using the CLI

Compile the 32×32 knight example:

python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

Render the 64×64 cat with a CRT effect and 8× scaling:

python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

Export only the animated GIF:

python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif

Check the available compiler options:

python scripts/pixelmirai_compiler.py --help

3. PixelMirai DSL Example

Example file: "examples/coin-16.pxm.dsl"

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

This example demonstrates canvas configuration, palette selection, background settings, frame definitions, layers, drawing commands, and export directives.

Explore the ""examples/"" (examples/) directory for more scripts.

4. Python API

The compiler may also be used programmatically. The following illustrates the intended usage pattern; confirm the exact methods against the current implementation before relying on it.

from scripts.pixelmirai_compiler import PixelMiraiEngine

engine = PixelMiraiEngine(width=32, height=32)
engine.set_palette("pico8")
engine.set_background("transparent")

frame = engine.new_frame(0)
layer = frame.new_layer("character")

layer.rect(10, 10, 12, 12, "#ffa300")
layer.pixel(14, 14, "#00e436")

engine.export_png("output.png", scale=12)
engine.export_pxm("output.pxm")

5. Testing

If the repository contains the test suite and development requirements, install them and run:

python -m pip install -r requirements-dev.txt
pytest tests/ -v

See the current repository files and CI workflow for the test commands supported by your checkout.

---

🧠 Design Principles

PixelMirai is built around several principles:

- Explicit over ambiguous — Sprite construction should be represented by understandable drawing instructions.
- Consistency over randomness — The same input should produce predictable rendering results under the same engine conditions.
- Pixel precision over artificial smoothness — Preserve the visual character of a discrete pixel grid.
- Automation over repetitive work — Enable scripts and compatible coding agents to create and reproduce assets.
- Open tooling over lock-in — Keep the project inspectable and extensible through Python and documented formats.

---

🗺️ Roadmap

Potential areas for continued development include:

- Improved DSL parsing and error reporting.
- More drawing primitives and palette options.
- Reliable alpha-transparency handling across supported exports.
- Stronger ".pxm" validation and project-loading support.
- Expanded automated tests and continuous integration.
- Better documentation and compatibility with AI coding agents.

See "GitHub Issues" (https://github.com/riantosee/PixelMirai-Agent/issues) for current bugs, suggestions, and development discussions.

---

🇮🇩 Bahasa Indonesia

🌟 Filosofi: Murni Grid, Bebas AI Slop

Di era ketika model difusi generatif sering menghasilkan gambar bergaya pixel art dengan piksel buram, ukuran piksel tidak konsisten, warna bercampur, dan tepi anti-aliasing yang mengganggu estetika retro, PixelMirai Engine hadir dengan pendekatan berbasis kode.

1. 100% Integer Grid — Setiap piksel menggunakan koordinat "(x, y)" bulat untuk menjaga penempatan piksel tetap presisi.
2. Palet Retro Terkurasi — Mendukung palet yang terinspirasi dari perangkat gaming klasik seperti PICO-8, Endesga32, Game Boy, dan CGA.
3. Format ".pxm" — Format proyek berbasis JSON dengan mekanisme checksum FNV-1a 32-bit yang terdokumentasi.
4. Siap untuk AI Agent — Instruksi "SKILL.md" membantu coding agent yang kompatibel bekerja dengan proyek PixelMirai.

✨ Fitur Utama

- 📜 PixelMirai DSL — Bahasa scripting deklaratif dengan perintah seperti "pixel", "rect", "hline", "vline", "circle", dan "fillcircle".
- 🎬 Animasi Multi-Frame — Membuat animasi sprite berdasarkan frame dan mengekspor urutan yang didukung menjadi GIF.
- 📺 CRT Retro Filter — Efek scanline horizontal dan vignette yang terinspirasi monitor arcade klasik.
- 🎨 Palet Retro — Mendukung palet warna untuk estetika pixel art yang konsisten.
- 📦 Format Proyek ".pxm" — Menyimpan data proyek dalam format JSON khusus dengan mekanisme checksum FNV-1a.
- 🛠️ CLI Compiler Python — Mengompilasi script DSL melalui command line.
- 🤖 AI Agent Skill ("SKILL.md") — Panduan terstruktur bagi coding agent yang kompatibel.

---

🚀 Panduan Memulai Cepat

1. Prasyarat dan Instalasi

Membutuhkan Python 3.10 atau lebih baru dan Pillow.

git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent
python -m pip install -r requirements.txt

2. Menjalankan CLI Compiler

Compile sprite kesatria berukuran 32×32:

python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

Render kucing 64×64 dengan CRT filter dan skala 8×:

python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

Ekspor hanya animasi GIF:

python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif

Lihat opsi compiler yang tersedia:

python scripts/pixelmirai_compiler.py --help

3. Contoh Sintaks DSL

Contoh file "examples/coin-16.pxm.dsl":

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

Contoh tersebut menunjukkan konfigurasi canvas, pemilihan palet, latar belakang, frame, layer, perintah menggambar, dan instruksi ekspor.

---

🇯🇵 日本語

🌟 開発理念：純粋なグリッド、AIスロップの排除

生成AIによる画像には、ピクセルのぼやけ、不均一なサイズ、混ざった色、不要なアンチエイリアスなどが発生することがあります。

PixelMirai Engine は、明示的なコードと離散的なピクセルグリッドを使って、再現性のあるドット絵制作を目指します。

1. 整数グリッド — "(x, y)" の整数座標を使い、ピクセルの配置を明確にします。
2. レトロパレット — PICO-8、Endesga32、Game Boy、CGA などに着想を得た配色を扱います。
3. 独自の ".pxm" 形式 — FNV-1a 32ビットチェックサムの仕組みを文書化した JSON ベースのプロジェクト形式です。
4. AIエージェント対応 — "SKILL.md" により、対応するコーディングエージェントがプロジェクトのルールを理解しやすくなります。

✨ 主な機能

- 📜 PixelMirai DSL — ピクセルアートを記述する宣言型スクリプト言語。
- 🎬 マルチフレームアニメーション — フレームを定義し、対応する形式に出力。
- 📺 CRTレトロフィルター — スキャンラインとビネットによるレトロな画面効果。
- 🎨 レトロパレット — 一貫したドット絵制作のための配色サポート。
- 📦 ".pxm" プロジェクト形式 — JSON ベースの独自形式とチェックサムの仕組み。
- 🛠️ Python CLI コンパイラ — コマンドラインから DSL スクリプトをコンパイル。
- 🤖 AIエージェントスキル — 対応するコーディングエージェント向けの手順書。

---

🚀 クイックスタート

1. インストール

Python 3.10 以上と Pillow が必要です。

git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent
python -m pip install -r requirements.txt

2. CLI コンパイラの使用

32×32 のナイトの例をコンパイルします。

python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

CRT エフェクト付きで 64×64 のネコを出力します。

python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

アニメーション GIF のみを出力します。

python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif

3. DSL の例

"examples/coin-16.pxm.dsl" には、キャンバス、パレット、背景、フレーム、レイヤー、描画コマンド、出力設定の例があります。

---

📁 Project Structure

PixelMirai-Agent/
├── .agents/
│   └── skills/
│       └── pixelmirai/
│           ├── SKILL.md
│           ├── examples/
│           └── references/
├── assets/
│   ├── cat-64.gif
│   ├── cat-64-crt.png
│   ├── cat-32.gif
│   ├── knight-32.gif
│   └── coin-16.gif
├── docs/
│   ├── dsl-specification.md
│   ├── palette-endesga32.md
│   └── pxm-format-spec.md
├── examples/
│   ├── cat-64.pxm.dsl
│   ├── cat-32.pxm.dsl
│   ├── knight-32.pxm.dsl
│   └── coin-16.pxm.dsl
├── scripts/
│   ├── pixelmirai_compiler.py
│   ├── generate_cat_art.py
│   └── generate_cat_64.py
├── SKILL.md
├── requirements.txt
├── LICENSE
└── README.md

The exact contents may change as the project evolves.

---

👨‍💻 Creator & Socials

Created with passion by Rian.

- 🐙 GitHub: "@riantosee" (https://github.com/riantosee) · "@RianFix" (https://github.com/RianFix)
- 📸 Instagram: "@bisarianbisaryan" (https://www.instagram.com/bisarianbisaryan/)

"Pixel art never fades with time. Timeless in every era, precise in every grid."

---

📄 License

This project is open-source software released under the terms of the "MIT License" (LICENSE).