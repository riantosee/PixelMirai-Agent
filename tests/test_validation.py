import pytest
from scripts.pixelmirai_compiler import (
    PixelMiraiEngine,
    ValidationError,
    normalize_hex,
    hex_to_rgba,
)


def test_canvas_bounds_validation():
    # Valid
    e1 = PixelMiraiEngine(1, 1)
    assert e1.width == 1 and e1.height == 1

    e2 = PixelMiraiEngine(2048, 2048)
    assert e2.width == 2048 and e2.height == 2048

    # Invalid lower
    with pytest.raises(ValidationError):
        PixelMiraiEngine(0, 32)

    with pytest.raises(ValidationError):
        PixelMiraiEngine(-16, 32)

    # Invalid upper
    with pytest.raises(ValidationError):
        PixelMiraiEngine(2049, 32)


def test_scale_bounds_validation():
    engine = PixelMiraiEngine(32, 32)
    engine.set_scale(1)
    engine.set_scale(64)

    with pytest.raises(ValidationError):
        engine.set_scale(0)

    with pytest.raises(ValidationError):
        engine.set_scale(65)


def test_fps_bounds_validation():
    engine = PixelMiraiEngine(32, 32)
    engine.set_fps(1)
    engine.set_fps(120)

    with pytest.raises(ValidationError):
        engine.set_fps(0)

    with pytest.raises(ValidationError):
        engine.set_fps(121)


def test_hex_color_validation():
    # 3-hex expands to 6-hex
    assert normalize_hex("#fff") == "#ffffff"
    assert normalize_hex("#123") == "#112233"

    # 6-hex normalizes lowercase
    assert normalize_hex("#FF004D") == "#ff004d"

    # 4-hex and 8-hex
    assert normalize_hex("#ffff") == "#ffffffff"
    assert normalize_hex("#ff004d80") == "#ff004d80"

    # Invalid hex formats
    with pytest.raises(ValidationError):
        normalize_hex("ff004d")  # Missing #

    with pytest.raises(ValidationError):
        normalize_hex("#zzzzzz")

    with pytest.raises(ValidationError):
        normalize_hex("#12")

    with pytest.raises(ValidationError):
        normalize_hex("#12345")


def test_hex_to_rgba():
    assert hex_to_rgba("#000000") == (0, 0, 0, 255)
    assert hex_to_rgba("#ffffff") == (255, 255, 255, 255)
    assert hex_to_rgba("#ff004d80") == (255, 0, 77, 128)


def test_drawing_parameter_validation():
    engine = PixelMiraiEngine(32, 32)
    layer = engine.new_frame().new_layer("test")

    # Rect width and height must be > 0
    with pytest.raises(ValidationError):
        layer.rect(0, 0, 0, 10, "#ffffff")

    with pytest.raises(ValidationError):
        layer.rect(0, 0, 10, -5, "#ffffff")

    # Circle radius must be >= 0
    with pytest.raises(ValidationError):
        layer.circle(16, 16, -1, "#ffffff")

    with pytest.raises(ValidationError):
        layer.fillcircle(16, 16, -2, "#ffffff")
