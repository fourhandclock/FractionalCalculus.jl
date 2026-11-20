"""Portable static integrity audit of the validated ST-04 checkpoint.

This checks retained execution records; it does not itself compile LaTeX/Lean
or run a numerical method. --library-tree selects the exact intended package
snapshot when unrelated work is present in the surrounding working tree.
"""

import argparse
import ast
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
RUN = HERE / "results/checkpoint-st04"
REQUIRED = {
    "julia-legendre-01", "python-counterexamples-01", "python-st03-01",
    "python-st04-01", "latex-checkpoint-01", "lean-coefficients-06",
    "lean-quadrature-02", "lean-coefficient-axioms-01", "lean-quadrature-axioms-01",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def heading_anchors(path):
    anchors, counts = [], Counter()
    for match in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", path.read_text(), re.MULTILINE):
        heading = re.sub(r"[`*_]", "", match[1].lower())
        slug = "".join(ch for ch in heading if ch.isalnum() or ch in " -_").replace(" ", "-")
        count = counts[slug]
        counts[slug] += 1
        anchors.append(slug if count == 0 else f"{slug}-{count}")
    return set(anchors)


def public(path):
    return not any(x in path.parts for x in (".lake", "__pycache__", "integration-2026-11-20", "latex-build"))


def run_checks(library_tree):
    checks = []

    def check(name, condition, details):
        checks.append({"check": name, "passed": bool(condition), "details": details})

    protected = json.loads((RUN / "protected-files.json").read_text())["files"]
    changed = []
    for name, record in protected.items():
        path = library_tree / name
        if not path.is_file() or digest(path.read_bytes().replace(b"\r\n", b"\n")) != record["lf_sha256"]:
            changed.append(name)
    check("production_and_historical_files", not changed,
          {"files_checked": len(protected), "changed_or_missing": changed, "comparison": "LF-normalized SHA-256"})
    runner = Path("studies/legendre/test/runtests.jl")
    check("tested_entrypoint_includes_audit",
          (library_tree / runner).read_bytes() == (ROOT / runner).read_bytes()
          and (ROOT / runner).read_text().count('include("proof_audit.jl")') == 1,
          "The intended study entrypoint matches the executed snapshot and includes the actual-library audit once.")

    for record in json.loads((HERE / "sources/inputs.json").read_text())["inputs"]:
        path = HERE / record["path"]
        check(f"input:{record['basename']}", path.is_file() and digest(path.read_bytes()) == record["sha256"],
              {"bytes": record["bytes"], "sha256": record["sha256"]})
    main = HERE / "mathematical-verification.tex"
    original = HERE / "sources/legendre_spectral_verification_notes_st04.tex"
    check("original_author_latex", main.read_bytes() == original.read_bytes(), "Byte-identical; not reconstructed ST-04 LaTeX.")

    for path in sorted((HERE / "scripts").glob("*.py")):
        try:
            compile(ast.parse(path.read_text(), filename=path.name), path.name, "exec")
            ok, detail = True, "Parsed/compiled in memory; not evaluated."
        except (SyntaxError, ValueError) as error:
            ok, detail = False, str(error)
        check(f"python_syntax:{path.name}", ok, detail)

    broken, count = [], 0
    for path in sorted(HERE.rglob("*.md")):
        if not public(path):
            continue
        for match in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            value = match[1].strip().strip("<>")
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            count += 1
            if not target.exists() or not public(target):
                broken.append({"from": str(path.relative_to(HERE)), "target": value})
            elif parsed.fragment and target.suffix == ".md" and unquote(parsed.fragment) not in heading_anchors(target):
                broken.append({"from": str(path.relative_to(HERE)), "target": value, "reason": "missing anchor"})
    check("public_local_links", not broken, {"checked": count, "broken": broken, "external_links_fetched": False})

    tex = re.sub(r"(?<!\\)%[^\n]*", "", main.read_text())
    stack, errors = [], []
    for position, character in enumerate(tex):
        if character not in "{}":
            continue
        n, previous = 0, position - 1
        while previous >= 0 and tex[previous] == "\\":
            n, previous = n + 1, previous - 1
        if n % 2:
            continue
        if character == "{":
            stack.append(position)
        elif stack:
            stack.pop()
        else:
            errors.append(position)
    check("tex_literal_braces", not stack and not errors, {"unclosed": stack, "unmatched": errors})
    env, errors = [], []
    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", tex):
        if match[1] == "begin":
            env.append(match[2])
        elif env and env[-1] == match[2]:
            env.pop()
        else:
            errors.append(match.group())
    check("tex_environment_nesting", not env and not errors, {"unclosed": env, "mismatches": errors})
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", tex)
    check("tex_references", len(labels) == len(set(labels)) and set(refs) <= set(labels),
          {"labels": len(labels), "references": len(refs), "missing": sorted(set(refs) - set(labels))})
    sections = re.split(r"\\section\{", tex)[1:]
    equations = [len(re.findall(r"\\begin\{equation\}", s)) for s in sections]
    props = [len(re.findall(r"\\begin\{proposition\}", s)) for s in sections]
    check("source_mathematical_structure", equations == [2, 0, 0, 6, 7, 7, 7, 0] and props == [0, 0, 0, 2, 2, 1, 0, 0]
          and len(re.findall(r"\\begin\{observation\}", tex)) == 8,
          {"sections": len(sections), "equations_by_section": equations, "propositions_by_section": props})
    for left, right in ((r"\[", r"\]"), (r"\(", r"\)")):
        check(f"math_delimiters:{left}", tex.count(left) == tex.count(right), {"opens": tex.count(left), "closes": tex.count(right)})

    theorem_names = []
    forbidden = []
    for path in sorted((HERE / "lean").glob("*.lean")):
        source = re.sub(r"--[^\n]*", "", path.read_text())
        if re.search(r"\b(sorry|admit|axiom)\b", source):
            forbidden.append(path.name)
        theorem_names += re.findall(r"^theorem\s+(\w+)", source, re.MULTILINE)
    check("lean_source_integrity", len(theorem_names) == 23 and not forbidden,
          {"theorems": len(theorem_names), "forbidden_declarations": forbidden})
    audited = []
    bad_axioms = []
    for label in ("lean-coefficient-axioms-01", "lean-quadrature-axioms-01"):
        output = (RUN / f"{label}.stdout.log").read_text()
        for name, axioms in re.findall(r"'LegendreAudit\.(\w+)' depends on axioms: \[([^]]*)\]", output):
            audited.append(name)
            bad_axioms.extend(set(x.strip() for x in axioms.split(",")) - {"propext", "Classical.choice", "Quot.sound"})
        if "sorryAx" in output:
            bad_axioms.append("sorryAx")
    check("axiom_audit", Counter(audited) == Counter(theorem_names) and not bad_axioms,
          {"audited_theorems": len(audited), "unexpected_axioms": bad_axioms})

    index = json.loads((RUN / "validation-index.json").read_text())
    check("required_run_inventory", set(index["required_runs"]) == REQUIRED, sorted(index["required_runs"]))
    for label in sorted(REQUIRED):
        record = json.loads((RUN / f"{label}.json").read_text())
        stale = []
        for name, sha in record["source_sha256"].items():
            relative = name.removeprefix("$WORKSPACE/")
            prefix = ".checkpoint-tools/checkpoint-tree/"
            target = library_tree / relative[len(prefix):] if relative.startswith(prefix) else ROOT / relative
            if not target.is_file() or digest(target.read_bytes()) != sha:
                stale.append(name)
        outputs = []
        for name, info in record["output"].items():
            path = RUN / name
            if not path.is_file() or digest(path.read_bytes()) != info["sha256"] or path.stat().st_size != info["bytes"]:
                outputs.append(name)
        check(f"retained_run:{label}", record["outcome"] == "completed" and record["returncode"] == 0 and not stale and not outputs,
              {"stale_sources": stale, "changed_outputs": outputs, "outcome": record["outcome"], "returncode": record["returncode"]})

    return {"created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "kind": "static_checkpoint_integrity", "python_version": sys.version,
            "payloads_executed_by_this_check": False, "checks": checks,
            "passed": all(c["passed"] for c in checks)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library-tree", type=Path, default=ROOT)
    parser.add_argument("--report", type=Path, help="New JSON output; never overwrites old evidence.")
    args = parser.parse_args()
    report = run_checks(args.library_tree.resolve())
    if args.report:
        with args.report.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
            handle.write("\n")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
