# Round 2 operational results — v3.7.0 raw-Git finalizer

**Exercise completed:** 2026-07-16 UTC
**Scope:** Controlled post-v3.7.0 operational exercise of the Trusted Finalizer's
raw-Git derivation path. This is not an independent assessment, a benchmark, or
a production-readiness claim.

## Preceding trust-root maintenance

- [PR #11](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/11)
  merged at 71315505eda3b8ed5291562ab6b53a20ff36b04b.
- Its reviewed change set modified only
  .github/workflows/evoguard-reverify.yml and
  .github/workflows/evoguard-seal.yml.
- MANA-awam approved PR #11. This is a technical separation-of-roles exercise
  only: both identities are controlled by the same project owner and are not
  independent review.
- The configured Guard release digest after maintenance is
  1d36f7ec45f47f9f6c3178a25a58accf8f8beb0ffd9d29e7bf93b7fe17ad3ec9. It
  matches the published v3.7.0 evo-guard.pyz checksum.

## Controlled candidate

[PR #12](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/12)
remains open and unmerged. It changes exactly one unprotected source file,
calc/ops.py (+2/-0), at:

~~~text
base: 71315505eda3b8ed5291562ab6b53a20ff36b04b
head: f892649ca3fa1a8c58a787c55c641d50ae94ddc9
base tree: b9e810162bba73ab84be0b35253d9240965a6f89
head tree: a7633c141735dcb2a6bfb92f16f9dc0d68bbe6c3
~~~

The reverify workflow itself runs from protected main; therefore its workflow
head SHA is the base commit above, while the signed candidate source is PR #12's
separate head commit.

## Observed workflow result

| Stage | Immutable evidence | Observed result |
| --- | --- | --- |
| Reverify | [run 29536858222](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29536858222), attempt 1, workflow ID 314551862 | Completed successfully. The no-secret reverify and raw-Git binding derivation both completed. |
| Environment gate | [seal run 29536888905](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29536888905) | GitHub records environment evoguard-finalizer as approved by MANA-awam; administrator bypass is disabled. This is not independent approval. |
| Seal | Same seal run | Completed successfully after the environment gate. |
| Required check | Check run 87750163586, GitHub Actions app ID 15368 | EvoGuard Trusted Finalizer completed SUCCESS; its final decision was ALLOW. |
| Semantic result | Signed record inside the finalized bundle | Black-box verifier pack: 2/2 passed; observed candidate isolation: docker; protected violations: none. |

## Signed evidence and independent recomputation

The final artifact is evoguard-finalized-evidence-29536858222, uploaded by the
seal run as GitHub artifact 8390929866.

~~~text
finalized.evb SHA-256:
c5543eefbbf8e6c285ae4680b0005ec093f18091eacc8312afd862c7c2563cab

bundle key ID:
sha256:68e67c09cd1a6e997fc982454b0c5f14d72af76680dca78b8077aaed571feea4

record/verdict.json SHA-256:
542838ea19ff7d3aa25fb1f9bc1a06c99ec1ce2445a592d9dd19f0769f546731

trusted-finalizer-git-bindings SHA-256:
8d6055d2c9d854a7b8801fee0c40bac54afa0ee6f04c8e1f64ea08a611575eee

trusted-finalizer-handoff SHA-256:
8adc8c2026c9cec8a1f0db54d74a82f71e8842cdc438a99fe42036f73b62fdb4
~~~

An external verification independently obtained the PR revisions and Git trees
from GitHub's API, verified the published v3.7.0 asset checksum, fetched the two
immutable Git objects into a fresh bare repository, and re-derived the raw-Git
binding. The independently derived binding matched the signed bundle material
exactly.

~~~text
candidate SHA-256:
1aba7fc0f229e458572167b32ab28e2f5b4e93510599cc6a9055c691262900a3

effective-policy SHA-256:
9f7a3d4b609c274c674648f14ea42ab2c3aac48bdc238c186abd86b4c729afcb

verifier-pack SHA-256:
e864e79a2e3ac35fc83a8170b7da2608c5831c282cce01a6583df84400271e7e
~~~

verify-finalized --require-pass, using the externally fetched public key and
externally reconstructed source/context, returned verified: true and decision:
ALLOW.

Recheck the durable bundle with a Python interpreter and the published v3.7.0
evo-guard.pyz whose SHA-256 is recorded above:

~~~text
python -I evo-guard.pyz verify-finalized evidence/round2/finalized.evb --trusted-pub evidence/round2/finalizer-public.pem --expected-source evidence/round2/expected-source.json --expected-context evidence/round2/expected-context.json --require-pass
~~~

## External verification inputs

~~~json
{"base_sha":"71315505eda3b8ed5291562ab6b53a20ff36b04b","head_sha":"f892649ca3fa1a8c58a787c55c641d50ae94ddc9","pull_request_number":12,"workflow_run_attempt":1,"workflow_run_id":"29536858222"}
~~~

The accompanying expected-context.json, derived-bindings.json, and
finalizer-public.pem are required verification inputs; their SHA-256 values are
listed in evidence/round2/MANIFEST.sha256.

## Limits

- This validates one controlled source-only candidate, not arbitrary
  repositories, malicious runners, or broad detection efficacy.
- The MANA approval and PR #11 review are not independent review.
- Docker observation is not a VM-equivalence or host-escape claim.
- This round does not bind a release artifact, OCI image, deployment, SBOM, or
  provenance statement to the finalizer decision.
- PR #12 is intentionally unmerged. The result is evidence of the controlled
  workflow run, not evidence that an application change was accepted into
  production.
- Current branch-protection settings are observable separately; this document
  does not replace GitHub audit history for any maintenance exception.
