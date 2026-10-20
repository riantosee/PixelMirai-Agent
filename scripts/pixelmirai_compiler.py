#!/usr/bin/env python3
"""
PixelMirai Compiler — Unified CLI & Python API
================================================
Converts .pxm.dsl scripts → PNG + GIF + CRT + .pxm

Usage:
  python pixelmirai_compiler.py <script.pxm.dsl> [options]

Options:
  --out <dir>      Output directory (default: ../public/exports/)
  --only <fmt>     Only export specific format: png|gif|crt|pxm
  --verbose        Debug output (print each pixel placed)
  --name <name>    Override output filename (without extension)
  --scale <n>      Override scale factor (1-16)
  --crt            Force CRT filter on
  --no-crt         Force CRT filter off
  --fps <n>        Override frame rate for GIF

Author: RianFix / PixelMirai Engine
Version: 1.0.0
"""

import sys
import os
import json
import re
import struct
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    print("❌ Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# PALETTE PRESETS
# ═══════════════════════════════════════════════════════════════

PALETTES = {
    'pico8': [
        '#000000', '#1d2b53', '#7e2553', '#008751',
        '#ab5236', '#5f574f', '#c2c3c7', '#fff1e8',
        '#ff004d', '#ffa300', '#ffec27', '#00e436',
        '#29adff', '#83769c', '#ff77a8', '#ffccaa',
    ],
    'endesga32': [
        '#be4a2f', '#d77643', '#ead4aa', '#e4a672',
        '#b86f50', '#733e39', '#3e2731', '#a22633',
        '#e43b44', '#f77622', '#feae34', '#fee761',
        '#63c74d', '#3e8948', '#265c42', '#193c3e',
        '#124e89', '#0099db', '#2ce8f5', '#ffffff',
        '#c0cbdc', '#8b9bb4', '#5a6988', '#3a4466',
        '#262b44', '#181425', '#ff0044', '#68386c',
        '#b55088', '#f6757a', '#e8b796', '#c28569',
    ],
    'gameboy': ['#0f380f', '#306230', '#8bac0f', '#9bbc0f'],
    'cga': [
        '#000000', '#0000aa', '#00aa00', '#00aaaa',
        '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa',
        '#555555', '#5555ff', '#55ff55', '#55ffff',
        '#ff5555', '#ff55ff', '#ffff55', '#ffffff',
    ],
}


# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert #rrggbb to (r, g, b)."""
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def fnv1a_32(data: bytes) -> str:
    """FNV-1a 32-bit hash (matches lib/project-file.js)."""
    h = 2166136261
    for b in data:
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF
    return format(h, '08x')


def safe_print(msg: str):
    """Print that handles Windows CP1252 by replacing unknown chars."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', errors='replace').decode('ascii'))


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# PIXEL LAYER
# ═══════════════════════════════════════════════════════════════

class PixelLayer:
    def __init__(self, name: str, width: int, height: int, verbose=False):
        self.name = name
        self.width = width
        self.height = height
        self.verbose = verbose
        # pixels stored as dict {(x,y): '#rrggbb'}
        self.pixels: dict = {}

    def _clamp(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def pixel(self, x: int, y: int, color: str):
        x, y = int(x), int(y)
        if self._clamp(x, y):
            self.pixels[(x, y)] = color
            if self.verbose:
                print(f"  px ({x},{y}) = {color}")

    def rect(self, x: int, y: int, w: int, h: int, color: str):
        for dy in range(int(h)):
            for dx in range(int(w)):
                self.pixel(int(x) + dx, int(y) + dy, color)

    def hline(self, y: int, x1: int, x2: int, color: str):
        for x in range(int(x1), int(x2) + 1):
            self.pixel(x, int(y), color)

    def vline(self, x: int, y1: int, y2: int, color: str):
        for y in range(int(y1), int(y2) + 1):
            self.pixel(int(x), y, color)

    def circle(self, cx: int, cy: int, radius: int, color: str):
        """Bresenham circle (outline only)."""
        cx, cy, r = int(cx), int(cy), int(radius)
        x, y = r, 0
        err = 0
        while x >= y:
            for px, py in [
                (cx+x, cy+y), (cx+y, cy+x),
                (cx-y, cy+x), (cx-x, cy+y),
                (cx-x, cy-y), (cx-y, cy-x),
                (cx+y, cy-x), (cx+x, cy-y),
            ]:
                self.pixel(px, py, color)
            y += 1
            err += 1 + 2*y
            if 2*(err-x) + 1 > 0:
                x -= 1
                err += 1 - 2*x

    def fillcircle(self, cx: int, cy: int, radius: int, color: str):
        cx, cy, r = int(cx), int(cy), int(radius)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx)**2 + (y - cy)**2 <= r*r:
                    self.pixel(x, y, color)

    def render_to_image(self, base_image: Image.Image) -> Image.Image:
        """Composite this layer onto base_image (returns new image)."""
        img = base_image.copy()
        draw = ImageDraw.Draw(img)
        for (x, y), color in self.pixels.items():
            rgb = hex_to_rgb(color)
            draw.point((x, y), fill=rgb)
        return img

    def to_palette_pixels(self, palette: list) -> list:
        """Convert pixel dict to [[x, y, paletteIdx], ...]."""
        result = []
        pal_lower = [c.lower() for c in palette]
        for (x, y), color in self.pixels.items():
            c = color.lower()
            if c in pal_lower:
                idx = pal_lower.index(c)
            else:
                # Find closest color
                r1, g1, b1 = hex_to_rgb(color)
                best_idx = 0
                best_dist = float('inf')
                for i, pc in enumerate(pal_lower):
                    r2, g2, b2 = hex_to_rgb(pc)
                    d = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2
                    if d < best_dist:
                        best_dist = d
                        best_idx = i
                idx = best_idx
            result.append([x, y, idx])
        return result


# ═══════════════════════════════════════════════════════════════
# FRAME
# ═══════════════════════════════════════════════════════════════

class PixelFrame:
    def __init__(self, index: int, width: int, height: int, verbose=False):
        self.index = index
        self.width = width
        self.height = height
        self.verbose = verbose
        self.layers: list[PixelLayer] = []
        self._current_layer: PixelLayer | None = None

    def new_layer(self, name: str) -> PixelLayer:
        layer = PixelLayer(name, self.width, self.height, self.verbose)
        self.layers.append(layer)
        self._current_layer = layer
        return layer

    def get_or_create_layer(self, name: str) -> PixelLayer:
        for l in self.layers:
            if l.name == name:
                self._current_layer = l
                return l
        return self.new_layer(name)

    @property
    def current_layer(self) -> PixelLayer:
        if self._current_layer is None:
            return self.new_layer('default')
        return self._current_layer

    def render(self, background_color: tuple) -> Image.Image:
        img = Image.new('RGB', (self.width, self.height), background_color)
        for layer in self.layers:
            img = layer.render_to_image(img)
        return img


# ═══════════════════════════════════════════════════════════════
# ENGINE
# ═══════════════════════════════════════════════════════════════

class PixelMiraiEngine:
    """Core rendering engine."""

    def __init__(self, width=32, height=32, verbose=False):
        self.width = width
        self.height = height
        self.verbose = verbose
        self.palette: list = list(PALETTES['pico8'])
        self.background: tuple = (29, 43, 83)   # dark-blue
        self.scale: int = 8
        self.crt: bool = False
        self.fps: int = 6
        self.name: str = 'untitled'
        self.frames: list[PixelFrame] = []
        self._current_frame: PixelFrame | None = None

    def set_palette(self, name_or_list):
        if isinstance(name_or_list, list):
            self.palette = name_or_list
        elif name_or_list in PALETTES:
            self.palette = list(PALETTES[name_or_list])
        else:
            raise ValueError(f"Unknown palette preset: {name_or_list}")

    def set_background(self, hex_color: str):
        self.background = hex_to_rgb(hex_color)

    def new_frame(self, index: int | None = None) -> PixelFrame:
        if index is None:
            index = len(self.frames)
        frame = PixelFrame(index, self.width, self.height, self.verbose)
        self.frames.append(frame)
        self._current_frame = frame
        return frame

    def get_or_create_frame(self, index: int) -> PixelFrame:
        for f in self.frames:
            if f.index == index:
                self._current_frame = f
                return f
        return self.new_frame(index)

    @property
    def current_frame(self) -> PixelFrame:
        if self._current_frame is None:
            return self.new_frame(0)
        return self._current_frame

    def _render_frame(self, frame: PixelFrame) -> Image.Image:
        return frame.render(self.background)

    def _scale_image(self, img: Image.Image, scale: int) -> Image.Image:
        return img.resize(
            (img.width * scale, img.height * scale),
            Image.NEAREST
        )

    def _apply_crt(self, img: Image.Image) -> Image.Image:
        """Apply CRT scanline + vignette effect."""
        w, h = img.size
        result = Image.new('RGB', (w, h), (0, 0, 0))
        pixels_src = img.load()
        pixels_dst = result.load()

        # Copy with scanline darkening
        for y in range(h):
            scanline = (y % 2 == 1)
            for x in range(w):
                r, g, b = pixels_src[x, y]
                if scanline:
                    # Darken every other row (CRT scanline)
                    r = int(r * 0.55)
                    g = int(g * 0.55)
                    b = int(b * 0.55)
                pixels_dst[x, y] = (r, g, b)

        # Vignette overlay
        cx, cy = w // 2, h // 2
        max_dist = ((cx**2) + (cy**2)) ** 0.5
        pixels_out = result.load()
        for y in range(h):
            for x in range(w):
                dist = ((x - cx)**2 + (y - cy)**2) ** 0.5
                factor = 1.0 - 0.45 * (dist / max_dist) ** 2
                r, g, b = pixels_out[x, y]
                pixels_out[x, y] = (
                    int(r * factor),
                    int(g * factor),
                    int(b * factor),
                )

        return result

    # ── Exports ──────────────────────────────────────────────

    def _log(self, msg: str):
        """Safe print that strips non-ASCII emoji for Windows CP1252 terminals."""
        safe_print(msg)

    def export_png(self, path: str, scale: int | None = None):
        ensure_dir(str(Path(path).parent))
        sc = scale or self.scale
        img = self._render_frame(self.frames[0] if self.frames else self.new_frame())
        img = self._scale_image(img, sc)
        img.save(path)
        self._log(f"[OK] PNG  -> {path}  ({img.width}x{img.height})")

    def export_crt(self, path: str, scale: int | None = None):
        ensure_dir(str(Path(path).parent))
        sc = scale or self.scale
        img = self._render_frame(self.frames[0] if self.frames else self.new_frame())
        img = self._scale_image(img, sc)
        img = self._apply_crt(img)
        img.save(path)
        self._log(f"[OK] CRT  -> {path}  ({img.width}x{img.height})")

    def export_gif(self, path: str, fps: int | None = None, scale: int | None = None):
        ensure_dir(str(Path(path).parent))
        sc = scale or self.scale
        _fps = fps or self.fps
        duration = int(1000 / _fps)

        if not self.frames:
            self.new_frame()

        frames_rendered = []
        for frame in sorted(self.frames, key=lambda f: f.index):
            img = self._render_frame(frame)
            img = self._scale_image(img, sc)
            frames_rendered.append(img.convert('P', palette=Image.ADAPTIVE))

        frames_rendered[0].save(
            path,
            save_all=True,
            append_images=frames_rendered[1:],
            loop=0,
            duration=duration,
            optimize=False,
        )
        self._log(f"[OK] GIF  -> {path}  ({len(frames_rendered)} frames @ {_fps}fps)")

    def export_pxm(self, path: str):
        ensure_dir(str(Path(path).parent))
        frames_data = []
        for frame in sorted(self.frames, key=lambda f: f.index):
            layers_data = []
            for layer in frame.layers:
                pixels = layer.to_palette_pixels(self.palette)
                layers_data.append({
                    'name': layer.name,
                    'pixels': pixels,
                })
            frames_data.append({
                'index': frame.index,
                'layers': layers_data,
            })

        project = {
            'version': '1.0',
            'format': 'PixelMirai',
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'palette': self.palette,
            'frames': frames_data,
            'fps': self.fps,
        }

        # Compute checksum BEFORE adding it
        content_bytes = json.dumps(
            {k: v for k, v in project.items()},
            separators=(',', ':'), sort_keys=True
        ).encode('utf-8')
        project['checksum'] = fnv1a_32(content_bytes)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(project, f, separators=(',', ':'))

        self._log(f"[OK] PXM  -> {path}  (checksum: {project['checksum']})")


# ═══════════════════════════════════════════════════════════════
# DSL PARSER
# ═══════════════════════════════════════════════════════════════

class DSLParser:
    """Parse .pxm.dsl scripts into PixelMiraiEngine calls."""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def parse_file(self, dsl_path: str) -> PixelMiraiEngine:
        with open(dsl_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return self.parse(text, name=Path(dsl_path).stem.replace('.pxm', ''))

    def parse(self, dsl_text: str, name: str = 'untitled') -> PixelMiraiEngine:
        engine = None
        current_frame: PixelFrame | None = None
        current_layer: PixelLayer | None = None
        exports: list = []

        lines = dsl_text.splitlines()
        for lineno, raw_line in enumerate(lines, 1):
            line = raw_line.strip()
            # Handle // comments
            if '//' in line:
                line = line[:line.index('//')].strip()
            # Strip inline comments: only strip '#' that is NOT a hex color
            if ' #' in line:
                parts_check = line.split(' #')
                rebuilt = parts_check[0]
                for seg in parts_check[1:]:
                    hex_match = re.match(r'^[0-9a-fA-F]{3}([0-9a-fA-F]{3})?\b', seg)
                    if hex_match:
                        rebuilt += ' #' + seg
                    else:
                        break
                line = rebuilt.strip()
            elif line.startswith('#'):
                continue
            if not line:
                continue

            parts = line.split()
            cmd = parts[0].lower()

            try:
                # ── Header commands (before frame blocks) ──
                if cmd in ('canvas', 'size'):
                    w = int(parts[1])
                    h = int(parts[2]) if len(parts) > 2 else w
                    engine = PixelMiraiEngine(w, h, self.verbose)
                    engine.name = name
                    if self.verbose:
                        print(f"Canvas: {w}x{h}")

                elif cmd == 'palette':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'palette'")
                    pal_name = parts[1].lower().replace('-', '')
                    engine.set_palette(pal_name)

                elif cmd == 'background':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'background'")
                    val = parts[1].lower()
                    if val == 'transparent':
                        engine.set_background('#000000')
                        engine._bg_transparent = True
                    else:
                        engine.set_background(parts[1])

                elif cmd == 'scale':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'scale'")
                    engine.scale = int(parts[1])

                elif cmd == 'crt':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'crt'")
                    engine.crt = (parts[1].lower() == 'on')

                elif cmd == 'fps':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'fps'")
                    engine.fps = int(parts[1])

                # ── Frame block ──
                elif cmd == 'frame':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'frame'")
                    idx = int(parts[1])
                    current_frame = engine.get_or_create_frame(idx)
                    current_layer = None

                # ── Layer block ──
                elif cmd == 'layer':
                    if engine is None:
                        raise ValueError("'canvas' must come before 'layer'")
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    # Layer name may be quoted
                    layer_name = parts[1].strip('"\'')
                    current_layer = current_frame.get_or_create_layer(layer_name)

                # ── Draw commands ──
                elif cmd == 'pixel':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    current_layer.pixel(int(parts[1]), int(parts[2]), parts[3])

                elif cmd == 'pixels':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    color = parts[1]
                    for coord in parts[2:]:
                        if ',' in coord:
                            px_str, py_str = coord.split(',')
                            current_layer.pixel(int(px_str), int(py_str), color)

                elif cmd == 'rect':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    current_layer.rect(
                        int(parts[1]), int(parts[2]),
                        int(parts[3]), int(parts[4]),
                        parts[5]
                    )

                elif cmd == 'hline':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    current_layer.hline(
                        int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
                    )

                elif cmd == 'vline':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    current_layer.vline(
                        int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
                    )

                elif cmd == 'circle':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    current_layer.circle(
                        int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
                    )

                elif cmd == 'fillcircle':
                    if current_layer is None:
                        if current_frame is None:
                            current_frame = engine.get_or_create_frame(0)
                        current_layer = current_frame.get_or_create_layer('default')
                    current_layer.fillcircle(
                        int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
                    )

                # ── Export commands ──
                elif cmd == 'export':
                    fmt = parts[1].lower()
                    fname = parts[2].strip('"\'') if len(parts) > 2 else None
                    exports.append((fmt, fname))

                else:
                    if self.verbose:
                        print(f"  [line {lineno}] Unknown command: {cmd!r} (skipped)")

            except (IndexError, ValueError) as e:
                safe_print(f"  [WARN] DSL parse error at line {lineno}: {raw_line!r}")
                safe_print(f"   -> {e}")
                continue

        if engine is None:
            raise ValueError("DSL must start with a 'canvas W H' command")

        return engine, exports


# ═══════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='PixelMirai Compiler — DSL → PNG + GIF + CRT + .pxm',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('script', help='Path to .pxm.dsl script file')
    parser.add_argument('--out', default=None, help='Output directory')
    parser.add_argument('--only', default=None, choices=['png', 'gif', 'crt', 'pxm'],
                        help='Only export this format')
    parser.add_argument('--verbose', action='store_true', help='Debug pixel output')
    parser.add_argument('--name', default=None, help='Override output filename')
    parser.add_argument('--scale', type=int, default=None, help='Scale factor (1-16)')
    parser.add_argument('--crt', action='store_true', help='Force CRT on')
    parser.add_argument('--no-crt', action='store_true', dest='no_crt', help='Force CRT off')
    parser.add_argument('--fps', type=int, default=None, help='GIF frame rate')

    args = parser.parse_args()

    # Parse DSL
    dsl_parser = DSLParser(verbose=args.verbose)
    try:
        engine, exports = dsl_parser.parse_file(args.script)
    except FileNotFoundError:
        safe_print(f"[ERR] Script not found: {args.script}")
        sys.exit(1)
    except ValueError as e:
        safe_print(f"[ERR] DSL Error: {e}")
        sys.exit(1)

    # Apply CLI overrides
    if args.scale:
        engine.scale = args.scale
    if args.fps:
        engine.fps = args.fps
    if args.crt:
        engine.crt = True
    if args.no_crt:
        engine.crt = False

    # Determine output directory
    script_path = Path(args.script).resolve()
    if args.out:
        out_dir = Path(args.out)
    else:
        # Walk up from script to find package.json / next.config.mjs (project root)
        # then use public/exports inside it
        search = script_path.parent
        project_root = None
        for _ in range(6):
            if (search / 'package.json').exists() or (search / 'next.config.mjs').exists():
                project_root = search
                break
            search = search.parent
        if project_root:
            out_dir = project_root / 'public' / 'exports'
        else:
            # Fallback: same dir as script
            out_dir = script_path.parent / 'exports'
    ensure_dir(str(out_dir))

    # Determine base name
    base_name = args.name or engine.name

    print(f"\n[PixelMirai Compiler]")
    print(f"   Script  : {args.script}")
    print(f"   Canvas  : {engine.width}x{engine.height}")
    print(f"   Frames  : {len(engine.frames)}")
    print(f"   Scale   : {engine.scale}x  ->  {engine.width*engine.scale}x{engine.height*engine.scale}px")
    print(f"   CRT     : {'on' if engine.crt else 'off'}")
    print(f"   FPS     : {engine.fps}")
    print(f"   Out dir : {out_dir}")
    print()

    # Determine which formats to export
    if args.only:
        formats = [args.only]
    elif exports:
        formats = [fmt for fmt, _ in exports]
    else:
        formats = ['png', 'gif', 'crt', 'pxm']

    if engine.crt and 'crt' not in formats:
        formats.append('crt')

    # Do exports
    for fmt in formats:
        if fmt == 'png':
            engine.export_png(str(out_dir / f'{base_name}.png'))
        elif fmt == 'gif':
            engine.export_gif(str(out_dir / f'{base_name}.gif'))
        elif fmt == 'crt':
            engine.export_crt(str(out_dir / f'{base_name}-crt.png'))
        elif fmt == 'pxm':
            engine.export_pxm(str(out_dir / f'{base_name}.pxm'))

    print(f"\n[Done] Files saved to: {out_dir}")


if __name__ == '__main__':
    main()
