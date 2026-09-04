"""ZeroOne compatibility/development entry point - V2.0.9."""
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from vm.vm import ZeroOneVM
from zo import main as cli_main


def compile_source(source):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    code = Assembler().assemble(Generator().generate(ast))
    return tokens, ast, code


def execute(code):
    vm = ZeroOneVM()
    vm.load(code)
    vm.run()
    return vm


def main(argv=None):
    # Keep main.py as a compatibility wrapper. The supported CLI lives in zo.py.
    return cli_main(argv)


if __name__ == "__main__":
    main()
