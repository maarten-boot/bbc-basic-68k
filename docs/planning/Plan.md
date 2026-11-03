# Plan: BBC BASIC 68k

The work from 2026-11-03 on, in this repo. History before that:
`mboot/PORT_PLAN.md` (phases 0-6, done) and the BBCZ80 log (entries
1-121, `../BBCZ80/mboot/log/`, branch `mboot/conversation-log`).
Spec IDs refer to `Spec.md`, test IDs to `Tests.md`.

## Open items

| ID | Item | Status | Spec |
|---|---|---|---|
| P1 | **docs/planning**: Spec.md, Plan.md, Tests.md, conversation log; fold in the hand-over note | Spec agreed (2026-11-03); crosscheck Spec/Plan/code next | all |
| P2 | **BBCZ80:** a README line pointing here; keep or remove `src68k/` there | the user's choice | - |
| P3 | **Minix items** | on hold until the user says so | S3.1 |
| P3a | c_l5b_recovery fails only in the full Minix bascheck session | on hold | S1.6 |
| P3b | c_l1_core and x02bigarr need more than `-S 64k` | on hold | S1.5, S3.1 |
| P3c | TIME$ under Minix | on hold | S1.1 |
| P3d | x05align under Minix | on hold | S1.1 |
| P4 | **Interpreter speed-up**: CON (decimal constants re-parsed every pass), LOCATE, ITEM/XEQ1 dispatch; ~6000 cycles per FOR pass now | parked until needed | S7.1 |
| P5 | **Agon emulator** for the tests | optional; building it needs permission | S1.1 |
| P6 | **"BBC BASIC" name**: confirm with R.T. Russell whether the name may be used for this derived work | open (flagged) | S8.2 |
| P7 | **`../rosco_m68k` branch**: the hand-over says `release/version-2.42`, the checkout is on `planning/session-docs` (`release/version-2.42` exists only on origin; `maint/2.42` locally). Check which the build needs before rebuilding | open | S6.1 |
| P8 | **Test gaps** from Tests.md: an S1.4 test (Z80-saved `.BBC` file) | proposed | S1.4 |

## Done

* 2026-11-03: planning files committed (d5280ec, pushed); Spec agreed:
  S1.6, S6.3, S7.1 confirmed.

* 2026-11-01: import from BBCZ80 eaae913 (6628baf); full regression
  passes locally; CI run 41342193509 succeeds, image byte-identical.

## Next step

Crosscheck Spec.md, Plan.md and the code (P1), on the user's go.
