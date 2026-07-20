#!/usr/bin/env python3
"""Cross-check every cited BibTeX DOI against Crossref metadata.

This is a metadata identity check, not a sentence-level claim audit. It reads
the live manuscript, SI and bibliography, queries Crossref for the union of
cited keys, and writes stable JSON/Markdown reports beside this script.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

import requests


SCRIPT = Path(__file__).resolve()
EXPECTED_CITED_KEYS = 44


def locate_manuscript_root() -> Path:
    """Support both manuscript/audit_R582 and release-root/audit layouts."""

    candidates = (SCRIPT.parents[1], SCRIPT.parents[1] / "manuscript")
    required = ("main_R582.tex", "SI_R582.tex", "refs.bib")
    for candidate in candidates:
        if all((candidate / name).is_file() for name in required):
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"Cannot locate active R582 TeX/BibTeX sources; searched: {searched}")


ROOT = locate_manuscript_root()
OUT_JSON = Path(__file__).with_name("CITATION_DOI_CROSSREF_AUDIT.json")
OUT_MD = Path(__file__).with_name("CITATION_DOI_CROSSREF_AUDIT.md")
AUDIT_DATE = "2026-07-20"
MANUAL_OVERRIDES = {
    "Park2021": {
        "note": "identity verified against the publisher-linked KCI record",
        "verification_url": "https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002786128",
    },
    "Tichter2020": {
        "note": "institutional DOI is not registered in Crossref; identity verified in the official Refubium record",
        "verification_url": "https://refubium.fu-berlin.de/handle/fub188/28518?show=full",
    },
}


def cited_keys() -> set[str]:
    text = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in ("main_R582.tex", "SI_R582.tex")
    )
    keys: set[str] = set()
    pattern = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
    for match in pattern.finditer(text):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def bib_entries() -> dict[str, str]:
    text = (ROOT / "refs.bib").read_text(encoding="utf-8")
    starts = list(re.finditer(r"(?m)^\s*@\w+\s*\{\s*([^,\s]+)\s*,", text))
    return {
        match.group(1): text[match.start() : starts[i + 1].start() if i + 1 < len(starts) else len(text)]
        for i, match in enumerate(starts)
    }


def field(entry: str, name: str) -> str | None:
    match = re.search(rf"(?i)\b{re.escape(name)}\s*=\s*", entry)
    if not match:
        return None
    pos = match.end()
    while pos < len(entry) and entry[pos].isspace():
        pos += 1
    if pos >= len(entry):
        return None
    opener = entry[pos]
    if opener == "{":
        depth = 0
        for end in range(pos, len(entry)):
            char = entry[end]
            if char == "{" and (end == 0 or entry[end - 1] != "\\"):
                depth += 1
            elif char == "}" and (end == 0 or entry[end - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    return entry[pos + 1 : end].strip()
    if opener == '"':
        end = pos + 1
        while end < len(entry):
            if entry[end] == '"' and entry[end - 1] != "\\":
                return entry[pos + 1 : end].strip()
            end += 1
    end = entry.find(",", pos)
    return entry[pos : end if end >= 0 else len(entry)].strip()


def normalize_title(value: str) -> str:
    value = re.sub(r"\\[A-Za-z]+", " ", value)
    value = value.replace("{", "").replace("}", "")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def crossref_year(message: dict) -> int | None:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = message.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return int(parts[0][0])
    return None


def query_crossref(session: requests.Session, doi: str) -> tuple[int | None, dict | None, str | None]:
    url = f"https://api.crossref.org/works/{quote(doi, safe='')}"
    for attempt in range(3):
        try:
            response = session.get(url, timeout=20)
        except requests.RequestException as exc:
            if attempt == 2:
                return None, None, str(exc)
            time.sleep(0.5 * (attempt + 1))
            continue
        if response.status_code == 200:
            return 200, response.json().get("message", {}), None
        if response.status_code in (429, 500, 502, 503, 504) and attempt < 2:
            time.sleep(0.8 * (attempt + 1))
            continue
        return response.status_code, None, response.text[:300]
    return None, None, "retry loop exhausted"


def build(refresh: bool) -> dict:
    keys = cited_keys()
    entries = bib_entries()
    if len(keys) != EXPECTED_CITED_KEYS:
        raise RuntimeError(
            f"Expected {EXPECTED_CITED_KEYS} unique active cited keys, found {len(keys)}"
        )
    missing = sorted(keys.difference(entries))
    if missing:
        raise RuntimeError(f"Active citation keys missing from refs.bib: {missing}")
    previous: dict[str, dict] = {}
    if OUT_JSON.is_file() and not refresh:
        try:
            previous = {item["key"]: item for item in json.loads(OUT_JSON.read_text(encoding="utf-8"))["records"]}
        except (KeyError, json.JSONDecodeError):
            previous = {}

    session = requests.Session()
    session.headers.update({"User-Agent": "ZIFB-R582-citation-audit/1.0 (metadata verification)"})
    records: list[dict] = []
    for index, key in enumerate(sorted(keys), start=1):
        entry = entries[key]
        doi = (field(entry, "doi") or "").strip().lower().removeprefix("https://doi.org/")
        local_title = field(entry, "title") or ""
        local_year_text = field(entry, "year") or ""
        local_year_match = re.search(r"\d{4}", local_year_text)
        local_year = int(local_year_match.group()) if local_year_match else None
        cached = previous.get(key)
        if cached and cached.get("doi") == doi and cached.get("http_status") == 200:
            records.append(cached)
            continue
        status, message, error = query_crossref(session, doi)
        if message is None:
            records.append(
                {
                    "key": key,
                    "doi": doi,
                    "http_status": status,
                    "local_title": local_title,
                    "local_year": local_year,
                    "crossref_title": None,
                    "crossref_year": None,
                    "title_similarity": None,
                    "verdict": "FAIL",
                    "note": error or f"HTTP {status}",
                }
            )
            continue
        remote_title = (message.get("title") or [""])[0]
        remote_year = crossref_year(message)
        similarity = SequenceMatcher(None, normalize_title(local_title), normalize_title(remote_title)).ratio()
        year_delta = None if local_year is None or remote_year is None else abs(local_year - remote_year)
        if similarity >= 0.90 and (year_delta is None or year_delta <= 1):
            verdict, note = "PASS", ""
        elif similarity >= 0.75 and (year_delta is None or year_delta <= 2):
            verdict, note = "WARN", "title/year requires manual review"
        else:
            verdict, note = "FAIL", "metadata identity mismatch"
        records.append(
            {
                "key": key,
                "doi": doi,
                "http_status": status,
                "local_title": local_title,
                "local_year": local_year,
                "crossref_title": remote_title,
                "crossref_year": remote_year,
                "title_similarity": round(similarity, 4),
                "verdict": verdict,
                "note": note,
            }
        )
        if index % 10 == 0:
            time.sleep(0.2)

    for item in records:
        override = MANUAL_OVERRIDES.get(item["key"])
        if override:
            item["verdict"] = "PASS"
            item["note"] = override["note"]
            item["verification_url"] = override["verification_url"]

    counts = {name: sum(item["verdict"] == name for item in records) for name in ("PASS", "WARN", "FAIL")}
    return {
        "audit_date": AUDIT_DATE,
        "scope": "union of cited keys in main_R582.tex and SI_R582.tex",
        "counts": counts,
        "records": records,
    }


def write_reports(report: dict) -> None:
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# R582 cited-DOI Crossref audit",
        "",
        f"Date: {report['audit_date']}",
        "",
        "This checks bibliographic identity only; it does not prove that a paper supports a sentence.",
        "",
        f"- PASS: {report['counts']['PASS']}",
        f"- WARN: {report['counts']['WARN']}",
        f"- FAIL: {report['counts']['FAIL']}",
        "",
        "| Verdict | Key | DOI | Local / Crossref year | Title similarity | Note |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in report["records"]:
        if item["verdict"] == "PASS":
            continue
        years = f"{item['local_year']} / {item['crossref_year']}"
        lines.append(
            f"| {item['verdict']} | `{item['key']}` | `{item['doi']}` | {years} | "
            f"{item['title_similarity']} | {item['note']} |"
        )
    if report["counts"]["WARN"] == 0 and report["counts"]["FAIL"] == 0:
        lines.append("| PASS | all cited entries | -- | -- | -- | no metadata mismatches |")
    manual = [item for item in report["records"] if item.get("verification_url")]
    if manual:
        lines.extend(["", "## Manual publisher/repository resolutions", ""])
        for item in manual:
            lines.append(
                f"- `{item['key']}`: {item['note']}. Verification: {item['verification_url']}"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A PASS means that the DOI resolves through Crossref and the returned title/year match the local BibTeX entry. Sentence-level claim support is audited separately against publisher pages or local full text.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    report = build(refresh=args.refresh)
    write_reports(report)
    print(json.dumps(report["counts"], ensure_ascii=False))
    return 1 if report["counts"]["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
