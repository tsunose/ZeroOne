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
from compiler.opcode import OpCode, NATIVE_NAMES


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

        self.locals_stack = []

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

        self.locals_stack.clear()

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
        if self.locals_stack:
            self.locals_stack[-1][name] = value
        else:
            self.memory[name] = value

    def store_local(self, name, value):
        if not self.locals_stack:
            self.locals_stack.append({})
        self.locals_stack[-1][name] = value

    def load_variable(self, name):
        for frame in reversed(self.locals_stack):
            if name in frame:
                return frame[name]
        if name not in self.memory:
            raise VMError(f"Undefined variable: {name}")
        return self.memory[name]

    def load_local(self, name):
        for frame in reversed(self.locals_stack):
            if name in frame:
                return frame[name]
        raise VMError(f"Undefined local variable: {name}")

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

    def native_call(self, name, args):
        """Execute a language built-in without exposing Python syntax to ZeroOne."""
        import os, sys, time, random, statistics, json, base64, hashlib, re, math
        from pathlib import Path

        a = args
        n = name.upper()
        if n == "ADD": return a[0] + a[1] if len(a) > 1 else a[0]
        if n == "SUB": return a[0] - a[1] if len(a) > 1 else a[0]
        if n == "MUL": return a[0] * a[1] if len(a) > 1 else a[0]
        if n == "DIV": return (a[0] / a[1] if not (isinstance(a[0], int) and isinstance(a[1], int)) else a[0] // a[1]) if len(a)>1 else a[0]
        if n == "MOD": return a[0] % a[1] if len(a)>1 else a[0]
        if n == "POWER": return a[0] ** a[1] if len(a)>1 else a[0]
        if n == "MAX": return max(a)
        if n == "MIN": return min(a)
        if n == "CLAMP": return max(a[1], min(a[0], a[2]))
        if n in {"ABS","SQRT","EXP","LN","LOG","LOG10","SIN","COS","TAN","ASIN","ACOS","ATAN","FLOOR","CEIL","ROUND","TRUNC","SIGN"}:
            f={"ABS":abs,"SQRT":math.sqrt,"EXP":math.exp,"LN":math.log,"LOG":math.log,"LOG10":math.log10,"SIN":math.sin,"COS":math.cos,"TAN":math.tan,"ASIN":math.asin,"ACOS":math.acos,"ATAN":math.atan,"FLOOR":math.floor,"CEIL":math.ceil,"ROUND":round,"TRUNC":math.trunc,"SIGN":lambda x:(x>0)-(x<0)}[n]; return f(a[0])
        if n == "FAC": return math.factorial(int(a[0]))
        if n in {"EQ","NE","LT","LE","GT","GE"}:
            if len(a) < 2: return False
            return {"EQ":a[0]==a[1],"NE":a[0]!=a[1],"LT":a[0]<a[1],"LE":a[0]<=a[1],"GT":a[0]>a[1],"GE":a[0]>=a[1]}[n]
        if n in {"AND","OR","XOR","NAND","NOR","XNOR"}:
            x,y=bool(a[0]),bool(a[1]); return {"AND":x and y,"OR":x or y,"XOR":x!=y,"NAND":not(x and y),"NOR":not(x or y),"XNOR":x==y}[n]
        if n == "NOT": return not a[0]
        if n in {"BITAND","BITOR","BITXOR","LSHIFT","RSHIFT","ARSHIFT"}: return {"BITAND":int(a[0])&int(a[1]),"BITOR":int(a[0])|int(a[1]),"BITXOR":int(a[0])^int(a[1]),"LSHIFT":int(a[0])<<int(a[1]),"RSHIFT":int(a[0])>>int(a[1]),"ARSHIFT":int(a[0])>>int(a[1])}[n]
        if n == "BITNOT": return ~int(a[0])
        if n == "STR" or n == "TEXT" or n == "TOSTRING": return str(a[0])
        if n == "CHAR": return chr(int(a[0]))
        if n in {"CONCAT","JOIN"}: return (str(a[0])+str(a[1])) if len(a)==2 else "".join(map(str,a))
        if n in {"LENGTH","SIZE"}: return len(a[0])
        if n == "UPPER": return str(a[0]).upper()
        if n == "LOWER": return str(a[0]).lower()
        if n == "TRIM": return str(a[0]).strip()
        if n == "REVERSE": return a[0][::-1]
        if n == "REPEAT": return str(a[0])*int(a[1] if len(a)>1 else 1)
        if n == "SPLIT": return str(a[0]).split(a[1] if len(a)>1 else " ")
        if n == "REPLACE": return str(a[0]).replace(str(a[1]),str(a[2]))
        if n == "STARTSWITH": return str(a[0]).startswith(str(a[1]))
        if n == "ENDSWITH": return str(a[0]).endswith(str(a[1]))
        if n == "CONTAINS": return a[1] in a[0]
        if n in {"STR_LEN","COUNTCHAR"}: return len(str(a[0]))
        if n in {"LIST","ARRAY"}: return list(a)
        if n == "PUSH": a[0].append(a[1]); return a[0]
        if n == "POP": return a[0].pop() if a[0] else None
        if n == "FIRST": return a[0][0] if a[0] else None
        if n == "LAST": return a[0][-1] if a[0] else None
        if n == "SORT": return sorted(a[0])
        if n == "UNIQUE": return list(dict.fromkeys(a[0]))
        if n == "INCLUDES": return a[1] in a[0]
        if n in {"INDEXOF","FINDINDEX"}: return (a[0].index(a[1]) if a[1] in a[0] else -1)
        if n in {"GETAT"}: return a[0][int(a[1])]
        if n == "SETAT": a[0][int(a[1])] = a[2]; return a[0]
        if n == "KEYS": return list(a[0].keys())
        if n == "VALUES": return list(a[0].values())
        if n == "ENTRIES": return list(a[0].items())
        if n in {"HAS","PROPERTY","PROP"}: return str(a[1]) in a[0] if isinstance(a[0],dict) else hasattr(a[0],str(a[1]))
        if n == "TYPE_OF" or n == "TYPEOF": return type(a[0]).__name__
        if n == "INT": return int(a[0])
        if n == "FLOAT": return float(a[0])
        if n == "BOOL": return self.is_truthy(a[0])
        if n == "NUMBER": return float(a[0]) if isinstance(a[0],str) and "." in a[0] else int(a[0])
        if n in {"STRINGIFY","JSON","STRINGIFY_JSON"}: return json.dumps(a[0], ensure_ascii=False)
        if n in {"PARSE","PARSE_JSON"}: return json.loads(str(a[0]))
        if n == "HASH": return hashlib.sha256(str(a[0]).encode()).hexdigest()
        if n == "MD5": return hashlib.md5(str(a[0]).encode()).hexdigest()
        if n in {"SHA","SHA256"}: return hashlib.sha256(str(a[0]).encode()).hexdigest()
        if n == "SHA1": return hashlib.sha1(str(a[0]).encode()).hexdigest()
        if n == "SHA512": return hashlib.sha512(str(a[0]).encode()).hexdigest()
        if n in {"BASE64","ENCODE64"}: return base64.b64encode(str(a[0]).encode()).decode()
        if n == "DECODE64": return base64.b64decode(str(a[0])).decode()
        if n == "HEX": return str(a[0]).encode().hex()
        if n == "INPUT": return input()
        if n == "RANDOM": return random.random()
        if n == "SLEEP": time.sleep(float(a[0])); return None
        if n == "TIME": return datetime.now().timestamp()
        if n == "TIMESTAMP": return datetime.now().timestamp()
        if n == "VERSION": return "0.3.0"
        if n == "SYSTEMOS": return os.name
        if n == "PLATFORM": return sys.platform
        if n == "ARCH": return __import__('platform').machine()
        if n == "ARGV": return sys.argv
        if n == "GETPID": return os.getpid()
        if n == "ENV": return os.environ.get(str(a[0]))
        if n == "FILE_EXISTS": return Path(a[0]).exists()
        if n == "FILE_SIZE": return Path(a[0]).stat().st_size
        if n == "FILE_READ": return Path(a[0]).read_text(encoding="utf-8")
        if n == "FILE_WRITE": Path(a[0]).write_text(str(a[1]),encoding="utf-8"); return True
        if n == "FILE_APPEND": Path(a[0]).open("a",encoding="utf-8").write(str(a[1])); return True
        if n == "DIR_LIST": return [p.name for p in Path(a[0]).iterdir()]
        if n == "DIR_EXISTS": return Path(a[0]).is_dir()
        if n == "PATH": return os.path.join(*map(str,a))
        if n == "REGEX": return re.compile(str(a[0]))
        if n == "MATCH": return re.search(str(a[0]),str(a[1])) is not None
        if n == "ASSERT":
            if not self.is_truthy(a[0]): raise VMError(str(a[1] if len(a)>1 else "Assertion failed"))
            return True
        if n in {"DEBUG","WARN","ERROR","DUMP"}: print(a[0] if a else "") ; return None
        return None

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

        if opcode == OpCode.STORE_LOCAL:
            self.store_local(operand, self.pop())
            self.ip += 1
            return

        if opcode == OpCode.LOAD_LOCAL:
            self.push(self.load_local(operand))
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

        if opcode == OpCode.CALL_NATIVE:
            argc = int(self.pop()) if self.stack else 0
            args = [self.pop() for _ in range(argc)][::-1]
            name = NATIVE_NAMES.get(int(operand))
            if name is None:
                raise VMError(f"Unknown native operation: {operand}")
            self.push(self.native_call(name, args))
            self.ip += 1
            return

        if opcode == OpCode.CALL:
            self.call_stack.append(self.ip + 1)
            self.locals_stack.append({})
            self.ip = operand
            return

        if opcode == OpCode.RETURN:
            if self.locals_stack:
                self.locals_stack.pop()
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
