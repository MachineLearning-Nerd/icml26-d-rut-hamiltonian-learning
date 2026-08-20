# Branch and identity audit

Repository: MachineLearning-Nerd/icml26-d-rut-hamiltonian-learning
Audit date: 2026-08-20

The legacy repository contained one branch. Its history was normalized before the dossier commit, and the public repository now exposes one clean branch.

| Legacy ref | Source tip before normalization | Clean ref | Role |
| --- | --- | --- | --- |
| master | 2b77a60fc18e914e74ed4fe3e61f9eadfe5f4f84 | main | Canonical documentation, classical proxies, outputs, and D-RUT audit boundary |

## Final verification contract

- main is the default branch.
- No master or orx branch remains.
- README.md, STATUS.md, CLAIM_EVIDENCE.md, and this branch audit are present on main.
- Every reachable commit has author and committer identity MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>.
- The repository name is icml26-d-rut-hamiltonian-learning.
- No branch is presented as an official quantum implementation or as an independent paper result.

## Recovery

A recovery bundle was created before history normalization. Its SHA-256 is 24822b201ed725b770d06b7fbbc141d1d62209237a590cacde571f9645a0b29f. The pre-normalization head is 2b77a60fc18e914e74ed4fe3e61f9eadfe5f4f84.

## Live verification

The final remote audit must confirm repository name icml26-d-rut-hamiltonian-learning, default branch main, sole remote branch main, published README and gate, and MachineLearning-Nerd as both author and committer on all reachable commits. The local contract is enforced by verify_final.py.
