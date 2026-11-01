# z80: R.T. Russell's Z80 BBC BASIC, the original of this port

These files are copied unchanged from [BBCZ80](https://github.com/rtrussell/BBCZ80),
version 5.4 (commit e4ae9ca, 2026-10-27, "Fix RESTORE DATA in a PROC/FN"),
under its zlib licence (`../licence.txt`). Russell's own README is
`README-BBCZ80.md`; `WHATSNEW.TXT` is his list of the version 5 features.

The 68k port uses them as follows:

| File | Used by | For |
|---|---|---|
| `src/MAIN.Z80` | `src68k/tools/mkmain.py` (every build) | The keyword table, error messages and LEXAN lists in `main.s` |
| `bin/cpm/BBCBASIC.COM` | `src68k/tools/runcpm.py`, under RunCPM | The Z80 reference output of a test (`bascheck.py`, when a `.ref` is missing) and tokenising the demo programs (`mkdemo.py --progs`) |
| `tests/*.BBC` | `test/bas/u_*.in`, `mkweb.py`, `fatcheck.py`, `bareprof.py` | Russell's test programs, run on the 68k version |
| `src/*.Z80` | people | The reference for the 68k code, whose comments use the Z80 labels |

To take a newer version from BBCZ80, copy the files again, then:
* update the commit above;
* run `make` (a new `main.s`) and the full test set;
* delete any `.ref` whose test should get a new Z80 reference.

The name "BBC BASIC" is used by permission of the British Broadcasting
Corporation (see `README-BBCZ80.md`).
