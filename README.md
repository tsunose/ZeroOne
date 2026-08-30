# ZeroOne V2.0.3

ZeroOne V2.0.3 is a bug-fix release that corrects two compiler-generation
issues found while testing V2.0.2, both directly relevant to the
self-hosting effort.

## V2.0.3 changes

- Fixed `CONTINUE` inside a `FOR` loop causing an infinite loop: the
  update step (e.g. `SET i = i + 1`) is no longer skipped. `FOR` loops
  now have a dedicated continue target placed right before the update
  step, separate from the condition-check target used by `BREAK` /
  `LOOP` / `WHILE` / `FOREACH`.
- Fixed function argument-count checking so it also applies to `FUNC`
  definitions nested inside `WHEN`, `SWITCH`, `LOOP`, `WHILE`, `FOR`,
  `FOREACH`, and `TRY`/`CATCH`/`FINALLY` blocks, not just top-level
  definitions. Previously, a mismatched-argument-count call to a nested
  function silently corrupted the VM operand stack instead of failing
  to compile.

See `CHANGELOG_v2.0.3.md` for the full technical detail on both fixes,
including root cause and reproduction steps.

## V2.0.2 changes (carried forward)

- Common built-in names such as `ADD`, `SIZE`, `SORT`, `LENGTH`, `PUSH`, `POP`, `PARSE`, and `FORMAT` are no longer globally reserved by the lexer.
- Legacy line-style aliases remain supported where practical, while built-in calls are resolved by the compiler.
- User-defined functions take precedence over native functions with the same name.
- Implemented VM arithmetic right shift (`>>>` / `ARSHIFT`).
- Implemented working lambda closures and dynamic lambda calls, including parameter binding.
- `TRY` / `FINALLY` now rethrows an uncaught exception after the `FINALLY` body.
- Function calls now report argument-count errors during compilation instead of causing VM stack underflow.
- `FOREACH` now uses a private iterator-end sentinel so a real `NULL` element does not terminate iteration.
- `main.py` is now a compatibility entry point for the current `zo.py` CLI instead of depending on the missing `sample.zo`.

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

## Known open items (not yet fixed / not yet confirmed as bugs)

- `>>` (`RSHIFT`) and `>>>` (`ARSHIFT`) currently always produce the same
  result (both are signed/arithmetic shifts). This looks like an
  intentional design choice rather than a bug, but is unconfirmed.
- The `NEW` keyword is reserved but not yet wired up in the parser —
  there is currently no way to instantiate a `CLASS` from ZeroOne source.

**Status: ZeroOne V2.0.3 - Development / bug-fix release**

The project remains under development. The priority is language completeness, reliable compiler/VM behavior, and eventual Python independence.
