"""Populate the committed Lean lockfile using shallow exact-revision fetches.

This setup command requires separately authorized network access. It never
refreshes revisions, edits an existing checkout, or fetches full history.
It operates only on this verification project's ignored dependency cache.
"""

import json
from pathlib import Path
import re
import subprocess


LEAN = Path(__file__).resolve().parents[1] / "lean"


def git(*args):
    return subprocess.run(["git", *map(str, args)], check=True, timeout=90,
                          stdout=subprocess.PIPE, text=True).stdout.strip()


def main():
    manifest = json.loads((LEAN / "lake-manifest.json").read_text())
    cache = LEAN / ".lake/packages"
    cache.mkdir(parents=True, exist_ok=True)
    for entry in manifest["packages"]:
        name, revision, url = entry["name"], entry["rev"], entry["url"]
        if entry["type"] != "git" or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", name):
            raise ValueError("Unsupported lockfile package")
        if not re.fullmatch(r"[0-9a-f]{40}", revision) or not url.startswith("https://github.com/"):
            raise ValueError("Expected an exact source revision and official GitHub dependency URL")
        target = cache / name
        if target.exists():
            if git("-C", target, "rev-parse", "HEAD") != revision:
                raise RuntimeError(f"Existing {name} has a different revision; left untouched")
            if git("-C", target, "status", "--porcelain"):
                raise RuntimeError(f"Existing {name} has source changes; left untouched")
        else:
            git("init", "-q", target)
            git("-C", target, "remote", "add", "origin", url)
            git("-C", target, "fetch", "--depth=1", "--no-tags", "origin", revision)
            git("-C", target, "checkout", "--quiet", "--detach", "FETCH_HEAD")
            if git("-C", target, "rev-parse", "HEAD") != revision:
                raise RuntimeError(f"Unexpected fetched revision for {name}")
        # Lake's cloud-release lookup needs an exact local release tag.
        # Fetch only the lockfile's explicit tag, then verify its peeled hash.
        tag = entry.get("inputRev", "")
        if re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
            present = subprocess.run(["git", "-C", str(target), "show-ref", "--verify", "--quiet", f"refs/tags/{tag}"])
            if present.returncode:
                git("-C", target, "fetch", "--depth=1", "--no-tags", "origin", f"refs/tags/{tag}:refs/tags/{tag}")
            if git("-C", target, "rev-parse", f"refs/tags/{tag}^{{commit}}") != revision:
                raise RuntimeError(f"Release tag for {name} does not match its pinned revision")
        print(f"{name}: {revision} (verified shallow source)", flush=True)


if __name__ == "__main__":
    main()
