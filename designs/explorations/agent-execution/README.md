# Agent execution exploration

Status: **NON-BINDING EXPLORATION**. Preserved discussion, not an implementation plan.

- [Architecture notes and research references](architecture-notes.md): roles, shared events, SDK mappings, execution outcomes, capabilities and a verifier extension example.
- [Candidate file structure](candidate-file-structure.md): full historical candidate inventory with per-path status.
- [Interactive Atlas](../../atlas/index.html): choose Explorations; zoom into agents, execution, adapters and events; open Reviewer run.

Open decisions: smallest useful event contract; unsupported capability behavior; native control hooks versus observations; role-specific results; transport for Codex; where deterministic evidence belongs. Claude/Codex parity must be demonstrated per required capability, never assumed from a common interface. No harness implementation is approved here.
