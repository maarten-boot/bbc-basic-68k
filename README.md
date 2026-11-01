# bbc-basic-68k

A bbc basic for the 68k CPU targeted currently at the [rosco-m68k](https://github.com/rosco-m68k/rosco_m68k) and a planned [Minix2](https://github.com/maarten-boot/minix-st-2.0.4/tree/rosco-m68k) on top of that platform (work in progress).

## Origins

Based on the original Z80 implementation at: [BBCZ80](https://github.com/rtrussell/BBCZ80)

## License

We use the same [Zlib](https://en.wikipedia.org/wiki/Zlib_License) licence as the BBCZ80 it is derived from.

[Licence](licence.txt)

## Implementation

The original Z80 code was translated with the help of [Claude](https://claude.ai/)
and a full [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) syntax also derived from the existing code. Later corrections were carried out by [Claude](https://claude.ai/)
using the [Agon](https://github.com/breakintoprogram/agon-bbc-basic)
implementation and the manuals at [RiscOs](https://www.riscos.com/support/developers/bbcbasic/bbcref.html).

R.T. Russell provided valuable assistance in the compatibility testing.

For those interested in the full porting process, the mboot directory contains the full conversation, planning and reviews.

## Workbench

For running several Claude conversations at the same time,
on different git repos I built a tool.
It keeps the development platform fully separated from the user.

- [session-workbench](https://github.com/maarten-boot/multi-session-ssh-dev).

And a tool to easily browse syntax data (ebnf, lark, yacc, lemon).

- [syntax-viewer](https://github.com/maarten-boot/syntax-viewer)

Tools built with [Claude](https://claude.ai/) naturally.

## Builds

For compatibility with Minix the [ACK compiler](https://github.com/davidgiven/ack) is used, lightly patched: the builds fetch a [release of maarten-boot/ack](https://github.com/maarten-boot/ack/releases) (`src68k/tools/getack.sh`).

An extensive test set,
derived by Claude from the relevant documentation and the original Z80 and Agon implementations,
is executed at build time
to verify an accurate implementation

Additional tests are always very welcome.

Standalone:

- rosco-m68k using the r68k quick emulator
- a standalone bin file for the rosco sd card
- a linux build with the r68k emulator
- a windows build with the r68k emulator


## Acknowledgements

We gratefully acknowledge the original implementors of all components used.

- [BBCZ80](https://github.com/rtrussell/BBCZ80)
- [Agon-bbc-basic](https://github.com/breakintoprogram/agon-bbc-basic)
- [Minix2-st](https://github.com/EmmanuelKasper/minix-st-2.0.4)
- [ACK](https://github.com/davidgiven/ack)
- [RiscOs](https://www.riscos.com/support/developers/bbcbasic/bbcref.html)
- [Claude](https://claude.ai/)
