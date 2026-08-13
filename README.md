# D-RUT Hamiltonian Learning — Reproduction Audit

This repository is an independent, clean-room audit of **Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation**. The paper proposes **D-RUT**, a quantum data-acquisition and classical coefficient-recovery protocol for finite-order continuous-variable Hamiltonians.

The repository contains small NumPy surrogates for the classical recovery geometry and six bounded checks. They are useful sanity checks, but they are not a quantum simulation, an implementation of D-RUT/RPE, or a full reproduction of the paper's theorems and experiments.

| Resource | Link |
| --- | --- |
| Audit source | [arXiv:2510.08419v2](https://arxiv.org/abs/2510.08419v2), revised 2026-05-29 |
| Paper HTML | [arXiv HTML v2](https://arxiv.org/html/2510.08419v2) |
| OpenReview record | [tiF3tA5pau](https://openreview.net/forum?id=tiF3tA5pau) |
| Repository target name | `MachineLearning-Nerd/icml26-d-rut-hamiltonian-learning` |

## Current status

**Overall result: partial / inconclusive.** The six finite local checks pass, but the paper-level reproduction is not established.

The distinction is important:

- **Local proxy check:** a small classical calculation produced the recorded value or trend.
- **Paper claim reproduced:** the quantum protocol, assumptions, estimator, metric, and evidence path were independently reproduced.

This repository currently supports only the first category. It does not simulate Fock-space states, controlled D-RUT circuits, random unitary transformations, Robust Phase Estimation (RPE), Trotterization, or the paper's full numerical systems.

## What the paper does

The paper considers finite-order bosonic Hamiltonians with unknown coefficients. Its core data-acquisition map is:

1. displace the system by a tunable complex parameter `β`;
2. average over number-preserving random unitary transformations to isolate a number-conserving effective Hamiltonian;
3. estimate its vacuum phase `C(β)` using ancilla measurements and Robust Phase Estimation;
4. recover coefficients from polynomial responses using radial Chebyshev interpolation and angular inverse discrete Fourier transforms.

For a single-mode term, the response has the schematic form

```text
C(β) = Σ g_(p,q) (β*)^p β^q
```

For multi-mode Hamiltonians, the paper first isolates single-mode terms and then learns interaction clusters by setting bystander displacements to zero. It also gives a first-quantized extension for position/momentum coefficients.

The paper's main theoretical targets include:

- Heisenberg-limited total evolution time `T ~ O(1/ε)` for bosonic coefficient RMSE;
- first-quantized scaling `T ~ O(1/ε_G)` under a bounded reference-frame mismatch;
- robustness to bounded state-preparation-and-measurement (SPAM) errors;
- a hierarchical multi-mode recovery strategy with a strictly better worst-case error bound than the compared simultaneous strategy.

The paper's v2 abstract and theorem statements describe these as quantum Hamiltonian-learning results; the NumPy code here only models selected linear-algebra consequences.

## What this repository contains

| Path | Purpose |
| --- | --- |
| `repro/src/drut.py` | Chebyshev sensing matrix, noisy linear coefficient recovery, covariance helpers, bisection helper, and an IDFT helper |
| `repro/src/verify_drut.py` | Runs six bounded classical proxy checks and writes `outputs/verdict.json` |
| `outputs/verdict.json` | Machine-readable proxy measurements and explicit paper-level boundary |
| `outputs/verify_run.log` | Human-readable local verifier transcript and proxy summary |
| `publication_gate.json` | Publication/documentation gate and limitations |
| `.trackio/logbook/` | Existing local experiment logbook artifact |
| `GATE_READY.md` | Human-readable documentation gate |
| `BRANCH_AUDIT.md` | Branch and commit-identity migration record |

There is no pinned paper PDF in this repository and no official author implementation. The arXiv links above are the paper source of record.

## Branch inventory

The published repository has one intentional branch:

| Branch | Purpose | State |
| --- | --- | --- |
| `main` | Documentation, classical proxies, outputs, and the D-RUT audit boundary | Canonical branch; no feature or experiment branches are retained |

The original `master` branch was a one-commit initialization branch. It is retired during this cleanup. The migration and identity normalization are recorded in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md).

## Claim-to-evidence ledger

The table separates the paper's claims from the evidence actually produced here. The `passed` values in `outputs/verdict.json` mean that the stated finite proxy check passed; they do not mean that the corresponding quantum theorem was reproduced.

| ID | Paper claim | How the paper produces the claim | Local evidence path | Local result and boundary |
| --- | --- | --- | --- | --- |
| C1 | Heisenberg-limited evolution-time scaling `T ~ O(1/ε)`. | D-RUT exposes a phase response, RPE estimates it, and the total evolution time is analyzed against target precision. | `estimate_coefficients()` adds noise `1/T` to a Chebyshev linear system and compares its finite slope with an artificial SQL `1/√T` path over `T={10,50,100,500,2000}`. | **Classical proxy passed:** slopes `-0.970` (Heisenberg surrogate) and `-0.462` (SQL surrogate). No D-RUT circuit or RPE was run. |
| C2 | First-quantized coefficient RMSE scales with `T ~ O(1/ε_G)`. | Apply the first-quantized extension under its bounded reference-frame mismatch assumption and measure physical-coefficient RMSE. | The same noisy linear recovery is run for one synthetic mode with noise `1/T`. | **Classical proxy passed:** slope `-1.182`. No position/momentum Hamiltonian or reference-frame map was simulated. |
| C3 | Bounded SPAM error propagates through coefficient recovery with a condition/Lipschitz bound. | Bound the response perturbation, propagate it through Chebyshev/Fourier inversion, and use the paper's `L_C` bound, which depends on degree, displacement radius, and coefficient magnitudes. | Fifty Gaussian perturbations are sent through a fixed `K`; the local fixture sets `L_C=1` and checks `||δg|| ≤ ||δβ||/σ_min(K)` with 1% tolerance. | **Finite linear proxy passed:** `σ_min(K)=2.4495`, max `||δg||=0.1366`, max bound `0.2129`. The paper's physical SPAM model and actual `L_C` derivation are not tested. |
| C4 | Hierarchical multi-mode recovery is strictly more statistically efficient than simultaneous recovery in the paper's comparison. | Zero non-participating displacements, recover single-mode coefficients first, then interaction clusters, and compare the resulting worst-case covariance/error bounds. | `hierarchical_covariance()` is compared with a block simultaneous covariance using a five-row Chebyshev fixture. | **Non-strict proxy only:** traces are exactly equal (`0.0075` vs `0.0075`); non-strict order passes, but strict improvement is **not observed**. This is not evidence for the paper's strict claim. |
| C5 | Bisection/RPE-style refinement has logarithmic iteration dependence on precision. | RPE uses a geometric evolution schedule and confidence-interval refinement; the paper's protocol includes measurement and phase-unwrapping details. | `bisection_search(x², 0.5, 0, 2)` is run at tolerances `10^-2` through `10^-10`; iterations are `[8,15,21,28,35]`, with iterations/log(1/tol) in `1.52–1.74`. | **Generic algorithm proxy passed:** log-log slope is `0.078` (near 0 is expected when iterations grow logarithmically). This is not an RPE implementation. |
| C6 | Chebyshev radial sampling plus angular IDFT recovers Hamiltonian coefficients. | Query `C(r,θ)` at Chebyshev radial nodes, solve the radial polynomial system, then use angular samples and inverse DFT to recover `g_(p,q)`. | A degree-15 Chebyshev sensing matrix is inverted exactly for a synthetic cosine polynomial. The `idft_recover()` helper is probed but is not part of the pass criterion. | **Radial Chebyshev proxy passed:** matrix recovery error `2.22e-16`; the IDFT probe error is `0.875` and `idft_path_tested=false`. End-to-end Chebyshev-plus-IDFT recovery is not verified. |

### Evidence production flow

```text
synthetic coefficients + Chebyshev design
                 │
                 ├── noisy linear recovery → C1, C2, C3
                 ├── block covariance comparison → C4
                 ├── generic monotone bisection → C5
                 └── Chebyshev matrix inversion → C6 radial proxy

all finite checks → outputs/verdict.json
```

The quantum path described by the paper is not present in this flow. There is no implementation of displacement gates, RUT averaging, ancilla X/Y measurement, RPE, Fock-space evolution, or Trotter error control.

## Reproduction boundary

The current limitations are explicit:

1. The code is classical NumPy linear algebra; it does not implement or simulate the D-RUT quantum protocol.
2. Noise laws `1/T` and `1/√T` are injected by hand. They are not estimated from RPE measurement outcomes.
3. The SPAM check uses `L_C=1` for a linear fixture rather than evaluating the paper's degree/radius/coefficient-dependent Lipschitz bound.
4. The covariance fixture produces equality, so it does not reproduce the paper's strict hierarchical-efficiency advantage.
5. The bisection helper is not the paper's RPE schedule or phase-unwrapping algorithm.
6. C6 verifies only radial Chebyshev matrix recovery; the IDFT helper is explicitly not tested end to end.
7. No paper-scale harmonic oscillator, Kerr oscillator, Bose–Hubbard dimer, multi-mode, first-quantized, or SPAM sweep is reproduced.

The appropriate current label is **bounded classical proxy evidence**, not **paper reproduced**.

## Run the local audit

From the repository root:

```bash
python3 repro/src/verify_drut.py
```

The command is CPU-only and writes `outputs/verdict.json`. It requires Python 3 and NumPy.

## Citation

If you use the paper or this audit, please cite the original work:

```bibtex
@article{huang2025continuous,
  title={Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation},
  author={Huang, Xi and Zhang, Lixing and Luo, Di},
  journal={arXiv preprint arXiv:2510.08419},
  year={2025},
  doi={10.48550/arXiv.2510.08419},
  url={https://arxiv.org/abs/2510.08419}
}
```

This repository is an independent audit and is not an author-maintained implementation.

## Thank you

Thank you to **Xi Huang, Lixing Zhang, and Di Luo** for developing D-RUT, connecting quantum measurement design with structured polynomial recovery, and making the protocol's Heisenberg-limit, SPAM, hierarchical-recovery, and first-quantized goals explicit enough to audit. This repository is intended to credit the original work while keeping classical proxy checks separate from the quantum claims they do not establish.
