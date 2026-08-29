"""
ZeroOne CLI

zo.py

Version 2.0.0
"""


import sys
import os


from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler

from compiler.bytecode import ByteCodeWriter
from compiler.bytecode import ByteCodeReader

from vm.vm import ZeroOneVM



# ==================================
# Utility
# ==================================


def file_exists(
    filename
):

    return os.path.exists(
        filename
    )



def read_source(
    filename
):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()



def change_extension(
    filename,
    ext
):

    base = os.path.splitext(
        filename
    )[0]

    return base + ext

# ==================================
# Compile
# ==================================


def compile_file(
    filename
):

    if not filename.endswith(
        ".zo"
    ):

        print(
            "Only .zo file is allowed."
        )

        return



    if not file_exists(
        filename
    ):

        print(
            "File not found:",
            filename
        )

        return



    print(
        "Compiling:",
        filename
    )



    # ----------------------
    # Read Source
    # ----------------------

    source = read_source(
        filename
    )



    # ----------------------
    # Lexer
    # ----------------------

    lexer = Lexer(
        source
    )

    tokens = lexer.tokenize()



    # ----------------------
    # Parser
    # ----------------------

    parser = Parser(
        tokens
    )

    ast = parser.parse()



    # ----------------------
    # Generator
    # ----------------------

    generator = Generator()

    code = generator.generate(
        ast
    )



    # ----------------------
    # Assembler
    # ----------------------

    assembler = Assembler()

    bytecode = assembler.assemble(
        code
    )

    # ----------------------
    # ByteCode Writer
    # ----------------------

    writer = ByteCodeWriter()


    for instruction in bytecode:

        opcode = instruction[0]

        operand = 0


        if len(instruction) > 1:

            operand = instruction[1]


        writer.add_instruction(
            opcode,
            operand
        )



    # ----------------------
    # Save
    # ----------------------

    output = change_extension(
        filename,
        ".zbc"
    )


    writer.save(
        output
    )


    print(
        "Created:",
        output
    )

# ==================================
# Run
# ==================================


def run_file(
    filename
):


    if not filename.endswith(
        ".zbc"
    ):

        print(
            "Only .zbc file is allowed."
        )

        return



    if not file_exists(
        filename
    ):

        print(
            "File not found:",
            filename
        )

        return



    print(
        "Running:",
        filename
    )



    # ----------------------
    # ByteCode Reader
    # ----------------------

    reader = ByteCodeReader()


    data = reader.load(
        filename
    )



    code = data[
        "instructions"
    ]



    constants = data.get(
        "constants",
        []
    )



    # ----------------------
    # VM
    # ----------------------

    vm = ZeroOneVM()


    vm.load(
        code,
        constants
    )


    vm.run()

# ==================================
# Help
# ==================================


def show_help():

    print(
"""
ZeroOne Compiler

Version 2.0.0


Usage:


  python zo.py compile <file.zo>


  python zo.py run <file.zbc>



Example:


  python zo.py compile hello.zo


  python zo.py run hello.zbc

"""
    )





# ==================================
# Main
# ==================================


def main():


    args = sys.argv



    if len(args) < 2:

        show_help()

        return



    command = args[1]



    # ----------------------
    # Compile
    # ----------------------

    if command == "compile":


        if len(args) < 3:

            show_help()

            return


        compile_file(
            args[2]
        )



    # ----------------------
    # Run
    # ----------------------

    elif command == "run":


        if len(args) < 3:

            show_help()

            return


        run_file(
            args[2]
        )



    else:


        show_help()





# ==================================
# Entry
# ==================================


if __name__ == "__main__":

    main()