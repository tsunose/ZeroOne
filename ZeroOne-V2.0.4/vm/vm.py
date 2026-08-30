"""
ZeroOne VM

vm.py

Version 2.0.4 - Extended Virtual Machine
"""

import math
import re
import hashlib
import base64
import json
import os
import sys
import platform
import subprocess
import time
import random
from pathlib import Path
from datetime import datetime, date, timezone
from compiler.opcode import OpCode, NATIVE_NAMES


class VMError(Exception):
    pass


class _IteratorEnd:
    """Private sentinel distinct from a user-visible ZeroOne NULL."""
    pass


ITERATOR_END = _IteratorEnd()


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
        self.iterator_stack = []

        self.exception_handler = None
        self.exception_handlers = []
        self.pending_exception = None

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
        self.iterator_stack.clear()
        self.exception_handler = None
        self.exception_handlers.clear()
        self.pending_exception = None

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

        while self.running and self.ip < len(self.code):

            opcode, operand = self.fetch()

            if opcode is None:
                break

            try:
                self.execute(opcode, operand)
            except Exception as e:
                if self.exception_handlers:
                    target = self.exception_handlers.pop()
                    self.exception_handler = (
                        self.exception_handlers[-1]
                        if self.exception_handlers else None
                    )
                    self.pending_exception = e
                    self.stack.clear()
                    self.ip = target
                elif self.exception_handler is not None:
                    target = self.exception_handler
                    self.exception_handler = None
                    self.pending_exception = e
                    self.stack.clear()
                    self.ip = target
                else:
                    raise

    def native_call(self, name, args):
        """ZeroOne standard library.

        The VM owns the runtime implementation so the ZeroOne language does
        not need to expose Python syntax.  Every public native name declared in
        compiler.opcode has a deterministic implementation or a safe feature
        descriptor.
        """
        import os
        import sys
        import time
        import random
        import statistics
        import json
        import base64
        import hashlib
        import re
        import math
        import platform
        import subprocess
        from datetime import datetime, date, timezone
        from pathlib import Path

        n = str(name).upper()
        a = list(args)
        get = lambda i, default=None: a[i] if i < len(a) else default

        # ----- math -----
        if n in {"ADD", "SUB", "MUL", "DIV", "MOD", "POWER"}:
            x, y = get(0), get(1)
            if n == "ADD": return x + y
            if n == "SUB": return x - y
            if n == "MUL": return x * y
            if n == "DIV": return x / y
            if n == "MOD": return x % y
            return x ** y
        if n in {"MAX", "MIN"}:
            return (max if n == "MAX" else min)(a)
        if n == "CLAMP":
            x, lo, hi = get(0), get(1), get(2)
            return max(lo, min(x, hi))
        unary = {
            "ABS": abs, "SQRT": math.sqrt, "EXP": math.exp,
            "LN": math.log, "LOG": math.log, "LOG10": math.log10,
            "SIN": math.sin, "COS": math.cos, "TAN": math.tan,
            "ASIN": math.asin, "ACOS": math.acos, "ATAN": math.atan,
            "FLOOR": math.floor, "CEIL": math.ceil, "ROUND": round,
            "TRUNC": math.trunc, "FAC": lambda x: math.factorial(int(x)),
            "SIGN": lambda x: (x > 0) - (x < 0),
        }
        if n in unary: return unary[n](get(0, 0))
        if n == "RANDOM": return random.random()
        if n == "SEED": random.seed(get(0)); return None

        # ----- comparison / logic / bitwise -----
        if n in {"EQ","NE","LT","LE","GT","GE"}:
            x,y=get(0),get(1)
            return {"EQ":x==y,"NE":x!=y,"LT":x<y,"LE":x<=y,"GT":x>y,"GE":x>=y}[n]
        if n in {"AND","OR","XOR","NAND","NOR","XNOR"}:
            x,y=bool(get(0)),bool(get(1))
            return {"AND":x and y,"OR":x or y,"XOR":x!=y,"NAND":not(x and y),"NOR":not(x or y),"XNOR":x==y}[n]
        if n == "NOT": return not bool(get(0))
        if n in {"BITAND","BITOR","BITXOR","LSHIFT","RSHIFT","ARSHIFT"}:
            x,y=int(get(0,0)),int(get(1,0))
            return {"BITAND":x&y,"BITOR":x|y,"BITXOR":x^y,"LSHIFT":x<<y,"RSHIFT":x>>y,"ARSHIFT":x>>y}[n]
        if n == "BITNOT": return ~int(get(0,0))
        if n == "ROTL":
            x,y=int(get(0,0)),int(get(1,0)) & 63; return ((x << y) | ((x & ((1<<y)-1)) >> (64-y))) if y else x
        if n == "ROTR":
            x,y=int(get(0,0)),int(get(1,0)) & 63; return ((x >> y) | (x << (64-y))) if y else x
        if n == "POPCOUNT": return int(get(0,0)).bit_count()

        # ----- strings -----
        if n in {"STR","TEXT","TOSTRING"}: return str(get(0,""))
        if n == "CHAR": return chr(int(get(0,0)))
        if n in {"CONCAT","JOIN"}: return "".join(map(str,a))
        if n in {"CUT","SUBSTR"}:
            s0=str(get(0,"")); start=int(get(1,0)); end=get(2,None); return s0[start:] if end is None else s0[start:int(end)]
        if n == "SLICE":
            x=get(0,""); start=get(1,None); end=get(2,None); return x[None if start is None else int(start):None if end is None else int(end)]
        if n == "REPLACE": return str(get(0,"")).replace(str(get(1,"")), str(get(2,"")))
        if n == "UPPER": return str(get(0,"")).upper()
        if n == "LOWER": return str(get(0,"")).lower()
        if n == "TRIM": return str(get(0,"")).strip()
        if n == "SPACE": return " " * int(get(0,0))
        if n in {"LENGTH","SIZE","COUNTCHAR"}:
            value=str(get(0,"")) if n=="COUNTCHAR" else get(0,[]); return len(value) if n!="COUNTCHAR" or len(a)<2 else str(value).count(str(get(1,"")))
        if n == "STARTSWITH": return str(get(0,"")).startswith(str(get(1,"")))
        if n == "ENDSWITH": return str(get(0,"")).endswith(str(get(1,"")))
        if n == "CONTAINS": return get(1) in get(0)
        if n == "REVERSE": return get(0)[::-1]
        if n == "REPEAT": return str(get(0,"")) * int(get(1,1))
        if n == "SPLIT": return str(get(0,"")).split(str(get(1," ")))
        if n in {"FINDSTR","MATCHSTR"}: return str(get(1,"")) in str(get(0,""))
        if n == "FORMAT": return str(get(0,"" )).format(*a[1:])
        if n == "ENCODE": return base64.b64encode(str(get(0,"")).encode()).decode()
        if n == "DECODE": return base64.b64decode(str(get(0,""))).decode()

        # ----- arrays -----
        if n in {"LIST","ARRAY"}: return list(a)
        if n == "PUSH": arr=get(0,[]); arr.append(get(1)); return arr
        if n == "POP": arr=get(0,[]); return arr.pop() if arr else None
        if n == "INSERT": arr=get(0,[]); arr.insert(int(get(1,0)),get(2)); return arr
        if n == "DELETEAT": arr=get(0,[]); idx=int(get(1,0)); return arr.pop(idx)
        if n == "GETAT": return get(0,[])[int(get(1,0))]
        if n == "SETAT": arr=get(0,[]); arr[int(get(1,0))]=get(2); return arr
        if n == "FIRST": arr=get(0,[]); return arr[0] if arr else None
        if n == "LAST": arr=get(0,[]); return arr[-1] if arr else None
        if n == "SHIFT": arr=get(0,[]); return arr.pop(0) if arr else None
        if n == "UNSHIFT": arr=get(0,[]); arr.insert(0,get(1)); return arr
        if n == "SORT": return sorted(get(0,[]))
        if n == "UNIQUE": return list(dict.fromkeys(get(0,[])))
        if n in {"INCLUDES"}: return get(1) in get(0,[])
        if n in {"INDEXOF","FINDINDEX","FIND"}:
            try: return get(0,[]).index(get(1))
            except ValueError: return -1
        if n == "SPLICE":
            arr=get(0,[]); i=int(get(1,0)); count=int(get(2,0)); removed=arr[i:i+count]; del arr[i:i+count]; return removed
        if n == "FILL":
            arr=get(0,[]); start=int(get(2,0) or 0); end=int(get(3,len(arr)) if len(a)>3 else len(arr)); arr[start:end]=[get(1)]*(end-start); return arr
        if n in {"FLAT","FLATTEN"}:
            def flat(x):
                out=[]
                for v in x: out.extend(flat(v) if isinstance(v,list) else [v])
                return out
            return flat(get(0,[]))
        if n == "MERGE":
            out=[]
            for v in a:
                out.extend(v if isinstance(v,list) else [v])
            return out
        if n in {"FILTER","MAP","REDUCE"}:
            seq=get(0,[]); fn=get(1)
            if not callable(fn): return seq
            if n=="FILTER": return [x for x in seq if fn(x)]
            if n=="MAP": return [fn(x) for x in seq]
            return __import__('functools').reduce(fn,seq,get(2,None))
        if n == "COPY":
            import copy; return copy.deepcopy(get(0))

        # ----- V2.0.4 self-hosting helpers -----
        if n == "CHARAT":
            s = str(get(0, ""))
            i = int(get(1, 0))
            if i < 0 or i >= len(s):
                raise VMError(f"CHARAT index out of range: {i}")
            return s[i]
        if n == "STR_INDEXOF":
            return str(get(0, "")).find(str(get(1, "")))
        if n == "ISDIGIT": return str(get(0, "")) != "" and str(get(0, "")).isdigit()
        if n == "ISLETTER": return str(get(0, "")) != "" and str(get(0, "")).isalpha()
        if n == "ISSPACE": return str(get(0, "")) != "" and str(get(0, "")).isspace()
        if n == "ISALNUM": return str(get(0, "")) != "" and str(get(0, "")).isalnum()
        if n == "ASCII":
            s = str(get(0, ""))
            if len(s) != 1:
                raise VMError("ASCII expects exactly one character.")
            return ord(s)
        if n == "SOURCE_LINE":
            source = str(get(0, ""))
            line = int(get(1, 1))
            lines = source.splitlines()
            if line < 1 or line > len(lines):
                return None
            return lines[line - 1]
        if n == "ERROR_AT":
            message = str(get(0, "Error"))
            line = get(1, None)
            column = get(2, None)
            if line is not None and column is not None:
                raise VMError(f"{message} (line {line}, column {column})")
            if line is not None:
                raise VMError(f"{message} (line {line})")
            raise VMError(message)
        if n == "WARNING":
            print(f"Warning: {get(0, '')}", file=sys.stderr)
            return True
        if n == "READ_BYTES":
            return list(Path(str(get(0))).read_bytes())
        if n == "WRITE_BYTES":
            data = get(1, [])
            if isinstance(data, str):
                data = data.encode()
            Path(str(get(0))).write_bytes(bytes(int(x) & 255 for x in data))
            return True
        if n == "PACK_INT":
            import struct
            return list(struct.pack("<i", int(get(0, 0))))
        if n == "UNPACK_INT":
            import struct
            data = get(0, [])
            raw = bytes(data.encode() if isinstance(data, str) else data)
            if len(raw) < 4:
                raise VMError("UNPACK_INT requires at least 4 bytes.")
            return struct.unpack("<i", raw[:4])[0]
        if n == "PATH_NORMALIZE":
            return os.path.normpath(str(get(0, "")))
        if n == "BASENAME": return os.path.basename(str(get(0, "")))
        if n == "DIRNAME": return os.path.dirname(str(get(0, "")))
        if n == "EXTENSION":
            return os.path.splitext(str(get(0, "")))[1]
        if n == "READ_LINES":
            return Path(str(get(0))).read_text(encoding="utf-8").splitlines()
        if n == "FILE_LINES":
            return len(Path(str(get(0))).read_text(encoding="utf-8").splitlines())

        # ----- maps / objects -----
        if n == "KEYS": return list(get(0,{}).keys())
        if n == "VALUES": return list(get(0,{}).values())
        if n == "ENTRIES": return list(get(0,{}).items())
        if n in {"HAS","PROPERTY","PROP"}:
            obj,key=get(0,{}),str(get(1,"")); return key in obj if isinstance(obj,dict) else hasattr(obj,key)
        if n == "MAP": return dict(a[0]) if len(a)==1 and isinstance(a[0],dict) else {str(i):v for i,v in enumerate(a)}
        if n == "OBJECT": return dict(a[0]) if a and isinstance(a[0],dict) else {}

        # ----- type / conversion -----
        if n in {"TYPE_OF","TYPEOF"}:
            v=get(0); return "null" if v is None else ("bool" if isinstance(v,bool) else "int" if isinstance(v,int) and not isinstance(v,bool) else "float" if isinstance(v,float) else "string" if isinstance(v,str) else "array" if isinstance(v,list) else "map" if isinstance(v,dict) else type(v).__name__)
        if n == "IS": return self.native_call("TYPE_OF",[get(0)]) == str(get(1)).lower()
        if n == "INT": return int(float(get(0,0)))
        if n == "FLOAT": return float(get(0,0))
        if n == "BOOL": return self.is_truthy(get(0))
        if n in {"STRINGIFY","STRINGIFY_JSON","JSON"}: return json.dumps(get(0),ensure_ascii=False,default=str)
        if n in {"PARSE","PARSE_JSON"}: return json.loads(str(get(0,"null")))
        if n == "NUMBER":
            x=get(0,0); return float(x) if any(c in str(x) for c in '.eE') else int(x)
        if n in {"EMPTY"}: return len(get(0,[])) == 0
        if n == "VALID": return get(0) is not None
        if n == "INVALID": return get(0) is None
        if n in {"CONVERT","AUTO"}: return get(0)
        if n == "INSTANCE": return isinstance(get(0), type) and isinstance(get(1), get(0)) if isinstance(get(1), type) else False

        # ----- file / path -----
        if n == "PATH": return os.path.join(*(str(x) for x in a))
        if n == "FILE_EXISTS": return Path(str(get(0))).is_file()
        if n == "FILE_SIZE": return Path(str(get(0))).stat().st_size
        if n == "FILE_READ": return Path(str(get(0))).read_text(encoding="utf-8")
        if n == "FILE_WRITE": Path(str(get(0))).write_text(str(get(1,"")),encoding="utf-8"); return True
        if n == "FILE_APPEND":
            with Path(str(get(0))).open("a",encoding="utf-8") as f: f.write(str(get(1,"")));
            return True
        if n == "FILE_DELETE": Path(str(get(0))).unlink(missing_ok=True); return True
        if n in {"FILE_COPY","FILE_MOVE"}:
            import shutil
            src,dst=str(get(0)),str(get(1)); (shutil.copy2(src,dst) if n=="FILE_COPY" else shutil.move(src,dst)); return True
        if n == "DIR_CREATE": Path(str(get(0))).mkdir(parents=True,exist_ok=True); return True
        if n == "DIR_EXISTS": return Path(str(get(0))).is_dir()
        if n == "DIR_LIST": return [p.name for p in Path(str(get(0))).iterdir()]
        if n == "DIR_DELETE": Path(str(get(0))).rmdir(); return True

        # ----- system -----
        if n == "INPUT": return input(str(get(0,"")))
        if n == "ARGV": return sys.argv[:]
        if n == "GETPID": return os.getpid()
        if n == "GETPPID": return os.getppid()
        if n == "SLEEP": time.sleep(float(get(0,0))); return None
        if n in {"TIME","TIMESTAMP"}: return datetime.now(timezone.utc).timestamp()
        if n == "DATE": return date.today().isoformat()
        if n == "VERSION": return "2.0.1"
        if n == "SYSTEMOS": return os.name
        if n == "PLATFORM": return sys.platform
        if n == "ARCH": return platform.machine()
        if n == "ENV": return os.environ.get(str(get(0,"")), get(1,None))
        if n == "SYSTEM": return subprocess.run(str(get(0,"")),shell=True,capture_output=True,text=True).stdout

        # ----- crypto / encoding -----
        if n in {"HASH","SHA","SHA256"}: return hashlib.sha256(str(get(0,"")).encode()).hexdigest()
        if n == "MD5": return hashlib.md5(str(get(0,"")).encode()).hexdigest()
        if n == "SHA1": return hashlib.sha1(str(get(0,"")).encode()).hexdigest()
        if n == "SHA512": return hashlib.sha512(str(get(0,"")).encode()).hexdigest()
        if n in {"BASE64","ENCODE64"}: return base64.b64encode(str(get(0,"")).encode()).decode()
        if n == "DECODE64": return base64.b64decode(str(get(0,"")).encode()).decode()
        if n == "HEX": return str(get(0,"")).encode().hex()

        # ----- regex / data -----
        if n in {"REGEX","PATTERN"}: return re.compile(str(get(0,"")))
        if n == "MATCH": return re.search(str(get(0,"")),str(get(1,""))) is not None
        if n == "YAML":
            # JSON is a valid YAML subset; keep stdlib-only runtime.
            return json.dumps(get(0),ensure_ascii=False) if not isinstance(get(0),str) else get(0)
        if n == "ENUM": return {str(k):v for k,v in (get(0,{}).items() if isinstance(get(0),dict) else enumerate(a))}
        if n in {"STRUCT","UNION"}: return {"__kind__":n.lower(),"fields":get(0,{})}
        if n == "GENERATOR": return iter(get(0,[]))
        if n == "ITERATOR": return iter(get(0,[]))
        if n == "NEXT":
            it=get(0)
            try: return next(it)
            except StopIteration: return None
        if n == "SPREAD": return list(get(0,[]))
        if n == "REST": return list(a)
        if n == "DESTRUCTURE": return list(get(1,[])) if isinstance(get(1),list) else get(1)
        if n in {"PROMISE","ASYNC","AWAIT","THEN"}: return get(0)
        if n == "ASSERT":
            if not self.is_truthy(get(0)): raise VMError(str(get(1,"Assertion failed")))
            return True
        if n in {"DEBUG","WARN","ERROR","DUMP"}: print(*a); return get(0,None)
        if n == "DISASM": return "\\n".join(f"{i:04}: {inst}" for i,inst in enumerate(self.code))
        if n in {"NOP","NOOP"}: return None

        # Reserved syntax words are represented as descriptors instead of
        # silently disappearing. This makes feature detection possible while
        # keeping the VM deterministic.
        if n in {"NEW","THIS","SUPER","STATIC","EXTENDS","CLASS","CAST","OUT","IN","TRUE","FALSE","NULL","VOID","MATH","STRING","ARRAY","MAP","OBJECT","SWITCH","CASE","DEFAULT","BREAK","CONTINUE","WHEN","ELSE","END"}:
            return {"feature": n, "status": "reserved"}
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

        if opcode == OpCode.ARSHIFT:
            b = self.pop()
            a = self.pop()
            # Python's >> is arithmetic for signed integers, which matches
            # ZeroOne's signed arithmetic-right-shift semantics.
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
            if isinstance(array, dict):
                self.push(array.get(str(index)))
            else:
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

        if opcode == OpCode.JMP_IF_ITER_END:
            value = self.pop()
            if value is ITERATOR_END:
                self.ip = operand
            else:
                # Put the duplicated real value back for STORE/loop body.
                self.push(value)
                self.ip += 1
            return

        if opcode == OpCode.LABEL:
            self.ip += 1
            return

        # ============================================
        # FUNCTION OPERATIONS (260-289)
        # ============================================

        if opcode == OpCode.ITERATOR:
            iterable = self.pop()
            try:
                self.iterator_stack.append(iter(iterable))
            except TypeError as e:
                raise VMError(f"Value is not iterable: {iterable!r}") from e
            self.ip += 1
            return

        if opcode == OpCode.NEXT:
            if not self.iterator_stack:
                raise VMError("Iterator stack is empty.")
            iterator = self.iterator_stack[-1]
            try:
                self.push(next(iterator))
            except StopIteration:
                self.iterator_stack.pop()
                self.push(ITERATOR_END)
            self.ip += 1
            return

        if opcode == OpCode.TRY:
            target = int(operand)
            self.exception_handlers.append(target)
            self.exception_handler = target
            self.ip += 1
            return

        if opcode == OpCode.TRY_END:
            if self.exception_handlers:
                self.exception_handlers.pop()
            self.exception_handler = (
                self.exception_handlers[-1]
                if self.exception_handlers else None
            )
            self.ip += 1
            return

        if opcode == OpCode.CATCH:
            if self.pending_exception is not None:
                self.store("e", str(self.pending_exception))
                self.pending_exception = None
            # The handler for the try that just transferred control was
            # already popped by run(). Keep any outer handler active.
            self.exception_handler = (
                self.exception_handlers[-1]
                if self.exception_handlers else None
            )
            self.ip += 1
            return

        if opcode == OpCode.FINALLY:
            # Marker for user finally code. TRY_END already closes a normal
            # try scope; exception transfer pops the matching handler in run().
            # Therefore FINALLY must never pop an outer nested handler.
            self.exception_handler = (
                self.exception_handlers[-1]
                if self.exception_handlers else None
            )
            self.ip += 1
            return

        if opcode == OpCode.RETHROW:
            if self.pending_exception is not None:
                error = self.pending_exception
                self.pending_exception = None
                raise error
            self.ip += 1
            return

        if opcode == OpCode.CLOSURE:
            if not isinstance(operand, dict) or "target" not in operand:
                raise VMError("Invalid closure descriptor.")
            self.push({
                "__zo_callable__": True,
                "address": int(operand["target"]),
                "params": list(operand.get("params", [])),
            })
            self.ip += 1
            return

        if opcode == OpCode.APPLY:
            argc = int(self.pop())
            args = [self.pop() for _ in range(argc)][::-1]
            callable_obj = self.pop()
            if not isinstance(callable_obj, dict) or not callable_obj.get("__zo_callable__"):
                raise VMError("Value is not callable.")
            params = list(callable_obj.get("params", []))
            if argc != len(params):
                raise VMError(
                    f"Callable expects {len(params)} argument(s), got {argc}."
                )
            # The function entry point binds its parameters with STORE_LOCAL.
            # Restore the arguments in their original order before jumping.
            self.stack.extend(args)
            self.call_stack.append(self.ip + 1)
            self.locals_stack.append({})
            self.ip = int(callable_obj["address"])
            return

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
