# ZeroOne v2.0.9

V2.0.9 is a stabilization release focused on the road to V2.1.0 and Python independence.

## Fixed

- Fixed `>>` arithmetic right shift vs `>>>` logical/unsigned 32-bit right shift.
- Restored and stabilized `CLASS` / `NEW` / `THIS` / bound method calls.
- Added inherited method and constructor lookup through `EXTENDS`.
- `init(...)` is the primary constructor; `constructor(...)` is also accepted for compatibility.
- Restored method-call parsing such as `obj.method(arg)`.
- Kept multiline array literals working.
- `int + string` and similar implementation-level Python exceptions are converted to ZeroOne `VMError` instead of leaking raw Python tracebacks.
- Hardened `.zbc` loading against truncated headers, malformed JSON, incomplete payloads, and malformed instruction entries.
- Updated `VERSION()` and CLI version to `2.0.9`.

## Self-hosting progress

- Expanded `self_hosting/lexer_v2.zo` for strings, escapes, floats, multi-character operators, and line comments.
- Kept the ZeroOne bootstrap compiler source in `self_hosting/self_compiler.zo`.
- Added regression coverage for classes, inheritance, short-circuit logic, multiline arrays, shifts, error conversion, versioning, and corrupted bytecode.

## Verification

Full test suite: **46 passed**.

Also manually verified:

- `self_hosting/lexer.zo`
- `self_hosting/lexer_v2.zo`
- `self_hosting/calculator.zo`
- `self_hosting/mini_interpreter.zo`
- `self_hosting/lexer_lib.zo`
- CLASS + inherited method execution
- ZeroOne-level error catching
- `python zo.py --version` -> `ZeroOne 2.0.9`

## Next: V2.1.0

The next milestone is full Python independence: ZeroOne-written Parser / AST / Code Generator / Assembler, a stable ZeroOne VM/runtime boundary, bootstrap/self-recompilation, and a workflow where the ZeroOne toolchain can rebuild itself without the Python compiler.
