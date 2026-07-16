# Round 1 operational results

**Date:** 2026-07-16  
**Scope:** controlled operational exercise of the trusted-finalizer reference
workflow. This is not an independent security assessment, a benchmark, or an
endorsement of the core project.

## Controls exercised

| Control | PR / run evidence | Observed result |
| --- | --- | --- |
| Clean source repair, then approval | [PR #1](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/1), [reverify](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29515568870), [seal](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29515607522) | The attempt-bound check completed `ALLOW`; the signed bundle verified externally against the API-derived PR/revision/tree context. |
| Cancellation after metadata | [fixture PR #3](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/3), [cancelled reverify](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29515358484), [reconcile](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29515381964) | Metadata created the attempt-bound check, the run was cancelled before the judge began, and the exact check completed `DENY`; no seal key was used. |
| Judge-owned pack modification | [fixture PR #4](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/4), [reverify](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29515899685), [seal](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29515940764) | Guard produced `REJECTED` for a protected judge file. The seal retained signed `DENY` evidence, and the bundle verified externally. |
| Source-only change that leaves the defect unfixed | [fixture PR #5](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/5), [reverify](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29516136994), [seal](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29516182771) | The external pack ran 2 tests, reported `FAIL` / `tests_failed`, and the finalizer completed the attempt-bound check `DENY`. The signed bundle verified externally. |

The adversarial fixture PRs are closed and were never merged. Their signed
evidence remains subject to the repository's Actions retention policy.

## What was independently recomputed in this exercise

For the positive result and both signed denials, a consumer command verified
the Ed25519 bundle signature using `security/finalizer-public.pem` and
external expected source/context derived from the GitHub API. That validates
the bundle's signature and exact binding to the named repository, workflow
attempt, PR revisions, and Git trees. It does **not** make the reviewer or the
evaluation independent.

## Limits and follow-up

- `MANA-awam` supplied the required environment approval, but it is controlled
  by the same project owner. It is a technical separation-of-roles exercise,
  not an independent review.
- The sealed Guard executable was the immutable `v3.6.0` release asset pinned
  by `EVOGUARD_GUARD_ARTIFACT_SHA256`. The reverify workflow includes a
  hash-locked Python/pytest bootstrap correction that is pending the core
  `v3.6.1` release; this pilot must update its pin and repeat a clean positive
  run after that release.
- These few fixtures do not measure false positives, coverage, resistance to
  every hostile runner escape, or effectiveness on external repositories.
- The next credible evidence step is a pre-registered evaluation by a
  genuinely independent maintainer or organization, followed by
  artifact-bound verification work. Do not treat Round 1 as a release claim.
