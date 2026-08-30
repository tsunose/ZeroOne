"""
ZeroOne Compiler

bytecode.py

Version 2.0.3
"""

import struct
import json


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

    VERSION = 3

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

    def add_constant(self, value):
        if value in self.constants:
            return self.constants.index(value)
        self.constants.append(value)
        return len(self.constants) - 1

    def add_instruction(self, opcode, operand=0):
        self.instructions.append(Instruction(opcode, operand))

    def write_header(self, file):
        file.write(self.MAGIC)
        file.write(struct.pack(">H", self.VERSION))

    def save(self, filename):
        payload = {
            "constants": self.constants,
            "instructions": [[i.opcode, i.operand] for i in self.instructions]
        }
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with open(filename, "wb") as file:
            self.write_header(file)
            file.write(struct.pack(">I", len(raw)))
            file.write(raw)


# =====================================
# Reader
# =====================================

class ByteCodeReader:
    MAGIC = b"ZOBC"
    VERSION = 3

    def __init__(self):
        self.constants = []
        self.instructions = []

    def load(self, filename):
        with open(filename, "rb") as file:
            magic = file.read(4)
            if magic != self.MAGIC:
                raise ByteCodeError("Invalid bytecode file.")
            version = struct.unpack(">H", file.read(2))[0]
            if version != self.VERSION:
                raise ByteCodeError(f"Unsupported bytecode version: {version}")
            size_raw = file.read(4)
            if len(size_raw) != 4:
                raise ByteCodeError("Truncated bytecode file.")
            size = struct.unpack(">I", size_raw)[0]
            payload = json.loads(file.read(size).decode("utf-8"))
        self.constants = payload.get("constants", [])
        self.instructions = [tuple(x) for x in payload.get("instructions", [])]
        return {"version": version, "constants": self.constants, "instructions": self.instructions}

