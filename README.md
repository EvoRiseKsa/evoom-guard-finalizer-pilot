# EvoOM Guard Trusted Finalizer pilot

This repository is a controlled operational pilot for the
[EvoOM Guard Trusted Finalizer](https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/tag/v3.6.1).
The finalizer was introduced in v3.6.0; this pilot pins its executable runtime
to the published v3.6.1 maintenance release.
It is intentionally small so that the authority boundary can be tested without
claiming an independent security review, broad efficacy study, or production
merge enforcement.

## What this pilot proves

The open source-only pull request fixes a deliberately broken CLI operation. The
base policy and external verifier pack are protected inputs. The reference
finalizer then demonstrates the attempt-bound Check Run, unprivileged candidate
re-verification, privileged sealing, and signed ALLOW/DENY evidence flow.

It does **not** prove that EvoOM Guard is generally correct, that Docker is a VM
boundary, or that the result is independent. A second account controlled by the
same owner may exercise the workflow but cannot provide independent review.

## Round 1 protocol

The pilot follows [`PILOT_PROTOCOL.md`](PILOT_PROTOCOL.md). In particular, the
`EvoGuard Trusted Finalizer` check is not a required status check until the
PASS → cancelled/failed attempt → fresh PASS sequence has been recorded against
GitHub's actual Check Run behaviour.

## Security boundary

`.evoguard.json`, `security/evoguard-pack/`, and `.github/workflows/` are
security-policy inputs. Do not modify them in an ordinary candidate pull request.
The private signing key belongs only in the `evoguard-finalizer` Environment,
never in the repository, an artifact, or a normal repository secret.

The explicit, audited procedure for changing those trust-root inputs is in
[`POLICY_MAINTENANCE.md`](POLICY_MAINTENANCE.md).
