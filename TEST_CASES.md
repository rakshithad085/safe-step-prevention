# Test Cases

Logic tests run with `python3 simulate_logic.py` using `sample_data.csv` (simulated readings, not real measurements). Hardware tests are planned for the prototype stage.

| # | Scenario | Expected behaviour | Type |
|---|---|---|---|
| 1 | Occupancy below warning level | Gate open, state NORMAL | Logic (in sample data) |
| 2 | Occupancy reaches warning level | Entry slowed, state WARNING | Logic (in sample data) |
| 3 | Occupancy reaches lock level | Gate locks, state LOCKED | Logic (in sample data) |
| 4 | Load exceeds limit while occupancy is low | Gate locks, state LOCKED | Logic (in sample data) |
| 5 | Staff manual override | State MANUAL, gate follows staff | Logic (in sample data) |
| 6 | Power failure or emergency | Gate opens, state OPEN_FAILSAFE | Logic (in sample data) |
| 7 | Two people pass the sensor together | Count may read low, so a manual headcount corrects it | Hardware (planned) |
| 8 | Wireless link drops | Hub keeps last safe state and sounds local alert | Hardware (planned) |
