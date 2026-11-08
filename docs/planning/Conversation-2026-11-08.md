# Conversation 2026-11-08

Continues `Conversation-2026-11-07.md`; numbering continues.

## 30. Commit

* **User:** "commit". 0b19564 (Plan P9 r68k done, log entries 28-29). This entry is not committed.

## 31. Pushed

* **User:** "i pushed". 0b19564 on origin. Not committed.

## 32. Is P9 closed?

* **User:** "is P9 now closed ?"
* No: the r68k half is done; minix-st-2.0.4 is still pinned at feea47f. Origin rosco-m68k is 02e71dd (12 commits on); local 782d7b7 is one more, not pushed. None of them touch src/lib or include, so the BBC BASIC image should not change. Asked the user: bump to 02e71dd, or close P9 as not needed.

## 33. P9 closed

* **User:** "close P9, not needed; commit". Plan P9 closed (minix-st-2.0.4 pin stays feea47f). Committed with entries 30-33.

## 34. Pushed

* **User:** "i pushed". 97fd53a on origin. Not committed.

## 35. Where were the speed tests run?

* **User:** were the speed comparisons for Russell done on MAME too, or only r68k?
* Answer: the BBC vs EhBASIC timings on MAME only (bench68.py, rosco_m68k_010, -bios v242); the alignment share on r68k (cycle profiler), cross-checked against MAME (BM1 2.86 s vs 2.80 s). Not committed.

## 36. A third BASIC coming

* **User:** a translation of the C-based BBCSDL to 68k is being prepared as an additional BASIC for testing; the user will say when it is ready.
* Plan P14 added (waiting). Not committed.

## 37. Commit

* **User:** "commit". Entries 34-37 and Plan P14 committed.

## 38. Pushed

* **User:** "i pushed". b0dc9d1 on origin. Not committed.

## 39. BBCSDL 68k ready for testing

* **User:** the new BASIC is at `../BBCSDL/build/rosco/ROSCODE1.BIN`.
* BBCSDL (branch mboot-68k-dev, d928fa7): "BBC BASIC for rosco-m68k Console v0.51"; gcc 13.3.1 -O2, -mcpu=68010, 64-bit double in software, byte-wise LE heap (BBC_LEMEM), TIME from the firmware tick.
* `bench68.py`: third dialect `sdl` (not in the default set). BM1 int in MAME: 421 cs per 10000 passes (BBC 68k 260). Full run started. Not committed.

* Full run done: BBCSDL float/int (cs, 10000 passes): bm1 538/421, bm2 2850/2550, bm3 8570/8628, bm4 8134/8604, bm5 8647/9117, bm6 12763/12558, bm7 21704/20426, bm8 29469, sieve 8435/7485 (one pass; 1899 primes). 2-4x slower than BBC 68k, BM8 6.5x. Addendum written to the report (tmp/, untracked); bench68 README, Plan P14, Tests T19 updated. Not committed.

## 40. Commit; profile BBCSDL under r68k

* **User:** "commit; then profile BBCSDL under r68k". Committed entries 38-40 with the bench68 change.
