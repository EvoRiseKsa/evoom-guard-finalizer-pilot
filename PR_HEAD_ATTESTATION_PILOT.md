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

## Staged method

1. This maintenance PR adds the dormant reusable builder and makes it a
   protected, Code Owner-routed trust-root path. It adds no caller and runs
   nothing.
2. A separate maintenance PR will add the pre-declared protected
   default-branch caller. It must reference this reusable workflow by full
   repository path and the exact SHA of this maintenance merge. A local
   reference, main reference, or tag is not acceptable.
3. A temporary, unmerged same-repository PR on the exact one-off ref will alter
   only a harmless source file. Its pushed head H will exercise the caller.
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
