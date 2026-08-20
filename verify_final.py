#!/usr/bin/env python3
"""Verify the published D-RUT audit contract without rerunning experiments."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDENTITY = (
    "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
)
EXPECTED_STATUS = (
    "INCONCLUSIVE_SIX_FINITE_CLASSICAL_PROXIES_C4_NON_STRICT_"
    "C6_IDFT_UNTESTED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE"
)
EXPECTED_RECOVERY_SHA = (
    "24822b201ed725b770d06b7fbbc141d1d62209237a590cacde571f9645a0b29f"
)


def fail(reason: str) -> None:
    print("FINAL_AUDIT=FAILED reason=" + reason)
    raise SystemExit(1)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("git_" + "_".join(args))
    return result.stdout.strip()


def load(relative_path: str) -> dict:
    try:
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(relative_path + "_invalid_" + type(error).__name__)
    raise AssertionError("unreachable")


branches = {
    line
    for line in git(
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:short)",
    ).splitlines()
    if line
}
if branches != {"main"}:
    fail("branches_" + ",".join(sorted(branches)))
if git("branch", "--show-current") != "main":
    fail("head_not_main")

all_refs = git(
    "for-each-ref",
    "--format=%(refname)",
).splitlines()
if any(
    ref.endswith("/master") or "/orx/" in ref
    for ref in all_refs
):
    fail("legacy_branch_ref")

commit_count = int(git("rev-list", "--count", "--all"))
if commit_count != 4:
    fail("commit_count_" + str(commit_count))

identity_rows = git(
    "log",
    "--all",
    "--format=%an <%ae>|%cn <%ce>",
).splitlines()
expected_row = EXPECTED_IDENTITY + "|" + EXPECTED_IDENTITY
if not identity_rows or any(row != expected_row for row in identity_rows):
    fail("noncanonical_commit_identity")

claims_doc = load("claims.json")
claims = {claim["id"]: claim for claim in claims_doc["claims"]}
expected_claims = {
    "C1": "VERIFIED_CLASSICAL_PROXY",
    "C2": "VERIFIED_CLASSICAL_PROXY",
    "C3": "VERIFIED_LINEAR_PROXY",
    "C4": "NON_STRICT_PROXY_ONLY",
    "C5": "VERIFIED_GENERIC_PROXY",
    "C6": "VERIFIED_RADIAL_PROXY_IDFT_UNTESTED",
}
if {claim_id: claims[claim_id]["status"] for claim_id in expected_claims} != expected_claims:
    fail("claim_statuses")
if claims_doc["audit"]["status"] != EXPECTED_STATUS:
    fail("claims_audit_status")
if claims_doc["audit"]["finite_proxies_passed"] != 6:
    fail("finite_proxies_passed")
if claims_doc["audit"]["paper_claims_verified"] != 0:
    fail("paper_claims_verified")
if claims_doc["audit"]["evidence_points"] != 12:
    fail("claims_evidence_points")

verdict = load("outputs/verdict.json")
if verdict.get("scope") != "bounded_clean_room_proxies":
    fail("verdict_scope")
if verdict.get("paper_reproduction") != "inconclusive":
    fail("paper_reproduction_status")
for name in (
    "c1_heisenberg",
    "c2_single_mode",
    "c3_spam_bound",
    "c4_covariance",
    "c5_bisection",
    "c6_chebyshev",
):
    claim = verdict.get("claims", {}).get(name, {})
    if claim.get("passed") is not True:
        fail(name + "_result")
    if claim.get("paper_claim_directly_tested") is not False:
        fail(name + "_paper_boundary")
if verdict["claims"]["c4_covariance"].get("strict_improvement_observed") is not False:
    fail("c4_strict_boundary")
if verdict["claims"]["c6_chebyshev"].get("idft_path_tested") is not False:
    fail("c6_idft_boundary")

gate = load("publication_gate.json")
if gate.get("tests_passed") is not True:
    fail("gate_tests")
if gate.get("publication_gate_passed") is not True:
    fail("gate_publication")
if gate.get("finite_proxy_diagnostics_passed") != 6:
    fail("gate_finite_proxies")
if gate.get("paper_claims_verified") != 0:
    fail("gate_paper_claims")
if gate.get("overall_status") != "INCONCLUSIVE":
    fail("gate_status")
if gate.get("quantum_protocol_implemented") is not False:
    fail("gate_quantum_boundary")
if gate.get("strict_hierarchical_improvement_observed") is not False:
    fail("gate_strict_boundary")
if gate.get("idft_path_tested") is not False:
    fail("gate_idft_boundary")

verdicts = load("reproduction_verdicts.json")
if verdicts.get("audit_status") != EXPECTED_STATUS:
    fail("verdict_status")
if verdicts.get("evidence", {}).get("current_score_claim") is not False:
    fail("current_score_claim")
if verdicts.get("evidence", {}).get("publication_allowed") is not False:
    fail("publication_boundary")

state = load("AUTONOMOUS_STATE.json")
if state.get("status") != EXPECTED_STATUS:
    fail("state_status")
if state.get("recovery", {}).get("bundle_sha256") != EXPECTED_RECOVERY_SHA:
    fail("recovery_sha")

manifest = load("EVIDENCE_MANIFEST.json")
missing = [
    path
    for path in manifest["required_paths"]
    if not (ROOT / path).is_file()
]
if missing:
    fail("missing_paths_" + ",".join(missing))

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for marker in (
    "2510.08419",
    "STATUS.md",
    "CLAIM_EVIDENCE.md",
    "Thank you",
    "not an author-maintained implementation",
    "0/6 paper claims",
    "IDFT",
):
    if marker not in readme:
        fail("readme_" + marker.replace(" ", "_"))

branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
if EXPECTED_IDENTITY not in branch_audit:
    fail("branch_audit_identity")
if "2b77a60fc18e914e74ed4fe3e61f9eadfe5f4f84" not in branch_audit:
    fail("branch_audit_source_tip")

print(
    "FINAL_AUDIT=VERIFIED "
    "branches=1 "
    "commits=4 "
    "claims=C1:C2:C3:C5_classical_proxy,C4_non_strict,C6_radial_proxy_idft_untested "
    "evidence_points=12 "
    "paper_claims_verified=0 "
    "current_score_claim=false "
    "publication_allowed=false"
)
