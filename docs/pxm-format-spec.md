# PixelMirai — Format .pxm Specification

## Overview

`.pxm` adalah format file project PixelMirai. Secara teknis berupa **JSON teks
biasa** (bukan binary), namun dengan **checksum FNV-1a 32-bit** untuk validasi
integritas. File ini bisa di-load langsung di PixelMirai Studio (drag-drop).

---

## File Structure

```json
{
  "version": "1.0",
  "format": "PixelMirai",
  "name": "project-name",
  "width": 64,
  "height": 64,
  "palette": [
    "#000000",
    "#1d2b53",
    "..."
  ],
  "frames": [
    {
      "index": 0,
      "layers": [
        {
          "name": "layer-name",
          "pixels": [
            [x, y, paletteIndex],
            [x, y, paletteIndex]
          ]
        }
      ]
    }
  ],
  "fps": 6,
  "checksum": "9d43519a"
}
```

---

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | ✅ | Format version, selalu `"1.0"` |
| `format` | string | ✅ | Selalu `"PixelMirai"` (case-sensitive) |
| `name` | string | ✅ | Nama project (tanpa ekstensi) |
| `width` | integer | ✅ | Lebar canvas dalam piksel |
| `height` | integer | ✅ | Tinggi canvas dalam piksel |
| `palette` | string[] | ✅ | Array hex colors `#rrggbb` (lowercase) |
| `frames` | Frame[] | ✅ | Array frame (minimal 1) |
| `fps` | integer | ✅ | Frame rate untuk animasi GIF |
| `checksum` | string | ✅ | FNV-1a 32-bit hash (8 hex chars) |

### Frame Object

| Field | Type | Description |
|-------|------|-------------|
| `index` | integer | Urutan frame (0-based) |
| `layers` | Layer[] | Array layer dalam frame ini |

### Layer Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Nama layer (unik dalam frame) |
| `pixels` | [x, y, idx][] | Array piksel sebagai [x, y, paletteIndex] |

---

## Checksum Algorithm

Checksum dihitung **sebelum** field `checksum` ditambahkan ke JSON.

### Python Implementation

```python
import json

def compute_checksum(project: dict) -> str:
    """
    Compute FNV-1a 32-bit checksum for a .pxm project.
    project dict must NOT contain 'checksum' key yet.
    """
    # Serialize dengan sort_keys + no spaces (canonical form)
    content = json.dumps(project, separators=(',', ':'), sort_keys=True)
    content_bytes = content.encode('utf-8')
    
    # FNV-1a 32-bit
    h = 2166136261  # FNV offset basis
    for b in content_bytes:
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF  # FNV prime, 32-bit mask
    
    return format(h, '08x')

# Contoh:
project = {
    "version": "1.0",
    "format": "PixelMirai",
    "name": "cat-64",
    "width": 64,
    "height": 64,
    "palette": ["#000000", "#ff6600"],
    "frames": [...],
    "fps": 6,
}
project["checksum"] = compute_checksum(project)
```

### JavaScript Implementation

```js
// Dari lib/project-file.js
function fnv1a32(data) {
  let h = 2166136261;
  for (const b of new TextEncoder().encode(data)) {
    h ^= b;
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h.toString(16).padStart(8, '0');
}

function validateProjectData(project) {
  const { checksum, ...rest } = project;
  const canonical = JSON.stringify(rest, Object.keys(rest).sort());
  const computed = fnv1a32(canonical);
  
  if (computed !== checksum) {
    return { valid: false, errors: [`Checksum mismatch: ${computed} ≠ ${checksum}`] };
  }
  return { valid: true, errors: [] };
}
```

---

## Pixel Storage Format

Piksel disimpan sebagai `[x, y, paletteIndex]`:
- `x`: kolom (0 = kiri)
- `y`: baris (0 = atas)  
- `paletteIndex`: index ke array `palette` (0-based)

Hanya piksel **yang memiliki warna** yang disimpan. Piksel transparan/kosong
tidak disimpan (background ditentukan saat render).

**Contoh:**
```json
{
  "name": "body",
  "pixels": [
    [10, 5, 0],   // (10,5) → palette[0] = "#000000"
    [11, 5, 3],   // (11,5) → palette[3] = "#008751"
    [12, 5, 9]    // (12,5) → palette[9] = "#ffa300"
  ]
}
```

---

## Loading di Studio

```
Cara 1: Drag & Drop
  → Drag file .pxm ke canvas di http://localhost:3000/studio
  
Cara 2: Open File Dialog
  → Klik "Buka Project" → pilih .pxm file
  
Cara 3: URL Parameter
  → http://localhost:3000/studio?project=/exports/cat-64.pxm
```

---

## Validasi & Error Codes

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `CHECKSUM_MISMATCH` | File dimodifikasi manual tanpa recompute checksum | Jalankan ulang compiler |
| `INVALID_FORMAT` | Field `format` bukan `"PixelMirai"` | Periksa header JSON |
| `PALETTE_INDEX_OOB` | `paletteIndex` >= panjang array `palette` | Periksa index pixel |
| `CANVAS_SIZE_ZERO` | `width` atau `height` = 0 | Minimum 8×8 |
| `FRAME_MISSING` | Array `frames` kosong | Minimal 1 frame |
| `VERSION_UNKNOWN` | `version` bukan `"1.0"` | Update compiler |

---

## Backward Compatibility

- `.pxm` v1.0 adalah satu-satunya versi yang ada sekarang
- Field tambahan (di luar spec) di-ignore saat loading (forward-compatible)
- Checksum **harus** valid — file tanpa checksum atau checksum salah ditolak

---

*Format spec ini adalah bagian dari PixelMirai Engine v1.0.0*  
*© 2026 RianFix — Pixel art tak akan luntur oleh zaman*
