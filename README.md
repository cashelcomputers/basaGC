basaGC
======

Apollo Guidance Computer for Kerbal Space Program

Thanks to Ron Burkey (<info@sandroid.org>) for VirtualAGC!

This is my reimplementation of the Apollo Guidance Computer (AGC) and Display/Keyboard (DSKY) for Kerbal Space Program.

_IMPORTANT:_ develop branch is broken, please use master branch for now.

UPDATE 16/3/16: I haven't looked at this project for quite some time, but i'm back from Duna now :) my next goal is to 
drop wxPython and move to PyQt5, so I can finally get away from Python 2.7 stay tuned...

Prerequisites:

- KSP (tested on 1.0.4)
- python 3.x
- PyQt5
- Telemachus mod for KSP (tested on 1.4.30)
- Mechjeb mod

To run basaGC, unzip the download to a folder of your choice. On Linux (since Linux rulz :) in a terminal change to
that directory and type "./basagc.py", on Windows double-click on the file basagc.py.

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
