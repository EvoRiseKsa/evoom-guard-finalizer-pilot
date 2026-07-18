# GitHub Artifact Attestation provider probe: first result

## Scope and status

This is a durable observation record for one bounded provider experiment. It
is not an EvoOM Guard product release, a Trusted Finalizer result, an artifact
admission record, or a deployment/release claim.

The experiment was introduced in PR [#18][pr-18] under the documented
trust-root maintenance procedure. It was merged at
`d284f296100c473a94094e5501b0b6b1dca5ba7e`; the exact required
`EvoGuard Trusted Finalizer` branch-protection binding was restored immediately
after that maintenance merge.

## Observed provider result

| Field | Value |
| --- | --- |
| Workflow run | [29622843800][run] |
| Event / source ref | `workflow_dispatch` / `refs/heads/main` |
| Source digest | `d284f296100c473a94094e5501b0b6b1dca5ba7e` |
| Subject | non-executable regular text file, 255 bytes |
| Subject SHA-256 | `59534a4ba0ce06259c240998014349438b760fa78ea30fb2d44f8c31ce28c66e` |
| GitHub attestation | [35922858][attestation] |
| Signed bundle SHA-256 / size | `185c35103bed79b28b02445c3b23b612db3ef86b5164aca31a7e87bf0502637e` / 12300 bytes |
| Runner GitHub CLI | `2.96.0` |
| Retained Actions artifact | `evoguard-github-attestation-provider-probe-29622843800-1` (ID `8422779253`, expires 2026-07-25T00:20:04Z) |
| Retained verifier-output SHA-256 | `215150d1e8071648e9887374caa3dbc478b9303f5c8381539e778f940747b7bd` |

The workflow used pinned `actions/attest`, then ran `gh attestation verify`
with exact repository, signer workflow, source ref/digest, SLSA v1 predicate,
GitHub Actions OIDC issuer, GitHub-hosted-runner, and one-selected-result
constraints. The `probe` workflow job also created an ordinary GitHub Actions
check run. It was not, and cannot satisfy, the separately required `EvoGuard
Trusted Finalizer` check.

## Independent re-verification and negative tests

A separate local verification using GitHub CLI `2.90.0` downloaded the
retained subject, rechecked its SHA-256, and selected one verified result under
the same constraints. The certificate reported the direct signer workflow and
reported both `buildSignerDigest` and `sourceRepositoryDigest` as
`d284f296100c473a94094e5501b0b6b1dca5ba7e`.

That signer digest is an observed provider value, not an admission-policy pin.
A deliberately zeroed source digest was rejected with exit code 1 and an
explicit `SourceRepositoryDigest` mismatch. A deliberately wrong signer
workflow path was also rejected with exit code 1.

## Explicit non-claims and next boundary

This result does not bind a PR head to a separately verified finalizer `ALLOW`,
does not create a V2 `.eab` admission record, use an admission key or protected
admission Environment, validate OCI, or bind a release/deployment artifact.
It does not establish reproducibility, a SLSA level, independent review, or
production merge enforcement.

The next valid technical question is whether a controlled PR-head or
merge-candidate builder can produce an attestation whose provider source digest
equals a separately verified finalizer context. That question requires a
separate threat-modelled pilot; this result does not answer it.

[attestation]: https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/attestations/35922858
[pr-18]: https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/18
[run]: https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29622843800
