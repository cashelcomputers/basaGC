basaGC
======

Apollo Guidance Computer for Kerbal Space Program

Thanks to Ron Burkey (<info@sandroid.org>) for VirtualAGC!

This is my reimplementation of the Apollo Guidance Computer (AGC) and Display/Keyboard (DSKY) for Kerbal Space Program.

_IMPORTANT:_ I have switched to the Gitflow development model. The most bleeding edge version can now be found in branch
<a href="https://github.com/cashelcomputers/basaGC/tree/develop">"develop"</a>. Stable version can be obtained from
branch <a href="https://github.com/cashelcomputers/basaGC/tree/master">"master"</a>.

Prerequisites:

- KSP (tested on 0.25)
- python 2.7.x
- wxPython 2.8.x (may work with 3.0, but this is untested. YMMV)
- Telemachus mod for KSP (tested on 1.4.27)
- Mechjeb mod

To run basaGC, unzip the download to a folder of your choice. On Linux (since Linux rulz :) in a terminal change to
that directory and type "./basagc.py", on Windows double-click on the file basagc.py.

For Windows users, you can get wxPython from here:
<a href=http://downloads.sourceforge.net/project/wxpython/wxPython/2.8.12.0/wxPython2.8-win32-unicode-2.8.12.0-py27.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fwxpython%2Ffiles%2FwxPython%2F2.8.12.0%2F&ts=1391681128&use_mirror=
hivelocity>link</a>

Please Note! This is a work in progress. Only a few functions of the AGC are implemented. Some buttons and warning
lamps don't work.

Historical note: I have attempted to follow, as closely as possible 
and with the documentation available to me, the real life AGC. 
However, some things have to be changed for KSP, for a number of 
reasons.

Known issues:
------------
- see doc/known_issues.md



***
Proudly bought to you by Buchanan and Son Avionics (a division of Buchanan and Son Aerospace).
