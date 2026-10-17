#!/usr/bin/env python3
"""Generate and check status/status.json (kritva-program status schema 2.0).

Proprietary and confidential. Copyright (c) 2026 Kritvaos. All rights reserved.

Reports task FACTS only (D-011): execution, git_sync, readiness, evidence. Review and acceptance live
in kritva-program approvals.json. Task facts come from ``status/tasks.csv`` (columns: task_id, legacy_id,
title, execution, readiness, implementation_commit). Fails closed on a missing, duplicate or unrecognised
value. ``evidence`` is always empty until real evidence is recorded centrally. ``git_sync`` is SYNCED only
when ``implementation_commit`` is an ancestor of origin/main; with no implementation commit it is
NOT_COMMITTED. ``source.commit`` is the inspected revision (HEAD), not the commit that contains this file.

Usage:  python3 scripts/status/gen_status.py            write status/status.json
        python3 scripts/status/gen_status.py --check    validate; verify it matches status/tasks.csv
Standard library only. Python 3.8+. Exit: 0 ok, 1 check failed, 2 usage/input error.
"""
import argparse, csv, hashlib, json, re, subprocess, sys
from pathlib import Path

EXECUTION = {"NOT_STARTED", "IN_PROGRESS", "BLOCKED", "COMPLETE"}
READINESS = {"PLANNABLE", "IMPLEMENTABLE", "HARDWARE-BLOCKED"}
SHA = re.compile(r"^[0-9a-f]{40}$")


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def validate(value, schema, path="$"):
    """Minimal JSON Schema subset: type, enum, const, required, properties, additionalProperties,
    items, pattern, minLength. Enough for status.schema.json; returns a list of error strings."""
    errs = []
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: {value!r} not in {schema['enum']}")
    types = schema.get("type")
    if types is not None:
        ts = types if isinstance(types, list) else [types]
        py = {"string": str, "object": dict, "array": list, "null": type(None)}
        if not any(isinstance(value, py[t]) for t in ts):
            errs.append(f"{path}: expected {ts}, got {type(value).__name__}")
            return errs
    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path}: {value!r} does not match {schema['pattern']}")
        if len(value) < schema.get("minLength", 0):
            errs.append(f"{path}: too short")
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path}: missing required '{k}'")
        props = schema.get("properties", {})
        for k, v in value.items():
            if k in props:
                errs += validate(v, props[k], f"{path}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{path}: unexpected property '{k}'")
    if isinstance(value, list) and "items" in schema:
        for i, v in enumerate(value):
            errs += validate(v, schema["items"], f"{path}[{i}]")
    return errs


def read_tasks(path):
    rows, seen = [], set()
    with open(path, newline="", encoding="utf-8") as f:
        for n, r in enumerate(csv.DictReader(f), start=2):
            tid = (r.get("task_id") or "").strip()
            if not tid or tid in seen:
                raise ValueError(f"{path}:{n}: missing or duplicate task_id '{tid}'")
            seen.add(tid)
            if r["execution"] not in EXECUTION:
                raise ValueError(f"{path}:{n}: unrecognised execution '{r['execution']}'")
            if r["readiness"] not in READINESS:
                raise ValueError(f"{path}:{n}: unrecognised readiness '{r['readiness']}'")
            ic = (r.get("implementation_commit") or "").strip()
            if ic and not SHA.match(ic):
                raise ValueError(f"{path}:{n}: implementation_commit must be a full 40-hex SHA")
            rows.append(r)
    if not rows:
        raise ValueError(f"{path}: no tasks")
    return rows


def git_sync(root, r):
    ic = (r.get("implementation_commit") or "").strip()
    if not ic:
        return "NOT_COMMITTED"
    if git(root, "cat-file", "-e", ic + "^{commit}")[0] != 0:
        return "NOT_COMMITTED"
    if git(root, "merge-base", "--is-ancestor", ic, "origin/main")[0] == 0:
        return "SYNCED"
    return "COMMITTED"


def task_facts(root, rows):
    return [{"task_id": r["task_id"], "execution": r["execution"], "git_sync": git_sync(root, r),
             "readiness": r["readiness"], "evidence": []} for r in rows]


def build(root, ws, rows):
    rc, commit = git(root, "rev-parse", "HEAD")
    if rc != 0 or not SHA.match(commit):
        raise ValueError("cannot resolve HEAD (not a git checkout?)")
    _, branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    _, when = git(root, "log", "-1", "--format=%cI")
    return {"schema_version": "2.0", "workstream_id": ws["workstream_id"], "repo": ws["repo"],
            "source": {"branch": None if branch in ("", "HEAD") else branch, "commit": commit, "tag": None},
            "tasks": task_facts(root, rows), "updated_at": when}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    sd = a.root / "status"
    try:
        ws = json.loads((sd / "workstream.json").read_text(encoding="utf-8"))
        schema_p = sd / "status.schema.json"
        want = (sd / "status.schema.json.sha256").read_text().split()[0]
        got = hashlib.sha256(schema_p.read_bytes()).hexdigest()
        if want != got:
            print(f"ERROR   vendored schema SHA-256 {got} != recorded {want}")
            return 1
        schema = json.loads(schema_p.read_text(encoding="utf-8"))
        rows = read_tasks(sd / "tasks.csv")
        if a.check:
            cur = json.loads((sd / "status.json").read_text(encoding="utf-8"))
            errs = validate(cur, schema)
            exp = {"workstream_id": ws["workstream_id"], "repo": ws["repo"], "tasks": task_facts(a.root, rows)}
            for k, v in exp.items():
                if k == "tasks":
                    # git_sync may legitimately advance after the report was written; compare the rest
                    strip = lambda ts: [{x: y for x, y in t.items() if x != "git_sync"} for t in ts]
                    if strip(cur.get(k, [])) != strip(v):
                        errs.append("tasks differ from status/tasks.csv (regenerate with gen_status.py)")
                elif cur.get(k) != v:
                    errs.append(f"{k} differs from status/workstream.json")
            for e in errs:
                print("ERROR  ", e)
            print(f"gen_status --check: {len(cur.get('tasks', []))} task(s); {len(errs)} error(s).")
            return 1 if errs else 0
        out = build(a.root, ws, rows)
        errs = validate(out, schema)
        if errs:
            print("\n".join("ERROR   " + e for e in errs))
            return 1
        (sd / "status.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        print(f"gen_status: wrote status/status.json ({len(out['tasks'])} tasks, source {out['source']['commit'][:8]})")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"gen_status: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
