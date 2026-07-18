# Trust-root policy maintenance

The trusted finalizer deliberately rejects ordinary pull requests that modify
its trust root. That includes `.github/workflows/evoguard-reverify.yml`,
`.github/workflows/evoguard-seal.yml`, `.evoguard.json`, and
`security/evoguard-pack/`, and the policy-protected `.github/CODEOWNERS` file.
A `REJECTED` record with
`reason_code: protected_harness_edit` is the expected result for such a pull
request; it is not evidence that the guard malfunctioned.

Those files decide what is judged, who may seal evidence, and which Guard
artifact is trusted. They therefore need a separate, explicit governance
procedure rather than an implicit bypass of the normal candidate gate.

The provider-probe workflow is **not** part of the finalizer trust root and the
finalizer does not itself treat that path as a protected harness input. It is separately Code
Owner-governed because its exact signer workflow path becomes part of the
provider-verification observation. Changing `.github/CODEOWNERS` to add or
alter that routing remains a finalizer-protected policy change, so the initial
addition still follows this maintenance procedure. Its current purpose and
non-claims are in
[`ARTIFACT_ATTESTATION_PROBE.md`](ARTIFACT_ATTESTATION_PROBE.md). Do not broaden
it into an admission, release, deployment, or status-check workflow without a
new threat-model review.

The reusable PR-head attestation builder and its pre-declared future caller are
distinct protected trust-root inputs. The eventual caller is untrusted input
and must have no repository or Environment secret, must not target an
Environment, and must have no admission, release, deployment, or merge
authority. The builder's exact workflow identity can later be used in a
provenance verification policy, so changes to either workflow or their Code
Owner routing always follow this maintenance procedure. This maintenance change
increments the declared pilot policy version so later verdict evidence cannot
silently present it as the prior policy. Its staged method and explicit
non-claims are in
[PR_HEAD_ATTESTATION_PILOT.md](PR_HEAD_ATTESTATION_PILOT.md).

## Required maintenance procedure

1. Open a narrowly scoped pull request and identify it as a trust-root policy
   maintenance change. Do not mix application features or unrelated cleanup
   into it.
2. Record the exact release tag, source commit, asset checksum, policy/pack
   digests, and pre-merge validation that motivate the change. Verify a release
   asset against its published `SHA256SUMS` before pinning it.
3. Obtain the required code-owner and pull-request approval from a different
   GitHub identity or an organization-controlled reviewer. A same-owner second
   account provides only a technical separation of roles; it is not independent
   review.
4. Preserve all branch protections except the one candidate status check that
   cannot authorize a change to itself. Snapshot the protection settings,
   temporarily remove **only** the `EvoGuard Trusted Finalizer` required check,
   merge the reviewed maintenance PR, and immediately restore that exact
   required check with its GitHub Actions app binding. The PR, review,
   protection change, and restoration must remain visible in GitHub's audit
   history.
5. Once the new templates are on the protected base, update any matching
   repository variable or Environment configuration. Never update a checksum
   variable before its base workflow downloads the matching release URL.
6. Create a fresh source-only PR and run the full reverify → environment
   approval → seal sequence. Verify the resulting signed bundle with the
   independently supplied public key and API-derived run/revision/tree context.
   Publish the outcome, including any denial or failure.

## Non-goals and stop conditions

This procedure does not make the software, reviewer, or evaluation
independent. It is not a way to let candidate code alter a judge, to skip
evidence verification, or to weaken the normal finalizer gate. If the
post-maintenance source-only run fails, restore the previous known-good trust
root or stop the rollout; do not claim that the new policy is operational.
