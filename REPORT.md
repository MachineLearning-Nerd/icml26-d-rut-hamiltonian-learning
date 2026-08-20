# Reproduction report

## Executive result

This repository provides six bounded classical proxy checks related to D-RUT Hamiltonian learning. All six local checks pass, but zero of six paper claims are independently verified because the quantum protocol and complete recovery pipeline are absent.

## Results

| Claim | Result | Boundary |
| --- | --- | --- |
| C1 | Heisenberg surrogate slope -0.970 versus SQL -0.462 | hand-injected linear noise |
| C2 | single-mode slope -1.182 | hand-injected classical recovery |
| C3 | max perturbation 0.1366 below max bound 0.2129 | fixed linear fixture, L_C = 1 |
| C4 | traces equal at 0.0075 | non-strict ordering only |
| C5 | bisection slope 0.078 | generic bisection, not RPE |
| C6 | radial error 2.22e-16 | IDFT probe untested, error 0.875 |

## Interpretation

The outputs support the recorded classical linear-algebra behavior in the selected fixtures. They do not reproduce the quantum D-RUT/RPE protocol, Heisenberg or SPAM proofs, strict hierarchical comparison, end-to-end IDFT, or paper-scale experiments.

## Publication boundary

The repository is suitable as an explicitly partial classical audit when its quantum and IDFT gaps remain visible. It is not suitable for a claim of complete paper reproduction, quantum-protocol validation, or a current competition score.
