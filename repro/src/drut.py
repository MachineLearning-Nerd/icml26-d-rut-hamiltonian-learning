"""Clean-room numerical proxies for D-RUT (arXiv 2510.08419). numpy, CPU.

The paper's D-RUT protocol estimates Hamiltonian coefficients g from quantum
phase measurements.  This module models the classical coefficient-recovery
pieces only; it does not simulate quantum states, RPE, D-RUT circuits, or
Trotterization.
Math: sensing matrix K (Chebyshev-node design), estimated coefficients ĝ = K⁻¹·β,
where β are measured phases with noise ~ 1/T (Heisenberg) or 1/√T (SQL).

The verifier checks bounded proxies for:
  c1: O(1/ε) evolution-time scaling (Heisenberg limit)
  c2: single-mode RMSE ε_G with O~(1/ε_G) evolution
  c3: SPAM error bound ||δg|| <= (L_C/σ_min(K)) ||δβ||
  c4: hierarchical Cov <= simultaneous Cov
  c5: bisection convergence O(log(1/ε_R))
  c6: Chebyshev-node sampling + IDFT reconstruction
"""
from __future__ import annotations
import numpy as np


def chebyshev_nodes(n, a=-1, b=1):
    """Chebyshev nodes of the first kind on [a,b]."""
    k = np.arange(1, n + 1)
    nodes = 0.5 * (a + b) + 0.5 * (b - a) * np.cos((2 * k - 1) * np.pi / (2 * n))
    return nodes


def sensing_matrix(n_modes, n_nodes, start_mode=0):
    """Build sensing matrix K from Chebyshev-node displacements.
    K[i,j] = Chebyshev basis T_{start_mode+i} evaluated at node j."""
    nodes = chebyshev_nodes(n_nodes)
    K = np.zeros((n_modes, n_nodes))
    for i in range(n_modes):
        mode = start_mode + i
        for j in range(n_nodes):
            K[i, j] = np.cos(mode * np.arccos(nodes[j]))
    return K, nodes


def estimate_coefficients(g_true, K, noise_std, rng):
    """Simulate phase measurement with noise, recover coefficients via K⁻¹.
    g_true: true coefficients (n_modes,), K: sensing matrix (n_modes, n_nodes).
    noise_std ~ 1/T (Heisenberg) or 1/sqrt(T) (SQL)."""
    n_modes, n_nodes = K.shape
    # true phases: β = K^T @ g_true
    beta_true = K.T @ g_true
    # noisy measurement
    beta_noisy = beta_true + rng.normal(0, noise_std, n_nodes)
    # recover via least squares: ĝ = (K K^T)^{-1} K @ beta_noisy
    g_hat = np.linalg.lstsq(K.T, beta_noisy, rcond=None)[0]
    return g_hat


def idft_recover(beta, n_modes):
    """Inverse DFT helper; the verifier does not claim an end-to-end IDFT test."""
    return np.fft.ifft(beta).real[:n_modes]


def hierarchical_covariance(K_single, K_coupling, noise_var):
    """Hierarchical: estimate single-mode coeffs first, then coupling.
    Cov_hier = block_diag(Cov_single, Cov_coupling)."""
    Cov_s = noise_var * np.linalg.inv(K_single @ K_single.T)
    Cov_c = noise_var * np.linalg.inv(K_coupling @ K_coupling.T)
    n_s = Cov_s.shape[0]; n_c = Cov_c.shape[0]
    Cov_hier = np.zeros((n_s + n_c, n_s + n_c))
    Cov_hier[:n_s, :n_s] = Cov_s
    Cov_hier[n_s:, n_s:] = Cov_c
    return Cov_hier


def simultaneous_covariance(K_full, noise_var):
    """Simultaneous: estimate all coefficients at once."""
    return noise_var * np.linalg.inv(K_full @ K_full.T)


def bisection_search(f, target, lo, hi, tol=1e-10):
    """Bisection search (c5): converges in O(log(1/tol)) iterations."""
    iters = 0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if f(mid) < target:
            hi = mid
        else:
            lo = mid
        iters += 1
    return 0.5 * (lo + hi), iters
