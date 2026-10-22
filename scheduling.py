# FCFS and Non-Preemptive SJF CPU Scheduling
import copy


def read_int(prompt, minimum, allow_equal=True):
    """Keep asking until a valid integer >= minimum is entered."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("  Invalid input: please enter a whole number.")
            continue
        if value < minimum or (value == minimum and not allow_equal):
            print(f"  Invalid input: value must be {'>=' if allow_equal else '>'} {minimum}.")
            continue
        return value


def read_processes():
    n = read_int("Enter number of processes: ", 1)
    processes, used_ids = [], set()
    for i in range(n):
        print(f"--- Process {i + 1} ---")
        while True:
            pid = input("  Process ID   : ").strip().upper()
            if not pid:
                print("  Invalid input: Process ID cannot be empty.")
            elif pid in used_ids:
                print("  Invalid input: Process ID already used.")
            else:
                break
        used_ids.add(pid)
        at = read_int("  Arrival Time : ", 0)
        bt = read_int("  Burst Time   : ", 1)
        processes.append({"pid": pid, "at": at, "bt": bt, "order": i})
    return processes


def build_result(processes, timeline):
    """Compute CT, TAT and WT from the execution timeline."""
    finish = {pid: end for pid, start, end in timeline if pid != "IDLE"}
    rows = []
    for p in processes:
        ct = finish[p["pid"]]
        tat = ct - p["at"]
        rows.append((p["pid"], p["at"], p["bt"], ct, tat, tat - p["bt"]))
    return rows


def fcfs(processes):
    # Order by arrival time; tie -> the process entered first
    queue = sorted(processes, key=lambda p: (p["at"], p["order"]))
    timeline, time = [], 0
    for p in queue:
        if time < p["at"]:
            timeline.append(("IDLE", time, p["at"]))
            time = p["at"]
        timeline.append((p["pid"], time, time + p["bt"]))
        time += p["bt"]
    return timeline


def sjf(processes):
    # Non-preemptive: shortest burst among arrived processes.
    # Tie-break: smaller burst -> earlier arrival -> entered first
    remaining, timeline, time = list(processes), [], 0
    while remaining:
        ready = [p for p in remaining if p["at"] <= time]
        if not ready:
            next_at = min(p["at"] for p in remaining)
            timeline.append(("IDLE", time, next_at))
            time = next_at
            continue
        p = min(ready, key=lambda x: (x["bt"], x["at"], x["order"]))
        timeline.append((p["pid"], time, time + p["bt"]))
        time += p["bt"]
        remaining.remove(p)
    return timeline


def show(title, processes, timeline):
    print("\n" + "=" * 58)
    print(f"  {title}")
    print("=" * 58)
    print("Execution Sequence :", " -> ".join(t[0] for t in timeline))
    print("\nStart/End Intervals:")
    for pid, start, end in timeline:
        label = "CPU IDLE" if pid == "IDLE" else pid
        print(f"  {label:<9}: {start:>3} - {end:<3}")
    rows = build_result(processes, timeline)
    print("\n PID   AT   BT   CT   TAT   WT")
    print("-" * 33)
    for r in rows:
        print(f" {r[0]:<5}{r[1]:<5}{r[2]:<5}{r[3]:<5}{r[4]:<6}{r[5]}")
    n = len(rows)
    print("-" * 33)
    print(f"Average Turnaround Time : {sum(r[4] for r in rows) / n:.2f}")
    print(f"Average Waiting Time    : {sum(r[5] for r in rows) / n:.2f}")


def main():
    print("FCFS and SJF (Non-Preemptive) Scheduling\n")
    original = read_processes()
    # Each algorithm gets its own deep copy; original data is never changed
    data_fcfs = copy.deepcopy(original)
    data_sjf = copy.deepcopy(original)

    print("\nOriginal Process Data (same dataset for both algorithms)")
    print(" PID   AT   BT")
    for p in original:
        print(f" {p['pid']:<5}{p['at']:<5}{p['bt']}")

    show("FCFS SCHEDULING", data_fcfs, fcfs(data_fcfs))
    show("SJF (NON-PREEMPTIVE) SCHEDULING", data_sjf, sjf(data_sjf))


if __name__ == "__main__":
    main()
