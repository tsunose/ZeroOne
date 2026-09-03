# ZeroOne v2.0.8

## Bug fixes
- Fixed `>>`/`>>>` distinction: `>>` is arithmetic and `>>>` is 64-bit unsigned.
- Implemented `NEW ClassName(...)`, constructor `init`, `THIS`, and bound class methods.
- Invalid `ADD` type combinations now raise ZeroOne `VMError` instead of raw Python `TypeError`.
- Multiline array literals are now accepted.
- Updated `VERSION()` to `2.0.8`.

## Self-hosting
- Added ZeroOne source for a bootstrap/self-hosting compiler core.
- No generated self-compiled binary is included.
