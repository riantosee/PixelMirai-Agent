<div align="center">👾 PixelMirai Agent

A Deterministic Pixel Art Engine & AI Agent Skill

Create pixel art with precision. Animate with code. Build with consistency.

Pixel art never fades with time.

<br>""License: MIT" (https://img.shields.io/badge/License-MIT-yellow.svg)" (LICENSE)
""Python 3.10+" (https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)" (https://www.python.org/downloads/)
""Pillow" (https://img.shields.io/badge/Powered%20by-Pillow-8CAAE6.svg)" (https://python-pillow.org/)
""GitHub Stars" (https://img.shields.io/github/stars/riantosee/PixelMirai-Agent?style=flat&logo=github)" (https://github.com/riantosee/PixelMirai-Agent/stargazers)
""Issues" (https://img.shields.io/github/issues/riantosee/PixelMirai-Agent)" (https://github.com/riantosee/PixelMirai-Agent/issues)

"Explore the Gallery" (#-pixel-art-gallery) · "Quick Start" (#-quick-start) · "Documentation" (#-documentation) · "Contributing" (#-contributing)

</div>---

🎨 Pixel Art Gallery

PixelMirai is built around a simple idea: every pixel should be intentional.

Sprites and animations can be described through a compact domain-specific language (DSL) and rendered by a Python-based engine. The goal is predictable, reproducible pixel art without relying on generative image output.

<div align="center">🐱 Royal Calico Cat · 64×64| 📺 CRT Retro Edition
<img src="assets/cat-64.gif" width="280" alt="Animated 64 by 64 royal calico cat sprite">| <img src="assets/cat-64-crt.png" width="280" alt="Royal calico cat with a retro CRT effect">
Idle animation, blinking, and tail movement| Retro scanlines and vignette effect

⚔️ 8-Bit Knight · 32×32| 🐱 Classic Cat · 32×32| 🪙 Gold Coin · 16×16
<img src="assets/knight-32.gif" width="180" alt="Animated 8-bit knight walking">| <img src="assets/cat-32.gif" width="180" alt="Classic animated pixel cat">| <img src="assets/coin-16.gif" width="180" alt="Animated spinning gold coin">
Walking animation| Idle and blink animation| Spinning coin animation

</div>---

✨ Why PixelMirai?

PixelMirai explores a code-first approach to pixel art, where sprites are defined using explicit drawing commands and discrete coordinates.

- 🎯 Deterministic Rendering — Generate artwork from explicit instructions instead of relying on random image generation.
- 📐 Integer-Based Pixel Grids — Design around discrete pixel coordinates for crisp, consistent sprite construction.
- 🎨 Retro Color Palettes — Work with palettes inspired by classic gaming aesthetics, including PICO-8, Endesga32, Game Boy, and CGA.
- 🎬 Frame-Based Animation — Define multiple frames and compile supported animations into GIF files.
- 📺 CRT Effects — Add a retro monitor look with optional scanlines and vignette effects.
- 📜 PixelMirai DSL — Describe sprites with readable commands instead of manually editing every pixel.
- 🤖 AI Agent Integration — Use the included "SKILL.md" instructions to help compatible coding agents work with the engine.
- 📦 PixelMirai Project Format — Work with the custom ".pxm" project format and its documented serialization and integrity mechanisms.

PixelMirai is designed for developers, indie game creators, pixel artists, and AI-agent builders who value reproducible asset generation.

🚀 Quick Start

1. Requirements

- Python 3.10 or newer
- Git
- Pillow and the dependencies listed in "requirements.txt"

2. Install

git clone https://github.com/riantosee/PixelMirai-Agent.git
cd PixelMirai-Agent

python -m venv .venv

Activate the virtual environment:

Windows

.venv\Scripts\activate

Linux / macOS

source .venv/bin/activate

Install the dependencies:

python -m pip install -r requirements.txt

3. Compile Your First Sprite

Compile the included knight example:

python scripts/pixelmirai_compiler.py examples/knight-32.pxm.dsl

Render the cat with a CRT effect and increased output scale:

python scripts/pixelmirai_compiler.py examples/cat-64.pxm.dsl --crt --scale 8

Export only the animated GIF:

python scripts/pixelmirai_compiler.py examples/coin-16.pxm.dsl --only gif

Check the compiler's available options with:

python scripts/pixelmirai_compiler.py --help

«Output formats and command-line options depend on the current compiler implementation. Use "--help" to confirm the options supported by your version.»

---

🧩 Meet the PixelMirai DSL

PixelMirai DSL is a small, declarative language for describing pixel art. A script can define a canvas, palette, background, frames, layers, and drawing commands.

Example: Animated Coin

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

Save the script as "coin-16.pxm.dsl", then compile it using the CLI.

Explore the ""examples/"" (examples/) directory for more sample scripts.

---

🛠️ Use Cases

PixelMirai can serve as a foundation for projects such as:

- 2D game assets — Characters, items, icons, and simple sprite animations.
- Procedural art — Generate repeatable artwork from code and parameters.
- AI-assisted asset creation — Let coding agents produce structured DSL scripts that the engine can render.
- Creative tooling — Build workflows around palettes, frames, layers, and reusable sprite definitions.
- Learning projects — Explore raster graphics, coordinate systems, animation, and file serialization with Python.

🤖 AI Agent Skill

PixelMirai includes a "SKILL.md" entry point that describes how an AI coding agent can interact with the project.

The skill can help compatible agents:

1. Understand the PixelMirai DSL and project conventions.
2. Create or modify sprite scripts.
3. Use the available compiler commands.
4. Follow the project's palette and pixel-grid rules.
5. Produce assets through a reproducible rendering workflow.

Agent compatibility depends on the instructions and skill-loading mechanisms supported by each tool.

📁 Project Structure

PixelMirai-Agent/
├── .agents/
│   └── skills/
│       └── pixelmirai/       # Agent skill and supporting references
├── assets/                   # Gallery images and rendered sprites
├── docs/                     # DSL, palette, and format documentation
├── examples/                  # Example PixelMirai DSL scripts
├── scripts/
│   ├── pixelmirai_compiler.py # Core engine and CLI compiler
│   ├── generate_cat_art.py    # Procedural sprite generator
│   └── generate_cat_64.py     # 64×64 sprite generator
├── SKILL.md                   # Root agent skill entry point
├── requirements.txt           # Runtime dependencies
├── LICENSE                    # MIT License
└── README.md                  # Project overview

Some files and optional development tools may vary between versions.

📚 Documentation

Start with these resources:

- "DSL Specification" (docs/dsl-specification.md) — Language syntax and drawing commands.
- "PXM Format Specification" (docs/pxm-format-spec.md) — Custom project format documentation.
- "Endesga32 Palette Reference" (docs/palette-endesga32.md) — Palette reference.
- "Example Scripts" (examples/) — Ready-to-explore sprite definitions.
- "Agent Skill Instructions" (SKILL.md) — Instructions for compatible AI coding agents.

🧪 Testing

If the repository includes a configured test suite and development dependencies, install them and run:

python -m pip install -r requirements-dev.txt
pytest tests/ -v

If either the development requirements file or test directory is not present in your checkout, follow the repository's current testing instructions instead.

🗺️ Roadmap

Potential areas for continued development include:

- More drawing primitives and palette support.
- Improved parser diagnostics and validation.
- Reliable transparency and animation exports.
- Better ".pxm" project interoperability.
- Expanded automated tests and continuous integration.
- Easier integration with AI coding tools and creative workflows.

See the "open issues" (https://github.com/riantosee/PixelMirai-Agent/issues) for current work and opportunities to contribute.

🤝 Contributing

Contributions, bug reports, feature requests, and constructive feedback are welcome.

1. Check existing issues before starting substantial work.
2. Create a focused branch for your changes.
3. Include tests or reproducible examples when fixing bugs.
4. Update the relevant documentation when behavior changes.
5. Open a pull request describing the change and its verification.

For bugs, include your Python version, operating system, command used, and a minimal example that reproduces the issue.

👨‍💻 Creator

Created by Rian — "@riantosee on GitHub" (https://github.com/riantosee).

PixelMirai is an ongoing open-source project built around a love for pixel art, programming, and creative tooling.

📄 License

PixelMirai Agent is released under the "MIT License" (LICENSE).

---

<div align="center">Pixel art never fades. Every pixel has a purpose.

<sub>Built with Python, precision, and a love for classic game aesthetics.</sub>

</div>