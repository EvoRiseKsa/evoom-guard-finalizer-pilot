# PR-head artifact-attestation pilot

## Question

The unresolved admission problem is a provenance-identity question, not a
release-format question. A finalizer can allow a pull-request head revision H,
whereas a normal release is built later from a merged revision M. A valid
artifact admission must not silently substitute M for H.

This staged pilot asks one narrow provider question:

> Can GitHub generate and externally verify a provenance attestation whose
> source digest is the exact open same-repository pull-request head H, and
> whose signer is a reviewed reusable builder on the protected default branch?

The existing manual provider probe proved only protected-default-branch
metadata. It did not answer this question.

## Round 1 status

The staged method below records the completed Round 1 observation from
2026-07-18. PR #22 was open when the eligible source head H was pushed and
verified; it was later closed unmerged after the evidence was retained. This
document is a protocol and boundary record for that historical experiment. It
does not authorize a new candidate push, artifact admission, or any production
operation.

## Exact trust boundary

The reusable builder is intentionally fixed to this one pilot repository,
repository ID 1302971633, default branch main, and the one candidate ref
refs/heads/evoguard/pr-head-attestation-pilot/round1. It is not a generic
workflow service.

GitHub gives a reusable workflow the caller context. Therefore any future
caller is deliberately treated as untrusted input. The builder declares no
inputs or caller-supplied secrets; it uses only the automatically supplied
GitHub token under its declared minimal permissions. It materializes no
candidate checkout and constructs a small regular file only after GitHub API
responses confirm all of the following:

- the event is a push for the exact one-off pilot ref;
- the event SHA is H and maps to exactly one open PR;
- that PR targets main;
- the PR base and head repository IDs are the fixed pilot repository;
- the PR head ref and SHA exactly equal the event ref and H.

It re-fetches the selected PR before it constructs the file, so an update
visible at that second read is rejected. H is immutable, and later evidence
must still compare the recorded H and base SHA. It then requests a GitHub
attestation and verifies one result with the exact repository, reusable
workflow path, source ref, source digest H, GitHub OIDC issuer,
GitHub-hosted-runner constraint, and SLSA v1 predicate. It records a bounded
non-secret subject, result, bundle checksum, and observed signer digest for
seven days.

An eventual Actions job check is not, does not satisfy, and cannot influence
the required EvoGuard Trusted Finalizer check or a merge decision.

## Caller boundary

GitHub loads a `push` workflow from the pushed candidate revision.  The
default-branch caller is therefore not a trust root by itself when a candidate
run begins: a candidate author can alter that candidate's copy.  The caller is
pre-declared as a protected path to govern what can merge into `main`, but that
does not make its unmerged copy authoritative.

For that reason, the reviewed default-branch caller declares no repository or
Environment secrets, targets no Environment, and has no admission, release,
deployment, status-check, or merge authority. It passes no input and no secret
to the builder. Its only intended operation is a reusable-workflow call pinned
by full SHA to the PR-A maintenance merge:

`EvoRiseKsa/evoom-guard-finalizer-pilot/.github/workflows/evoguard-pr-head-attest-builder.yml@cd6175d7dadb968339090545060d441d181363d5`

The provider result is acceptable only if its certificate `buildSignerDigest`
equals that SHA and external verification also binds the attestation to the
exact candidate H.  A matching path name or an ordinary Actions check is not
enough. A candidate can also alter its copy of the caller's `uses` reference;
such a result is rejected unless those external identity checks still prove the
reviewed builder at the stated SHA.

“Has no secret” above describes the reviewed default-branch caller, not an
unmerged candidate copy. Immediately before the controlled run, record these
repository preconditions again: no repository secret is present; the default
workflow token setting is read-only; and the key-bearing `evoguard-finalizer`
Environment still requires review and permits protected branches only. Those
are current operational controls, not guarantees made by a candidate workflow
file.

## Staged method

1. PR-A added the dormant reusable builder and made it a protected, Code
   Owner-routed trust-root path. It added no caller and ran nothing.
2. PR-B adds the pre-declared protected default-branch
   caller. It references the reusable workflow by full repository path and
   the exact PR-A merge SHA
   `cd6175d7dadb968339090545060d441d181363d5`. A local reference, main
   reference, or tag is not acceptable. The caller remains dormant until the
   exact one-off branch in the next step is pushed.
3. Create the exact one-off branch and open the temporary, unmerged
   same-repository PR. Its first push can correctly fail closed because no PR
   exists yet for the builder to bind; that run is not evidence. After the PR
   is open, push one further harmless source-only revision. That second pushed
   head is H and is the only run eligible for this experiment.
4. The resulting attestation will be verified independently against H and the
   reusable builder identity. The observed signer digest will be recorded
   before any later experiment considers pinning it.
5. The finalizer must independently reach ALLOW for the same H and base before
   any future design considers an admission record.

## Acceptance and stop conditions

The experiment passes only if independent verification confirms the exact H,
the exact reusable builder workflow path, expected GitHub OIDC issuer,
hosted-runner constraint, provenance predicate, and exactly one selected
attestation. The retained receipt, subject digest, bundle digest, and external
verification result must be preserved before the short-lived artifact expires.

Stop without advancing if the provider reports a merge SHA instead of H, the
signer identity is not the reusable builder, the PR association is ambiguous,
the verifier accepts a weaker identity, the observed signer digest is not the
PR-A merge SHA, or any job requires a candidate checkout, secret, Environment,
finalizer key, release, deployment, admission, or merge privilege.

No result of this pilot is artifact admission, V2 admission, artifact-bound
finalization, a release claim, a deployment claim, or proof of independent
review. It cannot close the core artifact-admission issue by itself.

## Review limitation

The designated Code Owner identity MANA-awam and EvoRiseKsa are controlled by
the same project owner. Their use documents technical separation of roles, not
independent review.
