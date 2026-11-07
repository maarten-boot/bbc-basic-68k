# Conversation log, 2026-11-07

Continues `Conversation-2026-11-06.md`.

## 17. Benchmarks against other 68000 BASICs; the cost of unaligned access

* **User:** "read the handover and continue, skip the z80 ideas for now
  the original question was regarding 68000 basic's". The hand-over is
  `Handover-benchmark-2026-11-07.md` (untracked): R.T. Russell's question
  how this BASIC compares with other 68000 BASICs, and whether the
  unaligned (byte-wise) access costs much. Step 4 (Z80 timings) skipped.
  This ends the pause of entry 16 for this work.
* **EhBASIC 68k 3.52**: `ehbasic.bin` of rosco-m68k/example_programs
  (firmware-2.x, fa4b2a9, sha256 4ccee8df...) downloaded into
  `build/ehbasic/dl`. Its source is in `../rosco_m68k/code/software/
  ehbasic`: 32-bit floats, `&` integer variables, `LEEK`.
* **MAME:** `-bios v242` (the board's firmware; the image's default is
  v250 DEV, which `mamebare.sh` uses). EhBASIC boots from the card
  (5216784 bytes free) and the firmware tick at `$40C` runs under it.
  EhBASIC polls the console and loses typed-ahead characters, so the
  programs are typed a character at a time, each after its echo.
* New `src68k/test/bench68/` (Rugg/Feldman BM1-BM8 and the sieve, one
  template for both BASICs, 10000 passes; `@` = the variable type) and
  `tools/bench68.py` (MAME, a boot per BASIC and type).
* **Alignment:** rebuilt `build/r68kprof`; bareprof on the same programs;
  `m68k-elf-objdump` (the roscopeco/rosco_m68k image) for the
  disassembly; new `tools/leprof.py` counts the byte-wise LE helpers,
  their calls and the inline 2-5 byte field accesses (13 sites, checked
  by hand) and estimates aligned BE and LE costs.
* **Found:** r68k charges 4 cycles per bit for an immediate shift, the
  68000/68010 2 (Musashi source says 6+2n; measured 38 for lsl.w #8).
  About 3 % of every r68k profile; leprof corrects it. With the
  correction r68k and MAME agree within ~2 % (bm1 float: 28.6 M cycles
  = 2.86 s, MAME 2.80 s).
* **Result (alignment, corrected):** byte-wise LE access is 2.6-9.4 % of
  the cycles; aligned big-endian data would save 2.0-7.8 %, aligned
  little-endian 1.0-3.8 %.
* **MAME results** (all 36 runs clean, 1899 primes in both; repeats
  within 0.2 %): BBC BASIC 68k is 1.10-1.61x faster than EhBASIC with
  real variables and 1.40-1.91x with integer variables (EhBASIC converts
  `&` variables to float on use, `MOVE.l (a0),d0` then LAB_AYFC; its
  data is aligned big-endian, and it is still slower).
* **Report** for the user to pass on: `tmp/bench-68k-basics-2026-11-07.md`
  (set-up, table, method and table of the byte-wise share, where the
  time goes, how to reproduce). Plan P12 (done) and P13 (r68k shift
  timing, the user's call); Tests T19 extended. Not committed.

## 18. Commit

* **User:** "commit". Committed the benchmark programs, bench68.py,
  leprof.py, the hand-over note and the planning updates (with entry 16
  of 2026-11-06). The report stays in tmp/ (not in git).

## 19. Pushed

* **User:** "pushed". e531bb1 on origin. This entry is not committed.

## 20. P13 for the r68k thread

* **User:** "show me P13 as i will have to tell that thread what to look at".
* Located the cause in r68k (Musashi): immediate-count shifts are charged
  2 cycles per bit twice, once in `m68ki_build_opcode_table`
  (`musashi/m68k_in.c` line 218, "For all shift operations with known
  shift distance") and once in each of the 24 `M68KMAKE_OP(..., s, .)`
  handlers (`USE_CYCLES(shift<<CYC_SHIFT)`). Register-count shifts are
  right. Profile: 6+4n (word/byte), 8+4n (long). No change made.

## 21. Commit

* **User:** "commit". fa881d2 (log entries 19-20). This entry is not committed.

## 22. r68k updated: patches dropped, leprof correction removed

* **User:** relayed the r68k thread's notes: drop the two r68k patch
  files; remove the shift correction in `leprof.py`; update the outdated
  notes in PORT_PLAN.md.
* r68k `rosco-minix-duart` now has the profiler (`7b95236`) and the shift
  fix (`6e0177e`); the illegal-instruction fix was already `2d92829`.
* Done: `git rm` of `mboot/patches/r68k-0001-*` and `r68k-0002-*`;
  `leprof.py` without `correct()`; `bench.py`/`bareprof.py` docstrings
  build `build/r68kprof` from r68k 6e0177e+ without a patch; PORT_PLAN.md
  sections 2 (illegal-instruction fix), 13 (profiler) and the MAME/r68k
  gap note updated. Plan P13 done.
* Check: rebuilt `build/r68kprof` from `../r68k`; bareprof + leprof on
  BM1 and sieve (float): 28.6 M cycles, 8.7/6.8/3.4 % and 9.2/7.2/3.3 %,
  the same as the report's corrected figures.
* Not committed.
