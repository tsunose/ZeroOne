# ZeroOne V2

ZeroOne V2 is the expanded development version of **ZeroOne**, a programming language designed to be easy to write, read, and learn.

## What changed in V2

- Expanded lexer and parser for the growing ZeroOne syntax.
- Large built-in/standard-library catalog for math, strings, arrays, maps, types, files, JSON, hashing, regex, system information, and runtime helpers.
- Bytecode compiler pipeline: **Lexer -> Parser -> AST -> Generator -> Assembler -> Bytecode -> VM**.
- Versioned `.zbc` bytecode format.
- Stronger Virtual Machine and a single canonical runtime.
- `zo.py` command-line compiler and runner.
- More tests for expressions, functions, arrays, maps, files, JSON, and native registration.
- Reserved features now have explicit runtime descriptors instead of silently disappearing.

## Example

```zeroone
SET value = ADD(2, 3)
OUT value
EXIT
```

## CLI

```text
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

## The main goal: self-hosting

V2 is a foundation for the long-term goal of **self-hosting**: replacing the Python implementation of the compiler with a compiler written in ZeroOne itself.

Current direction:

```text
Python compiler
      -> ZeroOne bytecode
      -> ZeroOne VM
```

Target:

```text
ZeroOne compiler
      -> ZeroOne bytecode
      -> ZeroOne VM
```

The project is still under development. Some advanced language keywords are reserved/runtime descriptors rather than full syntax yet; they are deliberately exposed so their semantics can be implemented incrementally without changing the project layout.

## Status

**ZeroOne V2.0.0 - Development**

The priority is language completeness, reliable compiler/VM behavior, and eventually Python independence.

## V2.0.1

V2.0.1 is a bug-fix release based on release testing of V2.0.0.

- Fixed native calls from expressions for names such as `FAC` and bitwise functions.
- Added lexer support for bitwise operators, `?`, and `;`.
- Fixed `FOR` assignment initializer/update handling.
- Added VM iterator support for `FOREACH`.
- Added basic VM `TRY` / `CATCH` / `FINALLY` execution.
- Fixed missing runtime standard-library imports.
- Added release regression tests in `ZeroOne-V2/tests/test_release_201.py`.
