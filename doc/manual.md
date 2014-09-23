Intro to the display:
=====================

Astronauts interact with the computer by entering verb and noun pairs (or sometimes just verbs, e.g. V35). By pressing [VERB], the astronaut indicated to the computer that the next two digits are a command to do something, e.g. entering [VERB]16 tells the computer we want to monitor data in the three data display registers (from the top down,
R1, R2 and R3). Next the astronaut would enter the data to act on, e.g. [NOUN]44 tells the computer we want to act
on apoapsis, periapsis and time to apoapsis. Finally the astronaut hits [ENTR] to tell the computer to execute the request. So for example entering [VERB]16[NOUN]44[ENTR] tells the computer we want to display apoapsis, periapis and time to apoapsis in the three data registers.

If there is either a + or - sign in the data registers, the data displayed is in decimal, if the sign is absent then the data displayed is in octal.

You can enter the noun first if you so wish ie N44V16E is equivalent to V16N44E.

In this manual, I shall abbreviate the keypresses as follows:
V16N44E means key in [VERB]16[NOUN]44[ENTR].
Currently implemented programs:
Program 00: Idle
Program 11: Launch Monitor

Currently implemented verbs:
---------------------------

Verb 01: Display Octal component 1 in R1
Verb 02: Display Octal component 2 in R1
Verb 03: Display Octal component 3 in R1
Verb 04: Display Octal component 1 and 2 in R1 and R2
Verb 05: Display Octal component 1, 2 and 3 in R1, R2 and R3
Verb 06: Display decimal in R1 or R1, R2 or R1, R2, R3

Verb 11: Monitor Octal component 1 in R1
Verb 12: Monitor Octal component 2 in R1
Verb 13: Monitor Octal component 3 in R1
Verb 14: Monitor Octal component 1 and 2 in R1 and R2
Verb 15: Monitor Octal component 1, 2 and 3 in R1, R2 and R3
Verb 16: Monitor decimal in R1 or R1, R2 or R1, R2, R3

Verb 35: Lamp Test (this verb is a bit different, to run it we simply key in V35E).
Verb 37: Run program as specified by noun eg V37N11E executes Program 11.

Currently implemented nouns:
----------------------------

Noun 09: Alarm codes
Noun 44: Apoapsis as XXXX.X, periapsis as XXXX.X, time to apoapsis in
seconds
Noun 62: Surface speed, altitude ASL in meters, Vertical speed


Detailed Program 11 (Launch Monitor) listing:
This program is intended to be executed before launch, although you
can execute it at any time. P11 will first display noun 62. When
apoapsis (as displayed in R2) is greater than 50,000m, the KEY REL
lamp will flash, indicating the computer has more data to display.
When the astronaut kits [KEY REL], P11 displays noun 44.
This essentially is the orbit insertion display. Note at this point
the scale factor of the data changes to fit it in the display
registers. Apoapsis and periapsis should be read as XXXX.X km (in other
words, the precision is in hundreds of meters). The original AGC
didnt't have decimal places in the display registers, so we don't have
them here.
Detailed Program 30 (Hohmann transfer program) listing:
NOTE: P30 is similiar in functionality to the Protractor mod. Like
that mod, P30 will get you in the ballpark for a intercept, some
manual tweaking of your burn will be necessary.
WARNING: P30 assumes that your origin and destination planets orbits
inclination are the same, and your current orbit is circular and not
inclined. P30 will issue program alarms in this case.
To execute a Hohmann transfer, key in V37N30E. This will make the
neccesary calculations and update the display with V16N21. This will
display phase angle, ejection angle and ejection velocity. Any alarms
will be indicated by the PROG indicator. Alarms can be viewed with
V05N09E. The KEY REL indicator will light, indicating there is more
data to display. Hit the KEY REL button, and V16N22 will display phase
angle difference, ejection angle difference, and delta-v required. For
the most fuel-efficient approach, wait until phase angle difference is
close to 0, when wait until ejection angle difference is near 0, then
burn prograde until your velocity has increased by the amount
specified in register 3. Then adjust your trajectory slightly to get a
intercept (see note above)
Alarm codes:
When there is an program alarm, the PROG indicatorwill illuminate.
Keying in V05N09E will display the alarm codes, with R1 displaying the
latest alarm code, and R2 and R3 displaying previous codes. Alarm codes
are displayed in octal. Alarm codes currently inplemented are listed below:
x1xxx = warning
x2xxx = unrecoverable error, noun or program terminated
xx1xx series: KSP errors
xx2xx: orbital parameter errors
xx3xx: display errors
xx4xx: basaGC errors
01112: vessel out of power, telemetry unreliable
01113: Telemachus antenna off, telemetry unreliable
01114: not in a vessel, telemetry unreliable
01210: orbit not circular, manually perform mid-course correction
01211: orbit inclined, manually perform mid-course correction
01212: orbital inclinations differ, manually perform mid-course correction
01312: maneuver not calculated yet
02110: no connection to KSP
02111: no target set
02213: bodies not orbiting same parent
02214: unable to calculate maneuver, program terminated
02310: too much data to display
02311: cannot operate on noun with this verb
02410: JSON decoding error
