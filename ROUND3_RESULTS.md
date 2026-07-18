# PR-head provenance pilot — Round 1 result

**Exercise completed:** 2026-07-18 UTC
**Scope:** one controlled same-repository source-only PR-head provenance observation plus an independently re-verified Trusted Finalizer result. This is not artifact admission, a release claim, deployment authorization, independent review, or production merge enforcement.

## What was tested

The unresolved identity question is whether a GitHub attestation can bind the **open PR head H**, rather than a later merge revision, to a reviewed reusable builder.

- Builder trust-root maintenance [PR #20](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/20) merged at `cd6175d7dadb968339090545060d441d181363d5`.
- Pinned no-secret caller maintenance [PR #21](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/21) merged at `8fafe54d673c096c8c7ee552293bdeef516325cb`.
- Controlled candidate [PR #22](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/22) remains **open and unmerged**. It changed only the `calc/ops.py` function docstring.
- Immutable base B: `8fafe54d673c096c8c7ee552293bdeef516325cb`
- Immutable candidate head H: `1b6087051e97785ddf39291d147d0fe4649ef74b`
- Base tree: `2a33f1bf547157bd24a331f00b96b0ec55e9c3a9`
- Head tree: `fdd26cff0f320a275c7fc93d82bab12c231c6dbd`

The initial branch push had no open PR and [failed closed](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29625531076) at the exact association check. It produced no attestation and is not evidence.

## PR-head attestation observation

The second push occurred only after PR #22 was open.

| Property | Verified fact |
| --- | --- |
| Caller/builder run | [29625589844](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29625589844), attempt 1 |
| Attestation | [ID 35927772](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/attestations/35927772) |
| Attested binding SHA-256 | `2fb06b577609f43bcf287b7b834a6c4b3de018a0774430d63ebabc141997fa19` |
| Attestation bundle SHA-256 | `57857436324991d249d185238488b5f8257418f9f115d2377218911fac4f17f5` |
| Source ref | `refs/heads/evoguard/pr-head-attestation-pilot/round1` |
| Certificate source digest | `1b6087051e97785ddf39291d147d0fe4649ef74b` |
| Observed builder signer digest | `cd6175d7dadb968339090545060d441d181363d5` |
| In-run receipt verifier | `gh version 2.96.0`, captured by the builder-run receipt |
| Separate external repeat | `gh version 2.90.0`, exact repository/ref/H, builder path, GitHub OIDC issuer, SLSA v1, hosted-runner denial, and limit 1 |

A separate local `gh attestation verify` selected exactly one result and separately confirmed:

- `sourceRepositoryDigest == H == 1b6087051e97785ddf39291d147d0fe4649ef74b`
- `buildSignerDigest == cd6175d7dadb968339090545060d441d181363d5 == PR-A merge cd6175d7dadb968339090545060d441d181363d5`

`evidence/round3/pr-head-attestation-binding.json` is the exact regular-file subject. The receipt is retained with its SHA-256 in the manifest so this GitHub attestation can be queried again after the short-lived Actions artifact expires.

## Same-H Trusted Finalizer result

A manual [EvoGuard Reverify run 29625694041](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29625694041), attempt 1, independently derived raw-Git bindings for the same B/H pair. Its no-secret reverify completed successfully. The separate [seal run 29625712528](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29625712528) was approved through the protected `evoguard-finalizer` Environment by MANA-awam and completed successfully.

That approval and all PR reviews are same-owner technical separation of roles, **not independent review**.

| Property | Verified fact |
| --- | --- |
| Required check | `EvoGuard Trusted Finalizer` completed PASS on PR #22 |
| Final decision | `ALLOW` |
| Finalized evidence artifact | GitHub artifact ID 8423782917; original expiry 2026-08-17 |
| Decoded `finalized.evb` SHA-256 | `fccdd094b54a6f6db3cc9c587596f9074e31df45100a9c00138ae4488083e35c` |
| Guard release | published `v3.7.0` `evo-guard.pyz`; SHA-256 `1d36f7ec45f47f9f6c3178a25a58accf8f8beb0ffd9d29e7bf93b7fe17ad3ec9` |
| Candidate snapshot SHA-256 | `025ce76cc75f539d3597a2c9245b2cabadd96467489c492e0b7cde685e6fa405` |
| Effective policy SHA-256 | `a709c33bfe317ecac4e4fdc822a158ccb56c18f3d9564425638a5882d6cf4174` |
| Verifier-pack SHA-256 | `e864e79a2e3ac35fc83a8170b7da2608c5831c282cce01a6583df84400271e7e` |

The release asset was downloaded from the immutable `v3.7.0` release and its SHA-256 matched the protected repository variable. An external recomputation derived the bindings from raw Git objects using GitHub API commit/tree identifiers, then `verify-finalized --require-pass` returned `verified: true` and `decision: ALLOW`.

## Reproduce

The evidence tree is pinned to LF bytes in `.gitattributes`. `MANIFEST.sha256` records SHA-256 digests and detects accidental change once that manifest is trusted; it is not an independent trust root. `finalized.evb.b64` and `verdict.json.b64` are Base64 transports so their decoded bytes exactly match the binary signed envelope and its no-terminal-LF verdict material.

```text
python -c "import base64, hashlib, pathlib; data=base64.b64decode(b''.join(pathlib.Path('evidence/round3/finalized.evb.b64').read_bytes().split()), validate=True); assert hashlib.sha256(data).hexdigest() == 'fccdd094b54a6f6db3cc9c587596f9074e31df45100a9c00138ae4488083e35c', 'digest mismatch'; pathlib.Path('round3-finalized.evb').write_bytes(data)"
python -c "import base64, hashlib, pathlib; data=base64.b64decode(b''.join(pathlib.Path('evidence/round3/verdict.json.b64').read_bytes().split()), validate=True); assert hashlib.sha256(data).hexdigest() == 'ad112cdd49bfeb7dbc3a52bc502ee65e6baeb5116becdd63a2ec05252dc05b26', 'digest mismatch'; pathlib.Path('round3-verdict.json').write_bytes(data)"
python -I evo-guard.pyz verify-finalized round3-finalized.evb --trusted-pub evidence/round3/finalizer-public.pem --expected-source evidence/round3/expected-source.json --expected-context evidence/round3/expected-context.json --require-pass
gh attestation verify evidence/round3/pr-head-attestation-binding.json --repo EvoRiseKsa/evoom-guard-finalizer-pilot --signer-workflow EvoRiseKsa/evoom-guard-finalizer-pilot/.github/workflows/evoguard-pr-head-attest-builder.yml --source-ref refs/heads/evoguard/pr-head-attestation-pilot/round1 --source-digest 1b6087051e97785ddf39291d147d0fe4649ef74b --predicate-type https://slsa.dev/provenance/v1 --cert-oidc-issuer https://token.actions.githubusercontent.com --deny-self-hosted-runners --limit 1 --format json
```

## What this does and does not establish

This records one positive controlled observation that:

1. an attestation can be externally verified for the exact unmerged PR head H;
2. the verified signer digest equals the reviewed PR-A reusable-builder merge; and
3. the existing Trusted Finalizer independently produced an ALLOW for the same H/base pair.

It does **not** bind any released artifact, package, container image, SBOM, deployment, or merge to this result. It does not prove general behavior across repositories, malicious callers/runners, or attacker-controlled GitHub accounts. It does not close the core artifact-admission issue. PR #22 must remain open and unmerged.
