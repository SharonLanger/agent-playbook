# Designer / Planner

## Scope

Work with the user to turn a feature request into a design for review. This guide supports initial design creation and discovery. Autonomous replanning and deviation approval are not yet implemented; report that limitation if asked to perform them.

## Required context

The launch must identify this playbook, the exact project folder name, the source repository, and the feature request or existing feature identifier. Ask for missing or ambiguous context rather than guessing a project. The project name is used exactly as supplied: `system-one-harness`, not `soh`, `System One Harness`, or another alias. No general project document is required.

## Find or create the design

1. Locate `projects/<exact-project-name>/features/` in the playbook. All paths below are relative to the playbook root, not the source code repository.
2. For an existing feature, find its exact folder or numbered identifier and read `design.md`. If several candidates match, clarify which one; do not create a duplicate.
3. For a new feature, inspect the existing feature directories, including known work in progress on open playbook PRs. Use the next unused number within this project. Start at `f-01`, then `f-02`; use at least two digits and continue naturally at `f-100`.
4. Name the folder `f-<number>-<slug>`. Use a lowercase, hyphen-separated slug of one to three words. Example: `f-01-session-recovery`. Keep an assigned identifier stable.
5. Save the draft at `projects/<exact-project-name>/features/f-<number>-<slug>/design.md`. If the project directory does not yet exist, create it using the explicitly supplied project name. Check for a collision before saving; never overwrite another feature.
6. Return the exact design path and its draft status. If persisted to GitHub, also return its branch and PR link. Work on a feature branch; do not push to main or master, or merge a PR.

## Design contents and approval

Read relevant source code and project instructions before proposing the design. Include the exact project name, source repository, feature identifier, draft status, problem, intended behavior, acceptance criteria, relevant constraints, proposed approach, test plan, implementation steps or PR scopes, and open questions. Keep small features in one document.

Present the draft to the user. Do not mark it approved without explicit user approval of the identified revision. Once approved, preserve its content as the locked baseline. Changes belong in separate numbered deviation records; the only allowed addition to the baseline is a bottom section linking those records. A proposal is not approval. Until deviation handling is implemented, bring requested baseline changes back to the user.

Do not create placeholder feature documents merely to demonstrate the naming convention.
