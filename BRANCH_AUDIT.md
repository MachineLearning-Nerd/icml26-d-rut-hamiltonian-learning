# Branch and identity audit

Audit date: 2026-08-13

## Before cleanup

| Item | Observed value |
| --- | --- |
| Repository | `MachineLearning-Nerd/icml26-repro-tiF3tA5pau-d-rut-protocol` |
| Branch | `master` |
| Branch tip | `0794f6da2c2c80b70c5055c6862e0c4425365ec5` |
| Reachable commits | 1 |
| Commit identity | `DineshAI <dinesh.ai.bot@gmail.com>` |
| Commit message trailer | inherited `Co-Authored-By: Claude <noreply@anthropic.com>` |
| Remote | GitHub repository under `MachineLearning-Nerd` |

## Cleanup actions

1. Add the paper description, repository contents, branch inventory, claim/evidence ledger, citation, thank-you note, and explicit proxy boundary to `README.md`.
2. Make `outputs/verdict.json` identify finite proxy evidence, the equality result for C4, and the untested IDFT path.
3. Update the publication gate and add this branch audit.
4. Rename the GitHub repository to `icml26-d-rut-hamiltonian-learning`.
5. Rename the canonical branch from `master` to `main` and retire `master`.
6. Rewrite reachable author and committer metadata to `MachineLearning-Nerd` and remove the inherited co-author trailer.
7. Verify live repository metadata, branch count, branch tip, file set, stale links, whitespace, output JSON, and commit identities after publication.

## Final branch contract

The final repository should have exactly one published branch:

```text
main → canonical documentation and bounded classical D-RUT proxy audit
```

No branch is presented as an official quantum implementation or as an independent paper result. Migration is complete only when GitHub reports `main` as the default and `master` is absent.

## Live verification

The final remote audit confirmed repository name `icml26-d-rut-hamiltonian-learning`, default branch `main`, sole remote branch `main`, canonical paper homepage, README and gate publication, and MachineLearning-Nerd as both author and committer on all reachable commits.
