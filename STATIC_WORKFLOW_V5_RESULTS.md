# Static workflow v5 boundary exercise — PR #25

**Exercise completed:** 2026-07-18 UTC
**Scope:** one controlled, same-owner test of the base-owned static workflow audit and the separate Trusted Finalizer boundary. This is not independent review, artifact admission, a release/deployment decision, or evidence that a proposed trust-root implementation audited itself.

## Candidate and observed runs

[PR #25](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/25) remains **draft, open, blocked, and intentionally unmerged**. It changes only four explanatory comment lines in the protected file `.github/workflows/evoguard-static-security.yml`.

| Item | Immutable identifier | Observed result |
| --- | --- | --- |
| Base B | `5d8640032da7e304c1d077153967cdd4c8096391` | base tree `c7fb122039d508b50c06c4df35447b2d1ea164b5` |
| Candidate H | `c2d857ac64bbaabf021a31080f269ed608273191` | head tree `e60be70fa3a308fdbc3c6d35dedb22e007145155` |
| Static audit | [run 29629827620](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29629827620), job 88041186552 | success: bounded Git reads, actionlint, and pinned offline zizmor |
| Reverify | [run 29629895188](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29629895188), attempt 1 | success: raw-Git bindings re-derived before handoff |
| Seal | [run 29629908972](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29629908972) | workflow failure is expected because the signed decision is DENY |

The static audit ran from protected base-owned workflow bytes. It did not check out or execute candidate code. Its success only says the candidate YAML was parsed and analyzed as data; it does not approve a protected workflow change.

## Signed finalizer result

The published `v3.7.0` Guard asset had SHA-256:

~~~text
1d36f7ec45f47f9f6c3178a25a58accf8f8beb0ffd9d29e7bf93b7fe17ad3ec9
~~~

External verification against fresh raw Git objects and the public finalizer key returned `verified: true` and `decision: DENY`.

| Field | Value |
| --- | --- |
| Envelope SHA-256 | `76f56064095bbc0eb4eda5b960d33e8c3d4067a69b6e29fa334a0194012307a6` |
| Key ID | `sha256:68e67c09cd1a6e997fc982454b0c5f14d72af76680dca78b8077aaed571feea4` |
| Signed record SHA-256 | `511b8ad3d079da310201b204ea8ff26202d29700949e0f49909e3c5076fe650b` |
| Signed record verdict | `REJECTED` |
| Finalizer decision | `DENY` |
| Reason | `protected_harness_edit` |
| Protected path | `.github/workflows/evoguard-static-security.yml` |
| Policy SHA-256 | `fdc8fddcf843b71cdde93611873c71458ac788a9ca7812bf6d923bb0fc6b3df0` |

This is the expected result: a static tool can inspect a proposed trust-root edit without executing it, while the authority that satisfies the merge requirement rejects the protected-path edit.

## Durable inputs and reproduction

The `.evb` is stored as UTF-8 Base64 to preserve exact binary bytes. `MANIFEST.sha256` records the stored-file digests; it is a tamper detector after its own retrieval is trusted, not an independent trust root.

~~~text
python -c "import base64, hashlib, pathlib; p=pathlib.Path('evidence/static-workflow-v5-pr25/finalized.evb.b64'); raw=base64.b64decode(b''.join(p.read_bytes().split()), validate=True); assert hashlib.sha256(raw).hexdigest() == '76f56064095bbc0eb4eda5b960d33e8c3d4067a69b6e29fa334a0194012307a6'; pathlib.Path('pr25-finalized.evb').write_bytes(raw)"
gh release download v3.7.0 --repo EvoRiseKsa/EvoOM-Guard-m --pattern evo-guard.pyz --dir .
python -c "import hashlib, pathlib; assert hashlib.sha256(pathlib.Path('evo-guard.pyz').read_bytes()).hexdigest() == '1d36f7ec45f47f9f6c3178a25a58accf8f8beb0ffd9d29e7bf93b7fe17ad3ec9'"
python -I evo-guard.pyz verify-finalized pr25-finalized.evb --trusted-pub evidence/static-workflow-v5-pr25/finalizer-public.pem --expected-source evidence/static-workflow-v5-pr25/expected-source.json --expected-context evidence/static-workflow-v5-pr25/expected-context.json
~~~

Do **not** add `--require-pass`: the expected, verified decision here is DENY.

For an independent raw-Git re-derivation, clone the pilot bare, use B/H and the two recorded tree IDs above, then run `derive-finalizer-bindings` with repository ID `1302971633`, PR `25`, run `29629895188`, attempt `1`, and the Guard asset SHA. Extract `record/verdict.json` from the decoded bundle and run `verify-finalizer-bindings` against the recomputed bindings. The output must match the archived expected source/context and the archived `derived-bindings.json`.

## Limits

- This is one controlled same-owner exercise; MANA-awam's environment approval is a technical role separation, not independent review.
- It does not validate the proposed static workflow implementation before merge; the protected base implementation performed the audit.
- It does not attest a build artifact, package, container, SBOM, release, deployment, or production acceptance.
- PR #25 remains evidence only and must not be merged.
