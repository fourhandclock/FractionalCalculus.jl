"""Serial local command capture for this checkpoint's requested safeguards.

Limits are per process, not cgroup aggregate limits. Commands are inspected
local tests/builds and must not detach children. No installation or network
permission is conferred by this runner. Raw output is never overwritten.
"""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[4]


def portable(value):
    return str(value).replace(str(ROOT), "$WORKSPACE")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--cpu-seconds", type=int, default=120)
    parser.add_argument("--memory-mib", type=int, default=2048)
    parser.add_argument("--file-size-mib", type=int, default=256)
    parser.add_argument("--resident-mib", type=int, default=0,
                        help="Optional sampled sum-RSS limit for ordinary descendants (shared pages count repeatedly).")
    parser.add_argument("--cwd", type=Path, default=ROOT)
    parser.add_argument("--evidence", type=Path, default=ROOT / "research/legendre/verification/results/checkpoint-st04")
    parser.add_argument("--source", type=Path, action="append", default=[])
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command after -- is required")
    if any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in args.label):
        parser.error("label must be a simple filename component")
    args.evidence.mkdir(parents=True, exist_ok=True)
    record_path = args.evidence / f"{args.label}.json"
    stdout_path = args.evidence / f"{args.label}.stdout.log"
    stderr_path = args.evidence / f"{args.label}.stderr.log"
    if any(p.exists() for p in (record_path, stdout_path, stderr_path)):
        parser.error("evidence already exists; choose a new label")
    sources = {}
    for path in args.source:
        data = path.read_bytes()
        sources[portable(path.resolve())] = hashlib.sha256(data).hexdigest()
        # Retain the exact attempted proof/test source, including failed drafts.
        target = args.evidence / f"{args.label}.{path.name}.source.txt"
        with target.open("xb") as handle:
            handle.write(data)
    state = {
        "command": [portable(x) for x in command], "cwd": portable(args.cwd.resolve()),
        "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "limits": {"wall_seconds": args.timeout, "cpu_seconds_per_process": args.cpu_seconds,
                   "address_space_mib_per_process": args.memory_mib, "file_size_mib_per_file": args.file_size_mib,
                   "combined_log_limit_mib": 8, "log_monitor_interval_seconds": 0.2,
                   "sampled_descendant_rss_mib": args.resident_mib,
                   "cleanup_grace_seconds": 5, "aggregate_cgroup_limits": False},
        "source_sha256": sources, "environment": {key: portable(os.environ[key]) for key in (
            "JULIA_DEPOT_PATH", "JULIA_NUM_THREADS", "JULIA_NUM_PRECOMPILE_TASKS", "OPENBLAS_NUM_THREADS",
            "OMP_NUM_THREADS", "LEAN_NUM_THREADS", "PYTHONPATH", "PYTHONNOUSERSITE", "XDG_CACHE_HOME") if key in os.environ},
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }

    def limits():
        if hasattr(os, "sched_setaffinity"):
            os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
        resource.setrlimit(resource.RLIMIT_CPU, (args.cpu_seconds, args.cpu_seconds + 5))
        resource.setrlimit(resource.RLIMIT_AS, (args.memory_mib * 1024 ** 2,) * 2)
        resource.setrlimit(resource.RLIMIT_FSIZE, (args.file_size_mib * 1024 ** 2,) * 2)
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

    child = None
    start = time.monotonic()
    outcome = "completed"
    interrupted = None
    previous_handlers = {}
    peak_sampled_rss = 0

    def descendant_rss(pid):
        pending, seen, rss = [pid], set(), 0
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            try:
                fields = Path(f"/proc/{current}/statm").read_text().split()
                rss += int(fields[1]) * resource.getpagesize()
                pending.extend(int(x) for x in Path(f"/proc/{current}/task/{current}/children").read_text().split())
            except (OSError, ValueError, IndexError):
                pass
        return rss

    def cancel(sig, frame):
        nonlocal interrupted
        interrupted = sig
        raise KeyboardInterrupt

    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[sig] = signal.signal(sig, cancel)
        with stdout_path.open("xb") as out, stderr_path.open("xb") as err:
            child = subprocess.Popen(command, cwd=args.cwd, stdout=out, stderr=err,
                                     start_new_session=True, preexec_fn=limits)
            try:
                while child.poll() is None:
                    if args.resident_mib:
                        observed = descendant_rss(child.pid)
                        peak_sampled_rss = max(peak_sampled_rss, observed)
                        if observed > args.resident_mib * 1024 ** 2:
                            outcome = "resident_limit_exceeded"
                            break
                    remaining = args.timeout - (time.monotonic() - start)
                    if remaining <= 0:
                        outcome = "timeout"
                        break
                    if stdout_path.stat().st_size + stderr_path.stat().st_size > 8 * 1024 ** 2:
                        outcome = "log_limit_exceeded"
                        break
                    try:
                        child.wait(timeout=min(0.2, remaining))
                    except subprocess.TimeoutExpired:
                        pass
            except subprocess.TimeoutExpired:
                outcome = "timeout"
            except KeyboardInterrupt:
                outcome = "cancelled"
            finally:
                # Kill the isolated process group even after normal leader exit,
                # so ordinary non-detaching compiler children cannot outlive it.
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait(timeout=5)
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
    except Exception as error:
        outcome = "runner_error"
        state["error"] = f"{type(error).__name__}: {portable(error)}"
    finally:
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)
        state.update({"outcome": outcome, "returncode": None if child is None else child.returncode,
                      "elapsed_seconds": time.monotonic() - start, "interrupted_signal": interrupted,
                      "cleanup": "process_group_stop_attempted_and_direct_child_reaped" if child else "no_payload_started",
                      "scope_limitation": "Process groups retain ordinary children, not deliberately detached processes. No cgroup-isolation claim.",
                      "finished_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        state["child_usage"] = {"user_seconds": usage.ru_utime, "system_seconds": usage.ru_stime,
                                "peak_rss_kib": usage.ru_maxrss,
                                "peak_sampled_descendant_rss_bytes": peak_sampled_rss}
        state["output"] = {p.name: {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                           for p in (stdout_path, stderr_path) if p.exists()}
        with record_path.open("x", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2)
            handle.write("\n")
    print(json.dumps({"label": args.label, "outcome": outcome, "returncode": state["returncode"],
                      "elapsed_seconds": round(state["elapsed_seconds"], 3)}))
    return 0 if outcome == "completed" and state["returncode"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
