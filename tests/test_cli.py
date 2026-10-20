import subprocess
import sys
from pathlib import Path


def run_cli(*args):
    cmd = [sys.executable, "scripts/pixelmirai_compiler.py"] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True)


def test_cli_missing_file():
    res = run_cli("non_existent_file.dsl")
    assert res.returncode == 1
    assert "File not found" in res.stdout or "File not found" in res.stderr


def test_cli_invalid_scale():
    res = run_cli("examples/coin-16.pxm.dsl", "--scale", "999")
    assert res.returncode == 1
    assert "Scale factor must be between" in res.stdout or "Scale factor must be between" in res.stderr


def test_cli_compile_success(tmp_path):
    res = run_cli("examples/coin-16.pxm.dsl", "--out", str(tmp_path), "--only", "png")
    assert res.returncode == 0
    out_png = tmp_path / "coin-16.png"
    assert out_png.exists()
    assert out_png.stat().st_size > 0


def test_cli_custom_name(tmp_path):
    res = run_cli("examples/coin-16.pxm.dsl", "--out", str(tmp_path), "--name", "special_coin", "--only", "png")
    assert res.returncode == 0
    out_png = tmp_path / "special_coin.png"
    assert out_png.exists()


def test_cli_syntax_error_nonzero_exit(tmp_path):
    bad_dsl = tmp_path / "bad.dsl"
    bad_dsl.write_text("canvas 16 16\ninvalid_cmd_xyz 123\n", encoding="utf-8")

    res = run_cli(str(bad_dsl))
    assert res.returncode == 1
    assert "Unknown DSL command 'invalid_cmd_xyz'" in res.stdout or "Unknown DSL command 'invalid_cmd_xyz'" in res.stderr
