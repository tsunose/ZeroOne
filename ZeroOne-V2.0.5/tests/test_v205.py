import io
from contextlib import redirect_stdout
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from vm.vm import ZeroOneVM

def run_source(source):
    ast = Parser(Lexer(source).tokenize()).parse()
    code = Assembler().assemble(Generator().generate(ast))
    vm = ZeroOneVM()
    vm.load(code)
    out = io.StringIO()
    with redirect_stdout(out):
        vm.run()
    return out.getvalue()

def test_v205_self_hosting_core():
    out = run_source(
        'OUT(LENGTH("hello"))\n'
        'OUT(CHAR_AT("hello", 1))\n'
        'OUT(ORD("A"))\n'
        'OUT(CHR(66))\n'
        'OUT(TO_INT("42"))\n'
        'OUT(PARSE_FLOAT("3.5"))\n'
    )
    assert out == "5e65B423.5"

def test_v205_struct_enum_and_keyword_properties():
    out = run_source(
        'ENUM TokenType\nEOF\nIDENTIFIER\nNUMBER\nEND\n'
        'STRUCT Token\ntype\nvalue\nline\nEND\n'
        'SET t = Token(TokenType.NUMBER, "hello", 7)\n'
        'SET t.type = "new"\n'
        'OUT(t.type)\nOUT(t.value)\nOUT(t.line)\nOUT(TokenType.NUMBER)\n'
    )
    assert out == "newhello72"

def test_v205_zeroone_lambdas_in_higher_order_functions():
    out = run_source(
        'SET even = LAMBDA (x) => x % 2 == 0\n'
        'SET double = LAMBDA (x) => x * 2\n'
        'SET add = LAMBDA (a, b) => a + b\n'
        'SET a = [1,2,3,4,5]\n'
        'OUT(FILTER(a, even))\n'
        'OUT(MAP(a, double))\n'
        'OUT(REDUCE(a, add, 0))\n'
    )
    assert out == "[2, 4][2, 4, 6, 8, 10]15"

def test_v205_pack_unpack():
    assert run_source(
        'SET b = PACK("<I", 16909060)\n'
        'SET x = UNPACK("<I", b)\n'
        'OUT(x[0])\n'
    ) == "16909060"

def test_v205_import_export(tmp_path):
    lib = tmp_path / "lib.zo"
    main = tmp_path / "main.zo"
    lib.write_text('FUNC twice(x)\n RETURN x * 2\nEND\nEXPORT twice\n', encoding="utf-8")
    main.write_text('IMPORT "lib.zo"\nOUT(twice(21))\n', encoding="utf-8")
    from zo import compile_file
    bc = compile_file(str(main))
    data = __import__("compiler.bytecode", fromlist=["ByteCodeReader"]).ByteCodeReader().load(bc)
    vm = ZeroOneVM(); vm.load(data["instructions"])
    out = io.StringIO()
    with redirect_stdout(out): vm.run()
    assert out.getvalue() == "42"
