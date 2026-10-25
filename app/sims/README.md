# Simulators

Copies of two interactive pages from the Chalkline sample course (`course/units/04-stem/embeds/`, copied 2026-10-25 from commit 6c96dea):

- `lifts.html`: robot lifts (4-bar, 6-bar, DR4B) with the VEX IQ size rules.
- `catapult.html`: three catapult launchers (choo choo, snail cam, winch, latch and trigger).
- `embed.css`: the shared look for both. One change from the original: a phone layout at the end (picture above the panel).

**Changed from the original:** the Chalkline catapult has a *slip gear* (a gear with teeth cut off). VEX IQ has no slip gear and parts can't be cut, so this copy has the **choo choo** instead: two large gears with 3 standoffs between them push a bar on the arm, and the arm fires when a standoff passes the end of the bar.

They were written for that course as original work: plain SVG and JavaScript, no libraries, no internet needed. They are **copies**, not links, so changes in the Chalkline course don't reach this site (and the other way round). If you fix one, fix both or copy again.

The sidebar's **Simulators** list (`SIMS` in `app/index.html`) shows each page in a frame. `?mode=` picks the starting button: `four`, `six`, `dr4b` for lifts; `choo`, `cam`, `latch` for catapults.
