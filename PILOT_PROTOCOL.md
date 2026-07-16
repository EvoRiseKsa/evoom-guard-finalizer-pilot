# Round 1 operational protocol

This is an operational exercise of the v3.6.0 reference finalizer, not an
independent efficacy evaluation.

## Preconditions

- The reverify and seal workflows are copied together from the reviewed v3.6.0
  release templates.
- `EVOGUARD_GUARD_ARTIFACT_SHA256` is the reviewed v3.6.0 zipapp digest.
- The Ed25519 private key is an Environment secret named `EVOGUARD_FINALIZER_KEY`.
- The environment has a reviewer distinct from the candidate author before a
  production claim is made. Same-owner accounts do not meet that criterion.
- `EVOGUARD_REVERIFY_WORKFLOW_ID` is initially absent for the bootstrap attempt.

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

Do not make the display-name check required until the observations are published
with run IDs and the ruleset/branch-protection behaviour is unambiguous.
