# Sources and evidence boundaries

Reviewed 2026-11-12. Framework references explain APIs; our workflow numbers, schemas, formulas,
CLI contract and file placement are project-specific design decisions.

- [CrewAI Flows](https://docs.crewai.com/v1.15.40/en/concepts/flows): start/listen, typed state, router and kickoff concepts. This is a documentation version, not a selected package pin.
- [CrewAI installation](https://docs.crewai.com/v1.15.40/en/installation): check the selected distribution against our interpreter before pinning.
- [CrewAI telemetry](https://docs.crewai.com/v1.15.40/en/telemetry): usage telemetry and AMP tracing are separate settings; validate disablement on the selected version.
- [uv lockfile export](https://docs.astral.sh/uv/concepts/projects/export/) and [CLI reference](https://docs.astral.sh/uv/reference/cli/): proposed locked production-dependency export; verify against the project's pinned uv 0.13.6.
- [Dashmotion source](https://github.com/csthink/dashmotion/tree/ae2fe4f28c60caa53da8b15fa3537f4ea576f4ad): renderer, templates and structural checker used for this package's diagrams. See diagrams/THIRD-PARTY-NOTICES.txt.
- [Animated SVG source](https://github.com/omkamal/animated-diagrams-skill/tree/3de812d90c94baa4f9761684f36c3c322f1fb38c): adopted companion for narrated, scrubbed/code walkthroughs. Its GSAP/HyperFrames pipeline is not installed or executed for this package.

Read [the permanent diagram policy](../../diagrams/AUTHORING.md) before future visual work.
Illustrative snippets are original lesson examples. They are not imported by the app, run as
tests, or certified against a selected CrewAI package. Implementation verification belongs
in findings after approval. Documentation generation scripts are not application implementation.
