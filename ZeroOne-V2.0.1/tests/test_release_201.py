import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZO = ROOT / "zo.py"

def run_zo(source, name):
    src = ROOT / f"{name}.zo"
    bc = ROOT / f"{name}.zbc"
    src.write_text(source, encoding="utf-8")
    try:
        c = subprocess.run([sys.executable, str(ZO), "compile", src.name],
                           cwd=ROOT, text=True, capture_output=True)
        assert c.returncode == 0, c.stderr
        r = subprocess.run([sys.executable, str(ZO), "run", bc.name],
                           cwd=ROOT, text=True, capture_output=True)
        assert r.returncode == 0, r.stderr
        return r.stdout.strip()
    finally:
        src.unlink(missing_ok=True)
        bc.unlink(missing_ok=True)

def test_version():
    p = subprocess.run([sys.executable, str(ZO), "--version"],
                       cwd=ROOT, text=True, capture_output=True)
    assert p.returncode == 0
    assert "ZeroOne 2.0.1" in p.stdout

def test_native_function_call():
    assert run_zo("SET result = FAC(5)\nOUT result\nEXIT\n", "t_fac") == "120"

def test_bitwise_native_calls():
    src = """SET a = BITAND(12, 10)
SET b = BITOR(12, 10)
SET c = BITXOR(12, 10)
SET d = BITNOT(0)
SET e = LSHIFT(3, 2)
SET f = RSHIFT(16, 2)
SET g = POPCOUNT(15)
OUT a
OUT b
OUT c
OUT d
OUT e
OUT f
OUT g
EXIT
"""
    assert run_zo(src, "t_bits").splitlines() == ["8","14","6","-1","12","4","4"]

def test_ternary():
    assert run_zo("SET x = TRUE ? 10 : 20\nOUT x\nEXIT\n", "t_ternary") == "10"

def test_bitwise_operators():
    src = """OUT 12 & 10
OUT 1 | 2
OUT 1 ^ 3
OUT ~1
EXIT
"""
    assert run_zo(src, "t_bitops").splitlines() == ["8", "3", "2", "-2"]

def test_for_with_assignment_update():
    src = """SET total = 0
FOR SET i = 0; i < 5; SET i = i + 1
    SET total = total + i
END
OUT total
EXIT
"""
    assert run_zo(src, "t_for") == "10"

def test_foreach():
    src = """SET xs = [1, 2, 3]
SET total = 0
FOREACH x IN xs
    SET total = total + x
END
OUT total
EXIT
"""
    assert run_zo(src, "t_foreach") == "6"

def test_try_catch_finally():
    src = """TRY
    THROW "boom"
CATCH
    OUT "caught"
FINALLY
    OUT "finally"
END
EXIT
"""
    assert run_zo(src, "t_try").splitlines() == ["caught", "finally"]

def test_custom_catch_variable():
    src = """TRY
    THROW "boom"
CATCH (Exception: err)
    OUT err
END
EXIT
"""
    assert run_zo(src, "t_catch_var") == "boom"

def test_switch():
    src = """SET x = 2
SWITCH x
CASE 1:
    OUT "one"
CASE 2:
    OUT "two"
DEFAULT:
    OUT "other"
END
EXIT
"""
    assert run_zo(src, "t_switch") == "two"

def test_runtime_stdlib_imports():
    src = """OUT DATE()
OUT TIME()
OUT GETPID()
OUT PLATFORM()
EXIT
"""
    out = run_zo(src, "t_runtime").splitlines()
    assert len(out) == 4
    assert out[0]
    assert out[1]
    assert out[2].isdigit()
    assert out[3]
