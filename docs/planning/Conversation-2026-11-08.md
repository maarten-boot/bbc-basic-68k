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
