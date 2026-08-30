# ZeroOne V2.0.2

ZeroOne V2.0.2 is a bug-fix release focused on compiler/VM correctness and the path toward self-hosting.

## V2.0.2 changes

- Common built-in names such as `ADD`, `SIZE`, `SORT`, `LENGTH`, `PUSH`, `POP`, `PARSE`, and `FORMAT` are no longer globally reserved by the lexer.
- Legacy line-style aliases remain supported where practical, while built-in calls are resolved by the compiler.
- User-defined functions take precedence over native functions with the same name.
- Implemented VM arithmetic right shift (`>>>` / `ARSHIFT`).
- Implemented working lambda closures and dynamic lambda calls, including parameter binding.
- `TRY` / `FINALLY` now rethrows an uncaught exception after the `FINALLY` body.
- Function calls now report argument-count errors during compilation instead of causing VM stack underflow.
- `FOREACH` now uses a private iterator-end sentinel so a real `NULL` element does not terminate iteration.
- `main.py` is now a compatibility entry point for the current `zo.py` CLI instead of depending on the missing `sample.zo`.
- Added V2.0.2 regression tests for the fixes above.

## Example

```zeroone
FUNC add(a, b)
    RETURN a - b
END

SET result = add(10, 3)
OUT(result)
EXIT
```

## CLI

```text
python zo.py --version
python zo.py compile hello.zo
python zo.py run hello.zbc
python zo.py run-source hello.zo
```

## Architecture

```text
.zo
  |
Lexer
  |
Parser
  |
AST
  |
Generator
  |
Assembler
  |
.zbc
  |
ZeroOne VM
```

## Self-hosting goal

The long-term goal is to replace the Python implementation of the compiler with a compiler written in ZeroOne itself.

```text
Current:
Python compiler -> ZeroOne bytecode -> ZeroOne VM

Target:
ZeroOne compiler -> ZeroOne bytecode -> ZeroOne VM
```

**Status: ZeroOne V2.0.2 - Development / bug-fix release**

The project remains under development. The priority is language completeness, reliable compiler/VM behavior, and eventual Python independence.
