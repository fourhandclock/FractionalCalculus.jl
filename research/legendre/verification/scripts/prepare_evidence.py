"""Normalize only private path prefixes in new local execution evidence.

Raw copies are retained in an ignored local directory. Supplied inputs and
mathematical sources are never edited. Existing normalization manifests are
refused, so this cannot silently replace evidence from an earlier execution.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=ROOT / "research/legendre/verification/results/checkpoint-st04")
    parser.add_argument("--raw-dir", type=Path, default=ROOT / ".checkpoint-tools/raw-evidence")
    args = parser.parse_args()
    manifest = args.evidence / "path-normalization.json"
    if manifest.exists():
        parser.error("normalization already recorded; use a new evidence directory")
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    substitutions = [(str(ROOT).encode(), b"$WORKSPACE"), (str(Path.home()).encode(), b"$USER_HOME")]
    changed = {}
    for path in sorted(args.evidence.iterdir()):
        if path.suffix not in (".json", ".log"):
            continue
        data = path.read_bytes()
        normalized = data
        for old, new in substitutions:
            normalized = normalized.replace(old, new)
        if normalized != data:
            raw = args.raw_dir / path.name
            with raw.open("xb") as handle:
                handle.write(data)
            path.write_bytes(normalized)
            changed[path.name] = {"raw_sha256": digest(data), "public_sha256": digest(normalized),
                                  "raw_copy": f"$WORKSPACE/.checkpoint-tools/raw-evidence/{path.name}"}
    # Run records retain the original hashes explicitly, while their active
    # output hashes refer to the publishable, path-normalized logs.
    for path in sorted(args.evidence.glob("*.json")):
        record = json.loads(path.read_text())
        if "output" not in record:
            continue
        updates = {name: info for name, info in record["output"].items() if name in changed}
        if not updates:
            continue
        raw = args.raw_dir / path.name
        if not raw.exists():
            with raw.open("xb") as handle:
                handle.write(path.read_bytes())
        record["raw_output_before_path_normalization"] = updates
        record["path_normalization_manifest"] = "path-normalization.json"
        for name in updates:
            data = (args.evidence / name).read_bytes()
            record["output"][name] = {"bytes": len(data), "sha256": digest(data)}
        path.write_text(json.dumps(record, indent=2) + "\n")
        changed[path.name] = {"raw_sha256": digest(raw.read_bytes()), "public_sha256": digest(path.read_bytes()),
                              "raw_copy": f"$WORKSPACE/.checkpoint-tools/raw-evidence/{path.name}"}
    report = {"scope": "Only workspace/user-home path prefix substitution and explicit output-hash bookkeeping; no lines or numbers removed.",
              "prefix_categories": ["workspace directory -> $WORKSPACE", "user home -> $USER_HOME"],
              "files": changed}
    with manifest.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"normalized_files": len(changed), "manifest": manifest.name}))


if __name__ == "__main__":
    main()
