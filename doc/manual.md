Intro to the display:
=====================

Astronauts interact with the computer by entering verb and noun pairs (or sometimes just verbs, e.g. V35). By pressing
[VERB], the astronaut indicated to the computer that the next two digits are a command to do something, e.g. entering
[VERB]16 tells the computer we want to monitor data in the three data display registers (from the top down,
R1, R2 and R3). Next the astronaut would enter the data to act on, e.g. [NOUN]44 tells the computer we want to act
on apoapsis, periapsis and time to apoapsis. Finally the astronaut hits [ENTR] to tell the computer to execute the
request. So for example entering [VERB]16[NOUN]44[ENTR] tells the computer we want to display apoapsis, periapis and
time to apoapsis in the three data registers.

If there is either a + or - sign in the data registers, the data displayed is in decimal, if the sign is absent then the
data displayed is in octal.

You can enter the noun first if you so wish ie N44V16E is equivalent to V16N44E.

In this manual, I shall abbreviate the keypresses as follows:
V16N44E means key in [VERB]16[NOUN]44[ENTR].

*PLEASE NOTE:* the following lists may lag behind the program. For the latest info on verbs, nouns and programs,
consult the source.

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
- Verb 21: Load component 1 into R1
- Verb 22: Load component 2 into R2
- Verb 23: Load component 3 into R3

- Verb 35: Lamp Test (this verb is a bit different, to run it we simply key in V35E).
- Verb 36: Request fresh start
- Verb 37: Change program (major mode)

- Verb 75: Backup Liftoff Discrete
- Verb 82: Request orbital parameters display
- Verb 99: Please enable engine

Currently implemented nouns:
----------------------------

- Noun 09: Alarm codes
- Noun 14: Burn error display
- Noun 17: Spacecraft attitude
- Noun 25: Spacecraft mass
- Noun 30: Target ID
- Noun 31: Max thrust
- Noun 33: Time to ignition (TIG)
- Noun 36: Mission Elapsed Time
- Noun 38: Specific Impulse (Isp)
- Noun 43: Geographic Position
- Noun 44: Apoapsis as XXXX.X, periapsis as XXXX.X, time to apoapsis in HMMSS
- Noun 50: Surface velocity display
- Noun 62: Surface speed, altitude ASL in meters, Vertical speed
- Noun 95: TMI burn data display

Currently implemented programs (major modes):
---------------------------------------------

- Program 00: AGC idling (called POO by mission control :)
- Program 01: Prelaunch or service - Initialization program
- Program 02: Prelaunch or service - Gyrocompassing program
- Program 11: Earth orbit insertion monitor
- Program 15: TMI calculate
- Program 31: MOI burn calc
- Program 40: TMI execute

How to set up basaGC for launch:
----------------------------

Key in V37E01E (start program 01) to start the IMU. After 10 seconds, confirm NO ATT annunciator is extinguished. When
complete, P01 will start P02. P02 waits until it detects a liftoff, then automatically runs P11 (launch monitor.) The
data registers show, from top to bottom, orbital velocity (xxxx.x) ms-1, altitude rate (xxxx.x) ms-1, and altitude 
above pad (xxxx.x) km.

At any time during ascent, the user can run V82 to bring up the orbit insertion display. Apoapsis and periapsis should
be read as XXXX.X km, and time to apoapsis should be read in HMMSS. The original AGC didnt't have decimal places in the
display registers, so we don't have them here.

How to get to Mun:
----

Orbit around Kerbin must be circular, or neally so (eccentricity < 0.003). Key in V37E15E, which will start Program 11,
TMI burn calculator. V21 N25 is flashing, asking us to load (key in) the first component of N25, which is the whole 
part of your vessels mass (get mass from MechJeb) in tonnes, with leading zeros. For example, if your mass is 12.345
tonnes, the whole part is 12 (the part up to the decimal point). So we would key in 00012, then ENTR. Now V22 N25 is
flashing, asking us to enter the second component of N25, which is the fractional part of your vessels mass. In the
given abobe, this would be 345, so we would key in 34500 (add trailing zeros) followed by ENTR.

Next up, V21 N31 is flashing, asking for the whole part of your vessels total thrust (get it from MechJeb), in kN. For
example, if your vessels thrust is 34.567 kN, key in 00034 followed by ENTR. Then V22 N31 flashes, which is the
fractional part of your vessels thrust. In the given abobe, this would be 567, so we would key in 56700 (add trailing
zeros) followed by ENTR.

Next, V21 N38 is flashing, asking us for specific impulse (Isp) of our engines (right-click on rocket engines to find
Isp). Key in the value for Isp with leading zeros, eg 00350 where Isp = 350. Key in ENTR.

From here, follow the TMI Calc checklist in the checklists folder from "Calculation complete" onwards. More details
to be added here Soon(tm)

Alarm codes:
------------

When there is an program alarm, the PROG indicator will illuminate. Keying in V05N09E will display the alarm codes, with
R1 displaying the most recent alarm code, R2 the previous alarm code, and R3 displaying the last alarm code, regardless
if the alarm codes have been reset or not. Alarm codes are displayed in octal.

The second digit indicates the action performed:
- X1XXX: basic program alarm, essentially a warning
- X2XXX: so-called P00DOO abort: terminates the running program and executes Program 00 (P00)
- X3XXX: program restart: the currently running program will terminate and attempt to restart itself.
- X4XXX: computer restart: a serious error has occurred which the computer cannot recover from. The computer will flush
its memory and perform a hardware restart.

Alarm codes currently implemented are listed below:

- 0X110: Error contacting KSP
- 0X111: Telemetry not available
- 0X115: No burn data loaded
- 0X223: Invalid target selected
- 0X224: Orbit not circular
- 0X225: Vessel and target orbits inclination too far apart
