import sys
from pathlib import Path
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from compiler.bytecode import ByteCodeReader, ByteCodeError
from vm.vm import ZeroOneVM, VMError


def run(src):
    code = Assembler().assemble(Generator().generate(Parser(Lexer(src).tokenize()).parse()))
    vm = ZeroOneVM()
    vm.load(code)
    vm.run()
    return vm


def test_class_new_init_and_bound_method():
    src = '''
CLASS Counter
FUNC init(self, value)
    SET self.value = value
END
FUNC add(self, amount)
    SET self.value = self.value + amount
    RETURN self.value
END
END
SET c = NEW Counter(10)
SET r = c.add(5)
'''
    vm = run(src)
    assert vm.memory["r"] == 15
    assert vm.memory["c"]["value"] == 15


def test_class_inheritance_method_lookup():
    src = '''
CLASS A
FUNC init(self)
    SET self.x = 4
END
FUNC get(self)
    RETURN self.x
END
END
CLASS B EXTENDS A
END
SET b = NEW B()
SET r = b.get()
'''
    vm = run(src)
    assert vm.memory["r"] == 4


def test_short_circuit_and_or():
    src = '''
SET x = 0
FUNC boom()
    SET x = x + 1
    RETURN TRUE
END
SET a = FALSE AND boom()
SET b = TRUE OR boom()
'''
    vm = run(src)
    assert vm.memory["a"] is False
    assert vm.memory["b"] is True
    assert vm.memory["x"] == 0


def test_multiline_array():
    vm = run('''SET a = [\n  1,\n  2,\n  3\n]\n''')
    assert vm.memory["a"] == [1, 2, 3]


def test_shift_operators_are_distinct():
    vm = run('SET a = -8 >> 1\nSET b = -8 >>> 1\n')
    assert vm.memory["a"] == -4
    assert vm.memory["b"] == 2147483644


def test_add_type_error_is_zero_one_error_and_catchable():
    src = '''
SET caught = FALSE
TRY
    SET x = 1 + "a"
CATCH e
    SET caught = TRUE
    SET message = e
END
'''
    vm = run(src)
    assert vm.memory["caught"] is True
    assert "ADD" in str(vm.memory["message"])
    assert "TypeError" not in str(vm.memory["message"])


def test_version_everywhere():
    vm = run('SET v = VERSION()\n')
    assert vm.memory["v"] == "2.0.9"
    root = Path(__file__).resolve().parents[1]
    p = subprocess.run([sys.executable, str(root / "zo.py"), "--version"], text=True, capture_output=True)
    assert p.returncode == 0
    assert p.stdout.strip() == "ZeroOne 2.0.9"


def test_corrupt_bytecode_never_leaks_struct_or_json_exception(tmp_path):
    cases = {
        "short_header.zbc": b"ZOBC",
        "bad_payload.zbc": b"ZOBC\x00\x03\x00\x00\x00\x02{}",
        "bad_json.zbc": b"ZOBC\x00\x03\x00\x00\x00\x08not-json",
        "bad_instruction.zbc": b'ZOBC\x00\x03\x00\x00\x00\x33{"constants":[],"instructions":[[1,2,3]]}',
    }
    reader = ByteCodeReader()
    for name, data in cases.items():
        p = tmp_path / name
        p.write_bytes(data)
        try:
            reader.load(str(p))
        except ByteCodeError as exc:
            assert str(exc)
        else:
            raise AssertionError(f"corrupt file unexpectedly loaded: {name}")
