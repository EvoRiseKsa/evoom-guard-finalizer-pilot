# GitHub Artifact Attestation provider probe

> **Executed once, provider capability only.** The first successful run is
> recorded in [`PROVIDER_PROBE_RESULTS.md`](PROVIDER_PROBE_RESULTS.md). It is
> evidence about GitHub's provider behavior, not evidence that the pilot has
> artifact-bound admission.

## Purpose

The pilot's finalizer records an externally re-verified decision for a pull
request source revision. A GitHub Release attestation is a different product
from a GitHub Artifact Attestation, and neither one alone connects a finalizer
`ALLOW` to an artifact.

The `EvoGuard GitHub Artifact Attestation Provider Probe` workflow establishes
only the smallest missing provider fact: GitHub can produce and the GitHub CLI
can re-verify a build-provenance attestation for one exact regular file built
on this pilot's protected default branch.

The subject is a non-executable, run-specific text file containing only:

- a fixed format identifier;
- the repository name;
- the GitHub-controlled workflow run ID and attempt;
- the checked-out default-branch source ref and digest; and
- the fixed `provider-verification-only` purpose.

It does not run a candidate, build the pilot CLI, publish a release, use an
Environment, read a secret, issue a finalizer decision, or create a V2
admission record. GitHub Actions does create an ordinary `probe` check run;
that check does not create, satisfy, or influence the required `EvoGuard
Trusted Finalizer` check or a merge decision.

## Provider constraints actually enforced

The manually dispatched workflow refuses every ref except the default branch,
does not check out repository content, hashes the small regular-file subject,
and invokes the pinned `actions/attest` action.
It then runs `gh attestation verify` for the exact:

- `EvoRiseKsa/evoom-guard-finalizer-pilot` repository;
- `.github/workflows/evoguard-artifact-attestation-probe.yml` signer workflow;
- default-branch source ref and exact source digest;
- SLSA v1 predicate and GitHub Actions OIDC issuer;
- GitHub-hosted-runner constraint; and
- one-result lookup limit.

The initial probe deliberately does **not** pin a signer-workflow digest.
Its purpose is to discover and preserve the provider's observed direct-workflow
certificate semantics before any future protected admission policy pins that
value. Omitting that one prospective admission constraint is acceptable only
because this workflow produces no admission, release, deployment, or merge
decision.

The provider output is capped while written. The retained artifact contains
the subject, checksums, bounded provider result, and a compact receipt with
the GitHub attestation ID/URL, bundle checksum, and GitHub CLI version. The
receipt does not interpret `statement.predicate` data; GitHub documents that
predicate data can be controlled by the originating workflow. Successful
provider verification, with the listed identity flags, is the relevant
cryptographic observation.

## How the first run was made, and how to repeat a provider-only observation

1. Confirm the PR was merged using the trust-root procedure in
   [`POLICY_MAINTENANCE.md`](POLICY_MAINTENANCE.md), including restored branch
   protection and a technical MANA review. That is separation of roles only,
   not independent review.
2. Open **Actions** → **EvoGuard GitHub Artifact Attestation Provider Probe**.
3. Choose `main` and select **Run workflow**. Do not choose a tag or PR branch.
4. Wait for the one `probe` job. A pass means only that GitHub generated and
   then re-verified an attestation under the exact constraints above. It will
   create an ordinary Actions check run, not the required finalizer check.
5. Download the retained probe artifact before its seven-day expiry. Verify the
   two SHA-256 files locally and rerun `gh attestation verify` against the
   downloaded probe subject with the recorded repository, signer workflow,
   source ref, and source digest.
6. Record the run URL, source SHA, subject checksum, verifier output checksum,
   and any observed certificate/signer-digest detail in a separate review
   record. Do not add it to a release or label it an admission result.

## Success and stop conditions

A successful provider probe requires all of the following:

- `actions/attest` succeeds for the exact subject bytes;
- the bounded `gh attestation verify` command succeeds after at most three
  transient-read attempts;
- its bounded lookup returns exactly one selected verified result; and
- the subject hash remains unchanged before and after verification.

Stop instead of weakening controls if the provider cannot satisfy the exact
workflow/source identity, needs a broader permission, returns more than one
selected result, or makes the provider result too large to retain under the
bound. `--limit 1` limits the CLI lookup; it is not a claim that no other
attestations exist globally. The run-specific subject prevents an ordinary
rerun from reusing the same subject bytes.
Resolve the observed provider behavior in a new, reviewed change; do not turn
off identity flags, allow a candidate source ref, or add a key to this job.

## Explicit non-claims

This experiment does **not** establish artifact admission, release integrity,
reproducible builds, OCI provenance, deployment authorization, SLSA level,
independent review, or production merge enforcement. A later artifact-bound
gate would still need a protected builder for the exact finalizer source,
provider re-verification in a separate protected job, an independently
verified finalizer `ALLOW`, and a separate admission key and record.
