# Environment and rerun contract

## Runtime

- Intended runtime: CPU
- Python: standard virtual environment
- Numerical dependency: NumPy
- Main random generator seed: 42
- Mode fixture: five modes and twelve sensing nodes

## Protocol

- C1 uses evolution times {10, 50, 100, 500, 2000} with hand-injected 1/T and 1/square-root-T noise.
- C2 uses one synthetic mode and the same evolution-time grid.
- C3 uses fifty Gaussian perturbations and a fixed Chebyshev sensing matrix.
- C4 uses a small hierarchical/simultaneous covariance block fixture.
- C5 uses tolerances {10^-2, 10^-4, 10^-6, 10^-8, 10^-10}.
- C6 uses a degree-15 Chebyshev fixture and an explicit non-gating IDFT probe.

## Local rerun

Run:

    python3 repro/src/verify_drut.py

The producer writes outputs/verdict.json. The committed output and run log are the evidence snapshot checked by verify_final.py.

## Missing inputs

The D-RUT quantum protocol, Fock-space states, controlled random unitaries, ancilla measurement model, RPE schedule, phase unwrapping, Trotterization, physical Hamiltonian fixtures, and paper-scale experiments are not present.
