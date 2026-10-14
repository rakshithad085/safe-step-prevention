# Safe Step Prevention

**Automatic overcrowd prevention for railway platforms and footbridges, built around the Kumbh Mela problem.**

Submitted to *Hack for a Social Cause* (MY Bharat Portal) by **Rakshitha D**, Department of EEE, Tamil Nadu.
Theme: Disaster Mitigation & Resilience.

> **Project status:** concept and design stage (proof of concept). The hardware prototype has not been built yet. This repository holds the design, planned firmware logic, test scenarios and bill of materials. Nothing here claims tested results.

---

## 1. Problem

During the Kumbh Mela, railway stations near the event become dangerously crowded as pilgrims arrive and leave in huge numbers over a short period. Footbridges, platforms and gates were not designed for that load.

Reported incidents (estimates):

| Incident | Deaths | Cause |
|---|---|---|
| 2013, Allahabad Station foot overbridge | ~36 | Bridge railing collapsed from overcrowding |
| Feb 2025, New Delhi Railway Station | ~18 | Stampede while boarding trains to Kumbh |

Both happened despite heavy police presence. The gap was not manpower. It was real-time data on crowd density and structural load reaching the people who could act in time.

**Problem statement:** How can we detect dangerous overcrowding at a railway platform or footbridge in real time, and automatically prevent further entry before it becomes fatal, rather than relying only on staff noticing the danger by eye?

## 2. What existing systems do, and the gap

Large hub stations use holding shelters, ticket restrictions, one-way flow, AI-CCTV and drones feeding a control room. Gates are then closed manually.

Gaps we identified:

- This infrastructure is limited to a few hub stations and needs a very large budget.
- Existing systems estimate crowd density from cameras. We found none that measures physical strain on the bridge structure itself.
- A human must decide and act, so there is a delay between an alert and a gate closing.

## 3. Solution

A low-cost, automatic system for **one platform or footbridge checkpoint**:

1. **Occupancy sensors** (entry and exit) count how many people are on the platform or bridge right now.
2. A **load cell** on the bridge deck measures real structural strain, as an independent check.
3. A **central hub** compares both readings against safe thresholds.
4. An **automatic gate arm** locks the entry when a threshold is crossed.
5. A **staff dashboard** shows live readings and alerts. Staff keep full manual override at all times.

The system assists staff judgment. It never replaces human authority.

## 4. Architecture

```
 [Entry sensor] --\
                   >-- [Sensor node: Arduino Uno] ==(nRF24L01+)==> [Hub: Arduino Nano] --> [Servo gate arm]
 [Exit sensor]  --/            |                                         |
 [Load cell + HX711] ----------/                                         +--> [Buzzer + LED]
                                                                         +--> [Staff dashboard + manual override]
```

| Part | Role |
|---|---|
| Sensor node (Arduino Uno) | Reads entry/exit sensors and load cell, sends data to the hub |
| Hub (Arduino Nano) | Decision logic, gate control, alerts |
| Dashboard | Live occupancy, load and gate status; manual override |

## 5. Decision logic (planned)

The numbers below are **placeholders**. Real limits must be set from the structure's rated load and an engineering review.

```cpp
// Pseudocode for the hub (planned, not yet tested on hardware)
const int  OCCUPANCY_WARN  = 0.80 * MAX_OCCUPANCY;  // start slowing entry
const int  OCCUPANCY_LOCK  = 0.95 * MAX_OCCUPANCY;  // lock the gate
const float LOAD_LOCK_KG   = 0.90 * RATED_LOAD_KG;  // lock the gate

loop() {
  occupancy = entries - exits;
  load      = readLoadCell();

  if (manualOverride)            { followStaffCommand(); return; }
  if (powerFailOrEmergency)      { openGate(); return; }   // fail-safe

  if (occupancy >= OCCUPANCY_LOCK || load >= LOAD_LOCK_KG) {
    lockGate(); soundAlarm(); notifyDashboard("LOCKED");
  } else if (occupancy >= OCCUPANCY_WARN) {
    slowEntry(); notifyDashboard("WARNING");
  } else {
    openGate();
  }
}
```

## 6. Safety by design

| Risk | Mitigation |
|---|---|
| Sudden closure pushes the crowd outside | Slow the entry rate gradually, provide a holding area, warn well before the limit |
| Sensors undercount in dense crowds | Treat data as a strong signal, pair with periodic manual headcounts |
| Power or network failure traps people | Fail-safe: the gate opens automatically on power loss or emergency trigger |
| Prototype is not station-scale | Position as proof of concept; real use needs engineering review, safety testing and phased rollout |
| Servo motor wear | Real deployment needs industrial-grade actuators |

## 7. Bill of materials (prototype, approx. Rs. 1,900)

| Component | Purpose | Approx. cost |
|---|---|---|
| Arduino Uno | Sensor node | Rs. 500 |
| Arduino Nano | Central hub | Rs. 350 |
| HC-SR04 ultrasonic sensor x2 | Entry and exit counting | Rs. 140 |
| Load cell (up to 20 kg) + HX711 | Structural strain measurement | Rs. 250 |
| Micro servo motor | Gate arm | Rs. 150 |
| nRF24L01+ x2 | Wireless link | Rs. 200 |
| Buzzer + LED | Local alert | Rs. 30 |
| Breadboards, wires, solder | Assembly and testing | Rs. 250-300 |

## 8. Test scenarios (planned)

These describe what the finished prototype should do. They are test plans, not results.

| # | Scenario | Expected behaviour |
|---|---|---|
| 1 | Occupancy below warning level | Gate open, dashboard "NORMAL" |
| 2 | Occupancy reaches warning level | Entry slowed, dashboard "WARNING" |
| 3 | Occupancy reaches lock level | Gate locks, buzzer and LED on, dashboard "LOCKED" |
| 4 | Load cell reading exceeds limit while occupancy is low | Gate locks (independent structural check) |
| 5 | Staff presses manual override | Gate follows staff command |
| 6 | Power loss or emergency trigger | Gate opens (fail-safe) |
| 7 | Sensor reads two people passing together | Count may be low; manual headcount check corrects it |

## 9. Roadmap

1. Submission and screening (Oct 2026): design, README, deck.
2. State demo/pitch: build the breadboard prototype and demonstrate gate lock on trigger.
3. If selected nationally: improve the prototype, calibrate thresholds, add fail-safe testing with mentor guidance.
4. Propose a small supervised pilot, then engineering review and phased rollout.

## 10. Setup and run

**Run the logic simulation (no hardware needed):**
1. Install Python 3 (https://www.python.org/downloads/).
2. Download or clone this repository.
3. Open a terminal in the repository folder.
4. Run `python3 simulate_logic.py`. Each row of `sample_data.csv` is checked against the expected gate state, and the script prints PASS or FAIL.

**Build the hardware prototype (planned):**
1. Install the Arduino IDE (https://www.arduino.cc/en/software).
2. In Library Manager, install `HX711` and `RF24`.
3. Wire the parts as in `ARCHITECTURE.md` (components and costs are in section 7).
4. Set the limits below, upload the sensor-node sketch to the Arduino Uno and the hub sketch to the Arduino Nano. The firmware sketches will be added as the prototype is built.

**Environment variables / configuration:** the project needs no secrets or API keys, so no environment variables are required. The tunable limits are set at the top of the code:

| Name | Meaning | Default (placeholder) |
|---|---|---|
| `MAX_OCCUPANCY` | Safe maximum people at the checkpoint | 100 |
| `WARN_FRACTION` | Warning level as a fraction of MAX_OCCUPANCY | 0.80 |
| `LOCK_FRACTION` | Lock level as a fraction of MAX_OCCUPANCY | 0.95 |
| `RATED_LOAD_KG` | Rated load of the structure or test deck | 20 |
| `LOAD_LOCK_FRACTION` | Load lock level as a fraction of RATED_LOAD_KG | 0.90 |

Real limits must come from an engineering review of the actual structure.

## 11. Repository contents

- `README.md`: this document (setup, configuration, overview)
- `ARCHITECTURE.md`: technical design with architecture diagram, data flow and decision rules
- `sample_data.csv`: simulated sensor readings with expected outcomes
- `simulate_logic.py`: runs the decision logic against the sample data
- `TEST_CASES.md`: list of logic and hardware test cases
- `LICENSE`: MIT License
- The presentation deck (PDF)

## 12. License

Released under the MIT License, so other colleges and local bodies can reuse and improve it.

## 13. Author

**Rakshitha D**, Department of Electrical and Electronics Engineering, Tamil Nadu.
Individual participant, Hack for a Social Cause.
