import pytest
from PIL import Image
from scripts.pixelmirai_compiler import PixelMiraiEngine, DSLParser


def test_transparent_background_png(tmp_path):
    dsl = """
    canvas 16 16
    background transparent
    scale 2

    frame 0
      layer "dot"
        pixel 8 8 #ff004d
    """
    parser = DSLParser()
    engine, _ = parser.parse(dsl)
    out_file = tmp_path / "transparent.png"
    engine.export_png(out_file)

    img = Image.open(out_file)
    assert img.mode == 'RGBA'
    assert img.size == (32, 32)

    # Corner unpainted pixel should be completely transparent (alpha == 0)
    corner = img.getpixel((0, 0))
    assert corner[3] == 0

    # Painted pixel at (8*2, 8*2) = (16, 16) should be solid red (alpha == 255)
    painted = img.getpixel((16, 16))
    assert painted[0] == 255  # Red
    assert painted[1] == 0    # Green
    assert painted[2] == 77   # Blue (#ff004d)
    assert painted[3] == 255  # Solid Alpha


def test_opaque_background_png(tmp_path):
    dsl = """
    canvas 16 16
    background #1d2b53
    scale 2

    frame 0
      layer "dot"
        pixel 8 8 #ff004d
    """
    parser = DSLParser()
    engine, _ = parser.parse(dsl)
    out_file = tmp_path / "opaque.png"
    engine.export_png(out_file)

    img = Image.open(out_file)
    assert img.mode == 'RGB'
    corner = img.getpixel((0, 0))
    # Matches dark navy #1d2b53 = (29, 43, 83)
    assert corner == (29, 43, 83)


def test_transparent_animated_gif(tmp_path):
    dsl = """
    canvas 16 16
    background transparent
    fps 4
    scale 2

    frame 0
      layer "dot"
        pixel 4 4 #ffec27

    frame 1
      layer "dot"
        pixel 12 12 #ffec27
    """
    parser = DSLParser()
    engine, _ = parser.parse(dsl)
    out_file = tmp_path / "anim_transparent.gif"
    engine.export_gif(out_file)

    assert out_file.exists()
    assert out_file.stat().st_size > 0
    img = Image.open(out_file)
    assert img.is_animated
    assert img.n_frames == 2
