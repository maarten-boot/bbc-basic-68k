# Tests: BBC BASIC 68k

Every test suite that exists, traced to `Spec.md`. Commands run from
`src68k/` after the build (see "Build" below). Status is the last known
result, from the hand-over of 2026-11-03 (BBCZ80 log entries 114 and
118), unless a date says otherwise.

## Build (prerequisite for all)

    make bbcbasic
    python3 tools/mkdemo.py --progs
    python3 tools/mkbare.py && python3 tools/mkbare.py --demo
    python3 tools/mkhost.py

## Suites

| ID | Suite / command | What it checks | Spec | Last result |
|---|---|---|---|---|
| T1 | `bascheck.py` over `test/bas/*.in` (59 tests: `t*`, `k*`, `u_*`, `c_l*`, `x*`, `a*`) | Output against the Z80 under RunCPM (`.ref`), or a hand-written `.exp`. S1.4: the `u_*` tests run Russell's Z80-saved programs, and `t19z80file` LISTs one and checks that SAVE writes the Z80's bytes for all nine. S1.6 in particular: `t17loadroom` (LOAD that does not fit), `k07errors` (PROCdeep: No room), `kw/HIMEM` | S1.1, S1.3-S1.6, S4.1 | see T1-T3 runs; t19z80file 2026-11-03: ok on host, hostwin, bare |
| T2 | `bascheck.py` over `test/kw/*.in` (130, one per RISC OS keyword) | as T1 | S1.1, S4.5 | " |
| T3 | `bascheck.py` over `test/guide/*.in` (48, the RISC OS programming chapters) | as T1 | S1.1, S1.6, S4.1 | " |
| T1-3 runs | `BBC_EMU=host` / `hostwin` / `bare python3 tools/bascheck.py` | T1-T3 on each target | S3.2, S3.3 | host 0 of 234 (2 skipped), hostwin 0 of 234 (2 skipped), bare 0 of 236 |
| T4 | `bascheck.py test/diff/dNN*.in` (by hand, not in the normal run) | Shows each deliberate difference as a diff against the Z80 | S1.2.x, S4.4 | differences as documented |
| T5 | `mathcheck.py` (needs Minix in r68k) | FPP bit-identical to the Z80, random vectors per operation | S1.3 | not run since the move (Minix on hold) |
| T6 | `BBC_EMU=host python3 tools/asmcheck.py` | Inline assembler bytes against ACK `as` (the 68010's RTD and `MOVE CCR,<ea>` against fixed hex) | S2.1-S2.3 | 0 of 162 |
| T7 | `hostcheck.py` | PC programs: files of the starting folder, paths, `*` commands, `bbc68k NAME` (autorun, with a folder, not found), piped scripts (CR, LF, CR LF), Windows console keys | S3.3, S3.6, S4.3, S4.5, S5.4, S5.5 | ok |
| T8 | `editcheck.py ../build/host/linux/bbc68k` | Line editor on a 40-column vt100 model | S5.3 | ok |
| T9 | `ttycheck.py --exe ../build/host/linux/bbc68k` and `ttycheck.py ../build/bare/bbc68k-bare` | ESCape, typeahead, `*ESC OFF/ON`, ^S/^Q, editor, `*BYE` | S5.1-S5.3 | ok |
| T10 | `fatcheck.py` | Bare BASIC on FAT16 (mkfat.py and mkfs.fat) and FAT32 cards; `fsck.fat` clean afterwards | S4.2, S3.2 | ok |
| T11 | `mkbaredemo.py --test` | The bare demo boots; asm demo and card work | S3.5 | ok (without `--docker`) |
| T12 | `mkdemo.py --test` (`make demo`) | The Minix demo boots and runs | S3.1, S3.5 | not run since the move (Minix on hold) |
| T13 | `mkweb.py --test` (`make web`, needs emcc) | The web page | S3.4 | not run since the move |
| T14 | `make check`, `make oscheck` (Minix in r68k) | `hello`, `utiltest`, the OS layer via `osmon` | S3.1 | not run since the move (Minix on hold) |
| T15 | `tools/ci-windows.sh` via the GitHub workflow | Clean-room build of host and bare, then T1-T3 (host, bare), T6, T7 (linux), T8, T9, T10 | S6.1, S6.2 | run 41342193509: success |
| T16 | Compare the CI rosco image with a local build of the same commit (`cmp`) | Reproducible image | S6.3 | identical (60504 bytes, 6628baf) |
| T17 | Real board, by hand: boot `ROSCODE1.BIN` from the menu and from the card; run IOTIME, FILETEST, Russell's test programs; memcheck | The real machine | S3.2, S4.2 | pass (BBCZ80 log 108-119) |
| T18 | `make mamecheck` (MAME rosco-emulator, podman) | T1-T3, T6, T5 on the emulated real machine | S3.1, S1.3, S2 | not run since the move |
| T19 | `bench.py`, `bareprof.py`, `mamebare.sh`, `mamebench.py` over `test/bench/*.bas` | Measurement only, no pass/fail | S7.1 | profile: ~6000 cycles per FOR pass |

## Counts

59 + 130 + 48 = 237 tests (236 before t19z80file, 2026-11-03). The PC
programs (host, hostwin) skip the two marked `#typed` (`kw/INKEY`,
`kw/INKEY_STRING`: lines must be typed after the prompt), so they report
0 of 235, 2 skipped; bare runs all 237.

## The Z80 reference and bytes >= 128

RunCPM clears bit 7 of every character it writes to the console
(`mask8bit = 0x7f`, `../RunCPM/RunCPM/console.h`), so a `.ref` can never
show a byte >= 128; the 68k prints them as they are. A test that prints
such bytes needs a hand-made `.exp` (as `t19z80file`), or RunCPM built
with `mask8bit = 0xff`.

## Gaps (no test traces to these)

* **S1.5** is covered only indirectly (`x02bigarr`, `x06bigmem`,
  `d09bigarr`).
* **S3.6 under Minix** (`bbcbasic PROG`): no test (Minix on hold).
* **The Windows program in CI:** CI builds `bbc68k.exe` but runs only
  the Linux program's tests (no hostwin bascheck, `hostcheck.py linux`);
  the Windows tests run only locally under Wine.
* **S5.6** (`INKEY(-n)` FALSE) cannot be tested with typed input.
* **S8.x**: not testable.

## To verify on the next full run

* The unexplained batch failures of 2026-11-01 (host 217, hostwin 7-11,
  all at the start of a background run): keep the full output if it
  happens again.
