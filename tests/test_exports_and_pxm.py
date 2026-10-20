import json
from pathlib import Path
import pytest
from PIL import Image

from scripts.pixelmirai_compiler import (
    PixelMiraiEngine,
    PXMChecksumError,
    DSLParser,
)


def test_pxm_round_trip(tmp_path):
    # 1. Create engine and place pixels
    engine = PixelMiraiEngine(16, 16)
    engine.name = "round_trip_sprite"
    engine.set_palette('pico8')
    engine.set_fps(12)

    frame0 = engine.new_frame(0)
    layer0 = frame0.new_layer("base")
    layer0.rect(4, 4, 8, 8, "#ffa300")
    layer0.pixel(7, 7, "#ff004d")

    frame1 = engine.new_frame(1)
    layer1 = frame1.new_layer("base")
    layer1.rect(4, 4, 8, 8, "#ffec27")

    pxm_path = tmp_path / "sprite.pxm"
    engine.export_pxm(pxm_path)
    assert pxm_path.exists()

    # 2. Reload and verify checksum
    loaded = PixelMiraiEngine.load_pxm(pxm_path, verify_checksum=True)
    assert loaded.width == 16
    assert loaded.height == 16
    assert loaded.name == "round_trip_sprite"
    assert loaded.fps == 12
    assert len(loaded.frames) == 2

    # Verify frame 0 pixels
    l0 = loaded.frames[0].layers[0]
    assert l0.pixels[(7, 7)] == "#ff004d"
    assert l0.pixels[(4, 4)] == "#ffa300"

    # Verify frame 1 pixels
    l1 = loaded.frames[1].layers[0]
    assert l1.pixels[(4, 4)] == "#ffec27"


def test_corrupt_pxm_checksum_fails(tmp_path):
    engine = PixelMiraiEngine(8, 8)
    engine.new_frame().new_layer("l").pixel(0, 0, "#000000")

    pxm_path = tmp_path / "valid.pxm"
    engine.export_pxm(pxm_path)

    with open(pxm_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['checksum'] = "00000000"
    corrupt_path = tmp_path / "corrupt.pxm"
    with open(corrupt_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    with pytest.raises(PXMChecksumError):
        PixelMiraiEngine.load_pxm(corrupt_path, verify_checksum=True)


def test_all_bundled_pxm_exports_pass_verification():
    repo_root = Path(__file__).parent.parent
    pxm_dir = repo_root / "examples" / "exports"
    pxm_files = list(pxm_dir.glob("*.pxm"))
    assert len(pxm_files) >= 4

    for pxm_file in pxm_files:
        engine = PixelMiraiEngine.load_pxm(pxm_file, verify_checksum=True)
        assert engine.width > 0
        assert engine.height > 0
        assert len(engine.frames) > 0


def test_crt_export_properties(tmp_path):
    engine = PixelMiraiEngine(16, 16)
    engine.new_frame().new_layer("l").rect(2, 2, 12, 12, "#00e436")

    crt_path = tmp_path / "crt_test.png"
    engine.export_crt(crt_path, scale=4)

    assert crt_path.exists()
    img = Image.open(crt_path)
    assert img.size == (64, 64)
    assert img.mode == 'RGB'
