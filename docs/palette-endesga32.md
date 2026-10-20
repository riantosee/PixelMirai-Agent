# Endesga32 Palette — PixelMirai Reference

Palette `endesga32` tersedia via `palette endesga32` di DSL header.
Total 32 warna, cocok untuk sprite 64×64 ke atas yang butuh nuansa lebih kaya.

## Color Table

| Index | Name | Hex | RGB | Usage |
|-------|------|-----|-----|-------|
| 0 | brick-red | `#be4a2f` | 190,74,47 | batu bata, tanah |
| 1 | terra-cotta | `#d77643` | 215,118,67 | tanah terang, kulit |
| 2 | linen | `#ead4aa` | 234,212,170 | pasir, kertas tua |
| 3 | peach | `#e4a672` | 228,166,114 | kulit, kayu terang |
| 4 | sienna | `#b86f50` | 184,111,80 | kayu, kulit gelap |
| 5 | mahogany | `#733e39` | 115,62,57 | kayu gelap, shadow |
| 6 | dark-plum | `#3e2731` | 62,39,49 | shadow terdalam |
| 7 | crimson | `#a22633` | 162,38,51 | merah gelap, darah |
| 8 | scarlet | `#e43b44` | 228,59,68 | merah cerah, bahaya |
| 9 | pumpkin | `#f77622` | 247,118,34 | api, orange |
| 10 | amber | `#feae34` | 254,174,52 | emas muda, api |
| 11 | lemon | `#fee761` | 254,231,97 | kuning cerah, cahaya |
| 12 | lime | `#63c74d` | 99,199,77 | rumput cerah |
| 13 | forest | `#3e8948` | 62,137,72 | hutan, daun |
| 14 | pine | `#265c42` | 38,92,66 | hutan gelap |
| 15 | teal-dark | `#193c3e` | 25,60,62 | laut dalam |
| 16 | navy | `#124e89` | 18,78,137 | biru laut |
| 17 | sky | `#0099db` | 0,153,219 | langit siang |
| 18 | cyan | `#2ce8f5` | 44,232,245 | air, highlight |
| 19 | white | `#ffffff` | 255,255,255 | putih murni |
| 20 | silver | `#c0cbdc` | 192,203,220 | logam, es |
| 21 | steel | `#8b9bb4` | 139,155,180 | baja, batu |
| 22 | slate | `#5a6988` | 90,105,136 | batu gelap |
| 23 | midnight | `#3a4466` | 58,68,102 | malam |
| 24 | darknight | `#262b44` | 38,43,68 | malam terdalam |
| 25 | void | `#181425` | 24,20,37 | hitam void |
| 26 | hot-pink | `#ff0044` | 255,0,68 | neon, danger |
| 27 | purple | `#68386c` | 104,56,108 | sihir gelap |
| 28 | magenta | `#b55088` | 181,80,136 | sihir, bunga |
| 29 | rose | `#f6757a` | 246,117,122 | pink lembut |
| 30 | sand | `#e8b796` | 232,183,150 | pasir, kulit |
| 31 | tan | `#c28569` | 194,133,105 | kulit gelap, kayu |

## Penggunaan di DSL

```dsl
canvas 64 64
palette endesga32
background #181425    # void (index 25)

frame 0
layer "sky"
  rect 0 0 64 32 #0099db     # sky (index 17)
  
layer "ground"
  rect 0 32 64 32 #265c42    # pine (index 14)
  
layer "sun"
  fillcircle 48 12 8 #fee761  # lemon (index 11)
```

## Kombinasi Warna Harmonis

### Malam Kota Cyberpunk
- Background: `#181425` (void)
- Neon: `#ff0044` (hot-pink) + `#2ce8f5` (cyan)
- Bangunan: `#262b44` (darknight) + `#3a4466` (midnight)
- Lampu: `#feae34` (amber)

### Hutan Alam
- Sky: `#0099db` (sky)
- Rumput: `#63c74d` (lime)
- Pohon: `#265c42` (pine) + `#3e8948` (forest)
- Tanah: `#be4a2f` (brick-red)

### Dungeon Batu
- Dinding: `#5a6988` (slate) + `#3a4466` (midnight)
- Torch: `#f77622` (pumpkin) + `#fee761` (lemon)
- Shadow: `#181425` (void)
- Metal: `#c0cbdc` (silver)

### Kulit Karakter (untuk 64×64+)
- Light: `#e8b796` (sand)
- Mid: `#c28569` (tan)
- Dark: `#b86f50` (sienna)
- Shadow: `#733e39` (mahogany)
- Outline: `#3e2731` (dark-plum)
