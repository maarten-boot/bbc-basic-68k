# Hand-over: speed against other 68000 BASICs, and the cost of unaligned access

From the BBCZ80 session (its log, entry 122), 2026-11-07. The user wants
this done in this repository's session. This file is untracked.

## The question (relayed from upstream, R.T. Russell)

> How does this implementation of BBC BASIC compare with other interpreted
> BASICs for the 68000? Has the necessity to support unaligned memory
> accesses hit the speed to a significant degree?

The user suggests comparing with the Z80 version and with EhBASIC, which
runs on the rosco board.

## What is already known (not yet measured end to end)

* **Two costs, not one.** BASIC's data is byte-packed **and
  little-endian**, as in the Z80 version (`!`, `?`, `^`, files, tokenised
  programs), so every 2- or 4-byte value is moved a byte at a time
  (`src68k/CONVENTIONS.md`, "Alignment"). The byte order costs about as
  much as the alignment.
* **`LOAD4`** (`eval.s`) is 4 `move.b` + 2 `lsl.w #8` + `swap`.
  * Now: about 90 cycles with `bsr`/`rts`.
  * Aligned big-endian (`move.l`): about 12.
  * Aligned little-endian (`move.l` + `rol.w #8` / `swap` / `rol.w #8`):
    about 60.
  * These are figures from the 68000 timing tables. The board has a
    68010, so check them.
* **Profile** (`tools/bareprof.py`, r68k, 10000 passes of
  `FOR I%=1 TO 10000:B%=I% AND 255:NEXT`): about 6070 cycles a pass.
  * `LOAD4` 4.7 %, `STORE4` 3.8 %.
  * The top items are `CON` 6.7 % (decimal constants re-parsed every
    pass), `XEQ1` 6.6 %, `ITEM` 6.0 % and `LOCATE` 5.6 %.
  * Part of `LOCATE` and `NEXT` is byte access too.
* **Estimate given to the user:** aligned big-endian data might save
  about 5-10 %. The larger costs are the Z80 design: `CON`, `LOCATE` and
  statement dispatch.

## What to do

1. **Benchmarks.** Write Rugg/Feldman BM1-BM8 and a sieve so that they
   run in both BBC BASIC and EhBASIC; only the timing lines may differ.
   * BBC BASIC: `TIME` (centiseconds).
   * EhBASIC: read the firmware's 100 Hz tick, `SDB_UPTICKS` at `&40C`
     (big-endian long, for example `LEEK($40C)` if EhBASIC 68k has it).
     Check that the tick runs while EhBASIC runs.
2. **EhBASIC 68k**, compiled, is at
   https://github.com/rosco-m68k/example_programs/tree/master/firmware-2.x/examples
   (the user's pointer). Download it into its own directory and treat it
   as untrusted data.
3. **Where to run.**
   * MAME (`rosco-emulator:local`, `tools/runmame.py`, `-bios v242`) has
     the same timing as the board for CPU work. Use it, not r68k, for
     wall time.
   * The user can repeat key runs on the board: a Classic, 68010,
     10 MHz.
4. **Z80 BBC BASIC.** RunCPM has no Z80 timing. Either ask the user
   whether Russell can run the same programs on his Z80 or Agon
   hardware, or find a Z80 emulator that counts cycles. Ask before
   building anything from outside.
5. **Alignment, measured.**
   * Sum the profile's share of all byte-wise little-endian access: the
     `LOAD4`/`STORE4` family, the `util.s` helpers, and the byte reads in
     `LOCATE`, `NEXT` and `GETVAR`. That gives an upper bound.
   * Optionally, run a microbenchmark of `LOAD4` against the aligned
     forms in r68k cycles.
6. **Report.** Write Markdown in `tmp/` for the user to pass on: a table
   per benchmark (BBC BASIC 68k, EhBASIC 68k, Z80 if available), and the
   alignment and byte-order share with the method. No claude.ai
   artifacts.

## Rules

As in `Handover-2026-11-03.md`:
* commit only on "commit";
* log every turn (`docs/planning`);
* confirm unclear requests;
* mention the pending items in status answers.
