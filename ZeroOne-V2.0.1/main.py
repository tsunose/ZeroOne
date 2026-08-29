
"""
ZeroOne Compiler
main.py
Version 0.2.0
"""

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.vm import VirtualMachine
from compiler.assembler import Assembler


SOURCE_FILE = "sample.zo"


def read_source(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def print_tokens(tokens):

    print("========== TOKENS ==========")

    for token in tokens:

        print(token)

    print()


def print_ast(ast):

    print("=========== AST ===========")

    print(ast)

    print()


def print_code(code):

    print("========= BYTECODE =========")

    for i, instruction in enumerate(code):

        print(f"{i:04} : {instruction}")

    print()


def compile_source(source):

    lexer = Lexer(source)

    tokens = lexer.tokenize()

    parser = Parser(tokens)

    ast = parser.parse()

    generator = Generator()

    intermediate_code = generator.generate(ast)

    assembler = Assembler()

    code = assembler.assemble(intermediate_code)

    return tokens, ast, code


def execute(code):

    vm = VirtualMachine()

    vm.load(code)

    vm.execute()


def main():

    print("===================================")
    print(" ZeroOne Compiler Version 0.2.0")
    print("===================================")

    try:

        source = read_source(
            SOURCE_FILE
        )

        tokens, ast, code = compile_source(
            source
        )

        print_tokens(tokens)

        print_ast(ast)

        print_code(code)

        print("========== OUTPUT ==========")

        execute(code)

        print()

        print("Compile Success.")

    except Exception as e:

        print()

        print("Compile Failed")

        print(type(e).__name__)

        print(e)




if __name__ == "__main__":

    main()