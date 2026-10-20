# PixelMirai DSL — Gold Coin 16×16 (4-frame spin)
canvas 16 16
palette pico8
background transparent
scale 16
crt off
fps 10

# ── Frame 0: Full coin (facing front) ──
frame 0
layer "coin"
  fillcircle 8 8 6 #ffec27
  circle 8 8 6 #ab5236
  fillcircle 8 8 4 #ffa300
  pixel 6 7 #ffec27
  pixel 7 6 #ffec27
  pixel 8 6 #ffec27
  pixel 9 6 #ffec27
  pixel 6 8 #ffec27
  pixel 6 9 #ffec27
  pixel 8 10 #ffec27
  pixel 9 10 #ffec27
  pixel 10 7 #ab5236
  pixel 10 9 #ab5236

# ── Frame 1: 3/4 view (slight tilt) ──
frame 1
layer "coin"
  rect 5 2 6 12 #ffec27
  rect 6 2 4 12 #ffa300
  vline 5 2 13 #ab5236
  vline 10 2 13 #ab5236
  hline 2 5 10 #ab5236
  hline 13 5 10 #ab5236

# ── Frame 2: Edge-on (thin line) ──
frame 2
layer "coin"
  vline 8 2 13 #ffec27
  pixel 7 2 #ffa300
  pixel 9 2 #ffa300
  pixel 7 13 #ffa300
  pixel 9 13 #ffa300

# ── Frame 3: 3/4 view (other side) ──
frame 3
layer "coin"
  rect 5 2 6 12 #ffa300
  rect 6 2 4 12 #ffec27
  vline 5 2 13 #ab5236
  vline 10 2 13 #ab5236
  hline 2 5 10 #ab5236
  hline 13 5 10 #ab5236

export png "coin-16.png"
export gif "coin-16.gif"
export pxm "coin-16.pxm"
