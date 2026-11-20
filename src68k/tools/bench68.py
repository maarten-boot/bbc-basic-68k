#!/usr/bin/env python3
"""Rugg/Feldman BM1-BM8 and the sieve (test/bench68) on 68000 BASICs in MAME.

	bench68.py [-b BASIC ...] [-i IMAGE] [--bios V] [-t KIND ...] [-k] [PROG ...]

BASIC is bbc (bare BBC BASIC 68k, build/bare/ROSCODE1.BIN, make bare) or
eh (EhBASIC 68k 3.52 for rosco_m68k firmware 2.x, build/ehbasic/dl/
ehbasic.bin, from github.com/rosco-m68k/example_programs) or sdl (BBCSDL
translated to the 68k, ../BBCSDL/build/rosco/ROSCODE1.BIN); default bbc
and eh.
-i IMAGE replaces the image of the (single) BASIC given with -b.  KIND is
float or int (the variable type, see test/bench68/README.md); default
both.  Each BASIC and kind is one boot of the rosco-emulator
(rosco-emulator:local, rosco_m68k_010, -bios V, default v242 as on the
board, 5 MB), the machine whose timing matches the board.  The programs
are typed a character at a time, each after the echo of the one before
(EhBASIC polls the console and loses characters typed ahead), then RUN.
The timing is the BASIC's own clock: TIME, or the firmware's 100 Hz tick
at &40C for EhBASIC.

Prints a table of centiseconds (10000 passes; divide by 10 for the
published 1000-pass figures) and writes it, with the sessions' logs, to
build/bench68.  -k keeps the work directories.  PROG: names of programs
(default all of test/bench68/*.bas).
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
TOP = os.path.dirname(SRC)
MINIX = os.environ.get('MINIX', os.path.join(os.path.dirname(TOP), 'minix-st-2.0.4'))
TOOLS = os.path.join(MINIX, 'src', 'rosco', 'tools')
OUT = os.path.join(TOP, 'build', 'bench68')

BASICS = {
    'bbc': dict(image=os.path.join(TOP, 'build', 'bare', 'ROSCODE1.BIN'),
                prompt='>', boot='>',
                t0='TT=TIME', t1='PRINT "BENCH {name} ";TIME-TT', int='%'),
    'eh': dict(image=os.path.join(TOP, 'build', 'ehbasic', 'dl', 'ehbasic.bin'),
               prompt='Ready', boot='Ready',
               t0='TT=LEEK($40C)', t1='PRINT "BENCH {name} ";LEEK($40C)-TT', int='&'),
    'sdl': dict(image=os.path.join(os.path.dirname(TOP), 'BBCSDL', 'build', 'rosco', 'ROSCODE1.BIN'),
                prompt='>', boot='>',
                t0='TT=TIME', t1='PRINT "BENCH {name} ";TIME-TT', int='%'),
}


def program(path, basic, kind):
    """The program's lines for BASIC and KIND, or None if it has no such form."""
    b = BASICS[basic]
    name = os.path.basename(path)[:-4]
    text = open(path).read()
    if kind == 'int' and '@' not in text.replace('@T0@', '').replace('@T1@', ''):
        return None
    text = text.replace('@T0@', b['t0']).replace('@T1@', b['t1'].format(name=name))
    text = text.replace('@', b['int'] if kind == 'int' else '')
    return [l for l in text.splitlines() if l.strip()]


def typed(line):
    """Session commands: LINE a character at a time, each after its echo."""
    out = []
    for c in line:
        out += ['type \\x20' if c == ' ' else 'type ' + c, 'expect ' + c + '\t20']
    return out + ['type \\r', 'sleep 0.2']


def run(basic, kind, progs, image, bios, keep):
    b = BASICS[basic]
    w = os.path.join(OUT, '%s-%s' % (basic, kind))
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    os.chmod(w, 0o777)			# (the container's user writes the log)
    shutil.copy(image, os.path.join(w, 'ROSCODE1.BIN'))
    subprocess.run([sys.executable, os.path.join(TOOLS, 'mkfat.py'), '-s', '65536', '-o', '2048',
                    os.path.join(w, 'fat.img'), os.path.join(w, 'ROSCODE1.BIN')],
                   check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, os.path.join(TOOLS, 'mksd.py'), os.path.join(w, 'rosco_sd.bin'),
                    '06:' + os.path.join(w, 'fat.img')], check=True, stdout=subprocess.DEVNULL)
    ses = ['expect %s\t300' % b['boot']]
    names = []
    for p in progs:
        lines = program(p, basic, kind)
        if lines is None:
            continue
        names.append(os.path.basename(p)[:-4])
        ses += typed('NEW') + ['expect %s\t60' % b['prompt']]
        for l in lines:
            ses += typed(l)
        ses += typed('RUN') + ['expect %s\t1800' % b['prompt']]
    with open(os.path.join(w, 'session.txt'), 'w') as f:
        f.write('\n'.join(ses) + '\n')
    for f in os.listdir(w):
        os.chmod(os.path.join(w, f), 0o666)
    subprocess.run(['docker', 'run', '--rm', '-e', 'SDL_VIDEODRIVER=dummy',
                    '-v', w + ':/work', '-v', TOOLS + ':/tools:ro',
                    '--entrypoint', 'python3', 'rosco-emulator:local', '/tools/mamesession.py',
                    '-a', '-bios %s -ram 5m' % bios, '/opt/rosco', '/work/rosco_sd.bin',
                    '/work/session.log', '/work/session.txt'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log = open(os.path.join(w, 'session.log'), 'rb').read().decode('latin-1').replace('\r', '')
    shutil.copy(os.path.join(w, 'session.log'), os.path.join(OUT, '%s-%s.log' % (basic, kind)))
    res = {}
    for n in names:
        m = re.search(r'BENCH %s +(-?\d+)' % n, log)
        res[n] = int(m.group(1)) if m else None
    if '[session: timeout' in log:
        print('%s %s: the session timed out; see %s' % (basic, kind,
              os.path.join(OUT, '%s-%s.log' % (basic, kind))))
    if not keep:
        shutil.rmtree(w)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-b', action='append', choices=sorted(BASICS))
    ap.add_argument('-i')
    ap.add_argument('--bios', default='v242')
    ap.add_argument('-t', action='append', choices=['float', 'int'])
    ap.add_argument('-k', action='store_true')
    ap.add_argument('progs', nargs='*')
    a = ap.parse_args()
    basics = a.b or ['bbc', 'eh']
    kinds = a.t or ['float', 'int']
    if a.i and len(basics) != 1:
        sys.exit('-i needs a single -b')
    progs = sorted(glob.glob(os.path.join(SRC, 'test', 'bench68', '*.bas')))
    if a.progs:
        progs = [p for p in progs if os.path.basename(p)[:-4] in a.progs]
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for b in basics:
        for k in kinds:
            res[b, k] = run(b, k, progs, a.i or BASICS[b]['image'], a.bios, a.k)
    cols = [(b, k) for b in basics for k in kinds]
    names = [os.path.basename(p)[:-4] for p in progs]
    head = '| Program | ' + ' | '.join('%s %s' % c for c in cols) + ' |'
    rows = [head, '|---' * (len(cols) + 1) + '|']
    for n in names:
        cells = []
        for c in cols:
            v = res[c].get(n, 'n/a') if n in res[c] else 'n/a'
            cells.append('fail' if v is None else str(v))
        rows.append('| %s | %s |' % (n, ' | '.join(cells)))
    table = '\n'.join(rows)
    print(table)
    with open(os.path.join(OUT, 'results.md'), 'w') as f:
        f.write('Centiseconds, 10000 passes, MAME rosco_m68k_010 -bios %s\n\n%s\n' % (a.bios, table))
    return 0


if __name__ == '__main__':
    sys.exit(main())
