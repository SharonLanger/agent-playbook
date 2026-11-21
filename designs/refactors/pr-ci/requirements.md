# Requirements

- R1. Run the repository's deterministic gate, Atlas freshness and installed-wheel verification on every PR targeting public main, including docs-only changes and updates. Keep local execution possible before publication. Avoid paid private runs.
- R2. Ordinary merges require a PR and successful checks. Sharon may explicitly bypass a failure through a PR. A second reviewer is unnecessary. Protect main from force pushes and deletion.
- R3. In a development checkout, support displaying the version and intentionally bumping patch, minor or major. Preserve local build, verification and selection of installed versions. Users can clone and build.
- R4. For each maintainer version, record the merged PR numbers and titles since the preceding version. Keep this human-readable and lightweight. Private local experiments do not require a GitHub account.
- R5. Preserve the personal examples exclusion, existing services, data, credentials and frozen contracts. No service-backed or end-to-end jobs. Defer distribution, tags and narrative release summaries.
