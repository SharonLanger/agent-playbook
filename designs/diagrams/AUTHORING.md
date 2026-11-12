# Diagram authoring — project convention

Sharon adopted **Dashmotion** and **Animated SVG** for architecture explanations and learning
material. Use this policy for future stages as well as the system architecture. It persists
independently of disposable agent handoffs. Diagrams explain the approved design; they do not
change architecture decisions or authorize implementation.

## Which one to use

| Need | Use | Deliverable |
|---|---|---|
| Normal architecture, component boundaries, request/data paths | **Dashmotion, architecture mode** | Local HTML with inline animated SVG, plus static SVG for Markdown |
| Step order, branching, state transitions, one workflow's execution | **Dashmotion, flow mode** | Same format, with numbered explanations of inputs and outputs |
| Timed story, narrated/code walkthrough, sequence animation, pan/zoom through a large diagram | **Animated SVG** | Its supported HTML/video workflow, with a static diagram and readable text alternative |
| A small static relationship adequately explained in Markdown | Mermaid | A compact diagram; animation is optional when motion teaches nothing |

**Default to Dashmotion.** Use Animated SVG when teaching needs a controlled timeline, narration
or camera movement. Do not generate a video solely to decorate a simple diagram. Keep both
available as authoring references; neither belongs in the application's runtime dependencies.

## Verified sources

These are external skills, not bundled or automatically installed in this repository.
Read the actual SKILL.md and relevant references before using their tools. Fetch a pinned
revision into a separate authoring workspace; review changes before updating the reference.

- **Dashmotion**, `csthink/dashmotion`, reviewed version 2.2.4:
  [SKILL.md at ae2fe4f](https://github.com/csthink/dashmotion/blob/ae2fe4f28c60caa53da8b15fa3537f4ea576f4ad/skills/dashmotion/SKILL.md).
  MIT. Use its `scripts/layout.py` renderer and `scripts/check_diagram.py` checker.
- **Animated SVG**, `omkamal/animated-diagrams-skill`:
  [SKILL.md at 3de812d](https://github.com/omkamal/animated-diagrams-skill/blob/3de812d90c94baa4f9761684f36c3c322f1fb38c/SKILL.md).
  Apache-2.0. Follow its setup, rendering and contact-sheet checks when using its
  GSAP/HyperFrames pipeline; do not assume Node, Chrome or FFmpeg are installed.

Keep required notices for copied templates, code or assets. Fetching or reading instructions
is not an installation. Do not claim a skill's rendering pipeline was used unless it ran.

## Design and teaching rules

1. Establish the real nodes, boundaries, edges and outcomes from source or an explicitly
   labelled design proposal before drawing. Separate the shared application from each
   workflow's own flow/state/steps and tests.
2. Use consistent colors with text labels: ownership must remain clear without color.
   Include a legend where color means something. Keep text large enough to read.
3. Use movement to show direction or a particular execution path. A conditional diagram
   must not imply both exclusive branches execute. Label illustrative motion as such;
   it is not measured timing, a trace or evidence that the software works.
4. Explain what enters each step, what changes and what leaves it. State/history examples
   should match the workflow's documented test vectors exactly.
5. Keep architecture views focused. Put code walkthroughs and detailed scenarios in separate
   diagrams instead of making one enormous canvas.

## Delivery and verification

- Keep artifacts beside their owning design/lesson under `diagrams/`, with an `index.html`
  when there are several. Embed static SVGs in Markdown and link the animated HTML.
  GitHub source pages do not run HTML animations; open the local HTML in a browser.
- Local review viewers must work without a server, external fonts, CDN or network requests.
  Provide pause/resume, reduced-motion handling, accessible titles/descriptions and readable
  static fallbacks. For video, retain the companion text/static explanation.
- For Dashmotion, use the bundled layout tool when Python is available. Keep intermediate
  graph JSON outside delivered output. Run the bundled checker to **0 violations** after
  every final edit; use its mandated numeric review for labels/padding beyond checker coverage.
  Follow its verification instructions rather than substituting screenshot inspection.
- For Animated SVG, follow its separate render/contact-sheet workflow. A Dashmotion check
  is not a substitute for verifying a video timeline.
- Validate local links, SVG XML and inline JavaScript syntax where applicable. Record what
  actually ran and remaining limitations in the stage's findings. A structural pass is not
  evidence of application behavior or a claim that Sharon reviewed the visuals in PyCharm.
- Keep stage diagrams and their lessons permanently in `designs/stages/<stage>/`, including
  during design review. `designs/temporary/` is only for disposable agent handoffs; never
  remove stage diagrams during handoff cleanup. Keep this policy in its permanent location.
