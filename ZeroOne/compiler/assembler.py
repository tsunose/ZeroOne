"""Assembler for ZeroOne's intermediate bytecode."""

from compiler.errors import AssemblerError


class Assembler:
    def assemble(self, intermediate_code):
        if intermediate_code is None:
            raise AssemblerError("Intermediate code is empty.")

        code = []
        for instruction in intermediate_code:
            if isinstance(instruction, tuple):
                opcode, operand = instruction[0], instruction[1] if len(instruction) > 1 else None
            else:
                opcode, operand = instruction, None

            if operand is None:
                code.append((opcode,))
            else:
                code.append((opcode, operand))

        return code
