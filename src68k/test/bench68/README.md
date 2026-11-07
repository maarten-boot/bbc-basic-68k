# Benchmarks for 68000 BASICs: Rugg/Feldman BM1-BM8 and the BYTE sieve

The same programs for BBC BASIC 68k and EhBASIC 68k (`tools/bench68.py`).
Only the timing lines differ:

* `@T0@` starts the clock, `@T1@` prints `BENCH name ticks`:
  BBC BASIC `TIME` (centiseconds), EhBASIC `LEEK($40C)` (the firmware's
  100 Hz tick, `SDB_UPTICKS`).
* `@` after a variable name is its type: nothing (floating point), or an
  integer variable, `%` in BBC BASIC and `&` in EhBASIC. `bm8` has no
  integer form (its functions take real numbers).

The loops run 10000 times, not the original 1000, so that the 10 ms tick
gives at least 1 % resolution; divide by 10 to compare with the
published 1000-pass figures. The sieve is one pass over 8191 flags (1899
primes).

BM8 uses `LOG`, which is the natural logarithm in EhBASIC and the common
(base 10) logarithm in BBC BASIC (`LN` is BBC's natural log); the time is
taken as is.
