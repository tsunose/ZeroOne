import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from compiler.opcode import NATIVE_IDS
from vm.vm import ZeroOneVM

def run(src):
    code=Assembler().assemble(Generator().generate(Parser(Lexer(src).tokenize()).parse()))
    vm=ZeroOneVM(); vm.load(code); vm.run(); return vm

def test_math_string_array_map_types():
    vm=run('SET a = ADD(2,3)\nSET s = UPPER("ok")\nSET x = [1,2,3]\nSET m = {name:"ZeroOne"}\nSET n = m["name"]\nEXIT\n')
    assert vm.memory["a"] == 5
    assert vm.memory["s"] == "OK"
    assert vm.memory["x"] == [1,2,3]
    assert vm.memory["n"] == "ZeroOne"

def test_control_and_functions():
    vm=run('FUNC sum2(a,b)\nRETURN a+b\nEND\nSET x = sum2(4,5)\nWHEN x == 9\nSET ok = TRUE\nELSE\nSET ok = FALSE\nEND\nEXIT\n')
    assert vm.memory["x"] == 9 and vm.memory["ok"] is True

def test_files_and_json(tmp_path):
    p=str(tmp_path/"x.txt").replace("\\","/")
    src=f'SET p = "{p}"\nFILE_WRITE(p, "hello")\nSET x = FILE_READ(p)\nSET j = STRINGIFY_JSON({{a:1}})\nSET o = PARSE_JSON(j)\nEXIT\n'
    vm=run(src)
    assert vm.memory["x"]=="hello" and vm.memory["o"]["a"]==1

def test_all_declared_natives_are_registered():
    assert len(NATIVE_IDS) >= 190
    assert len(NATIVE_IDS) == len(set(NATIVE_IDS.values()))
