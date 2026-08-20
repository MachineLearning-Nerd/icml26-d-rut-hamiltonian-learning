# Claim evidence — D-RUT Hamiltonian Learning

Paper: Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation
Paper record: arXiv 2510.08419v2, OpenReview tiF3tA5pau
Repository scope: clean-room classical NumPy proxy audit

## C1 — Heisenberg scaling proxy

Paper anchor: Heisenberg-limited total evolution time.

Production path: repro/src/verify_drut.py::C1 builds a Chebyshev sensing matrix, injects 1/T noise and an artificial 1/square-root-T SQL noise law, solves the linear system, and compares log-log error slopes.

Observed result: Heisenberg surrogate slope is -0.970 and SQL surrogate slope is -0.462.

Verdict: VERIFIED_CLASSICAL_PROXY. No D-RUT circuit, RPE measurement, or quantum evolution was run.

## C2 — first-quantized scaling proxy

Paper anchor: first-quantized coefficient RMSE scaling.

Production path: repro/src/verify_drut.py::C2 repeats the noisy linear recovery for one synthetic mode with hand-injected 1/T noise.

Observed result: slope is -1.182.

Verdict: VERIFIED_CLASSICAL_PROXY. No position/momentum Hamiltonian or bounded reference-frame map was simulated.

## C3 — SPAM propagation proxy

Paper anchor: bounded SPAM perturbations propagate through coefficient recovery under a condition/Lipschitz bound.

Production path: repro/src/verify_drut.py::C3 sends fifty Gaussian perturbations through a fixed Chebyshev sensing matrix K, sets L_C = 1, and checks the local inverse bound.

Observed result: sigma-min(K) is 2.4495, maximum coefficient perturbation norm is 0.1366, and maximum local bound is 0.2129.

Verdict: VERIFIED_LINEAR_PROXY. The physical SPAM model and paper-specific L_C derivation are not tested.

## C4 — hierarchical covariance comparison

Paper anchor: hierarchical multi-mode recovery is strictly more statistically efficient than simultaneous recovery.

Production path: repro/src/verify_drut.py::C4 compares hierarchical_covariance with simultaneous_covariance on a five-row Chebyshev block fixture.

Observed result: both traces are 0.0075. Non-strict ordering passes, but strict improvement is false.

Verdict: NON_STRICT_PROXY_ONLY. This finite fixture does not support the paper's strict efficiency claim.

## C5 — logarithmic refinement proxy

Paper anchor: bisection/RPE-style refinement has logarithmic iteration dependence on precision.

Production path: repro/src/verify_drut.py::C5 calls a generic monotone bisection helper at tolerances 10^-2 through 10^-10 and checks iterations divided by log(1/tolerance).

Observed result: iteration counts are 8, 15, 21, 28, and 35, with a log-log slope of 0.078.

Verdict: VERIFIED_GENERIC_PROXY. This is not Robust Phase Estimation and does not implement its confidence or phase-unwrapping protocol.

## C6 — radial Chebyshev and angular IDFT recovery

Paper anchor: Chebyshev radial sampling plus angular IDFT recovers Hamiltonian coefficients.

Production path: repro/src/verify_drut.py::C6 inverts a degree-15 Chebyshev sensing matrix exactly and separately probes the IDFT helper.

Observed result: radial matrix recovery error is 2.22e-16. The IDFT probe error is 0.875 and idft_path_tested is false.

Verdict: VERIFIED_RADIAL_PROXY_IDFT_UNTESTED. End-to-end radial-plus-angular recovery is not verified.
