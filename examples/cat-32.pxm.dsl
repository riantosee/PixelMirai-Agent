# canvas setup
canvas 32 32
palette pico8
background #000000
scale 16
crt off
fps 6

# ── Frame 0: Idle ──────────────────────────────────────────
frame 0

layer "bg"
  rect 0 28 32 4 #5f574f

layer "shadow"
  rect 10 28 12 2 #1d2b53

layer "body"
  # main body (orange calico)
  rect 10 14 12 14 #ffa300
  # white chest bib
  rect 12 18 8 8 #fff1e8
  # tabby stripes
  hline 17 10 12 #ab5236
  hline 20 10 12 #ab5236
  hline 17 20 22 #ab5236
  hline 20 20 22 #ab5236

layer "head"
  # head block
  rect 8 6 16 12 #ffa300
  # ears
  rect 8 3 4 4 #ffa300
  rect 20 3 4 4 #ffa300
  # ear inner (pink)
  rect 9 4 2 2 #ff77a8
  rect 21 4 2 2 #ff77a8
  # outline
  pixel 8 6 #000000
  pixel 23 6 #000000
  pixel 8 17 #000000
  pixel 23 17 #000000

layer "face"
  # eyes (emerald)
  rect 10 9 4 3 #00e436
  rect 18 9 4 3 #00e436
  # pupils
  rect 11 9 2 3 #1d2b53
  rect 19 9 2 3 #1d2b53
  # eye shine
  pixel 12 9 #fff1e8
  pixel 20 9 #fff1e8
  # nose
  pixel 15 13 #ff77a8
  pixel 16 13 #ff77a8
  # mouth
  pixel 14 14 #1d2b53
  pixel 17 14 #1d2b53
  # whiskers
  hline 13 4 9 #c2c3c7
  hline 13 23 28 #c2c3c7

layer "collar"
  rect 9 18 14 2 #ff004d
  pixel 15 18 #ffec27
  pixel 15 19 #ffec27

layer "tail"
  # tail curling right
  vline 22 20 26 #ffa300
  pixel 23 24 #ffa300
  pixel 23 25 #ffa300
  pixel 22 26 #ffa300
  pixel 21 27 #ffa300

layer "paws"
  # front paws
  rect 10 26 4 2 #ffa300
  rect 18 26 4 2 #ffa300
  hline 27 11 13 #fff1e8
  hline 27 19 21 #fff1e8

# ── Frame 1: Blink ─────────────────────────────────────────
frame 1

layer "bg"
  rect 0 28 32 4 #5f574f

layer "shadow"
  rect 10 28 12 2 #1d2b53

layer "body"
  rect 10 14 12 14 #ffa300
  rect 12 18 8 8 #fff1e8
  hline 17 10 12 #ab5236
  hline 20 10 12 #ab5236
  hline 17 20 22 #ab5236
  hline 20 20 22 #ab5236

layer "head"
  rect 8 6 16 12 #ffa300
  rect 8 3 4 4 #ffa300
  rect 20 3 4 4 #ffa300
  rect 9 4 2 2 #ff77a8
  rect 21 4 2 2 #ff77a8

layer "face"
  # eyes CLOSED (blink)
  hline 10 10 13 #1d2b53
  hline 10 18 21 #1d2b53
  # nose & mouth same
  pixel 15 13 #ff77a8
  pixel 16 13 #ff77a8
  pixel 14 14 #1d2b53
  pixel 17 14 #1d2b53
  hline 13 4 9 #c2c3c7
  hline 13 23 28 #c2c3c7

layer "collar"
  rect 9 18 14 2 #ff004d
  pixel 15 18 #ffec27
  pixel 15 19 #ffec27

layer "tail"
  vline 22 20 26 #ffa300
  pixel 23 24 #ffa300
  pixel 23 25 #ffa300
  pixel 22 26 #ffa300
  pixel 21 27 #ffa300

layer "paws"
  rect 10 26 4 2 #ffa300
  rect 18 26 4 2 #ffa300
  hline 27 11 13 #fff1e8
  hline 27 19 21 #fff1e8

# ── Exports ────────────────────────────────────────────────
export png "cat-32.png"
export gif "cat-32.gif"
export crt "cat-32-crt.png"
export pxm "cat-32.pxm"
