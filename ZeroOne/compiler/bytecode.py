"""
ZeroOne Compiler

bytecode.py

Version 2.0.0
"""

import struct


class ByteCodeError(Exception):
    pass


class Instruction:

    def __init__(
        self,
        opcode,
        operand=0
    ):

        self.opcode = opcode
        self.operand = operand

    def to_tuple(self):

        return (
            self.opcode,
            self.operand
        )


class ByteCodeWriter:

    MAGIC = b"ZOBC"

    VERSION = 2

    def __init__(self):

        self.constants = []

        self.instructions = []

    # ==========================
    # Constant
    # ==========================

    def add_constant(
        self,
        value
    ):

        if value in self.constants:

            return self.constants.index(
                value
            )

        self.constants.append(
            value
        )

        return (
            len(self.constants) - 1
        )

    # ==========================
    # Instruction
    # ==========================

    def add_instruction(
        self,
        opcode,
        operand=0
    ):

        self.instructions.append(

            Instruction(
                opcode,
                operand
            )

        )

    # ==========================
    # Header
    # ==========================

    def write_header(
        self,
        file
    ):

        # MAGIC
        file.write(
            self.MAGIC
        )

        # VERSION
        file.write(
            struct.pack(
                ">H",
                self.VERSION
            )
        )

    # ==========================
    # Constant Table
    # ==========================

    def write_constants(
        self,
        file
    ):

        file.write(
            struct.pack(
                ">I",
                len(self.constants)
            )
        )

        for constant in self.constants:

            data = str(
                constant
            ).encode(
                "utf-8"
            )

            file.write(
                struct.pack(
                    ">I",
                    len(data)
                )
            )

            file.write(
                data
            )

    # ==========================
    # Instructions
    # ==========================

    def write_instructions(
        self,
        file
    ):

        file.write(
            struct.pack(
                ">I",
                len(self.instructions)
            )
        )

        for instruction in self.instructions:

            file.write(
                struct.pack(
                    ">H",
                    instruction.opcode
                )
            )

            file.write(
                struct.pack(
                    ">i",
                    instruction.operand
                )
            )

    # ==========================
    # Save
    # ==========================

    def save(
        self,
        filename
    ):

        with open(
            filename,
            "wb"
        ) as file:

            self.write_header(
                file
            )

            self.write_constants(
                file
            )

            self.write_instructions(
                file
            )


# =====================================
# Reader
# =====================================

class ByteCodeReader:

    MAGIC = b"ZOBC"

    VERSION = 2

    def __init__(self):

        self.constants = []

        self.instructions = []

    # ==========================
    # Load
    # ==========================

    def load(
        self,
        filename
    ):

        self.constants.clear()

        self.instructions.clear()

        with open(
            filename,
            "rb"
        ) as file:

            self.read_header(
                file
            )

            self.read_constants(
                file
            )

            self.read_instructions(
                file
            )

        return {

            "version": self.VERSION,

            "constants": self.constants,

            "instructions": self.instructions

        }

    # ==========================
    # Header
    # ==========================

    def read_header(
        self,
        file
    ):

        magic = file.read(4)

        if magic != self.MAGIC:

            raise ByteCodeError(
                "Invalid bytecode file."
            )

        version = struct.unpack(
            ">H",
            file.read(2)
        )[0]

        if version != self.VERSION:

            raise ByteCodeError(
                f"Unsupported bytecode version: {version}"
            )

    # ==========================
    # Constant Table
    # ==========================

    def read_constants(
        self,
        file
    ):

        count = struct.unpack(
            ">I",
            file.read(4)
        )[0]

        self.constants.clear()

        for _ in range(count):

            length = struct.unpack(
                ">I",
                file.read(4)
            )[0]

            value = file.read(
                length
            ).decode(
                "utf-8"
            )

            self.constants.append(
                value
            )

    # ==========================
    # Instructions
    # ==========================

    def read_instructions(
        self,
        file
    ):

        count = struct.unpack(
            ">I",
            file.read(4)
        )[0]

        self.instructions.clear()

        for _ in range(count):

            opcode = struct.unpack(
                ">H",
                file.read(2)
            )[0]

            operand = struct.unpack(
                ">i",
                file.read(4)
            )[0]

            self.instructions.append(
                (
                    opcode,
                    operand
                )
            )

    # ==========================
    # Debug
    # ==========================

    def disassemble(self):

        output = []

        for index, instruction in enumerate(
            self.instructions
        ):

            if isinstance(
                instruction,
                Instruction
            ):

                opcode = instruction.opcode
                operand = instruction.operand

            else:

                opcode = instruction[0]

                operand = (
                    instruction[1]
                    if len(instruction) > 1
                    else 0
                )

            output.append(
                (
                    index,
                    opcode,
                    operand
                )
            )

        return output

    def dump(self):

        print("========== ByteCode ==========")

        print(
            "Version :",
            self.VERSION
        )

        print(
            "Constants:",
            len(self.constants)
        )

        for index, value in enumerate(
            self.constants
        ):

            print(
                f"  [{index}] {value}"
            )

        print()

        print(
            "Instructions:",
            len(self.instructions)
        )

        for index, opcode, operand in self.disassemble():

            print(
                f"{index:04d}  "
                f"{opcode:03d}  "
                f"{operand}"
            )

        print("==============================")