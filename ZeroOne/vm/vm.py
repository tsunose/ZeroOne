"""
ZeroOne VM

vm.py

Version 3.0.0 - Extended Virtual Machine
"""

import math
import re
import hashlib
import base64
import json
from datetime import datetime
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

        self.loop_stack = []

        self.exception_handler = None

        self.running = False

    # ==========================
    # Reset
    # ==========================

    def reset(self):

        self.ip = 0

        self.stack.clear()

        self.memory.clear()

        self.call_stack.clear()

        self.loop_stack.clear()

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

    def is_truthy(self, value):
        """値のtruthiness判定"""

        if value is None or value is False:
            return False

        if value == 0 or value == "" or value == [] or value == {}:
            return False

        return True

    # ==========================
    # Stack
    # ==========================

    def push(self, value):

        self.stack.append(value)

    def pop(self):

        if not self.stack:

            raise VMError("Stack underflow.")

        return self.stack.pop()

    def peek(self):

        if not self.stack:

            raise VMError("Stack is empty.")

        return self.stack[-1]

    def dup(self):
        """スタックトップを複製"""

        if not self.stack:
            raise VMError("Stack is empty.")

        self.push(self.stack[-1])

    def swap(self):
        """スタックトップ2要素を交換"""

        if len(self.stack) < 2:
            raise VMError("Stack underflow.")

        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    # ==========================
    # Memory
    # ==========================

    def store(self, name, value):

        self.memory[name] = value

    def load_variable(self, name):

        if name not in self.memory:

            raise VMError(f"Undefined variable: {name}")

        return self.memory[name]

    # ==========================
    # Run
    # ==========================

    def run(self):

        self.running = True

        try:

            while self.running and self.ip < len(self.code):

                opcode, operand = self.fetch()

                if opcode is None:

                    break

                self.execute(opcode, operand)

        except Exception as e:

            if self.exception_handler:

                self.exception_handler(e)

            else:

                raise

    # ==========================
    # Execute
    # ==========================

    def execute(self, opcode, operand):

        # ============================================
        # STACK OPERATIONS (1-9)
        # ============================================

        if opcode == OpCode.PUSH:
            self.push(operand)
            self.ip += 1
            return

        if opcode == OpCode.POP:
            self.pop()
            self.ip += 1
            return

        if opcode == OpCode.DUP:
            self.dup()
            self.ip += 1
            return

        if opcode == OpCode.SWAP:
            self.swap()
            self.ip += 1
            return

        if opcode == OpCode.DEPTH:
            self.push(len(self.stack))
            self.ip += 1
            return

        if opcode == OpCode.CLEAR_STACK:
            self.stack.clear()
            self.ip += 1
            return

        # ============================================
        # MEMORY OPERATIONS (10-29)
        # ============================================

        if opcode == OpCode.STORE:
            value = self.pop()
            self.store(operand, value)
            self.ip += 1
            return

        if opcode == OpCode.LOAD:
            value = self.load_variable(operand)
            self.push(value)
            self.ip += 1
            return

        if opcode == OpCode.STORE_GLOBAL:
            value = self.pop()
            self.store(f"global_{operand}", value)
            self.ip += 1
            return

        if opcode == OpCode.LOAD_GLOBAL:
            value = self.load_variable(f"global_{operand}")
            self.push(value)
            self.ip += 1
            return

        # ============================================
        # ARITHMETIC OPERATIONS (30-59)
        # ============================================

        if opcode == OpCode.ADD:
            b = self.pop()
            a = self.pop()
            self.push(a + b)
            self.ip += 1
            return

        if opcode == OpCode.SUB:
            b = self.pop()
            a = self.pop()
            self.push(a - b)
            self.ip += 1
            return

        if opcode == OpCode.MUL:
            b = self.pop()
            a = self.pop()
            self.push(a * b)
            self.ip += 1
            return

        if opcode == OpCode.DIV:
            b = self.pop()
            a = self.pop()
            if b == 0:
                raise VMError("Division by zero.")
            self.push(a // b if isinstance(a, int) else a / b)
            self.ip += 1
            return

        if opcode == OpCode.MOD:
            b = self.pop()
            a = self.pop()
            if b == 0:
                raise VMError("Modulo by zero.")
            self.push(a % b)
            self.ip += 1
            return

        if opcode == OpCode.POWER:
            b = self.pop()
            a = self.pop()
            self.push(a ** b)
            self.ip += 1
            return

        if opcode == OpCode.NEG:
            value = self.pop()
            self.push(-value)
            self.ip += 1
            return

        if opcode == OpCode.ABS:
            value = self.pop()
            self.push(abs(value))
            self.ip += 1
            return

        if opcode == OpCode.SQRT:
            value = self.pop()
            self.push(math.sqrt(value))
            self.ip += 1
            return

        if opcode == OpCode.EXP:
            value = self.pop()
            self.push(math.exp(value))
            self.ip += 1
            return

        if opcode == OpCode.LN:
            value = self.pop()
            self.push(math.log(value))
            self.ip += 1
            return

        if opcode == OpCode.LOG:
            value = self.pop()
            self.push(math.log10(value))
            self.ip += 1
            return

        if opcode == OpCode.SIN:
            value = self.pop()
            self.push(math.sin(value))
            self.ip += 1
            return

        if opcode == OpCode.COS:
            value = self.pop()
            self.push(math.cos(value))
            self.ip += 1
            return

        if opcode == OpCode.TAN:
            value = self.pop()
            self.push(math.tan(value))
            self.ip += 1
            return

        if opcode == OpCode.FLOOR:
            value = self.pop()
            self.push(math.floor(value))
            self.ip += 1
            return

        if opcode == OpCode.CEIL:
            value = self.pop()
            self.push(math.ceil(value))
            self.ip += 1
            return

        if opcode == OpCode.ROUND:
            value = self.pop()
            self.push(round(value))
            self.ip += 1
            return

        if opcode == OpCode.MAX:
            b = self.pop()
            a = self.pop()
            self.push(max(a, b))
            self.ip += 1
            return

        if opcode == OpCode.MIN:
            b = self.pop()
            a = self.pop()
            self.push(min(a, b))
            self.ip += 1
            return

        # ============================================
        # COMPARISON (60-79)
        # ============================================

        if opcode in (OpCode.EQ, OpCode.NE, OpCode.LT, OpCode.LE, OpCode.GT, OpCode.GE):
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

        if opcode == OpCode.ISNULL:
            value = self.pop()
            self.push(value is None)
            self.ip += 1
            return

        if opcode == OpCode.ISNOTNULL:
            value = self.pop()
            self.push(value is not None)
            self.ip += 1
            return

        # ============================================
        # LOGICAL OPERATIONS (80-99)
        # ============================================

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
            self.push(not value)
            self.ip += 1
            return

        if opcode == OpCode.XOR:
            b = self.pop()
            a = self.pop()
            self.push(bool(a) != bool(b))
            self.ip += 1
            return

        # ============================================
        # BITWISE OPERATIONS (100-119)
        # ============================================

        if opcode == OpCode.BITAND:
            b = self.pop()
            a = self.pop()
            self.push(int(a) & int(b))
            self.ip += 1
            return

        if opcode == OpCode.BITOR:
            b = self.pop()
            a = self.pop()
            self.push(int(a) | int(b))
            self.ip += 1
            return

        if opcode == OpCode.BITXOR:
            b = self.pop()
            a = self.pop()
            self.push(int(a) ^ int(b))
            self.ip += 1
            return

        if opcode == OpCode.BITNOT:
            value = self.pop()
            self.push(~int(value))
            self.ip += 1
            return

        if opcode == OpCode.LSHIFT:
            b = self.pop()
            a = self.pop()
            self.push(int(a) << int(b))
            self.ip += 1
            return

        if opcode == OpCode.RSHIFT:
            b = self.pop()
            a = self.pop()
            self.push(int(a) >> int(b))
            self.ip += 1
            return

        # ============================================
        # STRING OPERATIONS (120-149)
        # ============================================

        if opcode == OpCode.STR_CONCAT:
            b = self.pop()
            a = self.pop()
            self.push(str(a) + str(b))
            self.ip += 1
            return

        if opcode == OpCode.STR_LEN:
            value = self.pop()
            self.push(len(str(value)))
            self.ip += 1
            return

        if opcode == OpCode.STR_UPPER:
            value = self.pop()
            self.push(str(value).upper())
            self.ip += 1
            return

        if opcode == OpCode.STR_LOWER:
            value = self.pop()
            self.push(str(value).lower())
            self.ip += 1
            return

        if opcode == OpCode.STR_REVERSE:
            value = self.pop()
            self.push(str(value)[::-1])
            self.ip += 1
            return

        if opcode == OpCode.STR_TRIM:
            value = self.pop()
            self.push(str(value).strip())
            self.ip += 1
            return

        if opcode == OpCode.CHAR_CODE:
            value = self.pop()
            self.push(ord(str(value)[0]) if value else 0)
            self.ip += 1
            return

        if opcode == OpCode.CODE_CHAR:
            value = self.pop()
            self.push(chr(int(value)))
            self.ip += 1
            return

        # ============================================
        # ARRAY OPERATIONS (150-189)
        # ============================================

        if opcode == OpCode.ARRAY_NEW:
            self.push([])
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_GET:
            index = self.pop()
            array = self.pop()
            self.push(array[int(index)])
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_SET:
            value = self.pop()
            index = self.pop()
            array = self.pop()
            array[int(index)] = value
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_PUSH:
            value = self.pop()
            array = self.pop()
            array.append(value)
            self.push(array)
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_POP:
            array = self.pop()
            value = array.pop() if array else None
            self.push(value)
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_LEN:
            array = self.pop()
            self.push(len(array))
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_REVERSE:
            array = self.pop()
            self.push(list(reversed(array)))
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_SORT:
            array = self.pop()
            self.push(sorted(array))
            self.ip += 1
            return

        if opcode == OpCode.ARRAY_SUM:
            array = self.pop()
            self.push(sum(array))
            self.ip += 1
            return

        # ============================================
        # MAP OPERATIONS (190-209)
        # ============================================

        if opcode == OpCode.MAP_NEW:
            self.push({})
            self.ip += 1
            return

        if opcode == OpCode.MAP_SET:
            value = self.pop()
            key = self.pop()
            map_obj = self.pop()
            map_obj[str(key)] = value
            self.push(map_obj)
            self.ip += 1
            return

        if opcode == OpCode.MAP_GET:
            key = self.pop()
            map_obj = self.pop()
            self.push(map_obj.get(str(key)))
            self.ip += 1
            return

        if opcode == OpCode.MAP_HAS:
            key = self.pop()
            map_obj = self.pop()
            self.push(str(key) in map_obj)
            self.ip += 1
            return

        if opcode == OpCode.MAP_KEYS:
            map_obj = self.pop()
            self.push(list(map_obj.keys()))
            self.ip += 1
            return

        if opcode == OpCode.MAP_VALUES:
            map_obj = self.pop()
            self.push(list(map_obj.values()))
            self.ip += 1
            return

        if opcode == OpCode.MAP_SIZE:
            map_obj = self.pop()
            self.push(len(map_obj))
            self.ip += 1
            return

        # ============================================
        # TYPE OPERATIONS (210-229)
        # ============================================

        if opcode == OpCode.TYPE_OF:
            value = self.pop()
            type_name = type(value).__name__
            self.push(type_name)
            self.ip += 1
            return

        if opcode == OpCode.CAST_INT:
            value = self.pop()
            self.push(int(value))
            self.ip += 1
            return

        if opcode == OpCode.CAST_FLOAT:
            value = self.pop()
            self.push(float(value))
            self.ip += 1
            return

        if opcode == OpCode.CAST_STR:
            value = self.pop()
            self.push(str(value))
            self.ip += 1
            return

        if opcode == OpCode.CAST_BOOL:
            value = self.pop()
            self.push(self.is_truthy(value))
            self.ip += 1
            return

        if opcode == OpCode.IS_INT:
            value = self.pop()
            self.push(isinstance(value, int))
            self.ip += 1
            return

        if opcode == OpCode.IS_STR:
            value = self.pop()
            self.push(isinstance(value, str))
            self.ip += 1
            return

        if opcode == OpCode.IS_ARRAY:
            value = self.pop()
            self.push(isinstance(value, list))
            self.ip += 1
            return

        if opcode == OpCode.IS_MAP:
            value = self.pop()
            self.push(isinstance(value, dict))
            self.ip += 1
            return

        # ============================================
        # CONTROL FLOW (230-259)
        # ============================================

        if opcode == OpCode.JMP:
            self.ip = operand
            return

        if opcode == OpCode.JMP_IF_TRUE:
            condition = self.pop()
            if self.is_truthy(condition):
                self.ip = operand
            else:
                self.ip += 1
            return

        if opcode == OpCode.JMP_IF_FALSE:
            condition = self.pop()
            if not self.is_truthy(condition):
                self.ip = operand
            else:
                self.ip += 1
            return

        if opcode == OpCode.JMP_IF_NULL:
            value = self.pop()
            if value is None:
                self.ip = operand
            else:
                self.ip += 1
            return

        if opcode == OpCode.LABEL:
            self.ip += 1
            return

        # ============================================
        # FUNCTION OPERATIONS (260-289)
        # ============================================

        if opcode == OpCode.CALL:
            self.call_stack.append(self.ip + 1)
            self.ip = operand
            return

        if opcode == OpCode.RETURN:
            if self.call_stack:
                self.ip = self.call_stack.pop()
            else:
                self.running = False
            return

        # ============================================
        # CLASS/OBJECT OPERATIONS (290-319)
        # ============================================

        if opcode == OpCode.GET_PROP:
            obj = self.pop()
            if isinstance(obj, dict):
                self.push(obj.get(operand))
            else:
                self.push(getattr(obj, operand, None))
            self.ip += 1
            return

        if opcode == OpCode.SET_PROP:
            value = self.pop()
            obj = self.pop()
            if isinstance(obj, dict):
                obj[operand] = value
            else:
                setattr(obj, operand, value)
            self.ip += 1
            return

        # ============================================
        # I/O OPERATIONS (320-349)
        # ============================================

        if opcode == OpCode.PRINT:
            value = self.pop()
            print(value, end="")
            self.ip += 1
            return

        if opcode == OpCode.PRINTLN:
            value = self.pop()
            print(value)
            self.ip += 1
            return

        # ============================================
        # HASH OPERATIONS (440-449)
        # ============================================

        if opcode == OpCode.MD5:
            value = self.pop()
            hash_obj = hashlib.md5(str(value).encode())
            self.push(hash_obj.hexdigest())
            self.ip += 1
            return

        if opcode == OpCode.SHA256:
            value = self.pop()
            hash_obj = hashlib.sha256(str(value).encode())
            self.push(hash_obj.hexdigest())
            self.ip += 1
            return

        if opcode == OpCode.BASE64_ENCODE:
            value = self.pop()
            encoded = base64.b64encode(str(value).encode()).decode()
            self.push(encoded)
            self.ip += 1
            return

        if opcode == OpCode.BASE64_DECODE:
            value = self.pop()
            decoded = base64.b64decode(value).decode()
            self.push(decoded)
            self.ip += 1
            return

        # ============================================
        # JSON OPERATIONS (450-459)
        # ============================================

        if opcode == OpCode.JSON_PARSE:
            value = self.pop()
            parsed = json.loads(str(value))
            self.push(parsed)
            self.ip += 1
            return

        if opcode == OpCode.JSON_STRINGIFY:
            value = self.pop()
            stringified = json.dumps(value)
            self.push(stringified)
            self.ip += 1
            return

        # ============================================
        # SYSTEM OPERATIONS (350-379)
        # ============================================

        if opcode == OpCode.TIME:
            self.push(datetime.now().timestamp())
            self.ip += 1
            return

        if opcode == OpCode.EXIT:
            self.running = False
            return

        # ============================================
        # EXCEPTION HANDLING
        # ============================================

        if opcode == OpCode.THROW:
            exception = self.pop()
            raise VMError(str(exception))

        # ============================================
        # MISC
        # ============================================

        if opcode == OpCode.NOP:
            self.ip += 1
            return

        # ============================================
        # Unknown Opcode
        # ============================================

        raise VMError(f"Unknown opcode: {OpCode.name(opcode)}")
