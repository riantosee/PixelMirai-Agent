# PixelMirai DSL (Domain Specific Language) Specification

PixelMirai DSL is a declarative, human-readable script format designed for writing deterministic retro pixel art sprites, multi-frame animations, and scenes.

---

## Grammar & Commands

### 1. Canvas / Size Header
```dsl
canvas <width> <height>
# or
size <width> [height]
```
- Sets the canvas dimensions in pixels (integer values). If only one parameter is passed to `size`, height defaults to width.
- Example: `canvas 64 64` or `size 32`

### 2. Palette Preset
```dsl
palette <preset_name>
```
- Supported presets:
  - `pico8` (or `pico-8`): 16-color retro console palette.
  - `endesga32`: 32-color extended rich game palette.
  - `gameboy`: 4-color monochrome classic LCD palette.
  - `cga`: 16-color IBM PC CGA palette.

### 3. Background Color
```dsl
background <hex_or_transparent>
```
- Examples: `background #1d2b53`, `background #000000`, `background transparent`.

### 4. Output Scaling & FPS
```dsl
scale <integer>
fps <integer>
```
- `scale`: integer upscale factor for exported PNGs (default: 8).
- `fps`: playback speed in frames per second for animated GIFs (default: 6).

### 5. CRT Filter
```dsl
crt on
# or
crt off
```
- Enables retro CRT simulation with scanlines and radial vignette shadow.

### 6. Frames and Layers
```dsl
frame <index>
  layer "<layer_name>"
```
- `frame`: 0-indexed frame container.
- `layer`: named layer within a frame.

### 7. Drawing Primitives
```dsl
# Single pixel
pixel <x> <y> <#color>

# Multiple pixels (batch)
pixels <#color> <x1,y1> <x2,y2> ...

# Solid rectangle
rect <x> <y> <width> <height> <#color>

# Horizontal line
hline <y> <x1> <x2> <#color>

# Vertical line
vline <x> <y1> <y2> <#color>

# Bresenham Circle outline
circle <cx> <cy> <radius> <#color>

# Solid Circle
fillcircle <cx> <cy> <radius> <#color>
```

### 8. Export Declarations
```dsl
export png "filename.png"
export gif "filename.gif"
export crt "filename-crt.png"
export pxm "filename.pxm"
```

---

## Comments
Both `# comment` and `// comment` syntax are supported.
Inline comments are automatically separated from hex color codes like `#ff004d`.
