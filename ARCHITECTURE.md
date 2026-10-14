# Safe Step Prevention: Technical Design

Status: design stage (proof of concept). The decision logic is simulated in `simulate_logic.py`. The hardware prototype is not built yet.

## 1. System overview

One checkpoint (a platform entry or a footbridge) is monitored by a sensor node. A central hub decides whether to keep the gate open, slow entry, or lock it. Staff can always override.

## 2. Architecture diagram

```
 [Entry sensor HC-SR04] --\
                           >-- [Sensor node: Arduino Uno] ==(nRF24L01+ wireless)==> [Hub: Arduino Nano]
 [Exit sensor HC-SR04]  --/            |                                                 |
 [Load cell + HX711] -----------------/                                                  +--> [Servo gate arm]
                                                                                         +--> [Buzzer + LED alert]
                                                                                         +--> [Staff dashboard + manual override]
```

## 3. Data flow

1. The two ultrasonic sensors count people entering and leaving. Occupancy = entries minus exits.
2. The load cell (through the HX711 amplifier) measures weight on the bridge deck in kg.
3. The sensor node sends occupancy and load to the hub over the nRF24L01+ link.
4. The hub compares both values with the configured limits and sets the gate state.
5. The dashboard shows the live values and the current state.

## 4. Decision rules (priority order)

| Priority | Condition | State | Gate |
|---|---|---|---|
| 1 | Power failure or emergency trigger | OPEN_FAILSAFE | Opens |
| 2 | Staff manual override active | MANUAL | Follows staff |
| 3 | Occupancy at or above lock level, or load at or above load limit | LOCKED | Locks, buzzer and LED on |
| 4 | Occupancy at or above warning level | WARNING | Entry slowed |
| 5 | Otherwise | NORMAL | Open |

## 5. Configuration

| Name | Meaning | Default (placeholder) |
|---|---|---|
| MAX_OCCUPANCY | Safe maximum people at the checkpoint | 100 |
| WARN_FRACTION | Warning level as a fraction of MAX_OCCUPANCY | 0.80 |
| LOCK_FRACTION | Lock level as a fraction of MAX_OCCUPANCY | 0.95 |
| RATED_LOAD_KG | Rated load of the structure or test deck | 20 |
| LOAD_LOCK_FRACTION | Load lock level as a fraction of RATED_LOAD_KG | 0.90 |

These values are placeholders. Real limits need an engineering review of the actual structure.

## 6. Safety design

- Fail-safe: the gate opens on power loss or emergency, so it never traps people.
- Gradual entry slowing before a full lock, plus a holding area before the gate.
- Sensors can undercount in dense crowds, so data is paired with periodic manual headcounts.
- A servo is a demo stand-in. Real deployment needs industrial-grade actuators.
