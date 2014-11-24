basaGC changelog
----------------

Please note that this file only contains changes from version 0.5.0 onwards. All dates are in dd/mm/yy format.

xx/xx/xx: version 0.5.5:
- Added alarm codes to help menu
- Many small bug fixes

17/11/14: version 0.5.4:
- Fixed a but where if user clicked on the log viewer (or help) dialog system close icon the window would get destroyed
rather than hidden
- Changed default log level to DEBUG
- Changed Noun 50 to display the first digit after decimal dot
- Fixed a bug where a backgrounded Monitor Verb couldn't be recalled with KEY REL button
- If there is no connection available to KSP, the NO ATT annunciator is illuminated and logged
- If KSP is paused or there is a problem with the Telemachus antenna, the STBY annunciator will illuminate and details
will be logged.

12/11/14: version 0.5.3:
- Added help viewer
- Added user-selectable display update interval
- Bug fixes

20/10/14: version 0.5.0:
- Added Program 15 (TMI initiate/cutoff)
- Lots of docstrings added
- Many bugfixes
- Added nouns: 17 (roll, pitch, yaw), 43 (latitude, longitude, altitude), 50 (surface velocity X, Y, Z)
- Added manubar to GUI
- Added items to menubar: settings, log viewer, quit, help/about
- Switched to <a href="http://nvie.com/posts/a-successful-git-branching-model/">Git Flow</a> development model
- Code cleanup
- Code refactoring for better PEP8 compliance
