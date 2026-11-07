#!/usr/bin/env python3
"""What the byte-wise little-endian access costs bare BBC BASIC 68k.

	leprof.py PROFILE DISASSEMBLY NAME ...

PROFILE is build/prof/bare.prof from tools/bareprof.py (one run per
benchmark, then its three own: console, ramfile, sdfile); NAME ... names
the benchmarks in order.  DISASSEMBLY is m68k-elf-objdump -D of the
profiled image (build/prof/bare/ROSCODE1.BIN, at 0x40000); the symbols
come from build/prof/bare/bbcbasic.out (anm), as in bareprof.

Counted as byte-wise access to multi-byte data:
* the helpers LOAD4, LOAD5, STORE4, STORE5, LDLE4, STLE4, LDLE2, STLE2
  (all their instructions, rts too), and the bsr/jsr instructions that
  call them;
* elsewhere, every run of instructions with at least two move.b of the
  same base register at different displacements (a field of 2-5 bytes,
  not a stream such as (a4)+) that are put together (a shift by 8 or a
  swap between them) or copied memory to memory, with those shifts,
  swaps and stack moves.  Separate single bytes side by side (a string
  descriptor's length bytes, FOR's frame) are not counted.
For each such access the cycles of aligned big-endian code are estimated
as one move per field (move.l 16 cycles, move.w or move.b 12; a 5-byte
float is a move.l and a move.b), executed as often; aligned little-endian
adds rol.w #8 / swap / rol.w #8 (48) per long and rol.w #8 (22) per word.
The report gives per benchmark: the share of all cycles in byte-wise
access, and the share that aligned big-endian and aligned little-endian
data would save.  r68k charges 4 cycles per bit for a shift or rotate by
an immediate count, the 68000/68010 2 (6+2n, 8+2n for a long): those
instructions' cycles, and the totals, are corrected to the 68000's
before anything is counted.  An upper-bound estimate: inline byte reads that are not
in such runs (e.g. a single byte, or LOCATE's name compare) are not
counted, and neither are the register moves the helpers' interface needs.
"""

import bisect
import os
import re
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(os.path.dirname(HERE))
STAGE = os.path.join(TOP, 'build', 'ack', 'dist')
HELPERS = ('LOAD4', 'LOAD5', 'STORE4', 'STORE5', 'LDLE4', 'STLE4', 'LDLE2', 'STLE2')
# bytes moved by one call of each helper
HBYTES = {'LOAD4': 4, 'STORE4': 4, 'LDLE4': 4, 'STLE4': 4, 'LOAD5': 5, 'STORE5': 5,
          'LDLE2': 2, 'STLE2': 2}


def symbols():
    out = subprocess.run([os.path.join(STAGE, 'bin', 'anm'), '-n',
                          os.path.join(TOP, 'build', 'prof', 'bare', 'bbcbasic.out')],
                         env=dict(os.environ, ACKDIR=STAGE), capture_output=True,
                         text=True, check=True).stdout
    syms = []
    for l in out.split('\n'):
        w = l.split()
        if len(w) == 4 and w[1] == '0' and w[3] != '(NULL)':
            syms.append((int(w[0], 16), w[3]))
    return sorted(syms)


def disasm(path):
    """[(address, mnemonic, operands)] in address order"""
    ins = []
    for l in open(path):
        m = re.match(r'\s+([0-9a-f]+):\t[0-9a-f ]+\t(\S+)\s*(.*)', l)
        if m:
            ins.append((int(m.group(1), 16), m.group(2), m.group(3)))
    return ins


def profile(path):
    runs, cur = [], None
    for l in open(path):
        if l.startswith('#'):
            cur = {'cycles': int(l.split()[4]), 'pc': {}}
            runs.append(cur)
        else:
            pc, c, n = l.split()
            cur['pc'][int(pc, 16)] = (int(c), int(n))
    return runs


SHIFT = re.compile(r'(as|ls|ro|rox)[lr]([bwl])$')


def correct(runs, ins):
    """Shifts by an immediate count at 68000 cost (see above)."""
    op = {a: (mn, o) for a, mn, o in ins}
    for r in runs:
        for a, (c, n) in list(r['pc'].items()):
            if a not in op:
                continue
            mn, o = op[a]
            m = SHIFT.match(mn)
            if m and o.startswith('#') and n:
                k = int(o[1:].split(',')[0])
                good = ((8 if m.group(2) == 'l' else 6) + 2 * k) * n
                r['cycles'] -= c - good
                r['pc'][a] = (good, n)


MEMB = re.compile(r'%(a[0-7]|sp)@(?:\((-?\d+)\))?(?![+-])')   # (An) or d(An), not (An)+ / -(An)
GLUE = re.compile(r'^(lsl|lsr|rol|ror)[wl]$')


def ideal(nbytes):
    """(aligned big-endian, aligned little-endian) cycles for a field"""
    be = le = 0
    while nbytes >= 4:
        be += 16; le += 16 + 48; nbytes -= 4
    while nbytes >= 2:
        be += 12; le += 12 + 22; nbytes -= 2
    if nbytes:
        be += 12; le += 12
    return be, le


def runs_of_fields(ins, helper_ranges):
    """[(set of addresses, bytes)] of inline multi-byte accesses"""
    found = []
    i = 0
    while i < len(ins):
        cur, bases, glue = [], defaultdict(set), False
        j = i
        while j < len(ins):
            a, mn, op = ins[j]
            if any(s <= a < e for s, e in helper_ranges):
                break
            if mn == 'moveb':
                ms = [m for m in MEMB.finditer(op)]
                if not ms:
                    break
                for m in ms:
                    bases[m.group(1)].add(int(m.group(2) or 0))
                glue |= len(ms) == 2		# memory to memory: a copy
            elif mn == 'swap' or (GLUE.match(mn) and op.startswith('#8,')):
                glue = True
            elif mn == 'movel' and op.endswith('%sp@-'):
                pass
            elif mn in ('addql', 'addl', 'addqw') and op.startswith('#4,%sp'):
                pass
            else:
                break
            cur.append(a)
            j += 1
        nbytes = max((len(v) for v in bases.values()), default=0)
        if nbytes >= 2 and glue:
            found.append((set(cur), nbytes))
            i = j
        else:
            i += 1
    return found


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    runs = profile(sys.argv[1])
    ins = disasm(sys.argv[2])
    names = sys.argv[3:]
    correct(runs, ins)
    syms = symbols()
    addrs = [v for v, _ in syms]
    where = dict((n, v) for v, n in syms)
    hr = {}
    for h in HELPERS:
        if h in where:
            k = addrs.index(where[h])
            hr[h] = (where[h], syms[k + 1][0])
    # LOAD5 falls into LOAD4 and STORE5 into STORE4: their ranges are the
    # one extra instruction; the entry counts say which field size ran
    fields = runs_of_fields(ins, list(hr.values()))
    calls = {}
    for a, mn, op in ins:
        if mn in ('bsrs', 'bsrw', 'bsrl', 'bsr', 'jsr'):
            m = re.match(r'(?:0x)?([0-9a-f]+)', op)
            if m:
                t = int(m.group(1), 16)
                for h, (s, e) in hr.items():
                    if t == s:
                        calls[a] = h
    print('%-8s %12s %8s %8s %8s' % ('', 'cycles', 'byte-LE', 'save BE', 'save LE'))
    for name, r in zip(names + ['console', 'ramfile', 'sdfile'], runs):
        pc = r['pc']
        cost = be = le = 0
        for h, (s, e) in hr.items():
            for a in range(s, e, 2):
                cost += pc.get(a, (0, 0))[0]
        # executions of each field size via the helpers: entries
        n4 = pc.get(hr['LOAD4'][0], (0, 0))[1] - pc.get(hr['LOAD5'][0], (0, 0))[1]
        n5 = pc.get(hr['LOAD5'][0], (0, 0))[1]
        s4 = pc.get(hr['STORE4'][0], (0, 0))[1] - pc.get(hr['STORE5'][0], (0, 0))[1]
        s5 = pc.get(hr['STORE5'][0], (0, 0))[1]
        for n, nb in ((n4, 4), (n5, 5), (s4, 4), (s5, 5)):
            b, l = ideal(nb)
            be += n * b; le += n * l
        for h in ('LDLE4', 'STLE4', 'LDLE2', 'STLE2'):
            if h in hr:
                n = pc.get(hr[h][0], (0, 0))[1]
                b, l = ideal(HBYTES[h])
                be += n * b; le += n * l
        for a, h in calls.items():
            cost += pc.get(a, (0, 0))[0]
        for addrset, nb in fields:
            c = sum(pc.get(a, (0, 0))[0] for a in addrset)
            n = max(pc.get(a, (0, 0))[1] for a in addrset)
            cost += c
            b, l = ideal(nb)
            be += n * b; le += n * l
        t = max(r['cycles'], 1)
        print('%-8s %12d %7.1f%% %7.1f%% %7.1f%%' % (name, t, 100.0 * cost / t,
              100.0 * (cost - be) / t, 100.0 * (cost - le) / t))
    print('\n%d inline field accesses found outside the helpers' % len(fields))


if __name__ == '__main__':
    main()
