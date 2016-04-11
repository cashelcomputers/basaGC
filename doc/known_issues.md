Known issues:

13/10/14: Program 15 (and all programs in general) need to be able to recompute on a regular basis ie every 50ms - DONE
2/12/14: Program 15 burn parameters need adjusting, and a function needs to be created that can dynamically readjust 
the burn parameters *during* the burn, based perhaps on:
- Apoapsis and periapsis
- Orbital period
- Orbital Velocity
Currently, P15 will *probably* get you in the neighborhood of a mun encounter on a free-return trajectory. I still 
need to implement a burn at Mun periapsis to circularize.

