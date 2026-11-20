#!/usr/bin/env python3
"""Where BBCSDL for the 68k spends its 68000 cycles (cf. bareprof.py).

	sdlprof.py [-d DIR] [-n TOP] [-t KIND ...] [-l LABEL] [PROG ...]

DIR is BBCSDL's rosco build (default ../BBCSDL/build/rosco: ROSCODE1.BIN,
bbcbasic.elf, bbcbasic.map).  The programs are test/bench68's (default
all), with the timing lines replaced by writes of 1 and 2 to &FFFFF0
(start and stop the profiler); KIND is float or int (default both).  All
run in one boot of the image under the profiling r68k, build/r68kprof
(r68k 7b95236 or later; see bench.py), without -d (firmware console;
under stdbuf -o0, or the prompt waits in the buffer),
R68K_RAM=5M.  BBCSDL copies itself to its link address (0x2000), so the
ELF's symbols (nm) name the addresses; the link map gives each address's
object, grouped as:
	interp	bbmain.o, bbexec.o, bbeval.o (the interpreter)
	os	bbccos.o, bbcrosco.o, posix.o, lefix.o, duartirq.o
	float	libgcc's soft-float (__adddf3, __muldf3, ...)
	intop	libgcc's integer helpers (__mulsi3, __divsi3, 64-bit ...)
	libm	newlib's maths library (sin, log, pow, ...)
	libc	the rest of newlib
The report gives per program the cycles and the groups' shares, then the
TOP functions (from 0.5 %); it is printed and saved in build/prof
(sdl-LABEL.txt, or sdl.txt).  Little-endian access is not split out: the
macros are inlined into the interpreter.
"""

import argparse
import bisect
import glob
import os
import pty
import re
import select
import subprocess
import sys
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
TOP = os.path.dirname(SRC)
EMU = os.path.join(TOP, 'build', 'r68kprof', 'r68k')
PROF = os.path.join(TOP, 'build', 'prof')
GROUPS = ('interp', 'os', 'float', 'intop', 'libm', 'libc')
INTERP = ('bbmain.o', 'bbexec.o', 'bbeval.o')
OS = ('bbccos.o', 'bbcrosco.o', 'posix.o', 'lefix.o', 'duartirq.o')


def program(path, kind):
    """the program's lines with the profiler's start and stop, or None"""
    text = open(path).read()
    if kind == 'int' and '@' not in text.replace('@T0@', '').replace('@T1@', ''):
        return None
    text = text.replace('@T0@', '?&FFFFF0=1').replace('@T1@', '?&FFFFF0=2')
    text = text.replace('@', '%' if kind == 'int' else '')
    return [l for l in text.splitlines() if l.strip()]


def symbols(elf):
    """[(address, name)] of the text symbols"""
    out = subprocess.run(['nm', '-n', elf], capture_output=True, text=True, check=True).stdout
    syms = []
    for l in out.split('\n'):
        w = l.split()
        if len(w) == 3 and w[1] in 'tTwW':
            syms.append((int(w[0], 16), w[2]))
    return syms


def group_of(obj):
    base = os.path.basename(obj)
    m = re.search(r'\((.*)\)$', base)
    member = m.group(1) if m else base
    if member in INTERP:
        return 'interp'
    if member in OS:
        return 'os'
    if 'libm.a' in obj:
        return 'libm'
    if 'libgcc.a' in obj:
        if re.search(r'double|float|fix|df2|sf2|fpgnulib|xfgnulib', member):
            return 'float'
        return 'intop'
    return 'libc'


def layout(mapfile):
    """[(start, end, group)] of the .text input sections, from the link map"""
    parts, inside, pend = [], False, None
    for l in open(mapfile):
        if l.startswith('.text '):
            inside = True
            continue
        if inside and re.match(r'^\.\w', l):
            break
        if not inside:
            continue
        m = re.match(r'^ (\.text\S*)\s*$', l)
        if m:
            pend = m.group(1)
            continue
        m = re.match(r'^ (?:(\.text\S*)\s+)?\s*0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S.*)$', l)
        if m and (m.group(1) or pend):
            a, n = int(m.group(2), 16), int(m.group(3), 16)
            if n:
                parts.append((a, a + n, group_of(m.group(4).strip())))
        pend = None
    return sorted(parts)


def run(image, lines):
    """type LINES at BBCSDL's prompt; the profile's runs [(cycles, {pc: cycles})]"""
    os.makedirs(PROF, exist_ok=True)
    pfile = os.path.join(PROF, 'sdl.prof')
    if os.path.exists(pfile):
        os.remove(pfile)
    fd, slave = pty.openpty()
    p = subprocess.Popen(['stdbuf', '-o0', EMU, image], stdin=slave, stdout=slave, stderr=subprocess.DEVNULL,
                         cwd=os.path.dirname(EMU),
                         env=dict(os.environ, R68K_RAM='5M', R68K_PROF=pfile))
    os.close(slave)
    buf = [b'']

    def until(pattern, limit):
        end = time.time() + limit
        while True:
            m = re.search(pattern, buf[0])
            if m:
                out, buf[0] = buf[0][:m.end()], buf[0][m.end():]
                return out
            r, _, _ = select.select([fd], [], [], max(0, end - time.time()))
            if not r:
                raise TimeoutError
            buf[0] += os.read(fd, 65536)

    out = b''
    try:
        out += until(rb'\n>', 60)
        for l in lines:
            for c in (l + '\r').encode('latin-1'):
                os.write(fd, bytes([c]))
                time.sleep(0.002)
            out += until(rb'(^|\n)>', 1800)
    except TimeoutError:
        out += buf[0] + b'\n(timeout)'
    finally:
        p.kill()
        p.wait()
    with open(os.path.join(PROF, 'sdl.out'), 'wb') as f:
        f.write(out)
    runs, cur = [], None
    if os.path.exists(pfile):
        for l in open(pfile):
            if l.startswith('#'):
                cur = [int(l.split()[4]), {}]
                runs.append(cur)
            else:
                pc, c, n = l.split()
                cur[1][int(pc, 16)] = int(c)
    return runs, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', default=os.path.join(os.path.dirname(TOP), 'BBCSDL', 'build', 'rosco'))
    ap.add_argument('-n', type=int, default=8)
    ap.add_argument('-t', action='append', choices=['float', 'int'])
    ap.add_argument('-l', default='')
    ap.add_argument('progs', nargs='*')
    a = ap.parse_args()
    if not os.path.exists(EMU):
        sys.exit('sdlprof: build the profiling r68k first (build/r68kprof)')
    progs = sorted(glob.glob(os.path.join(SRC, 'test', 'bench68', '*.bas')))
    if a.progs:
        progs = [p for p in progs if os.path.basename(p)[:-4] in a.progs]
    names, lines = [], []
    for k in a.t or ['float', 'int']:
        for p in progs:
            ls = program(p, k)
            if ls:
                names.append('%s-%s' % (os.path.basename(p)[:-4], k))
                lines += ['NEW'] + ls + ['RUN']
    syms = symbols(os.path.join(a.d, 'bbcbasic.elf'))
    saddr = [s for s, _ in syms]
    parts = layout(os.path.join(a.d, 'bbcbasic.map'))
    pstart = [s for s, _, _ in parts]
    runs, out = run(os.path.join(a.d, 'ROSCODE1.BIN'), lines)
    if len(runs) != len(names):
        sys.exit('sdlprof: %d profiles for %d programs; see build/prof/sdl.out'
                 % (len(runs), len(names)))
    rep = ['%-12s %12s ' % ('', 'cycles') + ' '.join('%7s' % g for g in GROUPS) + '   other']
    tops = []
    for name, (total, pcs) in zip(names, runs):
        g, f = defaultdict(int), defaultdict(int)
        for pc, c in pcs.items():
            k = bisect.bisect_right(pstart, pc) - 1
            g[parts[k][2] if k >= 0 and pc < parts[k][1] else 'other'] += c
            k = bisect.bisect_right(saddr, pc) - 1
            f[syms[k][1] if k >= 0 else '?'] += c
        t = max(total, 1)
        rep.append('%-12s %12d ' % (name, total) + ' '.join('%6.1f%%' % (100.0 * g[x] / t)
                                                          for x in GROUPS)
                   + ' %6.1f%%' % (100.0 * g['other'] / t))
        top = sorted(f.items(), key=lambda x: -x[1])[:a.n]
        tops.append('%s: ' % name + ', '.join('%s %.1f%%' % (n, 100.0 * c / t)
                                              for n, c in top if c * 200 >= t))
    text = '\n'.join(rep + [''] + tops) + '\n'
    print(text, end='')
    with open(os.path.join(PROF, 'sdl-%s.txt' % a.l if a.l else 'sdl.txt'), 'w') as fo:
        fo.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
