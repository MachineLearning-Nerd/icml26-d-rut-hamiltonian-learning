# Status — D-RUT Hamiltonian Learning

Paper: Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation
Paper record: arXiv 2510.08419v2, OpenReview tiF3tA5pau
Authors: Xi Huang, Lixing Zhang, and Di Luo
Repository: MachineLearning-Nerd/icml26-d-rut-hamiltonian-learning
Audit date: 2026-08-20
Audit state: INCONCLUSIVE_SIX_FINITE_CLASSICAL_PROXIES_C4_NON_STRICT_C6_IDFT_UNTESTED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE

## Outcome

Six finite classical proxy checks pass, but zero of six paper claims are independently verified. C4 observes equality rather than strict hierarchical improvement. C6 verifies radial Chebyshev matrix recovery but leaves the IDFT path untested. The quantum D-RUT/RPE protocol is not implemented.

| Claim | Local result | Evidence boundary |
| --- | --- | --- |
| C1 | VERIFIED_CLASSICAL_PROXY | Hand-injected noise scaling |
| C2 | VERIFIED_CLASSICAL_PROXY | Single-mode hand-injected noise |
| C3 | VERIFIED_LINEAR_PROXY | Fixed sensing matrix and L_C = 1 |
| C4 | NON_STRICT_PROXY_ONLY | Hierarchical and simultaneous traces equal |
| C5 | VERIFIED_GENERIC_PROXY | Generic bisection, not RPE |
| C6 | VERIFIED_RADIAL_PROXY_IDFT_UNTESTED | Radial inversion only |

The evidence package contains twelve scoped proxy points out of a twelve-point six-claim ledger. This is an evidence-package count, not a live judge score. No current score is claimed.

## Main blockers

- No D-RUT, RUT averaging, Fock-space, ancilla-measurement, RPE, or Trotter simulation exists.
- The strict C4 efficiency improvement is not observed.
- C6 does not verify end-to-end angular IDFT recovery.

## Files

- repro/src/drut.py — classical sensing and recovery helpers
- repro/src/verify_drut.py — six proxy diagnostic producer
- outputs/verdict.json — raw metrics and explicit paper-level flags
- CLAIM_EVIDENCE.md — claim production paths and boundaries
- REPORT.md — interpretation and publication boundary
