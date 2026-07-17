# GitHub Artifact Attestation verification template

> **Inactive reference template.** This directory is not a workflow in this
> pilot. It exists for an adopter that has both a protected build/release path
> and a real GitHub **Artifact Attestation** for the artifact it wants to
> admit. Do not copy it to `.github/workflows/` merely because the source
> project has a GitHub Release attestation.

The template performs one narrow operation: it downloads one protected exact
release asset and invokes `gh attestation verify` with an exact repository,
signer workflow, signer digest, source ref, and source digest. GitHub CLI is
therefore the provider-specific signature/identity verifier; EvoGuard is not
claiming to parse or independently validate the attestation bundle itself.

## Why it is not enabled in this pilot

`EvoRiseKsa/EvoOM-Guard-m` v3.7.0 has a GitHub **Release Attestation**, but its
`evo-guard.pyz` release asset does not currently have a GitHub Artifact
Attestation. A direct `gh attestation verify` for that asset therefore fails
closed with `no attestations found`. The finalizer pilot also deliberately has
no production build/release pipeline. Enabling this template here would create
either a perpetual failing job or an untrue provenance claim.

This distinction matters: a release attestation and an artifact attestation
are different GitHub products and must not be substituted for each other.

## Required deployment model

Copy `evoguard-verify-github-attestation.yml` into the *same protected
repository that produces the artifact*. Before enabling it, create the
`evoguard-artifact-attestation` Environment with all of these controls:

1. Protect deployment branches to the default branch.
2. Require a reviewer different from the release author, prevent self-review,
   and disable administrator bypass for a production claim.
3. Keep changes to the copied workflow and this Environment configuration under
   the same trust-root review procedure as the finalizer workflow.
4. Do not put a finalizer or artifact-admission private key in this Environment.
   This template only reads and verifies.

Set the following **Environment-scoped variables**. They describe one immutable
subject and are deliberately not workflow-dispatch inputs.

| Variable | Required exact value |
| --- | --- |
| `EVOGUARD_ATTESTATION_ARTIFACT_URL` | `https://github.com/<this-owner>/<this-repo>/releases/download/<tag>/<asset>` with no query, fragment, or percent encoding. The normal GitHub download redirect is followed only after this initial URL is validated. |
| `EVOGUARD_ATTESTATION_ARTIFACT_SHA256` | Lowercase SHA-256 of that exact downloaded asset, without a `sha256:` prefix. |
| `EVOGUARD_ATTESTATION_SOURCE_REPOSITORY` | Exactly the repository where the copied workflow executes. |
| `EVOGUARD_ATTESTATION_SIGNER_WORKFLOW` | Exact same-repository path `<owner>/<repo>/.github/workflows/<file>.yml`. |
| `EVOGUARD_ATTESTATION_SIGNER_DIGEST` | Exact lowercase 40- or 64-character `buildSignerDigest` Git object ID expected from the GitHub certificate. |
| `EVOGUARD_ATTESTATION_SOURCE_REF` | Exact `refs/heads/...` or `refs/tags/...` expected for the build source. |
| `EVOGUARD_ATTESTATION_SOURCE_DIGEST` | Exact lowercase 40- or 64-character `sourceRepositoryDigest` Git object ID expected for the build source. |

The template intentionally supports only a same-repository, direct signer
workflow. For a reusable/cross-repository builder, make a separately reviewed
derivative that has an exact `--signer-workflow` identity for the reusable
workflow; do not weaken it to `--owner` or a caller-controlled `--signer-repo`.

## What the workflow checks

The copied workflow:

- accepts no dispatcher-provided artifact, digest, repository, or workflow;
- runs only from its reviewed default-branch copy;
- checks the release URL shape and hashes downloaded bytes before and after
  verification;
- calls:

  ```bash
  gh attestation verify artifact \
    --repo "$SOURCE_REPOSITORY" \
    --signer-workflow "$SIGNER_WORKFLOW" \
    --signer-digest "$SIGNER_DIGEST" \
    --source-ref "$SOURCE_REF" \
    --source-digest "$SOURCE_DIGEST" \
    --predicate-type https://slsa.dev/provenance/v1 \
    --cert-oidc-issuer https://token.actions.githubusercontent.com \
    --deny-self-hosted-runners \
    --limit 1 \
    --format json
  ```

- refuses a GitHub CLI missing any required strict flag, and requires exactly
  one verified result from its bounded `--limit 1` lookup;
- writes a bounded JSON receipt containing the subject digest, fixed policy,
  GitHub CLI version, count of verified attestations, and SHA-256 of raw CLI
  output; and
- uploads only that receipt and its checksum. It does not upload a candidate
  checkout, a private key, or raw predicate data.

The `gh` command's success is the provider-specific cryptographic verification
point. GitHub documents that `statement.predicate` output can be manipulated by
the workflow that created an attestation, so the template deliberately does not
make a security decision from predicate fields.

## Relationship to EvoGuard finalizer and V2 digest admission

The receipt is **not** a finalizer decision, build admission, deployment
authorization, independent audit, or portable proof that a third party can
verify without GitHub. It is a bounded record that a protected job ran the
provider verifier under an exact policy. A consumer must independently rerun
`gh attestation verify` when it verifies the result.

An artifact-bound gate needs all of these separately authenticated relations:

1. A trusted finalizer produces an external, verified `ALLOW` for source commit
   `H`.
2. A protected builder builds the exact subject from `H` and produces the
   GitHub Artifact Attestation. Candidate-controlled build logic is not a
   trusted builder merely because it emits an attestation.
3. This template pins `--source-digest H`, the exact signer workflow, and the
   subject bytes, then runs GitHub's verifier.
4. A **different protected Environment and different Ed25519 key** may then
   run EvoOM Guard's `seal-artifact-digest-admission` with the matching
   verified finalizer bundle, subject digest, and this exact receipt. It must
   re-derive the source/finalizer match and re-run GitHub verification before
   accessing its admission key.

The next-minor V2 API currently present in the EvoOM Guard source tree (but
not in the released `v3.7.0` zipapp) binds an opaque provenance-reference file
by identity and digest. It does not itself validate a GitHub bundle, registry
state, a build, publication, or deployment. This template supplies the missing
provider check in a protected job; it does not erase the remaining
build/control-plane trust assumptions.

## Platform and retention limits

GitHub Artifact Attestations for GitHub Free, Pro, and Team are available only
for public repositories; private/internal repository support requires GitHub
Enterprise Cloud. Actions artifacts are retained only for the configured
period, so preserve the exact release artifact, finalizer evidence, receipt,
checksum, configuration change review, and independent re-verification
instructions outside ephemeral workflow artifacts when making a durable claim.

The verifier runs the GitHub-hosted runner's `gh` binary. The template records
its version and refuses a CLI missing any strict verification flag, but it does
not pin or independently attest that runner image or CLI binary. Treat the
hosted runner and GitHub CLI distribution as explicit provider trust
dependencies; a deployment needing a stronger toolchain supply-chain claim
needs a separately reviewed, pinned verifier distribution.

## Explicit non-claims

This template does not prove:

- that the build was reproducible or free of malicious source/build behavior;
- that a release tag, registry tag, deployment target, or SBOM is correct;
- that its protected Environment reviewer is independent;
- that the GitHub-hosted verification runner is a hardware/VM trust root; or
- that the pilot itself has completed artifact-bound admission.
