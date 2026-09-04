"""
ZeroOne Compiler

bytecode.py

Version 2.0.4
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
        try:
            with open(filename, "rb") as file:
                magic = file.read(4)
                if magic != self.MAGIC:
                    raise ByteCodeError("Invalid bytecode file.")

                version_raw = file.read(2)
                if len(version_raw) != 2:
                    raise ByteCodeError("Truncated bytecode file: missing version.")
                version = struct.unpack(">H", version_raw)[0]
                if version != self.VERSION:
                    raise ByteCodeError(f"Unsupported bytecode version: {version}")

                size_raw = file.read(4)
                if len(size_raw) != 4:
                    raise ByteCodeError("Truncated bytecode file: missing payload size.")
                size = struct.unpack(">I", size_raw)[0]

                raw = file.read(size)
                if len(raw) != size:
                    raise ByteCodeError("Truncated bytecode file: incomplete payload.")
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise ByteCodeError(f"Invalid bytecode payload: {exc}") from None

                if not isinstance(payload, dict):
                    raise ByteCodeError("Invalid bytecode payload: expected an object.")
                if "constants" not in payload or "instructions" not in payload:
                    raise ByteCodeError("Invalid bytecode payload: missing constants or instructions.")
                constants = payload.get("constants")
                instructions = payload.get("instructions")
                if not isinstance(constants, list) or not isinstance(instructions, list):
                    raise ByteCodeError("Invalid bytecode payload: malformed tables.")
                normalized = []
                for i, item in enumerate(instructions):
                    if not isinstance(item, (list, tuple)) or len(item) not in (1, 2):
                        raise ByteCodeError(f"Invalid instruction at index {i}.")
                    normalized.append(tuple(item))
        except ByteCodeError:
            raise
        except OSError as exc:
            raise ByteCodeError(f"Cannot read bytecode file: {exc}") from None
        except (TypeError, ValueError, OverflowError) as exc:
            raise ByteCodeError(f"Invalid bytecode file: {exc}") from None

        self.constants = constants
        self.instructions = normalized
        return {"version": version, "constants": self.constants, "instructions": self.instructions}

