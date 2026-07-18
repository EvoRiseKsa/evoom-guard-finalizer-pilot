# Static workflow-security audit

`EvoGuard Static Workflow Security` is a deliberately narrow complementary
control for the trusted-finalizer pilot. It is **not** a finalizer, an
admission decision, a release gate, or proof that a workflow is secure.

## Execution boundary

The workflow uses `pull_request_target` only so that its implementation comes
from protected `main`. It accepts open, same-repository pull requests targeting
the default branch. It does not check out the PR, execute its code, read a
repository or Environment secret, upload SARIF, or receive write permissions.

Instead, the base-owned `github-script` step asks GitHub's Git API for the
exact current PR-head tree and writes only bounded workflow and local-action
YAML blobs into a disposable snapshot. Symlinks, a truncated tree, more than
64 inputs, a blob over 512 KiB, or more than 2 MiB total fail closed.
`actionlint` receives only candidate workflow files because it validates
workflow syntax; `zizmor` receives the read-only snapshot and collects both
workflows and composite actions. Their containers have no network or Linux
capabilities and constrained CPU, memory, process, and temporary-storage
budgets. Before either analyzer prints candidate-controlled parser output, the
workflow temporarily disables GitHub workflow-command processing.

The candidate's `.github/zizmor.yml` is neither mounted nor honored. The
workflow fetches the baseline policy from the protected base workflow SHA and
passes it explicitly, so a candidate cannot disable an audit by editing its
own config. It also rejects a candidate workflow that contains a zizmor
inline-ignore directive. The workflow therefore does not rely on a
candidate-supplied suppression rule.

## Pinned analysis inputs

- Official `actionlint` OCI image `v1.7.12`, pinned to
  `sha256:b1934ee5f1c509618f2508e6eb47ee0d3520686341fec936f3b79331f9315667`
  (upstream source tag commit
  `914e7df21a07ef503a81201c76d2b11c789d3fca`).
- Official `zizmor` OCI image `v1.27.0`, pinned to
  `sha256:5800c8d5e83263d68a8874989b0eb3939e177540e9395de48158d24656141ee9`
  (upstream source tag commit
  `e2627367eb7c917a90503ce05a66872fd91da6fb`).
- `actions/github-script` pinned to
  `3a2844b7e9c422d3c10d287c895573f7108da1b3` (`v9.0.0`).

The workflow runs zizmor offline with strict collection and the regular
persona. It does not contact GitHub from the analyzer or trust a candidate
configuration file.

## Reviewed exception

`.github/zizmor.yml` contains two line-specific `dangerous-triggers`
exceptions: `evoguard-seal.yml:8` and
`evoguard-static-security.yml:10`. `workflow_run` and
`pull_request_target` are inherently high-risk triggers, so these exceptions
are not claims that either is generally safe. The former is necessary for the
pilot's separated sealing flow and is constrained by the configured numeric
workflow ID, an immutable pre-candidate control record, raw-Git re-derivation,
no candidate checkout, and Environment-gated key access. The latter is the
base-owned data-only audit described above: it has read-only permissions,
does not check out a PR, and never executes candidate bytes. Moving either
line restores the finding and requires review.

No audit is disabled globally. New workflow/action files and new locations in
existing files remain subject to the active rules.

## Rollout and interpretation

This check starts as advisory; it is not made a required branch-protection
context in the same maintenance change. After the maintenance change is merged
and protections are restored, a deliberately unmerged, comment-only change to
this static workflow should demonstrate that the base-owned audit runs on the
candidate bytes while the finalizer rejects the protected-harness edit. Record
that exercise before considering the check for branch protection.
