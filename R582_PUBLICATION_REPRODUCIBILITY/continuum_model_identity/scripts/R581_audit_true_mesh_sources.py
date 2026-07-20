from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
INPUTS = ROOT / "inputs"
MANIFESTS = ROOT / "manifests"
EXPECTED_INPUT_SHA256 = "4813B306F39330CCEAF819C4AB8815C55A3DF8A04726741F33ACB801B8806B9B"
EXPECTED_INPUT_BYTES = 889_150_140

SOURCE_NAMES = [
    "R581TrueMeshBuildProbe.java",
    "R581TrueMeshControlRun.java",
    "R581TrueMeshPhysicalRun.java",
]
INPUT_NAMES = [
    "R581_true_mesh_probe_input_COPY.mph",
    "R581_true_mesh_control_input_COPY.mph",
    "R581_true_mesh_physical_input_COPY.mph",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def extract_method(source: str, signature: str) -> str:
    start = source.index(signature)
    brace = source.index("{", start)
    depth = 0
    for index in range(brace, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise ValueError(f"Unclosed method {signature}")


def parse_probe_log(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"status": "not_run", "path": str(path)}
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r"TRUE_MESH_PROBE_OK,before_elements=(\d+),after_elements=(\d+),ratio=([0-9.eE+-]+),no_study_run=true",
        text,
    )
    if not match:
        return {"status": "log_present_but_acceptance_marker_missing", "path": str(path)}
    before = int(match.group(1))
    after = int(match.group(2))
    return {
        "status": "pass" if before == 1944 and after > before else "fail",
        "path": str(path),
        "before_elements": before,
        "after_elements": after,
        "ratio": float(match.group(3)),
        "no_study_run": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--probe-log",
        type=Path,
        default=ROOT / "logs" / "R581_true_mesh_probe_stdout.txt",
    )
    args = parser.parse_args()

    sources: dict[str, str] = {}
    source_records: list[dict[str, object]] = []
    required_literals = [
        'static final String HMAX = "0.00067";',
        'static final String HMIN = "3e-6";',
        'static final String HGRAD = "1.2";',
        "static final int DIS1_NUMELEM = 36;",
        "static final int DIS2_NUMELEM = 36;",
        "static final int DIS3_NUMELEM = 72;",
        '.feature("size").set("custom", "on")',
        '.feature("size").set("hmax", HMAX)',
        '.feature("size").set("hmin", HMIN)',
        '.feature("size").set("hgrad", HGRAD)',
        '.feature("map1").feature("dis1").set("numelem", DIS1_NUMELEM)',
        '.feature("map1").feature("dis2").set("numelem", DIS2_NUMELEM)',
        '.feature("map1").feature("dis3").set("numelem", DIS3_NUMELEM)',
        'mesh("mesh1").run()',
    ]
    for name in SOURCE_NAMES:
        path = SCRIPTS / name
        source = path.read_text(encoding="utf-8")
        sources[name] = source
        missing = [literal for literal in required_literals if literal not in source]
        source_records.append(
            {
                "file": name,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "brace_balance": source.count("{") - source.count("}"),
                "required_mesh_literals_all_present": not missing,
                "missing_literals": missing,
            }
        )

    probe_source = sources["R581TrueMeshBuildProbe.java"]
    probe_no_study_run = '.study("stdR522").run()' not in probe_source and "SOLVE_START" not in probe_source
    probe_saves_new_output_only = (
        "R581_true_mesh_probe_MESHED_ONLY.mph" in probe_source
        and "model.save(OUTPUT_MPH)" in probe_source
        and "model.save(INPUT_MPH)" not in probe_source
    )

    control_method = extract_method(
        sources["R581TrueMeshControlRun.java"], "static void applyTrueMeshRefinement(Model model)"
    )
    physical_method = extract_method(
        sources["R581TrueMeshPhysicalRun.java"], "static void applyTrueMeshRefinement(Model model)"
    )
    paired_mesh_method_identical = control_method == physical_method

    input_records: list[dict[str, object]] = []
    for name in INPUT_NAMES:
        path = INPUTS / name
        size = path.stat().st_size
        sha = sha256_file(path)
        input_records.append(
            {
                "file": name,
                "bytes": size,
                "sha256": sha,
                "size_pass": size == EXPECTED_INPUT_BYTES,
                "hash_pass": sha == EXPECTED_INPUT_SHA256,
            }
        )

    runtime_probe = parse_probe_log(args.probe_log)
    static_pass = bool(
        all(record["brace_balance"] == 0 for record in source_records)
        and all(record["required_mesh_literals_all_present"] for record in source_records)
        and probe_no_study_run
        and probe_saves_new_output_only
        and paired_mesh_method_identical
        and all(record["size_pass"] and record["hash_pass"] for record in input_records)
    )
    payload = {
        "audit_id": "R581_TRUE_MESH_STATIC_AUDIT",
        "static_status": "PASS" if static_pass else "FAIL",
        "runtime_probe": runtime_probe,
        "expected_input_elements": 1944,
        "required_refinement": {
            "hmax_m": 0.00067,
            "hmin_m": 0.000003,
            "hgrad": 1.2,
            "mapped_distribution_numelem": [36, 36, 72],
            "reason_for_distribution_refinement": (
                "mesh1/map1 uses explicit Distribution features 18/18/36; default-size changes alone retained 1944 elements"
            ),
        },
        "probe_no_study_run_static_check": probe_no_study_run,
        "probe_saves_new_output_only": probe_saves_new_output_only,
        "control_physical_mesh_method_byte_identical": paired_mesh_method_identical,
        "control_physical_mesh_method_sha256": hashlib.sha256(control_method.encode("utf-8")).hexdigest().upper(),
        "sources": source_records,
        "inputs": input_records,
        "launch_guard": "Do not compile/run the probe or either solve while another COMSOL process is active.",
    }
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    output = MANIFESTS / "R581_TRUE_MESH_STATIC_AUDIT.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    print(payload["static_status"])
    if not static_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
