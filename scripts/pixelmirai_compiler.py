#!/usr/bin/env python3
"""
PixelMirai Compiler — Unified CLI & Python API
================================================
Deterministic pixel art compiler for PixelMirai DSL (.pxm.dsl)
Compiles DSL scripts to PNG (with alpha transparency), GIF, CRT, and .pxm.

Author: RianFix / PixelMirai Engine
Version: 1.1.0
License: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: Pillow is required. Install it using: pip install Pillow")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# CONSTANTS & RESOURCE LIMITS
# ═══════════════════════════════════════════════════════════════

VERSION = "1.1.0"

MIN_CANVAS_DIM = 1
MAX_CANVAS_DIM = 2048

MIN_SCALE = 1
MAX_SCALE = 64

MIN_FPS = 1
MAX_FPS = 120

MAX_FRAMES = 1000

PALETTES: Dict[str, List[str]] = {
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
# EXCEPTIONS
# ═══════════════════════════════════════════════════════════════

class PixelMiraiError(Exception):
    """Base exception for PixelMirai engine."""
    pass


class DSLSyntaxError(PixelMiraiError):
    """Raised when DSL parsing encounters syntax or argument errors."""
    def __init__(self, message: str, line_num: int, line_text: str = ""):
        self.message = message
        self.line_num = line_num
        self.line_text = line_text
        context = f" on line {line_num}: '{line_text}'" if line_text else f" on line {line_num}"
        super().__init__(f"{message}{context}")


class ValidationError(PixelMiraiError):
    """Raised when parameters or constraints fail validation."""
    pass


class PXMChecksumError(PixelMiraiError):
    """Raised when a PXM file fails checksum verification."""
    pass


# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

HEX_REGEX = re.compile(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$')


def normalize_hex(hex_str: str) -> str:
    """Validate and normalize hex color to lowercase #rrggbb or #rrggbbaa."""
    s = hex_str.strip()
    if not HEX_REGEX.match(s):
        raise ValidationError(f"Invalid hexadecimal color: '{hex_str}'")
    s = s.lower()
    h = s.lstrip('#')
    if len(h) == 3:
        return '#' + ''.join(c * 2 for c in h)
    elif len(h) == 4:
        return '#' + ''.join(c * 2 for c in h)
    return '#' + h


def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    """Convert hex string (#rgb, #rgba, #rrggbb, #rrggbbaa) to (r, g, b, a)."""
    norm = normalize_hex(hex_color)
    h = norm.lstrip('#')
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    a = int(h[6:8], 16) if len(h) == 8 else 255
    return (r, g, b, a)


def fnv1a_32(data: bytes) -> str:
    """Compute FNV-1a 32-bit checksum."""
    h = 2166136261
    for b in data:
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF
    return format(h, '08x')


def safe_print(msg: str):
    """Safe console print handling Windows CP1252 character encoding."""
    try:
        print(msg)
    except UnicodeEncodeError:
        safe_msg = msg.encode('ascii', errors='replace').decode('ascii')
        print(safe_msg)


def ensure_dir(path: Union[str, Path]):
    Path(path).mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# PIXEL LAYER
# ═══════════════════════════════════════════════════════════════

class PixelLayer:
    """A 2D layer holding discrete pixel coordinates and their hex colors."""

    def __init__(self, name: str, width: int, height: int, verbose: bool = False):
        if not name:
            raise ValidationError("Layer name cannot be empty")
        self.name: str = name
        self.width: int = width
        self.height: int = height
        self.verbose: bool = verbose
        # Pixels stored as {(x, y): normalized_hex}
        self.pixels: Dict[Tuple[int, int], str] = {}

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def pixel(self, x: int, y: int, color: str):
        norm_color = normalize_hex(color)
        if self.is_in_bounds(x, y):
            self.pixels[(x, y)] = norm_color
            if self.verbose:
                safe_print(f"  layer '{self.name}' px ({x}, {y}) = {norm_color}")

    def rect(self, x: int, y: int, w: int, h: int, color: str):
        if w <= 0 or h <= 0:
            raise ValidationError(f"Rectangle width and height must be > 0 (got w={w}, h={h})")
        for dy in range(h):
            for dx in range(w):
                self.pixel(x + dx, y + dy, color)

    def hline(self, y: int, x1: int, x2: int, color: str):
        start = min(x1, x2)
        end = max(x1, x2)
        for x in range(start, end + 1):
            self.pixel(x, y, color)

    def vline(self, x: int, y1: int, y2: int, color: str):
        start = min(y1, y2)
        end = max(y1, y2)
        for y in range(start, end + 1):
            self.pixel(x, y, color)

    def circle(self, cx: int, cy: int, radius: int, color: str):
        """Bresenham circle outline."""
        if radius < 0:
            raise ValidationError(f"Circle radius must be >= 0 (got {radius})")
        if radius == 0:
            self.pixel(cx, cy, color)
            return

        x = radius
        y = 0
        err = 0
        while x >= y:
            for px, py in (
                (cx + x, cy + y), (cx + y, cy + x),
                (cx - y, cy + x), (cx - x, cy + y),
                (cx - x, cy - y), (cx - y, cy - x),
                (cx + y, cy - x), (cx + x, cy - y),
            ):
                self.pixel(px, py, color)
            y += 1
            err += 1 + 2 * y
            if 2 * (err - x) + 1 > 0:
                x -= 1
                err += 1 - 2 * x

    def fillcircle(self, cx: int, cy: int, radius: int, color: str):
        """Solid rasterized circle."""
        if radius < 0:
            raise ValidationError(f"Circle radius must be >= 0 (got {radius})")
        r2 = radius * radius
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                    self.pixel(x, y, color)

    def render_to_image(self, base_image: Image.Image) -> Image.Image:
        """Composite this layer onto base_image."""
        draw = ImageDraw.Draw(base_image)
        for (x, y), color in self.pixels.items():
            rgba = hex_to_rgba(color)
            draw.point((x, y), fill=rgba)
        return base_image

    def to_palette_pixels(self, palette: List[str]) -> List[List[int]]:
        """Convert pixels to [[x, y, palette_index], ...]."""
        result = []
        pal_lower = [c.lower() for c in palette]
        for (x, y), color in self.pixels.items():
            c = color.lower()
            if c in pal_lower:
                idx = pal_lower.index(c)
            else:
                # Nearest color fallback in RGB Euclidean space
                r1, g1, b1, _ = hex_to_rgba(color)
                best_idx = 0
                best_dist = float('inf')
                for i, pc in enumerate(pal_lower):
                    r2, g2, b2, _ = hex_to_rgba(pc)
                    d = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
                    if d < best_dist:
                        best_dist = d
                        best_idx = i
                idx = best_idx
            result.append([x, y, idx])
        return result


# ═══════════════════════════════════════════════════════════════
# PIXEL FRAME
# ═══════════════════════════════════════════════════════════════

class PixelFrame:
    """A container for ordered layers at a specific timeline frame index."""

    def __init__(self, index: int, width: int, height: int, verbose: bool = False):
        if index < 0:
            raise ValidationError(f"Frame index must be >= 0 (got {index})")
        self.index: int = index
        self.width: int = width
        self.height: int = height
        self.verbose: bool = verbose
        self.layers: List[PixelLayer] = []
        self._current_layer: Optional[PixelLayer] = None

    def new_layer(self, name: str) -> PixelLayer:
        layer = PixelLayer(name, self.width, self.height, self.verbose)
        self.layers.append(layer)
        self._current_layer = layer
        return layer

    def get_or_create_layer(self, name: str) -> PixelLayer:
        for layer in self.layers:
            if layer.name == name:
                self._current_layer = layer
                return layer
        return self.new_layer(name)

    @property
    def current_layer(self) -> PixelLayer:
        if self._current_layer is None:
            return self.new_layer('default')
        return self._current_layer

    def render(self, bg_rgba: Tuple[int, int, int, int]) -> Image.Image:
        """Render all layers composited over the background."""
        img = Image.new('RGBA', (self.width, self.height), bg_rgba)
        for layer in self.layers:
            img = layer.render_to_image(img)
        return img


# ═══════════════════════════════════════════════════════════════
# PIXELMIRAI ENGINE
# ═══════════════════════════════════════════════════════════════

class PixelMiraiEngine:
    """Core pixel art compilation and export engine."""

    def __init__(self, width: int = 32, height: int = 32, verbose: bool = False):
        self.validate_dimensions(width, height)
        self.width: int = width
        self.height: int = height
        self.verbose: bool = verbose
        self.palette: List[str] = list(PALETTES['pico8'])
        self.is_transparent: bool = False
        self.background_color: Tuple[int, int, int, int] = (29, 43, 83, 255)  # default dark-blue
        self.scale: int = 8
        self.crt: bool = False
        self.fps: int = 6
        self.name: str = 'untitled'
        self.frames: List[PixelFrame] = []
        self._current_frame: Optional[PixelFrame] = None

    @staticmethod
    def validate_dimensions(width: int, height: int):
        if not (MIN_CANVAS_DIM <= width <= MAX_CANVAS_DIM):
            raise ValidationError(
                f"Canvas width must be between {MIN_CANVAS_DIM} and {MAX_CANVAS_DIM} (got {width})"
            )
        if not (MIN_CANVAS_DIM <= height <= MAX_CANVAS_DIM):
            raise ValidationError(
                f"Canvas height must be between {MIN_CANVAS_DIM} and {MAX_CANVAS_DIM} (got {height})"
            )

    def set_palette(self, name_or_list: Union[str, List[str]]):
        if isinstance(name_or_list, list):
            validated = [normalize_hex(c) for c in name_or_list]
            if not validated:
                raise ValidationError("Palette cannot be empty")
            self.palette = validated
        else:
            key = name_or_list.lower().replace('-', '').replace('_', '')
            if key not in PALETTES:
                raise ValidationError(
                    f"Unknown palette preset '{name_or_list}'. Available: {list(PALETTES.keys())}"
                )
            self.palette = list(PALETTES[key])

    def set_background(self, value: str):
        v = value.strip().lower()
        if v == 'transparent':
            self.is_transparent = True
            self.background_color = (0, 0, 0, 0)
        else:
            self.is_transparent = False
            self.background_color = hex_to_rgba(value)

    def set_scale(self, scale: int):
        if not (MIN_SCALE <= scale <= MAX_SCALE):
            raise ValidationError(f"Scale factor must be between {MIN_SCALE} and {MAX_SCALE} (got {scale})")
        self.scale = scale

    def set_fps(self, fps: int):
        if not (MIN_FPS <= fps <= MAX_FPS):
            raise ValidationError(f"FPS must be between {MIN_FPS} and {MAX_FPS} (got {fps})")
        self.fps = fps

    def new_frame(self, index: Optional[int] = None) -> PixelFrame:
        if index is None:
            index = len(self.frames)
        if len(self.frames) >= MAX_FRAMES:
            raise ValidationError(f"Maximum frame limit reached ({MAX_FRAMES})")
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
        return frame.render(self.background_color)

    def _scale_image(self, img: Image.Image, scale: int) -> Image.Image:
        return img.resize((img.width * scale, img.height * scale), Image.NEAREST)

    def _apply_crt(self, img: Image.Image) -> Image.Image:
        """Apply CRT scanlines and radial vignette simulation."""
        w, h = img.size
        # CRT monitors operate in dark room environments; composite transparency over dark background
        comp = Image.new('RGB', (w, h), (13, 17, 23))
        if img.mode == 'RGBA':
            comp.paste(img, (0, 0), img)
        else:
            comp.paste(img, (0, 0))

        src_pix = comp.load()
        out_img = Image.new('RGB', (w, h), (0, 0, 0))
        dst_pix = out_img.load()

        # Step 1: Scanline darkening
        for y in range(h):
            is_scanline = (y % 2 == 1)
            for x in range(w):
                r, g, b = src_pix[x, y]
                if is_scanline:
                    r = int(r * 0.55)
                    g = int(g * 0.55)
                    b = int(b * 0.55)
                dst_pix[x, y] = (r, g, b)

        # Step 2: Radial vignette
        cx, cy = w // 2, h // 2
        max_dist = ((cx ** 2) + (cy ** 2)) ** 0.5
        for y in range(h):
            for x in range(w):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                factor = max(0.0, 1.0 - 0.45 * (dist / max_dist) ** 2)
                r, g, b = dst_pix[x, y]
                dst_pix[x, y] = (int(r * factor), int(g * factor), int(b * factor))

        return out_img

    # ── Exports ──────────────────────────────────────────────

    def export_png(self, path: Union[str, Path], scale: Optional[int] = None):
        ensure_dir(Path(path).parent)
        sc = scale or self.scale
        frame = self.frames[0] if self.frames else self.new_frame()
        img = self._render_frame(frame)
        img = self._scale_image(img, sc)

        if not self.is_transparent:
            # Convert to RGB for clean opaque PNG output
            img = img.convert('RGB')

        img.save(str(path))
        safe_print(f"[OK] PNG  -> {path} ({img.width}x{img.height}, mode={img.mode})")

    def export_crt(self, path: Union[str, Path], scale: Optional[int] = None):
        ensure_dir(Path(path).parent)
        sc = scale or self.scale
        frame = self.frames[0] if self.frames else self.new_frame()
        img = self._render_frame(frame)
        img = self._scale_image(img, sc)
        crt_img = self._apply_crt(img)
        crt_img.save(str(path))
        safe_print(f"[OK] CRT  -> {path} ({crt_img.width}x{crt_img.height})")

    def export_gif(self, path: Union[str, Path], fps: Optional[int] = None, scale: Optional[int] = None):
        ensure_dir(Path(path).parent)
        sc = scale or self.scale
        fps_val = fps or self.fps
        duration = max(10, int(1000 / fps_val))

        if not self.frames:
            self.new_frame()

        frames_rendered: List[Image.Image] = []
        for frame in sorted(self.frames, key=lambda f: f.index):
            raw = self._render_frame(frame)
            scaled = self._scale_image(raw, sc)

            if self.is_transparent:
                # Convert RGBA to palette with transparent color at index 0
                alpha = scaled.split()[-1]
                p_img = scaled.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
                # Create mask for transparency
                mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                p_img.paste(255, mask)
                frames_rendered.append(p_img)
            else:
                frames_rendered.append(scaled.convert('RGB').convert('P', palette=Image.ADAPTIVE))

        save_kwargs: Dict[str, Any] = {
            'save_all': True,
            'append_images': frames_rendered[1:],
            'loop': 0,
            'duration': duration,
            'optimize': False,
        }
        if self.is_transparent:
            save_kwargs['transparency'] = 255
            save_kwargs['disposal'] = 2

        frames_rendered[0].save(str(path), **save_kwargs)
        safe_print(f"[OK] GIF  -> {path} ({len(frames_rendered)} frames @ {fps_val}fps)")

    def export_pxm(self, path: Union[str, Path]):
        ensure_dir(Path(path).parent)
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

        project: Dict[str, Any] = {
            'version': '1.0',
            'format': 'PixelMirai',
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'palette': self.palette,
            'frames': frames_data,
            'fps': self.fps,
        }

        # Canonical FNV-1a checksum calculation
        content_bytes = json.dumps(project, separators=(',', ':'), sort_keys=True).encode('utf-8')
        project['checksum'] = fnv1a_32(content_bytes)

        with open(str(path), 'w', encoding='utf-8') as f:
            json.dump(project, f, separators=(',', ':'))

        safe_print(f"[OK] PXM  -> {path} (checksum: {project['checksum']})")

    # ── PXM Loading & Round-Trip ─────────────────────────────

    @classmethod
    def load_pxm(cls, path: Union[str, Path], verify_checksum: bool = True) -> PixelMiraiEngine:
        """Load and validate a .pxm project file into a PixelMiraiEngine instance."""
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"PXM file not found: {path}")

        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValidationError("Invalid PXM file: root must be a JSON object")

        if data.get('format') != 'PixelMirai':
            raise ValidationError(f"Invalid format identifier: '{data.get('format')}' (expected 'PixelMirai')")

        if verify_checksum:
            stored_checksum = data.get('checksum')
            if not stored_checksum:
                raise PXMChecksumError("PXM file is missing required 'checksum' field")

            # Try canonical schema checksum
            project_copy = {k: v for k, v in data.items() if k != 'checksum'}
            canonical = json.dumps(project_copy, separators=(',', ':'), sort_keys=True).encode('utf-8')
            computed = fnv1a_32(canonical)

            if computed != stored_checksum:
                # Fallback to studio project schema checksum
                studio_canonical = {
                    'projectName': data.get('projectName'),
                    'size': data.get('size'),
                    'frames': data.get('frames'),
                    'palette': data.get('palette'),
                    'settings': data.get('settings'),
                }
                c_bytes = json.dumps(studio_canonical, separators=(',', ':')).encode('utf-8')
                studio_computed = fnv1a_32(c_bytes)
                if studio_computed != stored_checksum:
                    raise PXMChecksumError(f"Checksum mismatch: computed {computed} != stored {stored_checksum}")

        # Dimension extraction (supports both width/height and size)
        width = int(data.get('width', data.get('size', 32)))
        height = int(data.get('height', data.get('size', 32)))
        engine = cls(width=width, height=height)
        engine.name = str(data.get('name', data.get('projectName', p.stem)))
        engine.palette = [normalize_hex(c) for c in data.get('palette', PALETTES['pico8'])]
        engine.fps = int(data.get('fps', 6))

        for f_idx, f_data in enumerate(data.get('frames', [])):
            actual_idx = int(f_data.get('index', f_idx))
            frame = engine.get_or_create_frame(actual_idx)
            for l_data in f_data.get('layers', []):
                l_name = str(l_data.get('name', 'default'))
                layer = frame.get_or_create_layer(l_name)
                pixels_data = l_data.get('pixels', [])

                if not pixels_data:
                    continue

                first_elem = pixels_data[0]
                if isinstance(first_elem, list):
                    # Standard v1.0 sparse format: [[x, y, palette_index], ...]
                    for px in pixels_data:
                        x, y, pal_idx = int(px[0]), int(px[1]), int(px[2])
                        if 0 <= pal_idx < len(engine.palette):
                            color = engine.palette[pal_idx]
                            layer.pixel(x, y, color)
                elif isinstance(first_elem, (str, type(None))):
                    # Studio flat 1D grid format: ["#hex", None, ...]
                    for idx, col in enumerate(pixels_data):
                        if col and col != 'transparent':
                            x = idx % width
                            y = idx // width
                            layer.pixel(x, y, col)

        return engine


# ═══════════════════════════════════════════════════════════════
# DSL PARSER
# ═══════════════════════════════════════════════════════════════

class DSLParser:
    """Strict and reliable parser for PixelMirai DSL scripts."""

    def __init__(self, verbose: bool = False, strict: bool = True):
        self.verbose = verbose
        self.strict = strict

    @staticmethod
    def _strip_comments_and_tokenize(line: str) -> List[str]:
        """Strip comments (both // and #) while preserving quotes and hex colors."""
        # 1. Handle // comments
        if '//' in line:
            # Only strip if not inside quotes
            in_quote = False
            quote_char = ''
            cut_idx = -1
            for i, ch in enumerate(line):
                if ch in ('"', "'"):
                    if not in_quote:
                        in_quote = True
                        quote_char = ch
                    elif quote_char == ch:
                        in_quote = False
                elif ch == '/' and not in_quote and i + 1 < len(line) and line[i + 1] == '/':
                    cut_idx = i
                    break
            if cut_idx != -1:
                line = line[:cut_idx]

        line = line.strip()
        if not line:
            return []

        # 2. Tokenize using shlex to respect quotes
        try:
            tokens = shlex.split(line, posix=True)
        except ValueError as e:
            raise ValidationError(f"Unmatched quote in line: {e}")

        # 3. Filter trailing comment tokens (tokens starting with # that are not hex colors)
        filtered_tokens = []
        for tok in tokens:
            if tok.startswith('#') and not HEX_REGEX.match(tok):
                # This token is a comment marker, stop tokenizing this line
                break
            filtered_tokens.append(tok)

        return filtered_tokens

    def parse_file(self, dsl_path: Union[str, Path]) -> Tuple[PixelMiraiEngine, List[Tuple[str, Optional[str]]]]:
        path = Path(dsl_path)
        if not path.is_file():
            raise FileNotFoundError(f"DSL file not found: {dsl_path}")
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        name = path.stem.replace('.pxm', '').replace('.dsl', '')
        return self.parse(text, name=name)

    def parse(self, dsl_text: str, name: str = 'untitled') -> Tuple[PixelMiraiEngine, List[Tuple[str, Optional[str]]]]:
        engine: Optional[PixelMiraiEngine] = None
        current_frame: Optional[PixelFrame] = None
        current_layer: Optional[PixelLayer] = None
        exports: List[Tuple[str, Optional[str]]] = []

        lines = dsl_text.splitlines()
        for lineno, raw_line in enumerate(lines, 1):
            try:
                tokens = self._strip_comments_and_tokenize(raw_line)
            except ValidationError as e:
                raise DSLSyntaxError(str(e), lineno, raw_line)

            if not tokens:
                continue

            cmd = tokens[0].lower()

            try:
                # ── Canvas / Size ──
                if cmd in ('canvas', 'size'):
                    if len(tokens) < 2:
                        raise DSLSyntaxError(f"'{cmd}' expects 1 or 2 integer dimensions", lineno, raw_line)
                    try:
                        w = int(tokens[1])
                        h = int(tokens[2]) if len(tokens) > 2 else w
                    except ValueError:
                        raise DSLSyntaxError(f"'{cmd}' dimensions must be integers", lineno, raw_line)

                    engine = PixelMiraiEngine(w, h, verbose=self.verbose)
                    engine.name = name
                    current_frame = None
                    current_layer = None

                elif cmd == 'palette':
                    if engine is None:
                        raise DSLSyntaxError("'palette' declaration requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'palette' expects preset name or color list", lineno, raw_line)
                    engine.set_palette(tokens[1])

                elif cmd == 'background':
                    if engine is None:
                        raise DSLSyntaxError("'background' declaration requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'background' expects hex color or 'transparent'", lineno, raw_line)
                    engine.set_background(tokens[1])

                elif cmd == 'scale':
                    if engine is None:
                        raise DSLSyntaxError("'scale' declaration requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'scale' expects an integer value", lineno, raw_line)
                    engine.set_scale(int(tokens[1]))

                elif cmd == 'crt':
                    if engine is None:
                        raise DSLSyntaxError("'crt' declaration requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 2 or tokens[1].lower() not in ('on', 'off'):
                        raise DSLSyntaxError("'crt' expects 'on' or 'off'", lineno, raw_line)
                    engine.crt = (tokens[1].lower() == 'on')

                elif cmd == 'fps':
                    if engine is None:
                        raise DSLSyntaxError("'fps' declaration requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'fps' expects an integer value", lineno, raw_line)
                    engine.set_fps(int(tokens[1]))

                # ── Frame Block ──
                elif cmd == 'frame':
                    if engine is None:
                        raise DSLSyntaxError("'frame' declaration requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'frame' expects integer frame index", lineno, raw_line)
                    frame_idx = int(tokens[1])
                    current_frame = engine.get_or_create_frame(frame_idx)
                    current_layer = None

                # ── Layer Block ──
                elif cmd == 'layer':
                    if engine is None:
                        raise DSLSyntaxError("'layer' declaration requires 'canvas' first", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'layer' expects layer name", lineno, raw_line)
                    layer_name = tokens[1]
                    current_layer = current_frame.get_or_create_layer(layer_name)

                # ── Drawing Commands ──
                elif cmd == 'pixel':
                    if engine is None:
                        raise DSLSyntaxError("'pixel' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 4:
                        raise DSLSyntaxError("'pixel' expects x y color", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    x, y = int(tokens[1]), int(tokens[2])
                    current_layer.pixel(x, y, tokens[3])

                elif cmd == 'pixels':
                    if engine is None:
                        raise DSLSyntaxError("'pixels' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 3:
                        raise DSLSyntaxError("'pixels' expects color followed by coordinate pairs", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    color = tokens[1]
                    for coord_pair in tokens[2:]:
                        if ',' not in coord_pair:
                            raise DSLSyntaxError(f"Coordinate pair must be 'x,y' (got '{coord_pair}')", lineno, raw_line)
                        px_str, py_str = coord_pair.split(',', 1)
                        current_layer.pixel(int(px_str), int(py_str), color)

                elif cmd == 'rect':
                    if engine is None:
                        raise DSLSyntaxError("'rect' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 6:
                        raise DSLSyntaxError("'rect' expects x y width height color", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    x, y, w, h = int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4])
                    current_layer.rect(x, y, w, h, tokens[5])

                elif cmd == 'hline':
                    if engine is None:
                        raise DSLSyntaxError("'hline' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 5:
                        raise DSLSyntaxError("'hline' expects y x1 x2 color", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    y, x1, x2 = int(tokens[1]), int(tokens[2]), int(tokens[3])
                    current_layer.hline(y, x1, x2, tokens[4])

                elif cmd == 'vline':
                    if engine is None:
                        raise DSLSyntaxError("'vline' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 5:
                        raise DSLSyntaxError("'vline' expects x y1 y2 color", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    x, y1, y2 = int(tokens[1]), int(tokens[2]), int(tokens[3])
                    current_layer.vline(x, y1, y2, tokens[4])

                elif cmd == 'circle':
                    if engine is None:
                        raise DSLSyntaxError("'circle' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 5:
                        raise DSLSyntaxError("'circle' expects cx cy radius color", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    cx, cy, r = int(tokens[1]), int(tokens[2]), int(tokens[3])
                    current_layer.circle(cx, cy, r, tokens[4])

                elif cmd == 'fillcircle':
                    if engine is None:
                        raise DSLSyntaxError("'fillcircle' command requires 'canvas' first", lineno, raw_line)
                    if len(tokens) < 5:
                        raise DSLSyntaxError("'fillcircle' expects cx cy radius color", lineno, raw_line)
                    if current_frame is None:
                        current_frame = engine.get_or_create_frame(0)
                    if current_layer is None:
                        current_layer = current_frame.get_or_create_layer('default')
                    cx, cy, r = int(tokens[1]), int(tokens[2]), int(tokens[3])
                    current_layer.fillcircle(cx, cy, r, tokens[4])

                # ── Export Directives ──
                elif cmd == 'export':
                    if len(tokens) < 2:
                        raise DSLSyntaxError("'export' expects format (png, gif, crt, pxm)", lineno, raw_line)
                    fmt = tokens[1].lower()
                    if fmt not in ('png', 'gif', 'crt', 'pxm'):
                        raise DSLSyntaxError(f"Unsupported export format '{fmt}' (expected png, gif, crt, pxm)", lineno, raw_line)
                    custom_filename = tokens[2] if len(tokens) > 2 else None
                    exports.append((fmt, custom_filename))

                else:
                    msg = f"Unknown DSL command '{cmd}'"
                    if self.strict:
                        raise DSLSyntaxError(msg, lineno, raw_line)
                    else:
                        safe_print(f"  [WARN] Line {lineno}: {msg} (skipped)")

            except (IndexError, ValueError) as err:
                msg = f"Invalid argument: {err}"
                if self.strict:
                    raise DSLSyntaxError(msg, lineno, raw_line)
                else:
                    safe_print(f"  [WARN] Line {lineno}: {msg} -> '{raw_line}'")
            except ValidationError as err:
                if self.strict:
                    raise DSLSyntaxError(str(err), lineno, raw_line)
                else:
                    safe_print(f"  [WARN] Line {lineno}: {err}")

        if engine is None:
            raise DSLSyntaxError("Script must declare canvas dimensions (e.g. 'canvas 32 32')", 1)

        return engine, exports


# ═══════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def find_repo_root(start_path: Path) -> Path:
    """Find repository root by walking upwards looking for marker files."""
    current = start_path.resolve()
    for _ in range(8):
        if (current / '.git').exists() or (current / 'requirements.txt').exists() or (current / 'SKILL.md').exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    return start_path.parent


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog='pixelmirai_compiler',
        description='PixelMirai Compiler — Deterministic DSL to PNG/GIF/CRT/PXM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('script', help='Path to .pxm.dsl script file')
    parser.add_argument('--out', default=None, help='Output directory')
    parser.add_argument('--only', default=None, choices=['png', 'gif', 'crt', 'pxm'],
                        help='Only export specified format')
    parser.add_argument('--name', default=None, help='Override output base filename')
    parser.add_argument('--scale', type=int, default=None, help=f'Scale factor ({MIN_SCALE}-{MAX_SCALE})')
    parser.add_argument('--crt', action='store_true', help='Force CRT scanline filter on')
    parser.add_argument('--no-crt', action='store_true', dest='no_crt', help='Force CRT off')
    parser.add_argument('--fps', type=int, default=None, help=f'GIF frame rate ({MIN_FPS}-{MAX_FPS})')
    parser.add_argument('--lenient', action='store_true', help='Skip invalid lines instead of failing')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    args = parser.parse_args(argv)

    script_path = Path(args.script)
    if not script_path.is_file():
        safe_print(f"[ERR] File not found: {args.script}")
        return 1

    dsl_parser = DSLParser(verbose=args.verbose, strict=(not args.lenient))
    try:
        engine, exports = dsl_parser.parse_file(script_path)
    except PixelMiraiError as e:
        safe_print(f"[ERR] DSL Error: {e}")
        return 1
    except Exception as e:
        safe_print(f"[ERR] Unexpected error while parsing: {e}")
        return 1

    # Apply command-line overrides
    try:
        if args.scale is not None:
            engine.set_scale(args.scale)
        if args.fps is not None:
            engine.set_fps(args.fps)
        if args.crt:
            engine.crt = True
        if args.no_crt:
            engine.crt = False
    except ValidationError as e:
        safe_print(f"[ERR] Validation Error: {e}")
        return 1

    # Determine output directory
    if args.out:
        out_dir = Path(args.out)
    else:
        repo_root = find_repo_root(script_path.parent)
        out_dir = repo_root / 'exports'
    ensure_dir(out_dir)

    base_name = args.name or engine.name

    safe_print(f"\n[PixelMirai Compiler v{VERSION}]")
    safe_print(f"   Script  : {script_path.name}")
    safe_print(f"   Canvas  : {engine.width}x{engine.height}")
    safe_print(f"   Frames  : {len(engine.frames)}")
    safe_print(f"   Scale   : {engine.scale}x -> {engine.width * engine.scale}x{engine.height * engine.scale}px")
    safe_print(f"   Alpha   : {'transparent' if engine.is_transparent else 'opaque'}")
    safe_print(f"   CRT     : {'on' if engine.crt else 'off'}")
    safe_print(f"   FPS     : {engine.fps}")
    safe_print(f"   Out dir : {out_dir}\n")

    # Determine export list
    export_targets: List[Tuple[str, str]] = []
    if args.only:
        export_targets.append((args.only, f"{base_name}.{args.only if args.only != 'crt' else 'png'}"))
    elif exports:
        for fmt, custom_fn in exports:
            fn = custom_fn if (custom_fn and not args.name) else f"{base_name}.{fmt}"
            if fmt == 'crt' and not fn.endswith('.png'):
                fn = f"{base_name}-crt.png"
            export_targets.append((fmt, fn))
    else:
        export_targets = [
            ('png', f"{base_name}.png"),
            ('gif', f"{base_name}.gif"),
            ('crt', f"{base_name}-crt.png"),
            ('pxm', f"{base_name}.pxm"),
        ]

    if engine.crt and not any(fmt == 'crt' for fmt, _ in export_targets):
        export_targets.append(('crt', f"{base_name}-crt.png"))

    # Execute exports
    for fmt, filename in export_targets:
        target_path = out_dir / filename
        try:
            if fmt == 'png':
                engine.export_png(target_path)
            elif fmt == 'gif':
                engine.export_gif(target_path)
            elif fmt == 'crt':
                engine.export_crt(target_path)
            elif fmt == 'pxm':
                engine.export_pxm(target_path)
        except Exception as e:
            safe_print(f"[ERR] Failed exporting {fmt} to {target_path}: {e}")
            return 1

    safe_print(f"\n[Done] Compilation successful! Files saved to: {out_dir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
