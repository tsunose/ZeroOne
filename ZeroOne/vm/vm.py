"""
ZeroOne VM

vm.py

Version 2.0.0
"""

from compiler.opcode import OpCode


class VMError(Exception):
    pass


class ZeroOneVM:

    def __init__(self):

        self.code = []

        self.constants = []

        self.ip = 0

        self.stack = []

        self.memory = {}

        self.call_stack = []

        self.running = False

    # ==========================
    # Reset
    # ==========================

    def reset(self):

        self.ip = 0

        self.stack.clear()

        self.memory.clear()

        self.call_stack.clear()

        self.running = False

    # ==========================
    # Load
    # ==========================

    def load(
        self,
        code,
        constants=None
    ):

        self.reset()

        self.code = code

        if constants is None:

            self.constants = []

        else:

            self.constants = list(constants)

    # ==========================
    # Utility
    # ==========================

    def current_instruction(self):

        if self.ip >= len(self.code):

            return None

        return self.code[self.ip]

    def fetch(self):

        instruction = self.current_instruction()

        if instruction is None:

            return None, None

        if len(instruction) == 1:

            return instruction[0], None

        return instruction[0], instruction[1]

    # ==========================
    # Stack
    # ==========================

    def push(
        self,
        value
    ):

        self.stack.append(
            value
        )

    def pop(self):

        if not self.stack:

            raise VMError(
                "Stack underflow."
            )

        return self.stack.pop()

    def peek(self):

        if not self.stack:

            raise VMError(
                "Stack is empty."
            )

        return self.stack[-1]

    # ==========================
    # Memory
    # ==========================

    def store(
        self,
        name,
        value
    ):

        self.memory[name] = value

    def load_variable(
        self,
        name
    ):

        if name not in self.memory:

            raise VMError(
                f"Undefined variable: {name}"
            )

        return self.memory[name]

    # ==========================
    # Run
    # ==========================

    def run(self):

        self.running = True

        while self.running:

            opcode, operand = self.fetch()

            if opcode is None:

                break

            self.execute(
                opcode,
                operand
            )

    # ==========================
    # Execute
    # ==========================

    def execute(
        self,
        opcode,
        operand
    ):

        # ----------------------
        # Stack
        # ----------------------

        if opcode == OpCode.PUSH:

            self.push(
                operand
            )

            self.ip += 1

            return

        if opcode == OpCode.POP:

            self.pop()

            self.ip += 1

            return

        # ----------------------
        # Memory
        # ----------------------

        if opcode == OpCode.STORE:

            value = self.pop()

            self.store(
                operand,
                value
            )

            self.ip += 1

            return

        if opcode == OpCode.LOAD:

            value = self.load_variable(
                operand
            )

            self.push(
                value
            )

            self.ip += 1

            return

        # ----------------------
        # Arithmetic
        # ----------------------

        if opcode in (
            OpCode.ADD,
            OpCode.SUB,
            OpCode.MUL,
            OpCode.DIV,
            OpCode.MOD
        ):

            b = self.pop()
            a = self.pop()

            if opcode == OpCode.ADD:

                self.push(a + b)

            elif opcode == OpCode.SUB:

                self.push(a - b)

            elif opcode == OpCode.MUL:

                self.push(a * b)

            elif opcode == OpCode.DIV:

                if b == 0:

                    raise VMError(
                        "Division by zero."
                    )

                self.push(a // b)

            elif opcode == OpCode.MOD:

                if b == 0:

                    raise VMError(
                        "Modulo by zero."
                    )

                self.push(a % b)

            self.ip += 1

            return

        # ----------------------
        # Compare
        # ----------------------

        if opcode in (
            OpCode.EQ,
            OpCode.NE,
            OpCode.LT,
            OpCode.LE,
            OpCode.GT,
            OpCode.GE
        ):

            b = self.pop()
            a = self.pop()

            if opcode == OpCode.EQ:

                self.push(a == b)

            elif opcode == OpCode.NE:

                self.push(a != b)

            elif opcode == OpCode.LT:

                self.push(a < b)

            elif opcode == OpCode.LE:

                self.push(a <= b)

            elif opcode == OpCode.GT:

                self.push(a > b)

            elif opcode == OpCode.GE:

                self.push(a >= b)

            self.ip += 1

            return

        # ----------------------
        # Logic
        # ----------------------

        if opcode == OpCode.AND:

            b = self.pop()
            a = self.pop()

            self.push(bool(a and b))

            self.ip += 1

            return

        if opcode == OpCode.OR:

            b = self.pop()
            a = self.pop()

            self.push(bool(a or b))

            self.ip += 1

            return

        if opcode == OpCode.NOT:

            value = self.pop()

            self.push(
                not value
            )

            self.ip += 1

            return

        # ----------------------
        # Jump
        # ----------------------

        if opcode == OpCode.JMP:

            self.ip = operand

            return

        if opcode == OpCode.JMP_IF_FALSE:

            condition = self.pop()

            if not condition:

                self.ip = operand

            else:

                self.ip += 1

            return

        if opcode == OpCode.JMP_IF_TRUE:

            condition = self.pop()

            if condition:

                self.ip = operand

            else:

                self.ip += 1

            return

        # ----------------------
        # Function
        # ----------------------

        if opcode == OpCode.CALL:

            self.call_stack.append(
                self.ip + 1
            )

            self.ip = operand

            return

        if opcode == OpCode.RETURN:

            if self.call_stack:

                self.ip = self.call_stack.pop()

            else:

                self.running = False

            return

        # ----------------------
        # Output
        # ----------------------

        if opcode == OpCode.PRINT:

            value = self.pop()

            print(value)

            self.ip += 1

            return

        # ----------------------
        # Exit
        # ----------------------

        if opcode == OpCode.EXIT:

            self.running = False

            return

        # ----------------------
        # Output
        # ----------------------

        if opcode == OpCode.PRINT:
            value = self.pop()
            print(value)
            self.ip += 1
            return

        # ----------------------
        # Exit
        # ----------------------

        if opcode == OpCode.EXIT:
            self.running = False
            return

        # ----------------------
        # Unknown Opcode
        # ----------------------

        raise VMError(
            f"Unknown opcode: {opcode}"
        )