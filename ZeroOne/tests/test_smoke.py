import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import compile_source


def test_compile_hello_program():
    source = 'OUT "Hello"\nEXIT\n'
    tokens, ast, code = compile_source(source)
    assert tokens is not None
    assert ast is not None
    assert code is not None


def test_lowercase_aliases_are_accepted():
    source = 'print "Hello"\nset name "Ada"\nexit\n'
    tokens, ast, code = compile_source(source)
    assert tokens is not None
    assert ast is not None
    assert code is not None


def test_control_aliases_are_accepted():
    source = 'when true\nout "branch"\nend\nexit\n'
    tokens, ast, code = compile_source(source)
    assert tokens is not None
    assert ast is not None
    assert code is not None


def test_many_command_names_are_accepted():
    source = 'add 1\narray\ntext\nfile\nnet\nsystemos\nsecure\nloop\nexit\n'
    tokens, ast, code = compile_source(source)
    assert tokens is not None
    assert ast is not None
    assert code is not None
