# Spec: BBC BASIC 68k

What the port is required to do, written down on 2026-11-03 from what
exists: the README, `mboot/PORT_PLAN.md` (decisions D1-D4),
`mboot/Z80_DIFFERENCES.md`, `src68k/CONVENTIONS.md`, `src68k/PHASE4.md`,
`src68k/ASSEMBLER.md`, the target READMEs (`src68k/host`, `src68k/bare`,
`src68k/demo`, `src68k/web`) and the test tools. Each item has an ID;
`Tests.md` traces the tests to these IDs.

Status: **agreed** (2026-11-03). S1.6, S6.3 and S7.1, first written
down from the code as built, were confirmed as requirements by the user.

## S1. Language: BBC BASIC (Z80) 5.4

* **S1.1 Same behaviour as the Z80 original.** For any program that does
  not depend on the items in S1.2, S4.4 or the CPU, the output is the
  same as R.T. Russell's BBC BASIC (Z80) 5.4 (`z80/bin/cpm/BBCBASIC.COM`,
  BBCZ80 e4ae9ca) under RunCPM. This includes its documented
  limitations and quirks (`Z80_DIFFERENCES.md` section 5).
* **S1.2 Deliberate differences**, each with a test in
  `src68k/test/diff/` and listed in `Z80_DIFFERENCES.md`:
  * S1.2.1 a string descriptor is 6 bytes (`d08desc`);
  * S1.2.2 arrays may have more than 64K elements (`d09bigarr`);
  * S1.2.3 `INKEY(-256)` is &44 (`d10inkey256`);
  * S1.2.4 `AUTO` with a step over 255 is "Silly" (`d11auto`);
  * S1.2.5 `LOCAL` with no variables does nothing, as Acorn
    (`d15localnone`);
  * S1.2.6 `RESTORE DATA` / `RESTORE ERROR` with nothing to restore give
    the manual's error (`d13restoredata`, `d14restoreerror`).
* **S1.3 Arithmetic.** The floating-point package (`math.s`) gives
  bit-identical results to the Z80's FPP: 40-bit floats (32-bit mantissa,
  8-bit exponent) and 32-bit integers.
* **S1.4 BASIC-visible memory is little-endian** (D2): `!`, `]`/`|`,
  stored variables and the tokenised program format. Tokenised `.BBC`
  files from the Z80 version load and run unchanged.
* **S1.5 32-bit addresses** (D1): `^`, `!`, `DIM`, PAGE/LOMEM/HIMEM and
  `END` are real 68k addresses; the workspace is not limited to 64 KB.
* **S1.6 Error handling.** Errors, `ON ERROR`, `ON ERROR LOCAL`, `ERR`,
  `ERL`, `REPORT` behave as in the Z80 version; running out of room
  (LOAD/CHAIN of a program that does not fit, deep recursion) gives an
  error, not a hang or crash.

## S2. The 68000 inline assembler (D3)

* **S2.1** `[ ... ]` assembles Motorola-syntax 68000 code (plus the
  two 68010 additions RTD and `MOVE CCR,<ea>`; not MOVEC/MOVES), with
  P%, O%, OPT, labels and two-pass assembly as
  in the Z80 version (`ASSEMBLER.md`).
* **S2.2** For each supported instruction and addressing mode the bytes
  are the same as the ACK assembler's.
* **S2.3** Directives, macros and the error messages are as in
  `ASSEMBLER.md`; `CALL` and `USR` run 68k machine code.

## S3. Targets

* **S3.1 Minix 2.0.4 on the rosco_m68k:** `bbcbasic`, a normal Minix
  program built with the ACK (`-S 64k`), installed by `make install`
  into the Minix tree's SD root. *(Minix work is on hold; see Plan.md.)*
* **S3.2 A bare rosco_m68k:** `ROSCODE1.BIN`, loaded by the firmware at
  0x40000, from the firmware's menu or as `ROSCODE1.BIN` on the SD card.
  It uses the memory the firmware reports, the firmware console speed,
  and keeps the firmware's 100 Hz tick and DUART set-up.
  Reference machine: rosco_m68k Classic, 68010, 10 MHz, 5 MB.
* **S3.3 PC programs:** `bbc68k` (Linux x86-64, static) and
  `bbc68k.exe` (Windows 10/11, 64-bit, only system DLLs): bare BBC BASIC
  in an embedded r68k, starting at the `>` prompt, with the demo programs
  built in.
* **S3.4 Web page:** `bbc68k.html`, one self-contained page that works
  offline (r68k in WebAssembly), with bare BBC BASIC; optionally the
  Minix demo.
* **S3.5 Demos:** the Minix demo (`bbc68k-demo`) and the bare demo
  (`bbc68k-bare`, tarball and container image), each with the demo
  programs and `CHAIN "menu"`.

* **S3.6 Start a program from the command line:** a program name given
  at start-up is CHAINed (Minix: `bbcbasic PROG`; PC programs:
  `bbc68k PROG`, and a folder in the name, such as a file dropped on the
  program, becomes BASIC's folder). Bare BASIC has no command line of
  its own: the PC program passes the name to it (`bare.c`, H_ARG).

## S4. Files and `*` commands

* **S4.1 Program files:** LOAD, SAVE, CHAIN; `OPENIN`/`OPENOUT`/`OPENUP`,
  `BGET#`, `BPUT#`, `PTR#`, `EXT#`, `EOF#`, `INPUT#`, `PRINT#`,
  `*SPOOL`, `*EXEC`.
* **S4.2 Bare: RAM store and SD card.** A RAM store (a quarter of the
  memory above BASIC's code) and FAT16/FAT32 on the SD card, with
  subdirectories, `*DIR`, `*CD`, `*MKDIR`, `*RMDIR`, `*ERA`, `*REN`;
  after any sequence of these the card passes `fsck.fat`.
* **S4.3 PC programs: the starting folder.** Files are those of the
  folder the program was started in; long names and subdirectories;
  case-insensitive match when the exact name is absent; `SAVE "prog"`
  writes `prog.BBC`; paths cannot leave the folder; names not found fall
  back to the RAM store.
* **S4.4 Modern-file-system behaviour** where CP/M differs
  (`Z80_DIFFERENCES.md` section 3): exact `EXT#`/`EOF#`, real `POS`,
  "File not found", "Bad name", spaces after `*` skipped.
* **S4.5 `*` commands** (`osl.c`, table `comds`): `*BYE`/`*QUIT`,
  `*CD`, `*DIR [afsp]` (also `*.`), `*ERA`/`*ERASE [afsp]`,
  `*ESC [ON|OFF]`, `*EXEC`, `*HELP` (the version), `*LOAD`, `*SAVE`,
  `*MKDIR`, `*OPT`, `*REN`/`*RENAME new=old`, `*RESET`, `*RMDIR`,
  `*SPOOL`, `*TYPE`. Any of them may be abbreviated with `.`; spaces
  after `*` are skipped. Anything else: under Minix it is run by the
  shell; on bare and the PC programs it is "Bad command".

## S5. Console

* **S5.1** ESCape stops a running program; `*ESC OFF` makes ESC a
  normal key (27) and `*ESC ON` restores it; ESCape still works after a
  `*` command.
* **S5.2** ^S/^Q stop and start output; typeahead during a run is kept
  for `GET`/`GET$`/`INKEY`.
* **S5.3** The line editor: cursor keys, `EDIT`, lines longer than the
  console width (wrapping on a vt100), ESCape abandons a line.
* **S5.4** Output is vt100 (`CLS`, `TAB(x,y)`); the Windows console is
  switched to that mode.
* **S5.5** PC programs read a piped or redirected script as typed keys,
  with CR, LF or CR LF line ends, and stop when the input is used up and
  BASIC is idle for 0.3 s, or at `*BYE`. Ctrl-] quits.
* **S5.6** `INKEY(-n)` for a held key is always FALSE (the console cannot
  see held keys).

## S6. Build and release

* **S6.1** Builds with a pinned ACK release
  (`maarten-boot/ack`, `minix68k-20261031`, checked by SHA-256,
  `tools/getack.sh`) and sibling checkouts of `minix-st-2.0.4`, `r68k`,
  `RunCPM`, `rosco_m68k`. CI pins them: minix-st-2.0.4 `feea47f`
  (rosco-m68k), r68k `23f4e66` (main), RunCPM `12fc57a`.
* **S6.2** CI (`.github/workflows/windows-exe.yml`) runs on every push
  to `main` and by hand; it builds and tests the Linux and Windows
  programs and the bare image (`tools/ci-windows.sh`) and publishes them
  as three artifacts. Actions are pinned by commit hash.
* **S6.3** The CI rosco image is byte-identical to a local
  build of the same commit.

## S7. Performance

* **S7.1** No requirement beyond "usable on the 10 MHz
  board". Changes are measured with the benchmarks (`test/bench`):
  cycles with r68k (`bench.py`, `bareprof.py`), wall time only with MAME
  (`mamebare.sh`, `mamebench.py`), whose SD timing matches the board.

## S8. Licence and attribution

* **S8.1** Zlib licence, as BBCZ80 (`licence.txt`).
* **S8.2** The name "BBC BASIC": Russell's README says the BBC's
  permission is not transferable to a derived work; its use here was
  confirmed by e-mail (the user, 2026-11-03; Plan.md P6).
