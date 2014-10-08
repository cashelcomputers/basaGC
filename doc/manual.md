Intro to the display:
=====================

Astronauts interact with the computer by entering verb and noun pairs (or sometimes just verbs, e.g. V35). By pressing [VERB], the astronaut indicated to the computer that the next two digits are a command to do something, e.g. entering [VERB]16 tells the computer we want to monitor data in the three data display registers (from the top down,
R1, R2 and R3). Next the astronaut would enter the data to act on, e.g. [NOUN]44 tells the computer we want to act
on apoapsis, periapsis and time to apoapsis. Finally the astronaut hits [ENTR] to tell the computer to execute the request. So for example entering [VERB]16[NOUN]44[ENTR] tells the computer we want to display apoapsis, periapis and time to apoapsis in the three data registers.

If there is either a + or - sign in the data registers, the data displayed is in decimal, if the sign is absent then the data displayed is in octal.

You can enter the noun first if you so wish ie N44V16E is equivalent to V16N44E.

In this manual, I shall abbreviate the keypresses as follows:
V16N44E means key in [VERB]16[NOUN]44[ENTR].


Currently implemented verbs:
---------------------------

- Verb 01: Display Octal component 1 in R1
- Verb 02: Display Octal component 2 in R1
- Verb 03: Display Octal component 3 in R1
- Verb 04: Display Octal component 1 and 2 in R1 and R2
- Verb 05: Display Octal component 1, 2 and 3 in R1, R2 and R3
- Verb 06: Display decimal in R1 or R1, R2 or R1, R2, R3

- Verb 11: Monitor Octal component 1 in R1
- Verb 12: Monitor Octal component 2 in R1
- Verb 13: Monitor Octal component 3 in R1
- Verb 14: Monitor Octal component 1 and 2 in R1 and R2
- Verb 15: Monitor Octal component 1, 2 and 3 in R1, R2 and R3
- Verb 16: Monitor decimal in R1 or R1, R2 or R1, R2, R3

- Verb 23: Load component 3 into R3

- Verb 35: Lamp Test (this verb is a bit different, to run it we simply key in V35E).
- Verb 36: Request fresh start
- Verb 37: Change program (major mode)

- Verb 75: Backup Liftoff Discrete
- Verb 82: Request orbital parameters display

Currently implemented nouns:
----------------------------

- Noun 09: Alarm codes
- Noun 17: Spacecraft altitude
- Noun 36: Mission Elapsed Time
- Noun 43: Geographic Position
- Noun 44: Apoapsis as XXXX.X, periapsis as XXXX.X, time to apoapsis in HMMSS
- Noun 62: Surface speed, altitude ASL in meters, Vertical speed

Currently implemented programs (major modes):
---------------------------------------------

- Program 00: AGC idling (called POO by mission control :)
- Program 11: Earth orbit insertion monitor
- Program 15: TMI initiate/cutoff

Detailed Program 11 listing:
----------------------------

IRL, P11 would be triggered automatically by receiving the liftoff discrete signal. At the moment you can start P11 by running Verb 75 (V75E). P11 will first display V16N62 (surface velocity, altitude rate of change, and altitude).

At any time during ascent, the user can run V82 to bring up the orbit insertion display. Apoapsis and periapsis should be read as XXXX.X km, and time to apoapsis should be read in HMMSS. The original AGC didnt't have decimal places in the display registers, so we don't have them here.

Alarm codes:
------------

When there is an program alarm, the PROG indicator will illuminate.
Keying in V05N09E will display the alarm codes, with R1 displaying the
most recent alarm code, R2 the previous alarm code, and R3 displaying the last alarm code, regardless if the alarm codes have been reset or not. Alarm codes are displayed in octal. Alarm codes currently inplemented are listed below:

