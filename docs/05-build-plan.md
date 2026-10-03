---
doc_id: TWK-BLD-001
title: TwinKit prototype build plan
project: TwinKit
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-02'
    author: Amish Chadha
    change: First build plan; design made constructable (TWK-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Concentrator, antenna and safety stop S5 name the US915 band chosen for the first build (TWK-DEC-001, 2026-10-02); no picture changed
---

# TwinKit prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order.*

The prototype is one TwinKit gateway on a bench: an aluminium plate on rubber feet carrying a short DIN rail, with five bought DIN modules clipped onto the rail from left to right. They are the input fuse and terminal blocks, the gateway enclosure that holds the single-board computer and the radio concentrator, the 12 V to 5 V converter, the backup (UPS) module, and a small battery box that holds the backup pack. An end stop at each end keeps the modules from sliding. Figure 1 shows the 20 components in the order you make or fit them. Five are made or worked in a small workshop: the plate is cut, drilled and tapped; the rail is cut and drilled; the enclosure base, the enclosure cover and the battery box base are bought and then cut or drilled. Everything else is bought and fitted with screws, clips and screw terminals. No soldering and no circuit board work is needed. The parts cost about USD 334 from the bill of materials.

> **Safety:** The prototype holds a 12.8 V lithium iron phosphate (LiFePO4) pack of about 19 Wh with its own protection board and fuse. Keep the pack lead unplugged from the UPS module until section 6 says otherwise, charge it only through the UPS module, and never leave a first build charging unattended. Use a certified, double-insulated 12 V adapter; nothing in this build touches mains wiring. Cut aluminium edges are sharp: deburr everything. A network gateway is an attack surface: keep it off the internet until its default credentials are changed.

## 2. What changed to make it buildable

The concept showed what the gateway does; some of its parts could not be made, fitted or held as drawn. Each change below keeps what the gateway does, and all of them are recorded in decision record TWK-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Backup pack | Drawn inside the UPS module | Its own 3-module battery box beside a 3-module UPS module (Figures 13 and 14) | Two bought parts cannot be put one inside the other |
| Enclosure vents | Slots in the two end walls, 2 mm from the neighbouring modules | The same slots in the two long walls (Figure 8) | Air can reach them; same area and spacing, so the temperature results stand |
| Computer and HAT | Floating inside the enclosure | Brass standoffs on the floor, a second set between the boards, and a header extender (Figure 10) | Every board is held by its own four holes |
| Antenna | Sitting on the cover with no hole | An SMA bulkhead through a 6.5 mm hole, with a pigtail to the HAT (Figure 12) | How a bulkhead is fitted |
| Cable entries | None | A network feed-through coupler and a power gland in the front wall (Figure 9) | The network and power leads need a way in |
| DIN rail | A U channel with no fixing | A true top-hat rail, 350 mm long, on three M4 screws (Figures 4 and 6) | Every module's clip hooks under the top-hat flanges |
| Ends of the rail | Nothing | Two screw-clamped end stops (Figure 16) | Nothing slides along the rail |
| Bench plate | Plywood or aluminium, no feet | 6 mm aluminium, tapped for the rail, on four rubber feet (Figures 2 and 3) | A tapped hole holds the rail with no nuts underneath |
| Wiring | No path for power or the power-fail signal into the enclosure | A USB-C power lead and a power-fail pair through the power gland (Figure 15) | The computer gets its power and its warning of an outage |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the long side of the modules that faces you on the bench, where the cable entries are; "left" and "right" are as seen from the front. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Bench plate

![Figure 2. Making sketch of the bench plate](../cad/drawings/TWK-DWG-101.png)

*Figure 2. Bench plate making sketch (TWK-DWG-101).*

![Figure 3. Hole layout of the bench plate](05-build-plan/plate-holes.png)

*Figure 3. Every hole, measured from the middle of the plate, with the rubber feet underneath shown dotted.*

**What it is and what it is made from.** The flat base that the rail is screwed to. It stands on the bench on four rubber feet, or screws to a wall or cabinet later through its corner holes. Aluminium sheet 6 mm thick, 5083, 6082 or 6061 class, cut to 360 x 180 mm.

**How to make it.**

1. Cut the blank to 360 x 180 mm, square. File the edges and round the corners to about 3 mm.
2. Scribe a centre line along the long side and mark the middle of it.
3. Rail holes: on the centre line, at the middle and 150 each side of it. Drill 3.3 mm right through and tap M4, keeping the tap square to the plate.
4. Corner holes: four 5.5 mm holes, 12 in from each long and each short edge.
5. Deburr every hole on both faces.
6. Clean the underside and press on four stick-on rubber feet, 20 across, centred 150 each side of the middle and 60 each side of the centre line (step 1).

**How it fits the parts next to it.**

![Figure 4. Joint 1: DIN rail on the bench plate](05-build-plan/joint-01.png)

*Figure 4. The rail's base lies flat on the plate; an M4 pan-head screw passes through it into a tapped hole.*

The rail's 27 mm wide base lies flat on the top face, along the centre line, with each end 5 in from the plate's short edges. Three M4 x 6 pan-head screws hold it, one in each tapped hole. Nothing else touches the plate: every module stands on the rail's flanges, 7.5 above it.

**Check before moving on.** An M4 screw runs into each tapped hole by hand. On a flat bench the plate rocks on none of its feet.

### 3.2 DIN rail

![Figure 5. Making sketch of the DIN rail](../cad/drawings/TWK-DWG-102.png)

*Figure 5. DIN rail making sketch (TWK-DWG-102).*

**What it is and what it is made from.** The standard rail that every module clips onto. TS35 x 7.5 slotted top-hat rail, steel or aluminium: 35 wide across its top flanges, 7.5 high, with a 27 wide base.

**How to make it.**

1. Cut a 350 length with a hacksaw. File both ends square and remove every burr, inside the channel too.
2. Mark three holes on the centre line of the base: at the middle and 150 each side of it.
3. Where a factory slot already falls within 3 of a mark, use the slot. Otherwise drill 4.5 through the base.

**How it fits the parts next to it.**

![Figure 6. Joint 2: how every module clips onto the rail](05-build-plan/joint-02.png)

*Figure 6. Seen along the rail, cut across. A hook on each side of the module's base reaches under the rail's flange; the base sits on top of the flanges.*

The base is screwed to the plate (Figure 4). Every module hooks its back edge under one flange and snaps its front edge over the other. The screw heads sit 3.9 below the modules' bases, so a module slides along the rail without catching.

**Check before moving on.** The rail lies flat along its whole length; a module clips on and slides from end to end without catching on a screw.

### 3.3 Gateway enclosure base, cut and drilled

![Figure 7. Cutting and drilling sketch of the enclosure base](../cad/drawings/TWK-DWG-103.png)

*Figure 7. Enclosure base cutting and drilling sketch (TWK-DWG-103).*

![Figure 8. Cut-outs in the enclosure base](05-build-plan/enclosure-holes.png)

*Figure 8. A: the front wall, with the vent slots, the network coupler hole and the power gland hole. B: the floor, with the four holes for the computer.*

**What it is and what it is made from.** The lower half of a bought 9-module DIN enclosure for a single-board computer: polycarbonate, 157.5 long, 90 deep and 44 high, with a DIN clip moulded under its floor. It holds the computer and the concentrator. You cut vent slots in both long walls, two entry holes in the front wall and four holes in the floor.

**How to make it.**

1. Decide which long wall is the front and mark it. Cover the walls and floor with masking tape.
2. Vent slots, both long walls: two slots 40 x 4, centred 32 left of the middle, from 2.5 to 6.5 and from 9.5 to 13.5 above the outside of the floor (Figure 8, A). Chain drill with a 3.5 drill and file to the line. Skip any slot the maker has already moulded in the same place.
3. Front wall, both centred 26 above the outside of the floor: a 20 hole 50 right of the middle for the network coupler, and a 16.2 hole 20 right of the middle for the power gland. Pilot 3 at low speed, then open out with a step drill, light pressure, with a block of wood behind the wall. Check each size on the part's datasheet before the last step.
4. Floor: four 2.7 holes for the computer, 58 apart along the base and 49 apart across it, the left pair 59 left of the middle and the right pair 1 left of it, 24.5 each side of the centre line (Figure 8, B). If the enclosure has moulded bosses for the computer, use them instead and skip this step.
5. Deburr every cut inside and out, peel the tape and clean with water and mild soap only; solvents craze polycarbonate.

**How it fits the parts next to it.**

![Figure 9. Joint 4: network coupler and power gland in the front wall](05-build-plan/joint-04.png)

*Figure 9. Each entry clamps the wall between its outside flange and its inside nut.*

The network coupler and the power gland go in from outside, flange and seal outside, nut inside (step 3). They sit 13.5 or more clear of both boards.

![Figure 10. Joint 3: the board stack at one corner](05-build-plan/joint-03.png)

*Figure 10. At each of the four corners: floor, 6 mm standoff, computer, 16 mm standoff, HAT. The header extender joins the two boards.*

Four 6 mm brass standoffs stand on the floor holes, each held by an M2.5 pan-head screw from underneath (step 4). The screw heads sit 4.75 outside the rail's flanges, so they never touch the rail. The computer sits on the standoffs with its network socket toward the coupler, and four 16 mm standoffs screw into the lower ones through the computer's holes. The HAT sits on the 16 mm standoffs and on a header extender pushed onto the computer's 40-pin header, and is held by four M2.5 screws. The active cooler on the computer clears the HAT by 8. The DIN clip under the floor hooks onto the rail (Figure 6).

**Check before moving on.** Lay the computer on the floor: its four holes line up with yours. No crack runs out from any hole under a bright lamp.

### 3.4 Gateway enclosure cover, drilled

![Figure 11. Drilling sketch of the enclosure cover](../cad/drawings/TWK-DWG-104.png)

*Figure 11. Enclosure cover drilling sketch (TWK-DWG-104).*

**What it is and what it is made from.** The upper half of the same bought enclosure, clear or tinted polycarbonate, 16 deep, closing onto the base with the maker's clips or screws. It carries the antenna.

**How to make it.**

1. Antenna hole: 6.5 through the top, 30 left of the middle and 20 behind the centre line (toward the back wall). Pilot 3, then step drill, with wood behind.
2. Vent slots, both long walls: two slots 40 x 4 in line with the base's slots, from 1.5 to 5.5 and from 6.5 to 10.5 above the cover's lower edge. Skip any the maker has already moulded.
3. Deburr and clean with water and mild soap.

**How it fits the parts next to it.**

![Figure 12. Joint 5: antenna bulkhead through the cover](05-build-plan/joint-05.png)

*Figure 12. The SMA bulkhead's flange and washer sit on top of the cover, its nut underneath; the whip screws onto the top.*

The bulkhead goes in from above with its nut inside (step 9). A U.FL pigtail runs from it to the HAT's antenna socket. The inside nut clears the HAT by about 22 when the cover is closed. The cover's lower edge sits on the base's upper edge all round (step 10).

**Check before moving on.** The bulkhead does not turn when the whip is screwed on finger tight.

### 3.5 Battery box base, drilled

![Figure 13. Drilling sketch of the battery box base](../cad/drawings/TWK-DWG-105.png)

*Figure 13. Battery box base drilling sketch (TWK-DWG-105).*

**What it is and what it is made from.** The lower half of a bought empty 3-module DIN enclosure, polycarbonate, 52.5 long, 90 deep and 44 high, with its own cover. It holds the backup pack on the rail beside the UPS module. One hole is drilled in its front wall.

**How to make it.**

1. A 12.2 hole in the middle of the front wall, 26 above the outside of the floor, for the M12 gland. Pilot 3, then step drill.
2. Deburr inside and out.
3. Stick a hook-and-loop pad, 38 x 60, to the middle of the floor, long side front to back. Its mate goes on the underside of the pack.

**How it fits the parts next to it.**

![Figure 14. Joint 6: backup pack in its battery box](05-build-plan/joint-06.png)

*Figure 14. The pack sits on the pad, 3.5 clear of the gland nut and clear of the cover.*

The pack (no larger than 38 x 70 x 38) lies on the pad, long side front to back, with its lead out through the gland. The gland goes in from outside with its seal outside and its nut inside. The cover closes without touching the pack. The box clips onto the rail 2 to the right of the UPS module.

**Check before moving on.** The pack's lead reaches the gland without strain, and the cover closes without force.

### 3.6 Wiring

![Figure 15. Block-level wiring](05-build-plan/wiring.png)

*Figure 15. Block-level wiring with wire sizes. Every connection is at a bought module's screw terminal or plug; no circuit board is made.*

Wire it like this, with stranded copper and a ferrule on every screw terminal. Run the wires along the front of the modules and tie them to adhesive tie mounts on the plate.

1. Adapter lead to the fuse holder and the two terminal blocks: 0.75 mm² (18 AWG), positive through the 3.15 A time-delay fuse.
2. Terminal blocks to the UPS module's input: 0.75 mm².
3. UPS module's output to the converter's input: 0.75 mm².
4. Converter's 5.1 V output to the computer: the USB-C power lead with bare ends, rated 5 A, in through the power gland.
5. UPS module's power-fail contact to a free GPIO pin and a ground pin on the HAT's pass-through header: a 0.25 mm² (24 AWG) twisted pair, through the same gland (the gland's insert has two holes).
6. Pack lead from the battery box gland to the UPS module's battery terminals: 0.75 mm². Leave it unplugged at the UPS end until stop S3 (section 6).
7. Patch lead from the computer's network socket to the inside of the network coupler (done in step 6).
8. U.FL pigtail from the HAT to the antenna bulkhead (done in step 10).

**Check before moving on.** With the adapter unplugged and the pack lead loose, every wire continues end to end and the adapter's positive does not read as a short (under 10 Ω) to ground. Every wire is labelled at both ends.

### 3.7 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **DIN rail (line 2).** TS35 x 7.5 slotted top-hat rail, at least 350 long. Made as section 3.2.
- **Gateway enclosure (lines 3 and 4).** 9-module DIN enclosure for a single-board computer, about 157.5 x 90 x 60, polycarbonate, DIN clip in the base, cover held by clips or screws. Worked as sections 3.3 and 3.4.
- **Computer (line 5).** Quad-core Arm board with 4 GB, Ethernet, Wi-Fi and a 40-pin header, 85 x 56 with four mounting holes 58 x 49 apart (Raspberry Pi 5 class).
- **Active cooler (line 6).** The clip-on heat sink and fan made for the computer, no taller than 8 above the board.
- **Concentrator HAT (line 7).** SX1302 or SX1303 8-channel LoRaWAN concentrator on a 40-pin HAT, US915 version for the first build, 65 x 56 with holes on the computer's pattern and a U.FL antenna socket.
- **microSD card (line 8).** 64 GB high-endurance, A2 class, flashed with the operating system before step 5.
- **Antenna (line 9).** 3 dBi whip for the 915 MHz band, SMA bulkhead for a 6.5 hole, U.FL pigtail about 150 long.
- **DC-DC converter (line 10).** DIN rail, 2 modules, 9 to 30 V in, 5.1 V 5 A out.
- **UPS module (line 11).** DIN rail DC UPS, 3 modules wide, with no battery inside, for an external 12.8 V LiFePO4 pack: 9 to 30 V input, a buck-boost charger to 14.6 V at 0.5 A or less that stops charging below 0 °C and above 45 °C, pass-through output, and a power-fail output that is a dry contact or an open collector (never a voltage).
- **Backup pack (line 12).** 12.8 V 1.5 Ah LiFePO4 (four 18650 cells in a 2 x 2 block), built-in protection board and fuse, no larger than 38 x 70 x 38, lead about 300 long, with a maker's datasheet.
- **Terminal blocks and fuse (line 13).** Two DIN screw terminal blocks and a DIN fuse holder for 5 x 20 fuses, with a 3.15 A time-delay fuse.
- **Battery box (line 17).** Empty 3-module DIN enclosure, about 52.5 x 90 x 60, base and cover. Drilled as section 3.5.
- **End stops (line 18).** Two screw-clamp end stops for TS35 rail, about 8 wide.
- **Board mounting kit (line 19).** Four M2.5 x 6 brass standoffs (female-female), four M2.5 x 16 standoffs (male-female), eight M2.5 x 5 pan-head screws, and a 2 x 20 header extender about 10 tall.
- **Cable entries (line 20).** A round RJ45 feed-through coupler for a 20 hole with a panel nut (Cat 6), a 0.15 m patch lead, an M16 x 1.5 nylon gland (IP68) with a two-hole sealing insert, and an M12 x 1.5 nylon gland (IP68) for 3 to 6.5 cable.
- **Fixings and wiring (line 21).** Three M4 x 6 pan-head screws, four stick-on rubber feet 20 across and 6 high, hook-and-loop pads, a USB-C power lead with bare ends rated 5 A, 0.75 mm² and 0.25 mm² stranded wire, ferrules, adhesive cable-tie mounts and ties.
- **Not in the kit.** A certified, double-insulated 12 V DC adapter of at least 2 A (or an existing 12 V supply), a laptop or phone for the dashboard, and a sensor node such as FieldNode.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: rubber feet under the bench plate

![Step 1](05-build-plan/step-01.png)

Seen from below. Clean the underside with alcohol, let it dry, and press a foot firmly onto each mark.

### Step 2: DIN rail onto the bench plate

![Step 2](05-build-plan/step-02.png)

Lay the rail on the centre line, 5 in from each end. Three M4 x 6 pan-head screws into the tapped holes, snug.

### Step 3: network coupler and power gland into the enclosure base

![Step 3](05-build-plan/step-03.png)

From outside, flange and seal outside, nut inside, tightened to the maker's torque. From inside, pass the bare end of the USB-C power lead and the power-fail pair out through the gland's two-hole insert, leaving about 150 inside, but do not tighten the gland cap yet.

### Step 4: lower standoffs into the enclosure floor

![Step 4](05-build-plan/step-04.png)

Four 6 mm standoffs on the four floor holes, an M2.5 pan-head screw into each from underneath, snug.

### Step 5: cooler and microSD card onto the computer

![Step 5](05-build-plan/step-05.png)

Clip the cooler into its two board holes and plug its fan lead into the fan socket. Push the flashed card into its slot, contacts toward the board.

### Step 6: computer onto the lower standoffs

![Step 6](05-build-plan/step-06.png)

Lay the computer on the standoffs with its network socket toward the coupler. Plug the patch lead into the computer and into the inside of the coupler, and the USB-C power lead into the computer.

### Step 7: upper standoffs and header extender

![Step 7](05-build-plan/step-07.png)

Screw a 16 mm standoff into each lower one through the computer's holes, finger tight plus a quarter turn. Push the header extender straight down onto the 40-pin header.

### Step 8: concentrator HAT onto the stack

![Step 8](05-build-plan/step-08.png)

Line the HAT's socket up with the extender and press down evenly until it rests on all four standoffs. Four M2.5 screws on top. Push the antenna pigtail onto the HAT's U.FL socket. Connect the power-fail pair to the free GPIO and ground pins named in the HAT's datasheet.

### Step 9: antenna bulkhead into the cover

![Step 9](05-build-plan/step-09.png)

From above, flange and washer outside, nut inside, snug. Screw the whip on finger tight.

### Step 10: close the gateway enclosure

![Step 10](05-build-plan/step-10.png)

Screw the pigtail onto the bulkhead from inside. Close the cover with the maker's clips or screws, checking that no wire is pinched at the joint. Pull the spare power lead out through the gland and tighten the gland cap. **Hold point:** the wiring checks of section 3.6 pass for the wires inside the enclosure.

### Step 11: terminal blocks and fuse holder onto the rail

![Step 11](05-build-plan/step-11.png)

At the left end of the rail, fuse holder outermost. Hook the back edge over the rail, then press the front down until the clip snaps. Leave the fuse out.

### Step 12: gateway enclosure onto the rail

![Step 12](05-build-plan/step-12.png)

2 to the right of the terminal blocks, cable entries to the front. It clips on the same way.

### Step 13: DC-DC converter and UPS module onto the rail

![Step 13](05-build-plan/step-13.png)

Each 2 to the right of the module before, terminals facing up.

### Step 14: battery box base onto the rail

![Step 14](05-build-plan/step-14.png)

2 to the right of the UPS module, gland to the front.

### Step 15: backup pack into the battery box

![Step 15](05-build-plan/step-15.png)

**Hold point:** safety stop S1 (section 6). Pass the pack's lead out through the gland, press the pack onto the pad, and tighten the gland cap on the lead. Do not connect the lead to the UPS module yet.

### Step 16: close the battery box

![Step 16](05-build-plan/step-16.png)

Cover on with the maker's clips or screws.

### Step 17: end stops at both ends

![Step 17](05-build-plan/step-17.png)

Slide each end stop along the rail until it presses against the last module and tighten its screw. Then wire the modules as section 3.6, leaving the fuse out and the pack lead loose.

![Figure 16. Joint 7: left end stop against the fuse holder](05-build-plan/joint-07.png)

*Figure 16. The end stop is clamped to the rail touching the fuse holder, so no module can slide.*

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of TWK-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Fit on the rail | R10 | Measure from the left end stop to the right one; push each module along the rail by hand | 345 or less; no module moves |
| Input polarity and fuse | R8 | Adapter plugged in, fuse in, pack lead loose; meter at the UPS input and the converter output | 11.4 to 12.6 V at the UPS input; 5.0 to 5.25 V at the converter output, polarity right |
| First boot and average power | R8 | Computer boots from the card; meter the adapter current for 10 min at idle | It boots; 8 W or less on average (6.4 W estimated) |
| Charge voltage and window | R9 | Pack connected, as stop S3; meter at the pack terminals as charging ends | Charging stops at 14.6 V, give or take 0.2 V |
| Outage ride-through | R9 | Unplug the adapter with the gateway running | The computer keeps running on the pack and logs the power-fail signal; it shuts down cleanly before the pack's cut-off |
| Network | R2, R11 | Ethernet through the coupler; log in, change the default credentials | Dashboard reached over TLS on the local network only |
| Radio | R1, R2 | One FieldNode or other LoRaWAN node within 10 m | Uplinks appear on the network server and in the database |
| Enclosure temperature at idle | R12 | Thermometer on the cover top and the computer's own temperature reading after 1 h at room temperature | Recorded for the TRL 4 thermal test; no throttling reported |
| Monitoring only | R16 | Inspect the wiring | No wire leaves the gateway to any output or actuator |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the pack comes into the workshop.** Pack voltage about 12.0 to 13.6 V; no swelling, dents or leaks; a datasheet from its maker; its protection board and fuse are built in. A charging spot ready on a non-combustible surface (ceramic tile or steel tray) with a fire extinguisher for electrical fires within reach.
- **S2. Before the adapter is plugged in.** The adapter is certified and double-insulated, 12 V DC, and its plug is undamaged. The fuse holder carries a 3.15 A time-delay fuse, not a larger one. With the fuse out, positive reads open to ground at the terminal blocks. Polarity at the terminal blocks is checked with a meter, not by wire colour. The pack lead is loose.
- **S3. Before the pack is connected to the UPS module.** The UPS module's charger is set for LiFePO4 at 14.6 V (the maker's setting, checked in its datasheet), its charge current is 0.5 A or less, and its charge stops below 0 °C and above 45 °C. The pack's polarity matches the UPS module's battery terminals, checked with a meter.
- **S4. First charge.** Attended the whole time, on the charging spot, with the battery box cover off; pack temperature checked by hand or thermometer every 15 minutes. Stop if the pack passes 45 °C, swells, smells or exceeds 14.6 V.
- **S5. Before the concentrator transmits.** The antenna is connected and is a 915 MHz antenna, matching the US915 concentrator. Transmitting without an antenna can damage the radio.
- **S6. Before the gateway joins any network beyond the bench.** Every default credential is changed, the dashboard is on TLS, and no port is open beyond the local network.
- **S7. Before any cabinet or mains-side installation (outside this plan).** Any wiring to an existing 12 V system or into a mains cabinet is done or checked by a qualified electrician under local code.

## 7. Tools, skills and workspace

**Tools.** Hacksaw with a 24 teeth per inch blade; bench vice with soft jaws; bench drill or a drill in a stand; drills 2.5 to 6 mm; step drill to 22 mm; M4 tap and tap wrench; flat and half-round files; deburring tool; scriber, engineer's square, steel rule and calipers; small screwdrivers (flat and Phillips) and a 5.5 mm nut driver for the M2.5 standoffs; spanners or a deep socket for the gland and coupler nuts; ferrule crimper and wire strippers; multimeter; thermometer; a computer with a card reader to flash the microSD card.

**Skills.** No certified trade is needed. Basic metalwork (marking out, sawing, drilling, tapping, filing), drilling plastic boxes, crimping ferrules, safe care of a lithium pack, and setting up a single-board computer from a flashed card. All circuits are extra-low voltage: 12 V nominal input, 14.6 V at most while the pack charges. No mains wiring is part of this build.

**Workspace.** A bench about 1.2 x 0.6 m; a metalwork corner kept apart from the electronics so chips stay off the boards; the charging spot of S1; a wired network socket or switch for the first checks.

**Personal protective equipment.** Safety glasses for cutting and drilling; cut-resistant gloves for handling cut aluminium; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 274 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/TWK-DWG-101` to `TWK-DWG-105`.
- General arrangement: `cad/drawings/TWK-DWG-001.pdf`, Rev P3.
- Calculations: `docs/04-calcs/01-sizing.md` (TWK-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; power [D1] to [D3], backup [E1] to [E3], temperature [F2], [F6], [F7], rail [H1], cost [I1], [I2].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (TWK-DDR-003), with TWK-DDR-001 and TWK-DDR-002; open items in `docs/06-design-decisions.md` (TWK-DEC-001).
- Requirements: `docs/03-requirements.md` (TWK-REQ-001 v0.5).
