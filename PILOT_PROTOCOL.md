# Round 1 operational protocol

> **Historical v3.6.1 record.** This protocol preserves the original Round 1
> exercise and its v3.6.1 asset pin. Do not use that historical pin for a new
> run. See [`STATUS.md`](STATUS.md) and [`ROUND2_RESULTS.md`](ROUND2_RESULTS.md)
> for the current v3.7.0 pilot reference and its controlled raw-Git record.

This is an operational exercise of the v3.6.1 reference finalizer, not an
independent efficacy evaluation.

## Preconditions

- The reverify and seal workflows are copied together from the reviewed v3.6.1
  release templates.
- `EVOGUARD_GUARD_ARTIFACT_SHA256` is the reviewed v3.6.1 zipapp digest
  (`4d3e074d707ffdae70e4b3d78e786245c77fd6bdc51782eb1b3f8c4ed0e12a34`).
- The Ed25519 private key is an Environment secret named `EVOGUARD_FINALIZER_KEY`.
- The environment has a reviewer distinct from the candidate author before a
  production claim is made. Same-owner accounts do not meet that criterion.
- The environment prevents self-review and does not permit administrator bypass.
- `EVOGUARD_REVERIFY_WORKFLOW_ID` is set to the reviewed reverify workflow ID.

## Required observations

1. Dispatch on the unchanged source-only PR with the workflow ID unset. The
   reference bootstrap must result in a signed/recorded `DENY`, not a key use.
2. Set the numeric workflow ID, perform a fresh dispatch, approve the protected
   environment, and record the resulting `ALLOW` and finalized evidence bundle.
3. Start a fresh dispatch on the same unchanged head, cancel it after metadata
   creates the pending Check Run, and verify reconciliation of that exact attempt
   to `DENY` without a signing key.
4. Perform a new full dispatch and obtain a fresh `ALLOW`. Record which check
   GitHub regards as satisfiable after the pass/cancel/pass sequence.
5. In separate PRs, confirm that a protected policy/pack change is rejected and
   that the unfixed source produces a black-box `DENY`.

## Completed operational record

The five required observations were recorded in
[`ROUND1_RESULTS.md`](ROUND1_RESULTS.md). The `EvoGuard Trusted Finalizer`
display-name check is now a required, strict status check on `main`, alongside
one current pull-request approval. The v3.6.1 runtime was revalidated by
[PR #8](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/pull/8),
with [reverify run 29519477551](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29519477551)
and [seal run 29519514560](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot/actions/runs/29519514560).

Future trust-root maintenance must follow
[`POLICY_MAINTENANCE.md`](POLICY_MAINTENANCE.md), including code-owner review.
