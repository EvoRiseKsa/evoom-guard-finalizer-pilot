# Pilot baseline after static-workflow v5 exercise

The trusted-finalizer pilot is frozen as an **evidence baseline**, not as a product release line.

## Baseline facts

- Published Guard asset: immutable `v3.7.0` `evo-guard.pyz`
- Published asset SHA-256: `1d36f7ec45f47f9f6c3178a25a58accf8f8beb0ffd9d29e7bf93b7fe17ad3ec9`
- Finalizer policy used for the latest boundary exercise: `trusted-finalizer-pilot` version `5`
- Policy SHA-256: `fdc8fddcf843b71cdde93611873c71458ac788a9ca7812bf6d923bb0fc6b3df0`
- Required merge context: `EvoGuard Trusted Finalizer`, constrained to the GitHub Actions app ID configured in branch protection.
- The signing key remains only in the protected `evoguard-finalizer` Environment. No private key is retained in this repository.

## Operating rule

Do not add unrelated features, provider adapters, release gates, ML/risk logic, or production claims to this pilot. Trust-root changes remain permitted only to correct a demonstrated defect and must follow `POLICY_MAINTENANCE.md`.

The next capability experiment is an isolated Artifact Admission Pilot. It must use separate keys, a separate protected Environment, a real bounded artifact, GitHub provenance pins, and a V2 admission receipt. It must not be represented as available through the published v3.7.0 asset until a new released version contains and has exercised the required code.
