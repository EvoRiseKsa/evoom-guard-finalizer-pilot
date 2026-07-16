# EvoOM Guard Trusted Finalizer pilot

This repository is a controlled operational pilot for the
[EvoOM Guard Trusted Finalizer](https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/tag/v3.6.1).
The finalizer was introduced in v3.6.0; this pilot pins its executable runtime
to the published v3.6.1 maintenance release.
It is intentionally small so that the authority boundary can be tested without
claiming an independent security review, broad efficacy study, or production
merge enforcement.

## What this pilot proves

A source-only pull request fixed a deliberately broken CLI operation. The base
policy and external verifier pack are protected inputs. The reference finalizer
demonstrated the attempt-bound Check Run, unprivileged candidate re-verification,
privileged sealing, and signed ALLOW/DENY evidence flow.

It does **not** prove that EvoOM Guard is generally correct, that Docker is a VM
boundary, or that the result is independent. A second account controlled by the
same owner may exercise the workflow but cannot provide independent review.

## Round 1 protocol

The pilot follows [`PILOT_PROTOCOL.md`](PILOT_PROTOCOL.md). The `EvoGuard
Trusted Finalizer` check is now a required, strict status check on `main`.
[`ROUND1_RESULTS.md`](ROUND1_RESULTS.md) records the completed PASS →
cancelled/failed attempt → fresh PASS sequence and the separate v3.6.1
revalidation.

## Security boundary

`.evoguard.json`, `security/evoguard-pack/`, and `.github/workflows/` are
security-policy inputs. `CODEOWNERS` also assigns those paths to the designated
technical reviewer, and it is itself listed in the policy's `protected` paths.
Do not modify them in an ordinary candidate pull request.
The private signing key belongs only in the `evoguard-finalizer` Environment,
never in the repository, an artifact, or a normal repository secret. That
Environment requires the designated reviewer, prevents self-review, and does
not permit administrator bypass.

The explicit, audited procedure for changing those trust-root inputs is in
[`POLICY_MAINTENANCE.md`](POLICY_MAINTENANCE.md).
