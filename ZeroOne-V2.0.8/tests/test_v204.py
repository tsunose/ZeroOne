import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from compiler.opcode import NATIVE_IDS
from vm.vm import ZeroOneVM, VMError

def run(src):
    code = Assembler().assemble(Generator().generate(Parser(Lexer(src).tokenize()).parse()))
    vm = ZeroOneVM(); vm.load(code); vm.run(); return vm

def test_for_continue_terminates():
    src = 'SET total = 0\nFOR SET i = 0; i < 5; SET i = i + 1\n    WHEN i == 2\n        CONTINUE\n    END\n    SET total = total + i\nEND\nEXIT\n'
    vm = run(src)
    assert vm.memory['total'] == 8

def test_nested_try_catch_preserves_outer_handler():
    src = 'SET result = ""\nTRY\n    SET result = "outer"\n    TRY\n        THROW "inner"\n    CATCH\n        SET result = result + "-inner"\n        THROW "rethrow"\n    END\nCATCH\n    SET result = result + "-outer"\nEND\nEXIT\n'
    vm = run(src)
    assert vm.memory['result'] == 'outer-inner-outer'

def test_nested_try_normal_flow_preserves_outer_handler():
    src = 'SET result = ""\nTRY\n    SET result = "outer"\n    TRY\n        SET result = result + "-inner"\n    FINALLY\n        SET result = result + "-finally"\n    END\n    THROW "outer-error"\nCATCH\n    SET result = result + "-caught"\nEND\nEXIT\n'
    vm = run(src)
    assert vm.memory['result'] == 'outer-inner-finally-caught'

def test_new_self_hosting_helpers():
    src = 'SET a = CHARAT("ZeroOne", 2)\nSET b = STR_INDEXOF("ZeroOne", "One")\nSET c = ISDIGIT("123")\nSET d = ISLETTER("A")\nSET e = ISSPACE(" ")\nSET f = ISALNUM("A9")\nSET g = ASCII("A")\nSET h = SOURCE_LINE("a\\nb\\nc", 2)\nSET p = PATH_NORMALIZE("a/../b")\nSET base = BASENAME("dir/test.zo")\nSET dir = DIRNAME("dir/test.zo")\nSET ext = EXTENSION("dir/test.zo")\nEXIT\n'
    vm = run(src)
    assert vm.memory['a'] == 'r'
    assert vm.memory['b'] == 4
    assert vm.memory['c'] is True
    assert vm.memory['d'] is True
    assert vm.memory['e'] is True
    assert vm.memory['f'] is True
    assert vm.memory['g'] == 65
    assert vm.memory['h'] == 'b'
    assert vm.memory['base'] == 'test.zo'
    assert vm.memory['dir'] == 'dir'
    assert vm.memory['ext'] == '.zo'

def test_pack_unpack_bytes(tmp_path):
    p = str(tmp_path / 'data.bin').replace('\\','/')
    src = 'SET data = PACK_INT(123456)\nWRITE_BYTES("' + p + '", data)\nSET raw = READ_BYTES("' + p + '")\nSET value = UNPACK_INT(raw)\nEXIT\n'
    vm = run(src)
    assert vm.memory['value'] == 123456
    assert len(vm.memory['raw']) == 4

def test_read_lines_and_file_lines(tmp_path):
    p = str(tmp_path / 'lines.txt').replace('\\','/')
    src = 'FILE_WRITE("' + p + '", "a\\nb\\nc")\nSET lines = READ_LINES("' + p + '")\nSET count = FILE_LINES("' + p + '")\nEXIT\n'
    vm = run(src)
    assert vm.memory['lines'] == ['a','b','c']
    assert vm.memory['count'] == 3

def test_error_at():
    try:
        run('ERROR_AT("bad token", 4, 7)\nEXIT\n')
    except VMError as e:
        assert 'line 4' in str(e) and 'column 7' in str(e)
    else:
        raise AssertionError('ERROR_AT did not raise VMError')

def test_new_native_ids_are_unique():
    names = ['CHARAT','STR_INDEXOF','ISDIGIT','ISLETTER','ISSPACE','ISALNUM','ASCII','SOURCE_LINE','ERROR_AT','WARNING','READ_BYTES','WRITE_BYTES','PACK_INT','UNPACK_INT','PATH_NORMALIZE','BASENAME','DIRNAME','EXTENSION','READ_LINES','FILE_LINES']
    assert all(name in NATIVE_IDS for name in names)
    assert len(NATIVE_IDS) == len(set(NATIVE_IDS.values()))
