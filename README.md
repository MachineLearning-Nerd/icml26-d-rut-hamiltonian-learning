# ICML 2026 Reproduction Audit: D-RUT Hamiltonian Learning

Independent, claim-by-claim evidence audit of [Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation](https://arxiv.org/abs/2510.08419v2) by Xi Huang, Lixing Zhang, and Di Luo.

Repository: [MachineLearning-Nerd/icml26-d-rut-hamiltonian-learning](https://github.com/MachineLearning-Nerd/icml26-d-rut-hamiltonian-learning)

## Executive result

The clean-room audit passes six bounded classical NumPy proxy checks, but it does not reproduce the paper-level quantum claims:

- C1, C2, C3, C5, and the radial part of C6 pass their local proxy checks.
- C4 observes only non-strict covariance ordering; the hierarchical and simultaneous traces are equal, so strict improvement is not observed.
- C6 does not test end-to-end IDFT recovery; its IDFT probe error is 0.875 and is explicitly excluded from the pass criterion.
- The quantum D-RUT/RPE/Fock-space protocol is not implemented.
- The dossier therefore records 6/6 finite classical proxies, 0/6 paper claims independently verified, and no current competition score.

The full status is in [STATUS.md](STATUS.md), the claim-to-evidence production paths are in [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md), and the machine-readable boundary is in [claims.json](claims.json) and [reproduction_verdicts.json](reproduction_verdicts.json).

## Paper record

- Title: Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation
- Authors: Xi Huang, Lixing Zhang, and Di Luo
- Paper: [arXiv 2510.08419v2](https://arxiv.org/abs/2510.08419v2)
- Paper HTML: [arXiv HTML v2](https://arxiv.org/html/2510.08419v2)
- OpenReview: [tiF3tA5pau](https://openreview.net/forum?id=tiF3tA5pau)

## What the paper does

The paper considers finite-order bosonic Hamiltonians with unknown coefficients. Its protocol:

1. displaces the system by a tunable complex parameter;
2. averages over number-preserving random unitary transformations to isolate an effective Hamiltonian;
3. estimates the vacuum phase using ancilla measurements and Robust Phase Estimation;
4. recovers coefficients through radial Chebyshev interpolation and angular inverse discrete Fourier transforms.

For a single-mode term, the response has the schematic form

    C(beta) = sum over p,q of g_(p,q) times conjugate(beta) to the p times beta to the q.

The paper targets Heisenberg-limited evolution time, a first-quantized extension, robustness to bounded SPAM errors, and a hierarchical multi-mode recovery strategy. It also discusses multi-mode and physical Hamiltonian-learning settings. This repository models only selected classical linear-algebra consequences.

This repository is an independent audit, not an author-maintained implementation.

## Claim ledger

| Claim | Paper-level statement | Local evidence | Boundary |
| --- | --- | --- | --- |
| C1 | Heisenberg-limited evolution-time scaling | Hand-injected 1/T noise versus artificial 1/square-root-T SQL noise | VERIFIED_CLASSICAL_PROXY |
| C2 | First-quantized coefficient scaling | Single-mode hand-injected 1/T linear recovery | VERIFIED_CLASSICAL_PROXY |
| C3 | SPAM perturbation propagation bound | Fixed Chebyshev linear system with L_C = 1 and fifty perturbations | VERIFIED_LINEAR_PROXY |
| C4 | Strict hierarchical statistical efficiency | Hierarchical trace 0.0075 equals simultaneous trace 0.0075 | NON_STRICT_PROXY_ONLY |
| C5 | Logarithmic refinement dependence | Generic bisection iterations at five tolerances | VERIFIED_GENERIC_PROXY |
| C6 | Chebyshev radial sampling plus angular IDFT recovery | Radial matrix error 2.22e-16; IDFT path explicitly untested | VERIFIED_RADIAL_PROXY_IDFT_UNTESTED |

The local pass status is not a paper reproduction status. No quantum theorem or end-to-end protocol claim is counted as independently verified.

## How each claim is produced

The executable producer is [repro/src/verify_drut.py](repro/src/verify_drut.py), supported by [repro/src/drut.py](repro/src/drut.py). It uses deterministic NumPy seeds and writes [outputs/verdict.json](outputs/verdict.json).

1. C1 builds a Chebyshev sensing matrix, injects hand-designed 1/T and 1/square-root-T noise into a linear coefficient recovery, and compares log-log error slopes.
2. C2 runs the same noisy linear recovery for one synthetic mode and records the slope under hand-injected 1/T noise.
3. C3 perturbs a fixed sensing vector fifty times, solves the linearized inverse problem, and checks the local bound with a fixture L_C = 1.
4. C4 compares hierarchical and simultaneous covariance traces for a small block fixture. The non-strict comparison passes, but equality means strict improvement is not observed.
5. C5 runs a generic monotone bisection helper for tolerances from 10^-2 through 10^-10 and checks the logarithmic iteration pattern. It is not RPE.
6. C6 inverts a degree-15 Chebyshev sensing matrix exactly. The IDFT helper is probed separately but is marked idft_path_tested = false and is not part of the pass criterion.

The quantum path described by the paper is not in this flow: there is no displacement gate, RUT averaging, ancilla measurement, RPE, Fock-space evolution, or Trotter-error implementation.

## Reproduction boundary

The concrete limitations are:

1. The code is classical NumPy linear algebra; it does not simulate the D-RUT quantum protocol.
2. The 1/T and 1/square-root-T noise laws are injected by hand rather than estimated from RPE measurements.
3. The SPAM check uses L_C = 1 for a linear fixture rather than the paper's degree/radius/coefficient-dependent bound.
4. C4 produces equality and cannot support the paper's strict hierarchical-efficiency claim.
5. The C5 bisection helper is not the paper's RPE schedule or phase-unwrapping algorithm.
6. C6 verifies only radial Chebyshev matrix recovery; end-to-end angular IDFT recovery is not verified.
7. No paper-scale oscillator, multi-mode, first-quantized, SPAM, or quantum simulation sweep is reproduced.

The appropriate current label is bounded classical proxy evidence, not paper reproduced.

## Reproduce the local audit

From the repository root:

    python3 repro/src/verify_drut.py

The command is CPU-only and writes outputs/verdict.json. It requires Python 3 and NumPy.

## Repository contents

| Path | Purpose |
| --- | --- |
| [repro/src/drut.py](repro/src/drut.py) | Chebyshev sensing matrix, noisy recovery, covariance helpers, bisection, and IDFT helper |
| [repro/src/verify_drut.py](repro/src/verify_drut.py) | Six bounded classical proxy checks |
| [outputs/verdict.json](outputs/verdict.json) | Machine-readable metrics and explicit paper-level flags |
| [outputs/verify_run.log](outputs/verify_run.log) | Recorded verifier transcript |
| [publication_gate.json](publication_gate.json) | Conservative publication/documentation gate |
| [GATE_READY.md](GATE_READY.md) | Gate receipt and limitations |
| [STATUS.md](STATUS.md) | Current reproduction boundary |
| [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) | Claim-to-evidence production ledger |
| [SOURCE_AUDIT.md](SOURCE_AUDIT.md) | Paper/source/implementation mapping |
| [ENVIRONMENT.md](ENVIRONMENT.md) | Runtime and rerun contract |
| [REPORT.md](REPORT.md) | Interpretation and publication boundary |
| [BRANCH_AUDIT.md](BRANCH_AUDIT.md) | Legacy branch mapping and identity contract |
| [verify_final.py](verify_final.py) | Static final-state verifier |

## Branches

The source repository contained one legacy branch, master. It is normalized to main. There are no master or orx branches in the published repository.

| Clean branch | Former ref | Purpose |
| --- | --- | --- |
| [main](https://github.com/MachineLearning-Nerd/icml26-d-rut-hamiltonian-learning/tree/main) | master | Canonical documentation, classical proxies, outputs, and D-RUT audit boundary |

## Citation

If this audit is useful, please cite the paper:

    @article{huang2025continuous,
      title = {Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation},
      author = {Huang, Xi and Zhang, Lixing and Luo, Di},
      journal = {arXiv preprint arXiv:2510.08419},
      year = {2025},
      doi = {10.48550/arXiv.2510.08419}
    }

Repository citation metadata is also provided in [CITATION.cff](CITATION.cff).

## Thank you

Thank you to Xi Huang, Lixing Zhang, and Di Luo for developing D-RUT, connecting quantum measurement design with structured polynomial recovery, and making the protocol's Heisenberg-limit, SPAM, hierarchical-recovery, and first-quantized goals explicit enough to audit. This repository credits the original work while keeping classical proxy checks separate from the quantum claims they do not establish.
