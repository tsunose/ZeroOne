"""Assembler for ZeroOne intermediate bytecode."""

from compiler.errors import AssemblerError
from compiler.opcode import OpCode


class Assembler:
    def assemble(self, intermediate_code):
        if intermediate_code is None:
            raise AssemblerError("Intermediate code is empty.")
        code = []
        labels = {}
        # First pass: labels point at executable instruction indices.
        for instruction in intermediate_code:
            if isinstance(instruction, tuple):
                opcode = instruction[0]
                operand = instruction[1] if len(instruction) > 1 else None
            else:
                opcode, operand = instruction, None
            if opcode == OpCode.LABEL:
                labels[str(operand)] = len(code)
            else:
                code.append((opcode,) if operand is None else (opcode, operand))
        # Second pass: resolve control-flow/function labels only.
        jump_ops = {OpCode.JMP, OpCode.JMP_IF_TRUE, OpCode.JMP_IF_FALSE, OpCode.JMP_IF_NULL, OpCode.JMP_IF_NOTNULL, OpCode.CALL, OpCode.TRY, OpCode.JMP_IF_ITER_END}
        resolved = []
        for inst in code:
            if len(inst) > 1 and inst[0] in jump_ops and isinstance(inst[1], str):
                if inst[1] not in labels:
                    raise AssemblerError(f"Unknown label: {inst[1]}")
                resolved.append((inst[0], labels[inst[1]]))
            elif len(inst) > 1 and inst[0] == OpCode.CLOSURE and isinstance(inst[1], dict):
                spec = dict(inst[1])
                target = spec.get("target")
                if target not in labels:
                    raise AssemblerError(f"Unknown label: {target}")
                spec["target"] = labels[target]
                resolved.append((inst[0], spec))
            else:
                resolved.append(inst)
        return resolved
