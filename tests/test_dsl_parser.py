import pytest
from scripts.pixelmirai_compiler import (
    DSLParser,
    DSLSyntaxError,
    PixelMiraiEngine,
)


def test_basic_dsl_parsing():
    dsl = """
    canvas 32 32
    palette pico8
    background #1d2b53
    scale 4
    fps 8

    frame 0
      layer "body"
        pixel 10 10 #ff004d
        rect 12 12 4 4 #00e436
        hline 20 5 15 #ffec27
        vline 8 5 15 #29adff
        circle 16 16 3 #fff1e8
        fillcircle 24 24 2 #ffa300

    export png "test.png"
    """
    parser = DSLParser(strict=True)
    engine, exports = parser.parse(dsl, name="test_sprite")

    assert engine.width == 32
    assert engine.height == 32
    assert engine.scale == 4
    assert engine.fps == 8
    assert len(engine.frames) == 1
    assert exports == [('png', 'test.png')]

    frame = engine.frames[0]
    layer = frame.get_or_create_layer('body')
    assert (10, 10) in layer.pixels
    assert layer.pixels[(10, 10)] == '#ff004d'


def test_comments_and_hex_colors_coexist():
    dsl = """
    canvas 16 16 // inline double-slash comment
    palette pico8 # inline hash comment
    background #000000 # black background

    frame 0
      layer "main"
        pixel 4 4 #ff004d # bright red pixel
        pixel 5 5 #00e436 // bright green pixel
    """
    parser = DSLParser(strict=True)
    engine, _ = parser.parse(dsl)
    layer = engine.frames[0].layers[0]
    assert layer.pixels[(4, 4)] == '#ff004d'
    assert layer.pixels[(5, 5)] == '#00e436'


def test_quoted_layer_names_and_filenames():
    dsl = """
    canvas 16 16
    frame 0
      layer "Knight's Shield & Armor"
        pixel 2 2 #ffffff
    export png "my custom export sprite.png"
    """
    parser = DSLParser(strict=True)
    engine, exports = parser.parse(dsl)
    assert engine.frames[0].layers[0].name == "Knight's Shield & Armor"
    assert exports == [('png', 'my custom export sprite.png')]


def test_unknown_command_raises_in_strict_mode():
    dsl = """
    canvas 16 16
    some_random_command 123
    """
    parser = DSLParser(strict=True)
    with pytest.raises(DSLSyntaxError) as exc_info:
        parser.parse(dsl)
    assert "Unknown DSL command 'some_random_command'" in str(exc_info.value)
    assert exc_info.value.line_num == 3


def test_missing_canvas_raises_syntax_error():
    dsl = """
    palette pico8
    pixel 1 1 #ffffff
    """
    parser = DSLParser(strict=True)
    with pytest.raises(DSLSyntaxError) as exc_info:
        parser.parse(dsl)
    assert "requires 'canvas' first" in str(exc_info.value) or "declare canvas" in str(exc_info.value)


def test_missing_argument_reports_exact_line_number():
    dsl = """
    canvas 16 16
    frame 0
      layer "base"
        rect 2 2 4 #ff004d
    """
    parser = DSLParser(strict=True)
    with pytest.raises(DSLSyntaxError) as exc_info:
        parser.parse(dsl)
    assert exc_info.value.line_num == 5
    assert "'rect' expects x y width height color" in str(exc_info.value)


def test_unmatched_quote_raises_syntax_error():
    dsl = """
    canvas 16 16
    layer "unclosed string
    """
    parser = DSLParser(strict=True)
    with pytest.raises(DSLSyntaxError) as exc_info:
        parser.parse(dsl)
    assert exc_info.value.line_num == 3
    assert "Unmatched quote" in str(exc_info.value)
