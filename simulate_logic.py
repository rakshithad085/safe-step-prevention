"""Simulation of the Safe Step Prevention decision logic.

Reads sample_data.csv, applies the hub rules from ARCHITECTURE.md and checks
each row against the expected state. This tests the logic only. It does not
control real hardware.

Run:  python3 simulate_logic.py
"""
import csv
import sys

# Configuration (placeholders, see ARCHITECTURE.md)
MAX_OCCUPANCY = 100
WARN_FRACTION = 0.80
LOCK_FRACTION = 0.95
RATED_LOAD_KG = 20
LOAD_LOCK_FRACTION = 0.90


def decide(occupancy, load_kg, manual_override, power_fail):
    if power_fail:
        return "OPEN_FAILSAFE"
    if manual_override:
        return "MANUAL"
    if occupancy >= LOCK_FRACTION * MAX_OCCUPANCY or load_kg >= LOAD_LOCK_FRACTION * RATED_LOAD_KG:
        return "LOCKED"
    if occupancy >= WARN_FRACTION * MAX_OCCUPANCY:
        return "WARNING"
    return "NORMAL"


def main(path="sample_data.csv"):
    failures = 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            got = decide(int(row["occupancy"]), float(row["load_kg"]),
                         int(row["manual_override"]), int(row["power_fail"]))
            ok = got == row["expected_state"]
            failures += not ok
            print(f"{row['time']}  occupancy={row['occupancy']:>3}  load={row['load_kg']:>5}kg  "
                  f"expected={row['expected_state']:<13} got={got:<13} {'PASS' if ok else 'FAIL'}")
    print("\nAll tests passed." if failures == 0 else f"\n{failures} test(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
