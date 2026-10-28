# bbc-basic-68k

A bbc basic for the 68k CPU targeted currently at the [rosco-m68k]([https://github.com/rosco-m68k/rosco_m68k) <br>and a planned [Minix2](https://github.com/maarten-boot/minix-st-2.0.4/tree/rosco-m68k) on top of that platform (work in progress).

## Origins

Based on the original Z80 implementation at: [BBCZ80](https://
github.com/rtrussell/BBCZ80)

## License

We use the same [Zlib](https://en.wikipedia.org/wiki/Zlib_License) licene as the BBCZ80 it is derived from. 

[Licence](license.txt)

## Implementation

The original Z80 code was translated with the help of Claude and a full ebnf syntax also derived from the existing code. Later corrections were carried aut by Claude using the [Agon](https://github.com/breakintoprogram/agon-bbc-basic) implementation and the manuals at [RiscOs](https://www.riscos.com/support/developers/bbcbasic/bbcref.html).

## Builds

For compatibility with Minix the [ACK compiler](https://github.com/davidgiven/ack/compare/default...maarten-boot:ack:rosco-minix68k) is used lightly patched.

A extensive test set is executed at build time to verify a accurate implementation (additional test are very welcome).

Standalone:

- rosco-m68k using the r68k quick emulator
- a standalone bin file for the rosco sd card
- a full rosco sd image file
- a linux build with the r68k emulator
- a windows build with the r68k emulator


## Acknowledgements

We gracefully acknowledge the original implementors of all components used.

- [BBCZ80](https://github.com/rtrussell/BBCZ80)
- [Agon-bbc-basic](https://github.com/breakintoprogram/agon-bbc-basic)
- [Minix2-st](https://github.com/EmmanuelKasper/minix-st-2.0.4)
- [ACK](https://github.com/davidgiven/ack)
- [RiscOs](https://www.riscos.com/support/developers/bbcbasic/bbcref.html) 
- 