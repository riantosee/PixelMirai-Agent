# PixelMirai DSL — 8-bit Knight 32×32 (4-frame walk cycle)
canvas 32 32
palette pico8
background #1d2b53
scale 12
crt off
fps 8

# ═══════════════════════════════
# FRAME 0: Stand / Step-left-up
# ═══════════════════════════════
frame 0

layer "shadow"
  rect 10 30 12 2 #000000

layer "legs"
  # left leg
  rect 10 22 5 8 #5f574f
  rect 10 28 5 2 #c2c3c7
  # right leg
  rect 17 22 5 8 #5f574f
  rect 17 28 5 2 #c2c3c7

layer "body"
  rect 8 12 16 12 #c2c3c7
  rect 9 13 14 10 #5f574f
  # chest detail
  rect 12 15 8 5 #83769c
  pixel 15 17 #fff1e8
  pixel 16 17 #fff1e8

layer "arms"
  # left arm (holding sword)
  rect 4 13 4 10 #c2c3c7
  # sword
  vline 3 5 16 #fff1e8
  pixel 3 4 #c2c3c7
  rect 2 16 3 2 #ab5236
  # right arm
  rect 24 13 4 10 #c2c3c7
  # shield
  rect 27 11 4 10 #ff004d
  pixel 28 13 #ffec27
  pixel 29 13 #ffec27
  pixel 28 17 #ffec27
  pixel 29 17 #ffec27

layer "head"
  rect 9 4 14 10 #c2c3c7
  # visor slit
  rect 10 7 12 3 #1d2b53
  pixel 12 8 #29adff
  pixel 13 8 #29adff
  pixel 16 8 #29adff
  pixel 17 8 #29adff
  # helmet plume
  vline 15 0 4 #ff004d
  pixel 14 1 #ff004d
  pixel 16 1 #ff004d
  pixel 14 2 #ffa300
  pixel 16 2 #ffa300

# ═══════════════════════════════
# FRAME 1: Walk step A (left foot forward)
# ═══════════════════════════════
frame 1

layer "shadow"
  rect 10 30 12 2 #000000

layer "legs"
  # left leg forward
  rect 9 22 5 9 #5f574f
  rect 9 29 5 2 #c2c3c7
  # right leg back
  rect 18 22 5 7 #5f574f
  rect 18 28 5 2 #c2c3c7

layer "body"
  rect 8 12 16 12 #c2c3c7
  rect 9 13 14 10 #5f574f
  rect 12 15 8 5 #83769c
  pixel 15 17 #fff1e8
  pixel 16 17 #fff1e8

layer "arms"
  rect 4 14 4 10 #c2c3c7
  vline 3 6 17 #fff1e8
  pixel 3 5 #c2c3c7
  rect 2 17 3 2 #ab5236
  rect 24 12 4 10 #c2c3c7
  rect 27 10 4 10 #ff004d
  pixel 28 12 #ffec27
  pixel 29 12 #ffec27
  pixel 28 16 #ffec27
  pixel 29 16 #ffec27

layer "head"
  rect 9 4 14 10 #c2c3c7
  rect 10 7 12 3 #1d2b53
  pixel 12 8 #29adff
  pixel 13 8 #29adff
  pixel 16 8 #29adff
  pixel 17 8 #29adff
  vline 15 0 4 #ff004d
  pixel 14 1 #ff004d
  pixel 16 1 #ff004d
  pixel 14 2 #ffa300
  pixel 16 2 #ffa300

# ═══════════════════════════════
# FRAME 2: Stand / Mid-step
# ═══════════════════════════════
frame 2

layer "shadow"
  rect 10 30 12 2 #000000

layer "legs"
  rect 10 22 5 8 #5f574f
  rect 10 28 5 2 #c2c3c7
  rect 17 22 5 8 #5f574f
  rect 17 28 5 2 #c2c3c7

layer "body"
  rect 8 11 16 13 #c2c3c7
  rect 9 12 14 11 #5f574f
  rect 12 14 8 5 #83769c
  pixel 15 16 #fff1e8
  pixel 16 16 #fff1e8

layer "arms"
  rect 4 12 4 10 #c2c3c7
  vline 3 4 15 #fff1e8
  pixel 3 3 #c2c3c7
  rect 2 15 3 2 #ab5236
  rect 24 12 4 10 #c2c3c7
  rect 27 11 4 10 #ff004d
  pixel 28 13 #ffec27
  pixel 29 13 #ffec27
  pixel 28 17 #ffec27
  pixel 29 17 #ffec27

layer "head"
  rect 9 3 14 10 #c2c3c7
  rect 10 6 12 3 #1d2b53
  pixel 12 7 #29adff
  pixel 13 7 #29adff
  pixel 16 7 #29adff
  pixel 17 7 #29adff
  vline 15 0 3 #ff004d
  pixel 14 1 #ff004d
  pixel 16 1 #ff004d

# ═══════════════════════════════
# FRAME 3: Walk step B (right foot forward)
# ═══════════════════════════════
frame 3

layer "shadow"
  rect 10 30 12 2 #000000

layer "legs"
  # left leg back
  rect 9 22 5 7 #5f574f
  rect 9 28 5 2 #c2c3c7
  # right leg forward
  rect 18 22 5 9 #5f574f
  rect 18 29 5 2 #c2c3c7

layer "body"
  rect 8 12 16 12 #c2c3c7
  rect 9 13 14 10 #5f574f
  rect 12 15 8 5 #83769c
  pixel 15 17 #fff1e8
  pixel 16 17 #fff1e8

layer "arms"
  rect 4 12 4 10 #c2c3c7
  vline 3 4 15 #fff1e8
  pixel 3 3 #c2c3c7
  rect 2 15 3 2 #ab5236
  rect 24 14 4 10 #c2c3c7
  rect 27 12 4 10 #ff004d
  pixel 28 14 #ffec27
  pixel 29 14 #ffec27
  pixel 28 18 #ffec27
  pixel 29 18 #ffec27

layer "head"
  rect 9 4 14 10 #c2c3c7
  rect 10 7 12 3 #1d2b53
  pixel 12 8 #29adff
  pixel 13 8 #29adff
  pixel 16 8 #29adff
  pixel 17 8 #29adff
  vline 15 0 4 #ff004d
  pixel 14 1 #ff004d
  pixel 16 1 #ff004d
  pixel 14 2 #ffa300
  pixel 16 2 #ffa300

export png "knight-32.png"
export gif "knight-32.gif"
export crt "knight-32-crt.png"
export pxm "knight-32.pxm"
