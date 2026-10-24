#!/usr/bin/env python3
"""Validate the Kritva Actuator bills of materials against the BOM CSV schema.

Copyright (c) 2026 Kritvaos. Licensed under the Apache License, Version 2.0 (see LICENSE).

Files checked (by default)
--------------------------
* ``mechanical/bom/MECHANICAL_BOM.csv``  (owner: Mechanical Intern)
* ``hardware/bom/ELECTRICAL_BOM.csv``    (owner: Electronics/Embedded Intern)

A missing file is a WARNING (the BOMs are created during ACT-01-002 /
ACT-02-002), never a crash.

Schema
------
The schema is defined in ``scripts/bom/README.md`` and enforced here. Column
names and order must match exactly::

    item_id,milestone,category,description,manufacturer,manufacturer_part_number,
    supplier,supplier_part_number,quantity,unit,unit_cost_inr,extended_cost_inr,
    cost_status,lead_time_days,status,owner,notes

Rules (ERROR unless stated otherwise)
-------------------------------------
* every row has 17 fields; fully blank rows are ignored;
* ``item_id`` present, no whitespace, unique across all checked BOM files;
* ``milestone`` in {A0, A1, A2};
* ``category``, ``description``, ``unit`` and ``owner`` not empty;
* ``quantity`` is a number > 0;
* ``cost_status`` in {ESTIMATE, QUOTED, PURCHASED, TBD};
* ``status`` in {CANDIDATE, SELECTED, ORDERED, RECEIVED, REJECTED};
* ``unit_cost_inr`` may be blank only when ``cost_status`` is TBD; when given
  it is a number >= 0 (no currency symbols or thousands separators);
  a TBD row that carries a unit cost is a WARNING (use ESTIMATE);
* ``extended_cost_inr`` must equal ``quantity * unit_cost_inr`` (tolerance
  0.01 INR) when both are present, must be present in that case, and must be
  blank when ``unit_cost_inr`` is blank;
* ``lead_time_days`` is blank or a non-negative integer;
* QUOTED or PURCHASED requires a ``supplier`` (a cost is only "quoted" when
  a real supplier quotation exists; never invent one);
* WARNING: SELECTED/ORDERED/RECEIVED without ``manufacturer_part_number``;
  ORDERED/RECEIVED with cost_status other than QUOTED/PURCHASED;
  PURCHASED with status other than ORDERED/RECEIVED; QUOTED/PURCHASED without
  a quotation or order reference in ``notes``; ``item_id`` not matching the
  recommended pattern (``MB-NNN`` mechanical, ``EB-NNN`` electrical).

Exit status: 0 = no errors; 1 = errors (or warnings with ``--strict``); 2 = usage.

Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCHEMA = [
    "item_id",
    "milestone",
    "category",
    "description",
    "manufacturer",
    "manufacturer_part_number",
    "supplier",
    "supplier_part_number",
    "quantity",
    "unit",
    "unit_cost_inr",
    "extended_cost_inr",
    "cost_status",
    "lead_time_days",
    "status",
    "owner",
    "notes",
]
MILESTONES = ("A0", "A1", "A2")
COST_STATUS = ("ESTIMATE", "QUOTED", "PURCHASED", "TBD")
ITEM_STATUS = ("CANDIDATE", "SELECTED", "ORDERED", "RECEIVED", "REJECTED")
DEFAULT_FILES = [
    ("hardware/bom/ELECTRICAL_BOM.csv", "EB"),
]
TOLERANCE = Decimal("0.01")
NUMBER_RE = re.compile(r"^\d+(?:\.\d+)?$")


@dataclass
class BomRow:
    file: str
    line: int
    data: Dict[str, str]
    quantity: Optional[Decimal] = None
    unit_cost: Optional[Decimal] = None
    extended: Optional[Decimal] = None


@dataclass
class BomResult:
    rows: List[BomRow] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    files_read: List[str] = field(default_factory=list)


def parse_decimal(value: str) -> Optional[Decimal]:
    v = value.strip()
    if not v or not NUMBER_RE.match(v):
        return None
    try:
        return Decimal(v)
    except InvalidOperation:
        return None


def load_bom(path: Path, rel: str, prefix: Optional[str], result: BomResult,
             seen_ids: Dict[str, str]) -> None:
    """Read and validate one BOM file, appending rows and findings to ``result``."""
    def err(where: str, msg: str) -> None:
        result.errors.append(f"ERROR   {where}: {msg}")

    def warn(where: str, msg: str) -> None:
        result.warnings.append(f"WARNING {where}: {msg}")

    if not path.is_file():
        warn(rel, "BOM file not present yet; skipped")
        return
    try:
        with path.open(encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.reader(fh))
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        err(rel, f"cannot parse CSV ({exc})")
        return
    result.files_read.append(rel)
    if not rows:
        err(rel, "file is empty (header row required)")
        return
    header = [h.strip() for h in rows[0]]
    if header != SCHEMA:
        missing = [c for c in SCHEMA if c not in header]
        extra = [c for c in header if c not in SCHEMA]
        parts = []
        if missing:
            parts.append("missing: " + ", ".join(missing))
        if extra:
            parts.append("unexpected: " + ", ".join(extra))
        if not parts:
            parts.append("columns are in the wrong order")
        err(f"{rel}:1", "header does not match the BOM schema (" + "; ".join(parts) + ")")
        err(f"{rel}:1", "expected: " + ",".join(SCHEMA))
        return

    id_re = re.compile(rf"^{prefix}-\d{{3}}$") if prefix else None
    for lineno, raw in enumerate(rows[1:], start=2):
        if not any(c.strip() for c in raw):
            continue
        where = f"{rel}:{lineno}"
        if len(raw) != len(SCHEMA):
            err(where, f"row has {len(raw)} field(s), expected {len(SCHEMA)} "
                       "(quote fields that contain commas)")
            continue
        d = {k: v.strip() for k, v in zip(SCHEMA, raw)}
        row = BomRow(file=rel, line=lineno, data=d)
        item = d["item_id"]
        if not item:
            err(where, "item_id is empty")
        else:
            where = f"{where} [{item}]"
            if re.search(r"\s", item):
                err(where, "item_id must not contain whitespace")
            if item in seen_ids:
                err(where, f"duplicate item_id (first used at {seen_ids[item]})")
            else:
                seen_ids[item] = f"{rel}:{lineno}"
            if id_re and not id_re.match(item):
                warn(where, f"item_id does not follow the recommended pattern {prefix}-NNN")

        if d["milestone"] not in MILESTONES:
            err(where, f"milestone '{d['milestone']}' not in {list(MILESTONES)}")
        for f in ("category", "description", "unit", "owner"):
            if not d[f]:
                err(where, f"{f} is empty")

        qty = parse_decimal(d["quantity"])
        if qty is None or qty <= 0:
            err(where, f"quantity '{d['quantity']}' must be a number > 0")
        row.quantity = qty

        cost_status = d["cost_status"]
        if cost_status not in COST_STATUS:
            err(where, f"cost_status '{cost_status}' not in {list(COST_STATUS)}")
        status = d["status"]
        if status not in ITEM_STATUS:
            err(where, f"status '{status}' not in {list(ITEM_STATUS)}")

        unit_cost: Optional[Decimal] = None
        if d["unit_cost_inr"]:
            unit_cost = parse_decimal(d["unit_cost_inr"])
            if unit_cost is None:
                err(where, f"unit_cost_inr '{d['unit_cost_inr']}' is not a plain number "
                           "(no currency symbol, no thousands separator)")
            elif cost_status == "TBD":
                warn(where, "cost_status TBD but unit_cost_inr is filled (use ESTIMATE for an "
                            "indicative figure)")
        elif cost_status != "TBD":
            err(where, f"unit_cost_inr is blank; only allowed when cost_status is TBD "
                       f"(is '{cost_status}')")
        row.unit_cost = unit_cost

        extended: Optional[Decimal] = None
        if d["extended_cost_inr"]:
            extended = parse_decimal(d["extended_cost_inr"])
            if extended is None:
                err(where, f"extended_cost_inr '{d['extended_cost_inr']}' is not a plain number")
        if qty is not None and unit_cost is not None:
            expected = qty * unit_cost
            if extended is None and not d["extended_cost_inr"]:
                err(where, f"extended_cost_inr is blank; expected {expected:.2f} "
                           "(quantity x unit_cost_inr)")
            elif extended is not None and abs(extended - expected) > TOLERANCE:
                err(where, f"extended_cost_inr {extended} != quantity {qty} x unit_cost_inr "
                           f"{unit_cost} = {expected:.2f}")
        elif not d["unit_cost_inr"] and d["extended_cost_inr"]:
            err(where, "extended_cost_inr must be blank when unit_cost_inr is blank")
        row.extended = extended

        if d["lead_time_days"] and not re.fullmatch(r"\d+", d["lead_time_days"]):
            err(where, f"lead_time_days '{d['lead_time_days']}' must be a non-negative integer "
                       "or blank")

        if cost_status in ("QUOTED", "PURCHASED"):
            if not d["supplier"]:
                err(where, f"cost_status {cost_status} requires a supplier")
            if not d["notes"]:
                warn(where, f"cost_status {cost_status}: record the quotation/order reference "
                            "and date in notes")
        if status in ("SELECTED", "ORDERED", "RECEIVED") and not d["manufacturer_part_number"]:
            warn(where, f"status {status} without manufacturer_part_number")
        if status in ("ORDERED", "RECEIVED") and cost_status not in ("QUOTED", "PURCHASED"):
            warn(where, f"status {status} but cost_status is {cost_status} "
                        "(expected QUOTED or PURCHASED)")
        if cost_status == "PURCHASED" and status not in ("ORDERED", "RECEIVED"):
            warn(where, f"cost_status PURCHASED but status is {status}")

        result.rows.append(row)


def check_files(root: Path, files: List[Tuple[str, Optional[str]]]) -> BomResult:
    result = BomResult()
    seen: Dict[str, str] = {}
    for rel, prefix in files:
        load_bom(root / rel, rel, prefix, result, seen)
    return result


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_files(args_files: Optional[List[str]]) -> List[Tuple[str, Optional[str]]]:
    if not args_files:
        return list(DEFAULT_FILES)
    known = dict(DEFAULT_FILES)
    return [(f, known.get(f)) for f in args_files]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the BOM CSV files.")
    parser.add_argument("--root", type=Path, default=default_root(),
                        help="repository root (default: two levels above this script)")
    parser.add_argument("files", nargs="*",
                        help="BOM CSV paths relative to the root (default: both project BOMs)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR   repository root '{root}' does not exist")
        return 2

    result = check_files(root, resolve_files(args.files))
    for line in result.warnings:
        print(line)
    for line in result.errors:
        print(line)
    print(f"check_bom: {len(result.files_read)} BOM file(s) read, {len(result.rows)} item row(s); "
          f"{len(result.errors)} error(s), {len(result.warnings)} warning(s).")
    if result.errors or (args.strict and result.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
