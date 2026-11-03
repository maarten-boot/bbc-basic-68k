# Conversation log, 2026-11-03

Continues the BBCZ80 log (`../BBCZ80/mboot/log/`, entries 1-121);
numbering restarts here.

## 1. Investigate the hand-over

* **User:** "investigate the current directory and report; it is a
  handover from a previous project, we will continue here".
* Read `docs/planning/Handover-2026-11-03.md` (untracked), the README,
  the import commit 6628baf, the layout, and the BBCZ80 log entries
  120-121. main = import = 6628baf, tree clean except the hand-over.
  Build outputs present in `build/`.
* **Found:** `../rosco_m68k` is on `planning/session-docs`, not
  `release/version-2.42` as the hand-over says (Plan.md P7).
* Reported the state, layout, working rules and pending items; proposed
  starting item 1.

## 2. Start item 1: docs/planning

* **User:** "yes, start on item 1".
* Created branch `planning/session-docs` (from main 6628baf).
* Wrote drafts: `Spec.md` (S1-S8, from PORT_PLAN, Z80_DIFFERENCES,
  CONVENTIONS, ASSEMBLER, the target READMEs and the tools),
  `Tests.md` (T1-T19 traced to the Spec, plus gaps), `Plan.md` (P1-P8)
  and this log. Not committed.
* Checked the bascheck counts: 58 + 130 + 48 = 236 tests; host/hostwin
  skip the two `#typed` ones (kw/INKEY, kw/INKEY_STRING), hence 234.

## 3. Commit

* **User:** "commit; keep the handover note". Committed the hand-over
  note and the four planning files on `planning/session-docs`. Spec
  questions (the *(as built)* items S6.3 and S7.1, and S1.6) still open
  for review.

## 4. Spec confirmed

* **User:** "pushed; confirm S6.3, S7.1 and S1.6; all yes". d5280ec
  pushed. Spec.md: status agreed, the *(as built)* marks removed;
  Plan.md: P1 now "crosscheck next", done entry added. Not committed.

## 5. Commit; the crosscheck

* **User:** "commit; then start the crosscheck". Committed 6a63eaf.
* Crosscheck of Spec, Plan and code (Plan.md, "Crosscheck 2026-11-03"):
  most items match the source. Spec corrected (S2.1: only RTD and MOVE
  CCR from the 68010; S4.5: the real `*` command table and fall-back;
  S6.1: the CI pins) and S3.6 added (command-line start). New plan
  items P9 (local checkouts ahead of the CI pins) and P10 (Windows
  program untested in CI); P8 extended with S3.6. Not committed.

## 6. Decisions on the open items

* **User:** "commit; P9 and P10 later; P1 ok; P2 leave it; P3 on hold;
  P4 parked; P6 is confirme[d] by email; P8 todo".
* Plan.md: P1 done (Spec changes accepted), P2 closed (left as it is),
  P6 closed (confirmed by e-mail; Spec S8.2 updated), P8 to do, P9 and
  P10 later; P3 on hold, P4 parked as before. Committed.
