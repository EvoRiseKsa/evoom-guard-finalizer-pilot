# EvoOM Guard Trusted Finalizer pilot

This repository is a controlled operational pilot for the
[EvoOM Guard Trusted Finalizer](https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/tag/v3.7.0).
The finalizer was introduced in v3.6.0. Its current trusted workflow templates
and executable pin use the published immutable v3.7.0 release asset.
It is intentionally small so that the authority boundary can be tested without
claiming an independent security review, broad efficacy study, or production
merge enforcement.

> **Current status.** [`STATUS.md`](STATUS.md) identifies the active v3.7.0
> reference, distinguishes historical Round 1 from current Round 2 evidence,
> and records the limits and pilot-closure procedure. This repository is
> source-available under the included [`LICENSE`](LICENSE); it is not
> OSI-approved open source.

## What this pilot proves

A source-only pull request fixed a deliberately broken CLI operation. The base
policy and external verifier pack are protected inputs. The reference finalizer
demonstrated the attempt-bound Check Run, unprivileged candidate re-verification,
privileged sealing, and signed ALLOW/DENY evidence flow.

It does **not** prove that EvoOM Guard is generally correct, that Docker is a VM
boundary, or that the result is independent. A second account controlled by the
same owner may exercise the workflow but cannot provide independent review.

## Round 1 protocol (historical v3.6.1)

The pilot follows [`PILOT_PROTOCOL.md`](PILOT_PROTOCOL.md). The `EvoGuard
Trusted Finalizer` check is now a required, strict status check on `main`.
[`ROUND1_RESULTS.md`](ROUND1_RESULTS.md) records the completed PASS →
cancelled/failed attempt → fresh PASS sequence and the separate v3.6.1
revalidation.

## Round 2 raw-Git finalizer record

[`ROUND2_RESULTS.md`](ROUND2_RESULTS.md) records a fresh, deliberately
source-only and unmerged v3.7.0 exercise. It records raw-Git derivation and
comparison of the candidate, policy, and verifier-pack bindings before the
privileged seal, plus verification of the resulting signed evidence against
fresh Git/API-derived context. It is still a controlled same-owner operational
exercise, not independent review, broad efficacy evidence, or production
merge-enforcement validation.

## GitHub Artifact Attestation provider probe

[`ARTIFACT_ATTESTATION_PROBE.md`](ARTIFACT_ATTESTATION_PROBE.md) defines a
separate, manually dispatched provider experiment. Its first run completed on
2026-07-18 and is recorded in
[`PROVIDER_PROBE_RESULTS.md`](PROVIDER_PROBE_RESULTS.md). It attested and
re-verified one non-executable file constructed from protected default-branch
metadata. It is not a finalizer, artifact-admission, release, deployment, or
merge gate, and the successful run must not be described as any of those
things.

## PR-head provenance pilot

[PR_HEAD_ATTESTATION_PILOT.md](PR_HEAD_ATTESTATION_PILOT.md) defines a separate
staged experiment for the unresolved distinction between a finalizer-allowed
pull-request head H and a later merged revision M. This first maintenance phase
adds only a dormant reusable builder. It has no caller and therefore creates no
run. It is not artifact admission, V2 admission, a release or deployment
control, or a merge gate.

## Security boundary

`.evoguard.json`, `security/evoguard-pack/`, and `.github/workflows/` are
security-policy inputs. `CODEOWNERS` also assigns those paths to the designated
technical reviewer, and it is itself listed in the policy's `protected` paths.
Do not modify them in an ordinary candidate pull request.
In the v3.7.0 pilot templates, both the reverify handoff and the key-bearing
seal derive and compare these bindings from immutable raw Git objects before
any sealing step can read the private key.
The private signing key belongs only in the `evoguard-finalizer` Environment,
never in the repository, an artifact, or a normal repository secret. That
Environment requires the designated reviewer, prevents self-review, and does
not permit administrator bypass.

The explicit, audited procedure for changing those trust-root inputs is in
[`POLICY_MAINTENANCE.md`](POLICY_MAINTENANCE.md).
