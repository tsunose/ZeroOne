#!/usr/bin/env python3
"""Quick test of the v2.0.5 parser fix for keywords as identifiers"""

import sys
sys.path.insert(0, 'ZeroOne-V2.0.5')

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.generator import Generator
from compiler.assembler import Assembler
from vm.vm import ZeroOneVM
import io
from contextlib import redirect_stdout

def run_source(source):
    """Compile and run source code"""
    try:
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        code = Assembler().assemble(Generator().generate(ast))
        vm = ZeroOneVM()
        vm.load(code)
        out = io.StringIO()
        with redirect_stdout(out):
            vm.run()
        return out.getvalue(), None
    except Exception as e:
        return None, str(e)

# Test 1: Using LENGTH as a variable
print("Test 1: SET LENGTH = 5")
result, error = run_source('SET LENGTH = 5\nOUT(LENGTH)\nEXIT\n')
if error:
    print(f"  ❌ FAILED: {error}")
else:
    print(f"  ✅ PASSED: Output = {repr(result)}")

# Test 2: Using CHAR as a variable
print("\nTest 2: SET CHAR = 10")
result, error = run_source('SET CHAR = 10\nOUT(CHAR)\nEXIT\n')
if error:
    print(f"  ❌ FAILED: {error}")
else:
    print(f"  ✅ PASSED: Output = {repr(result)}")

# Test 3: Using NUMBER as a variable
print("\nTest 3: SET NUMBER = 42")
result, error = run_source('SET NUMBER = 42\nOUT(NUMBER)\nEXIT\n')
if error:
    print(f"  ❌ FAILED: {error}")
else:
    print(f"  ✅ PASSED: Output = {repr(result)}")

# Test 4: Using SIZE in FOREACH loop
print("\nTest 4: FOREACH SIZE IN array")
result, error = run_source(
    'SET array = [1, 2, 3]\n'
    'FOREACH SIZE IN array\n'
    '  OUT(SIZE)\n'
    'END\n'
    'EXIT\n'
)
if error:
    print(f"  ❌ FAILED: {error}")
else:
    print(f"  ✅ PASSED: Output = {repr(result)}")

# Test 5: Function with keyword parameters
print("\nTest 5: FUNC LENGTH(x)")
result, error = run_source(
    'FUNC LENGTH(x)\n'
    '  RETURN x * 2\n'
    'END\n'
    'SET result = LENGTH(21)\n'
    'OUT(result)\n'
    'EXIT\n'
)
if error:
    print(f"  ❌ FAILED: {error}")
else:
    print(f"  ✅ PASSED: Output = {repr(result)}")

# Test 6: Lambda with keyword parameter
print("\nTest 6: LAMBDA (CHAR) => ...")
result, error = run_source(
    'SET double = LAMBDA (CHAR) => CHAR * 2\n'
    'SET result = double(21)\n'
    'OUT(result)\n'
    'EXIT\n'
)
if error:
    print(f"  ❌ FAILED: {error}")
else:
    print(f"  ✅ PASSED: Output = {repr(result)}")

print("\n" + "="*50)
print("All tests completed!")
