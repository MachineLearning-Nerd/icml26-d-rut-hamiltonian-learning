# Source audit

## Paper record

- Title: Continuous Variable Hamiltonian Learning at Heisenberg Limit via Displacement-Random Unitary Transformation
- Authors: Xi Huang, Lixing Zhang, and Di Luo
- arXiv: 2510.08419v2
- OpenReview: tiF3tA5pau
- Paper URL: https://arxiv.org/abs/2510.08419v2
- Paper HTML: https://arxiv.org/html/2510.08419v2

The repository is a clean-room classical NumPy audit. It contains no official author implementation and no quantum simulator.

## Claim-to-source mapping

| Claim | Paper anchor | Local producer or record |
| --- | --- | --- |
| C1 | Heisenberg evolution-time scaling | repro/src/verify_drut.py::C1 and drut.py::estimate_coefficients |
| C2 | first-quantized coefficient scaling | repro/src/verify_drut.py::C2 |
| C3 | SPAM bound | repro/src/verify_drut.py::C3 and drut.py::sensing_matrix |
| C4 | hierarchical efficiency | repro/src/verify_drut.py::C4 and drut.py covariance helpers |
| C5 | RPE/bisection logarithmic dependence | repro/src/verify_drut.py::C5 and drut.py::bisection_search |
| C6 | Chebyshev plus IDFT recovery | repro/src/verify_drut.py::C6 and drut.py::chebyshev_nodes, idft_recover |

## Scope and divergence audit

- C1 and C2 use hand-injected noise laws rather than measurement outcomes.
- C3 uses a fixed linear fixture with L_C = 1.
- C4 observes equality rather than strict improvement.
- C5 is generic bisection, not RPE.
- C6 passes radial inversion but does not test IDFT end to end.
- No displacement, RUT, Fock-space, ancilla, quantum evolution, or Trotter implementation exists.
- No current live-judge score is available or claimed.

## Attribution audit

The paper authors remain the authors of the paper and its claims. MachineLearning-Nerd applies only to this independent audit repository, its documentation, its branch normalization, and its reachable commit history.
