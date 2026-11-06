# Plan: BBC BASIC 68k

The work from 2026-11-03 on, in this repo. History before that:
`mboot/PORT_PLAN.md` (phases 0-6, done) and the BBCZ80 log (entries
1-121, `../BBCZ80/mboot/log/`, branch `mboot/conversation-log`).
Spec IDs refer to `Spec.md`, test IDs to `Tests.md`.

## Open items

| ID | Item | Status | Spec |
|---|---|---|---|
| P1 | **docs/planning**: Spec.md, Plan.md, Tests.md, conversation log; fold in the hand-over note | done (2026-11-03): Spec changes accepted | all |
| P2 | **BBCZ80:** a README line pointing here; keep or remove `src68k/` there | closed: left as it is (user, 2026-11-03) | - |
| P3 | **Minix items** | on hold until the user says so | S3.1 |
| P3a | c_l5b_recovery fails only in the full Minix bascheck session | on hold | S1.6 |
| P3b | c_l1_core and x02bigarr need more than `-S 64k` | on hold | S1.5, S3.1 |
| P3c | TIME$ under Minix | on hold | S1.1 |
| P3d | x05align under Minix | on hold | S1.1 |
| P4 | **Interpreter speed-up**: CON (decimal constants re-parsed every pass), LOCATE, ITEM/XEQ1 dispatch; ~6000 cycles per FOR pass now | parked until needed | S7.1 |
| P5 | **Agon emulator** for the tests | optional; building it needs permission | S1.1 |
| P6 | **"BBC BASIC" name**: confirm with R.T. Russell whether the name may be used for this derived work | closed: confirmed by e-mail (user, 2026-11-03) | S8.2 |
| P7 | **`../rosco_m68k` branch**: the hand-over says `release/version-2.42`, the checkout is on `planning/session-docs` (`release/version-2.42` exists only on origin; `maint/2.42` locally). Check which the build needs before rebuilding | open | S6.1 |
| P8 | **Test gaps** from Tests.md: an S1.4 test (Z80-saved `.BBC` file); an S3.6 test (command-line start) | done (2026-11-03): `t19z80file` for S1.4; S3.6 was already in `hostcheck.py` (autorun), missed by the crosscheck | S1.4, S3.6 |
| P9 | **Sibling checkouts ahead of the CI pins** (minix-st-2.0.4, r68k): bump the pins or not | later | S6.1, S6.3 |
| P10 | **Windows program untested in CI** | later | S3.3, S6.2 |
| P11 | **Releases and artifacts**: the Linux artifact without the extra zip; a tag `v*` publishes a release (workflow, ci-windows.sh, README) | done 2026-11-06: v0.1.0-beta released (pre-release), T20 ok | S6.2, S6.4 |

## Crosscheck 2026-11-03 (Spec, Plan, code)

Checked against the source:

* **Matches the Spec:** load address 0x40000 (`mkbare.py`); the firmware's
  100 Hz tick and ACR kept (`bare.c`); RAM store a quarter of the memory
  (`bare.c`); Ctrl-] quits and the 0.3 s idle end (`hostmain.cpp`); ACK
  release and SHA-256 pinned (`getack.sh`); three CI artifacts, actions
  pinned by hash; `OPENUP`, `TIME$` present; S1.6 has tests
  (`t17loadroom`, `k07errors` PROCdeep, `kw/HIMEM`).
* **Spec corrected:** S2.1 named "the 68010 instructions": only RTD and
  `MOVE CCR,<ea>` (as ASSEMBLER.md says). S4.5 now lists the real
  `*` command table, abbreviations, and the fall-back (Minix shell, else
  "Bad command"). S6.1 now names the CI pins.
* **Spec added:** S3.6, starting a program from the command line (Minix,
  PC programs, bare autorun); it was built but not written down.
* **Found, for the plan:**
  * P9: the local sibling checkouts are ahead of the CI pins
    (minix-st-2.0.4 `6d83d99` vs `feea47f`, r68k `24958aa` vs `23f4e66`).
    The images still match (T16), but a pin bump should be a decision,
    with the CI run as its test.
  * P10: the Windows program is built but not tested in CI (Tests.md
    gaps). Adding Wine to the CI run is possible but slow; decide.
  * P8 extended: tests for S3.6 (command-line start).
* **Plan vs Spec:** every open item traces to a Spec item; nothing in
  the Spec is without a test except S1.4, S3.6, S5.6, S8.x (Tests.md).

## Done

* 2026-11-03: P8, the test `t19z80file` (S1.4).
* 2026-11-03: planning files committed (d5280ec, pushed); Spec agreed:
  S1.6, S6.3, S7.1 confirmed.

* 2026-11-01: import from BBCZ80 eaae913 (6628baf); full regression
  passes locally; CI run 41342193509 succeeds, image byte-identical.

## Next step

Open for the user: P5, P7; later: P9, P10; on hold/parked: P3, P4.
