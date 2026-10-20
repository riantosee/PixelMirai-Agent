from pathlib import Path
from scripts.pixelmirai_compiler import DSLParser, main


def test_compile_all_bundled_examples(tmp_path):
    repo_root = Path(__file__).parent.parent
    examples_dir = repo_root / "examples"
    dsl_files = list(examples_dir.glob("*.pxm.dsl"))
    assert len(dsl_files) >= 4

    parser = DSLParser(strict=True)

    for dsl_file in dsl_files:
        engine, exports = parser.parse_file(dsl_file)
        assert engine.width > 0
        assert engine.height > 0
        assert len(engine.frames) > 0

        # Compile through CLI main
        ret = main([str(dsl_file), "--out", str(tmp_path), "--only", "png"])
        assert ret == 0

        # Verify PNG exists
        png_out = tmp_path / f"{dsl_file.stem.replace('.pxm', '')}.png"
        assert png_out.exists()
        assert png_out.stat().st_size > 0
