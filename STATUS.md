# Status — icml26-d-rut-hamiltonian-learning

- **Paper:** [Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation](https://arxiv.org/abs/2510.08419)
- **Short name:** D-RUT
- **OpenReview:** `tiF3tA5pau`
- **Paper-level reproduction:** **inconclusive / partial**
- **Local evidence:** **6/6 bounded classical proxy checks pass**
- **Compute:** deterministic NumPy, CPU-only
- **Canonical branch:** `main`

## Evidence summary

- C1: hand-injected `1/T` noise gives slope `-0.970`; the SQL surrogate gives `-0.462`.
- C2: single-mode hand-injected `1/T` noise gives slope `-1.182`.
- C3: the fixed linear fixture gives `σ_min(K)=2.4495`, max perturbation norm `0.1366`, and max local bound `0.2129`.
- C4: hierarchical and simultaneous covariance traces are both `0.0075`; strict improvement is not observed.
- C5: generic bisection uses `[8,15,21,28,35]` iterations for the tested tolerances, with iterations/log(1/tol) in `1.52–1.74`.
- C6: radial Chebyshev matrix recovery error is `2.22e-16`; the IDFT helper is not an accepted end-to-end test (`idft_path_tested=false`).

These results are classical proxies. The repository does not implement D-RUT, RPE, quantum states, controlled unitaries, or paper-scale experiments. The next substantive step would be an assumption-matched quantum or simulator implementation with direct tests of radial and angular recovery, SPAM propagation, and the strict hierarchical comparison.

See [`README.md`](README.md), [`GATE_READY.md`](GATE_READY.md), and [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md) for the full evidence boundary.
