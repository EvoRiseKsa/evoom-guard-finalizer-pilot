# Pilot status and claim boundary

## Current reference

This controlled pilot currently references the immutable EvoOM Guard `v3.7.0`
release asset. The checked-in `main` state at the time of this status document
is `37ae23a4e33127c85a317fd7208e955c272d1d31`. The configured Guard asset
digest is:

```text
1d36f7ec45f47f9f6c3178a25a58accf8f8beb0ffd9d29e7bf93b7fe17ad3ec9
```

Consumers should verify the release checksum for their own downloaded asset;
this pilot is not a distribution channel or a substitute for that verification.

## Evidence status

[`ROUND1_RESULTS.md`](ROUND1_RESULTS.md) is a historical v3.6.1 operational
record. [`ROUND2_RESULTS.md`](ROUND2_RESULTS.md) records the v3.7.0 controlled
raw-Git finalizer exercise, including a signed evidence bundle and public
verification inputs. Both are same-owner technical exercises, not independent
security review, a performance benchmark, or production merge-enforcement
evidence.

Pull request #12 remains intentionally open and unmerged because it is the
source-only candidate used by the recorded exercise. It must not be merged as
part of routine cleanup; when the pilot is retired, close it with an
explanatory comment that preserves this evidence context.

## Security and operating limits

The protected Environment and second account create a technical
separation-of-roles control. The two identities are controlled by the same
project owner, so they are not independent approval. The environment signing
key remains only in the protected Environment; no private key belongs in this
repository, an artifact, or a normal repository secret.

The pilot validates the documented finalizer workflow for a controlled,
source-only candidate. It does not establish a hostile-runner boundary,
general software correctness, OCI/release/deployment provenance, SBOM coverage,
or a production service assurance level.

## Completed provider probe

The first GitHub Artifact Attestation provider probe completed successfully on
2026-07-18. Its exact run, subject checksum, attestation identity, retained
artifact expiry, independent local re-verification, and negative tests are
recorded in [`PROVIDER_PROBE_RESULTS.md`](PROVIDER_PROBE_RESULTS.md). It has no
finalizer/admission key, protected admission Environment, release,
deployment, or merge-gate effect.

GitHub did create an ordinary Actions check run named `probe` for that
workflow. It neither creates, satisfies, nor influences the required
`EvoGuard Trusted Finalizer` check or a merge decision. The completed probe
establishes only that GitHub generated and re-verified provenance for its own
non-executable probe file under a bounded identity policy; it does not change
the limits above or close the artifact-admission work.

## Planned closure

Keep this repository public while it serves as inspectable controlled evidence.
After an explicit pilot-close decision, first verify retained evidence and
document the final state, then close intentionally open evidence PRs with their
context preserved, and only then archive the repository. Archiving is not a
security control and does not make prior public material private.
