basaGC: Apollo Guidance Computer for Kerbal Space Program.
======

This is my reimplementation of the [Apollo Guidance Computer](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer)
(AGC) and Display/Keyboard (DSKY) for Kerbal Space Program.

This branch contains the pre-3.0 release version. This will often be broken. New features in this release are mainly
moving away from using Telemachus and using either KOS or kRPC. Stay tuned...

Screenshots here: http://imgur.com/a/Tj5mJ

Prerequisites:
---

- KSP (tested on 1.1.2), should work on any version that kRPC works on
- [Python 3.4](https://www.python.org/downloads/release/python-344/)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
- [kRPC](https://github.com/krpc/krpc/releases) >= 0.3.4

Installation:
---
See [doc/installation.md](https://github.com/cashelcomputers/basaGC/blob/master/doc/installation.md)

Running basaGC:
-----

To run basaGC, unzip the download to a folder of your choice. On Linux, in a terminal change to
that directory and type "./basagc.py", on Windows double-click on the file basagc.py.



Please Note! This is a work in progress. Only a few functions of the AGC are implemented. Some buttons and warning
lamps don't work.

Historical note: I have attempted to follow, as closely as possible and with the documentation available to me, the
real life AGC. It should be noted that this is a superficial recreation, not a hard-core simulation of the AGC. Google
"Virtual AGC" for that!

Known issues:
------------
- see [doc/known_issues.md](https://github.com/cashelcomputers/basaGC/blob/master/doc/known_issues.md)



***
Proudly bought to you by Buchanan and Son Avionics (a division of Buchanan and Son Aerospace).
