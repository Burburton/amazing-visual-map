# amazing-visual-map — Product North Star, Experience Vision, Skill Map, and Canonical Loop Roadmap

## Document Control
- Project: `amazing-visual-map`
- Document Type: `Foundational Mother Document / Long-Horizon Product Definition`
- Intended Use: `Canonical source for async-dev canonical loop planning, feature decomposition, skill alignment, and long-term product evolution`
- Primary Audience: `async-dev / OpenCode execution loop, architect role, product-definer role, UX/visual design roles, reviewer/auditor roles`
- Status: `Foundational Draft`
- Language: `English-oriented product naming with Chinese explanation for execution clarity`

---

# 1. Executive Summary

`amazing-visual-map` is a **local-first project memory and visual map workspace** for async-dev style repositories and canonical-loop-driven projects.

It is **not** a conventional admin dashboard, static document browser, or issue list UI.

It is intended to become a **map-like project observatory** where a user can:
- understand current project state,
- see how the project evolved over time,
- explore the relationships between features, specs, issues, decisions, audits, and artifacts,
- discover what matters now,
- receive guidance on the most reasonable next action,
- and gradually experience the project as a **navigable memory landscape** rather than a pile of files.

This product must serve **two goals at the same time**:

1. **Practical Product Goal**  
   Build a genuinely useful local-first tool that reads async-dev project outputs and helps the user inspect, understand, and act on project state.

2. **Canonical Loop Validation Goal**  
   Serve as a medium-sized, long-horizon product that async-dev can continuously iterate on, using the canonical loop to improve:
   - product definition,
   - information architecture,
   - interaction design,
   - visual storytelling,
   - engineering execution,
   - audit quality,
   - and dogfooding feedback loops.

The product direction should strongly emphasize a **map metaphor**:
- project as terrain,
- project history as routes,
- issues as friction zones,
- feature clusters as regions,
- loop progress as movement,
- decisions as landmarks,
- next actions as trails or guided routes.

This metaphor is not decorative only. It must meaningfully shape product structure, navigation patterns, and visual identity.

---

# 2. Product North Star

## 2.1 North Star Statement

Build `amazing-visual-map` into a **local-first map-based project memory workspace** that transforms async-dev repository outputs into a navigable, story-aware, interaction-rich visual system for understanding and steering ongoing product evolution.

## 2.2 North Star User Outcome

When a user opens `amazing-visual-map`, they should quickly feel:
- “I understand where this project currently stands.”
- “I can see how we got here.”
- “I can identify what is blocked, drifting, unfinished, or high priority.”
- “I can explore the project naturally instead of manually hunting through files.”
- “This feels like entering a living project map, not opening a dead dashboard.”
- “This system helps me think about the next move.”

## 2.3 North Star Product Outcome

The product should progressively become:
- useful enough for regular dogfooding,
- structured enough for reliable canonical-loop execution,
- expressive enough to support interaction design iteration,
- visually distinct enough to avoid generic dashboard failure,
- extensible enough to support future multi-repo and cross-project memory evolution.

---

# 3. Why This Project Exists

## 3.1 Current Pain

Async-dev style project development generates many artifacts:
- specs,
- task breakdowns,
- implementation records,
- audits,
- reports,
- issue discussions,
- feedback documents,
- roadmap fragments,
- and evolving governance files.

These artifacts are valuable, but they tend to become:
- scattered,
- repetitive,
- hard to mentally organize,
- difficult to inspect quickly,
- and poor at communicating project shape and momentum.

The current failure mode is often:
- high documentation volume,
- low situational clarity,
- weak cross-artifact perception,
- hard-to-see drift,
- hard-to-sense project narrative.

## 3.2 The Opportunity

A map-oriented memory product can turn these artifacts into something more legible:
- a project territory,
- a sequence of journeys,
- a field of decisions,
- a set of regions and dependencies,
- an observable living system.

## 3.3 Why It Fits Canonical Loop

This project is ideal for canonical-loop-driven development because it can sustain many rounds of:
- product research,
- design exploration,
- data modeling,
- implementation,
- audit,
- dogfood feedback,
- redesign,
- and refinement.

It is not a one-off implementation target. It is a **long-run evolution surface**.

---

# 4. Product Definition

## 4.1 Product Category

`amazing-visual-map` should be treated as a:

- **local-first web application**,
- **project observatory**,
- **memory atlas**,
- **narrative workspace**,
- and **canonical loop testbed**.

## 4.2 Product Form

Recommended initial form:
- independent repository,
- local-first web app,
- browser-based UI,
- lightweight local backend or local parsing service,
- input is repo data / generated artifacts / project docs / structured outputs,
- no requirement for cloud dependency in V1.

## 4.3 What It Is Not

It is explicitly **not**:
- a generic admin dashboard,
- a boring file browser,
- a static markdown viewer,
- a GitHub clone,
- an issue tracker clone,
- a documentation portal,
- a “data table first” management console,
- a pure graph visualization toy with little utility.

## 4.4 Core Product Promise

The product promise is:

> Turn project artifacts into a navigable map of project memory, project state, project relationships, and project momentum.

---

# 5. Product Positioning Language

Use this language consistently in product definition, design reviews, and canonical-loop planning:

## 5.1 Preferred Positioning Terms
- `Project Observatory`
- `Memory Atlas`
- `Visual Map Workspace`
- `Narrative Project Map`
- `Local-First Project Memory`
- `Loop Inspection Workspace`
- `Project Terrain`
- `Decision Landmarks`
- `Guided Route to Next Action`

## 5.2 Language to Avoid
Avoid framing the product as:
- `dashboard`
- `management backend`
- `admin console`
- `file viewer`
- `doc portal`
- `status table`
- `issue board clone`

These terms tend to pull implementation toward generic and low-identity solutions.

---

# 6. Core Experience Vision

## 6.1 Experience Goal

The user should feel like they are entering a **living map of a project**, not reading a pile of system outputs.

The experience should progressively communicate:
- current position,
- movement history,
- unresolved terrain,
- regions of activity,
- risky zones,
- important landmarks,
- and possible next routes.

## 6.2 Desired Experience Qualities

The product should feel:
- spatial,
- layered,
- exploratory,
- readable,
- calm but intelligent,
- slightly cinematic,
- informative without being rigid,
- dynamic without being noisy,
- distinctive without becoming unusable.

## 6.3 Story-Aware Interface Principle

The interface should not simply state facts. It should help reveal:
- where the project came from,
- what forces shaped it,
- where work concentrated,
- where drift emerged,
- and what route forward is plausible.

Story here does **not** mean fictional decoration. It means:
- sequence,
- causality,
- turning points,
- dependencies,
- tension,
- and change over time.

---

# 7. Map Metaphor as Structural Product Principle

The map metaphor should guide product evolution deeply.

## 7.1 Mapping Concepts
Possible internal metaphor alignment:
- `project` → world / territory
- `feature group` → region / district / biome
- `feature detail` → site / zone / node
- `decision` → landmark
- `issue` → hazard / friction zone / fault line
- `audit finding` → warning signal / terrain instability
- `timeline` → trail / route / expedition history
- `next action` → recommended path / waypoint
- `health summary` → climate / atmosphere / system signal
- `repo relationship` → connected territory / linked maps

## 7.2 Constraints
The metaphor must:
- improve comprehension,
- support navigation,
- strengthen memory,
- and avoid becoming gimmicky.

The metaphor must not:
- obscure actual information,
- reduce usability,
- slow down core project inspection,
- or become a heavy fantasy layer disconnected from utility.

## 7.3 Product Rule
Every map-inspired design choice should answer:
- What user understanding does this improve?
- What navigation or comprehension problem does this solve?
- How does this remain practical for repeated dogfooding?

---

# 8. Long-Horizon Product Tracks

To support long-term canonical-loop iteration, the project must run across multiple product tracks in parallel.

## 8.1 Track A — Core Data and Memory Infrastructure
Focus:
- repo scanning,
- parsing,
- schema extraction,
- data contracts,
- state aggregation,
- cross-artifact linking,
- event/timeline model,
- caching and indexing,
- watch/update model.

Purpose:
- make the product genuinely usable,
- ensure stable foundations for long-term evolution.

## 8.2 Track B — Product Experience and Interaction
Focus:
- navigation models,
- page flow,
- focus view,
- overview-to-detail transitions,
- search and exploration patterns,
- next-action guidance,
- project journey presentation,
- route-based interaction design.

Purpose:
- avoid dead dashboard behavior,
- make complexity easier to understand.

## 8.3 Track C — Visual Language and Narrative Design
Focus:
- layout rhythm,
- motion language,
- spatial depth,
- atmosphere,
- state signaling,
- typography hierarchy,
- empty/loading states,
- visual storytelling mechanisms,
- map-inspired identity.

Purpose:
- create a distinct, memorable, evolving product language.

## 8.4 Track D — Design Research and Experience Experiments
Focus:
- concept variants,
- research questions,
- visual concept studies,
- comparative interaction experiments,
- design review findings,
- controlled redesign cycles.

Purpose:
- ensure the product keeps innovating without random drift.

## 8.5 Track E — Dogfood, Review, and Governance
Focus:
- experience audits,
- canonical loop feedback capture,
- usability friction logging,
- consistency review,
- audit severity frameworks,
- long-run maintainability rules.

Purpose:
- keep the product grounded and improve the development operating system itself.

---

# 9. Primary User Scenarios

## 9.1 Scenario A — Re-entering a Project Quickly
User wants to reopen a project and answer:
- Where are we now?
- What changed recently?
- What is incomplete?
- What is risky?
- What should happen next?

## 9.2 Scenario B — Understanding How a Project Evolved
User wants to understand:
- What features were built in what sequence?
- What decisions changed direction?
- Which issues caused churn or rework?
- How did audits reshape implementation?

## 9.3 Scenario C — Inspecting a Specific Feature in Context
User wants to inspect one feature and see:
- summary,
- state,
- linked specs,
- tasks,
- implementation progress,
- audit findings,
- related issues,
- downstream effects,
- current recommendation.

## 9.4 Scenario D — Discovering Structural Problems
User wants to sense:
- documentation drift,
- unresolved blocker concentration,
- repeated audit failures,
- orphan specs,
- stale features,
- misaligned reports.

## 9.5 Scenario E — Using the Product as a Project Steering Tool
User wants help deciding:
- what to prioritize next,
- what needs cleanup,
- what is missing in the current loop,
- and what route forward is best supported by current state.

---

# 10. Non-Goals for Early Phases

To preserve focus, the following should not be primary goals in early phases:
- full cloud sync,
- multi-user collaboration,
- enterprise permission systems,
- external platform integrations at large scale,
- giant real-time graph engine optimization,
- mobile-first adaptation,
- over-generalized support for all possible repository structures,
- “perfect universal project ontology” before practical dogfooding.

The early product must optimize for:
- one user,
- local usage,
- one or a few known repo structures,
- fast dogfood iteration,
- visible improvement per loop.

---

# 11. Experience Principles

These principles should guide all feature planning and design review.

## 11.1 Not a Backend
The UI must not collapse into a generic backend pattern by default.

## 11.2 Meaning Before Density
More information is not automatically better. Information must support understanding.

## 11.3 Spatial Over Flat When Helpful
When relationships matter, prefer spatial or structural expression over flat list-only presentation.

## 11.4 Narrative Where Sequence Matters
When time, causality, and turning points matter, use narrative structure rather than disconnected status summaries.

## 11.5 Progressive Disclosure
Do not overwhelm users on entry. Reveal depth gradually.

## 11.6 Guidance Without Rigidity
The product should suggest likely next steps without locking the user into a narrow flow.

## 11.7 Atmosphere Must Support Utility
Visual mood and cinematic polish are welcome only if they improve focus, clarity, and memory.

## 11.8 Identity Through System, Not Decoration
Distinctiveness should emerge from layout logic, motion logic, information expression, and metaphor discipline, not from random visual effects.

## 11.9 Dogfoodability Is Mandatory
A beautiful feature that does not help real project inspection should not be treated as successful.

## 11.10 The Map Must Stay Trustworthy
The user must feel that the map reflects real project state, not a stylized illusion disconnected from source data.

---

# 12. Anti-Patterns and Failure Modes

The project must actively guard against the following:

## 12.1 Generic Dashboard Drift
Symptoms:
- too many cards,
- too many summary numbers,
- weak navigational meaning,
- no sense of space or route.

## 12.2 Over-Stylized Uselessness
Symptoms:
- impressive visuals,
- poor legibility,
- unclear actions,
- weak repeat-use value.

## 12.3 Graph Toy Syndrome
Symptoms:
- fancy network visualization,
- little task relevance,
- low interpretability,
- no guidance.

## 12.4 File Browser Regression
Symptoms:
- product becomes mostly a tree of docs and markdown preview panes.

## 12.5 Storytelling Without Operational Value
Symptoms:
- product feels themed,
- but cannot actually help inspect, prioritize, or act.

## 12.6 Feature Pile Without Identity
Symptoms:
- many useful functions,
- no coherent experience language,
- product feels assembled rather than designed.

## 12.7 Design Research Without Product Constraint
Symptoms:
- endless concept exploration,
- little convergence,
- low practical progress.

---

# 13. Foundational Information Model Direction

This section defines a directional information model. It does not lock final schemas yet, but gives canonical loop planning a clear conceptual target.

## 13.1 Key Entities
Expected core entities may include:
- Project
- Repository
- Feature
- Spec
- Task Group
- Task Item
- Implementation Batch / Run
- Audit
- Audit Finding
- Report
- Decision
- Issue / Risk / Blocker
- Artifact
- Loop Run
- Milestone
- Link / Relationship
- Suggested Next Action
- Timeline Event

## 13.2 Relationship Direction
The product should ultimately be able to express relationships such as:
- feature ↔ spec
- feature ↔ task group
- feature ↔ audit
- feature ↔ issue
- issue ↔ audit finding
- decision ↔ timeline event
- report ↔ implementation batch
- project ↔ active route / next action
- repo ↔ region / cluster / related territory

## 13.3 State Model Direction
State should not be binary only. It may require richer semantics such as:
- active,
- stable,
- exploratory,
- blocked,
- drifting,
- incomplete,
- under review,
- needs consolidation,
- archived,
- high-risk,
- uncertain.

## 13.4 Time Model Direction
Time should support:
- recent changes,
- historical route,
- sequence of feature development,
- turning points,
- state transitions,
- staleness signals,
- and narrative summaries.

---

# 14. Core Product Surfaces

The product should evolve around a set of major surfaces.

## 14.1 Surface A — Observatory Home
Purpose:
- answer “where are we now?”
- show current project pulse,
- recent movement,
- active regions,
- risk signals,
- next action guidance.

This should not be a static KPI dashboard.

## 14.2 Surface B — Project Map / Terrain View
Purpose:
- present feature clusters,
- relationships,
- regions of activity,
- friction zones,
- landmarks,
- map-oriented exploration.

## 14.3 Surface C — Journey / Timeline View
Purpose:
- show how the project evolved,
- reveal major routes, detours, rework, and milestones,
- highlight turning points and decisions.

## 14.4 Surface D — Focus View
Purpose:
- inspect one feature, issue, audit, decision, or route in depth,
- provide context, state, linked artifacts, and recommended action.

## 14.5 Surface E — Narrative Briefing Mode
Purpose:
- give guided summaries such as:
  - “what happened recently,”
  - “what matters now,”
  - “what path forward is recommended.”

## 14.6 Surface F — Search / Route Discovery
Purpose:
- help users locate entities,
- discover relations,
- jump into meaningful project context,
- and navigate by intent rather than file name only.

---

# 15. Design Direction Framework

To keep the UI from becoming conventional, all design work should align with a structured design direction framework.

## 15.1 Primary Experience Tone
Target tone should combine:
- clarity,
- depth,
- motion restraint,
- map-like spatial intelligence,
- subtle drama,
- and a sense of living project memory.

## 15.2 Recommended Composite Style Direction
Primary direction:
- `Observatory + Memory Atlas`

Secondary direction:
- `Narrative Workspace`

Meaning:
- overall product behaves like an observatory and memory atlas,
- some key flows use guided narrative presentation.

## 15.3 Visual Themes to Explore
Potential themes to investigate through controlled experiments:
- terrain-inspired layered cartography,
- dark observatory mode with signal accents,
- minimal atmospheric system view,
- archive-meets-future interface language,
- project weather / climate cues,
- route and waypoint guidance metaphors,
- softly animated depth layers.

## 15.4 Motion Direction
Motion should express:
- traversal,
- route continuity,
- state transition,
- region reveal,
- focus shift,
- and depth.

Avoid motion that is merely decorative.

## 15.5 Interaction Priorities
Prioritize:
- focus transitions,
- map exploration,
- progressive reveal,
- contextual detail panels,
- guided exploration,
- and high-quality empty/loading states.

---

# 16. Design Research Operating Model

Design innovation must be made executable for canonical loop.

## 16.1 Every Design-Related Feature Should Include
- problem statement,
- target user understanding outcome,
- interaction hypothesis,
- visual hypothesis,
- alternatives considered,
- rationale for chosen direction,
- explicit anti-goals,
- validation criteria,
- future follow-up questions.

## 16.2 Design Research Questions Should Be Formalized
Examples:
- Should current-state understanding begin with summary, terrain, or story?
- Is a timeline better expressed as route, clustered events, or layered eras?
- How should warnings appear without collapsing the tone into alarm-fatigue?
- How can next actions feel like navigation rather than commands?
- How spatial should the map become before it harms clarity?
- What level of motion best conveys living state without distraction?

## 16.3 Controlled Exploration Rule
Design exploration is allowed and encouraged, but each experiment must be tied to a real product problem.

---

# 17. Skill Map

To support long-term canonical loop execution, `amazing-visual-map` requires both execution skills and design-research skills.

## 17.1 Core Execution Skills

### A. Product Architect
Responsibilities:
- define product boundary,
- structure roadmap,
- connect product vision to feature decomposition,
- keep product coherent over time.

### B. Information Architect / Memory Model Designer
Responsibilities:
- define entities,
- define relationships,
- define hierarchy,
- define route from source data to usable product structures.

### C. Repo Parser / Data Contract Engineer
Responsibilities:
- scan repo structures,
- parse artifacts,
- normalize source data,
- maintain stable contracts between repo output and UI layers.

### D. Frontend Experience Engineer
Responsibilities:
- implement high-fidelity UI,
- support motion and transitions,
- maintain component architecture,
- preserve performance and maintainability.

### E. Quality Reviewer / Test Strategist
Responsibilities:
- verify correctness,
- validate interaction behavior,
- ensure features are testable,
- ensure product remains usable under real conditions.

### F. Governance / Consistency Auditor
Responsibilities:
- ensure feature reports match actual implementation,
- track drift,
- audit product consistency,
- enforce documentation truthfulness.

## 17.2 Design Research Skills

### G. UX Interaction Researcher
Responsibilities:
- design user flows,
- propose interaction models,
- reduce friction,
- optimize understanding.

### H. Visual Narrative Designer
Responsibilities:
- develop map-like visual identity,
- create storytelling UI patterns,
- shape emotional and atmospheric quality,
- prevent UI genericness.

### I. Motion Language Designer
Responsibilities:
- define motion principles,
- design transitions,
- use animation to communicate structure and change.

### J. Design Critic
Responsibilities:
- identify dashboard drift,
- identify generic design shortcuts,
- challenge weak experience choices,
- push for conceptual clarity.

### K. Storytelling UI Reviewer
Responsibilities:
- assess whether sequence, causality, change, and guidance are truly expressed,
- prevent “theme only” storytelling.

### L. Dogfood Workflow Evaluator
Responsibilities:
- use the product during real project work,
- capture friction,
- generate grounded follow-up improvements.

## 17.3 Optional Future Skills
- Map Systems Designer
- Search & Discovery Designer
- Visual Systems Curator
- Cross-Repo Knowledge Mapper
- Product Briefing Writer

---

# 18. Skill Packaging Strategy

For async-dev compatibility, skill packaging should eventually separate into:

## 18.1 Foundation Skills
Used often, close to implementation:
- product-architect
- memory-model-designer
- parser-engineer
- frontend-experience-engineer
- test-reviewer
- governance-auditor

## 18.2 Experience Design Skills
Used for stronger design rounds:
- ux-interaction-researcher
- visual-narrative-designer
- motion-language-designer
- design-critic
- storytelling-ui-reviewer

## 18.3 Dogfood and Review Skills
Used for feedback loops:
- dogfood-workflow-evaluator
- experience-auditor
- consistency-reviewer

## 18.4 Suggested Rule
No major UX-facing feature should be executed with engineering skills only.  
At minimum, any high-visibility product surface should involve:
- product architect,
- UX interaction researcher,
- visual narrative designer,
- frontend experience engineer,
- reviewer/auditor.

---

# 19. Canonical Loop Fit

`amazing-visual-map` should be explicitly developed as a canonical-loop-native project.

## 19.1 Why It Fits the Loop
It can continuously produce:
- clear feature specs,
- manageable implementation batches,
- auditable outcomes,
- design review loops,
- dogfood findings,
- and roadmap-driven follow-up work.

## 19.2 What the Loop Should Improve Over Time
The loop should improve not only the product, but also:
- spec quality,
- design articulation quality,
- review rigor,
- feedback capture quality,
- and how async-dev handles design-heavy products.

## 19.3 Loop Cadence Philosophy
Use many medium or small rounds rather than giant redesign waves.

Each round should ideally produce one of:
- a foundational capability,
- a meaningful experience upgrade,
- a design-language improvement,
- a narrative exploration,
- or a governance-quality improvement.

---

# 20. Feature Type System for Long-Term Roadmap

To prevent backlog monotony, roadmap planning should use multiple feature categories.

## 20.1 Core Capability Features
Examples:
- repo scan pipeline,
- parser normalization,
- state aggregation,
- timeline model,
- link resolver.

## 20.2 Product Experience Features
Examples:
- observatory home redesign,
- route-based navigation,
- focus view architecture,
- contextual recommendation surfaces.

## 20.3 Design Language Features
Examples:
- motion system,
- visual hierarchy system,
- map layer design language,
- state signal semantics.

## 20.4 Narrative / Experimental Features
Examples:
- project journey mode,
- briefing mode,
- narrative summaries,
- decision-landmark system,
- guided route prototype.

## 20.5 Quality / Governance Features
Examples:
- experience audit rubric,
- data contract validation,
- report consistency enforcement,
- design review checklist,
- dogfood friction registry.

## 20.6 Research Features
Examples:
- compare three timeline metaphors,
- evaluate two map interaction models,
- test different next-action paradigms.

---

# 21. Roadmap Philosophy

The roadmap should evolve in phases, with each phase deepening both utility and design identity.

## 21.1 Phase 0 — Vision and Constraint Locking
Purpose:
- lock product definition,
- lock non-goals,
- lock experience principles,
- lock skill map,
- lock map metaphor rules,
- define first design direction shortlist.

## 21.2 Phase 1 — Foundation and Data Truth
Purpose:
- build repo reading pipeline,
- establish source contracts,
- create minimal usable product model,
- ensure data is trustworthy.

## 21.3 Phase 2 — First Usable Observatory
Purpose:
- build first real user-facing experience,
- provide current-state understanding,
- enable feature and timeline inspection,
- support repeated dogfooding.

## 21.4 Phase 3 — Map Identity and Narrative Structure
Purpose:
- move beyond utility,
- make the product recognizably map-based,
- strengthen route/history/landmark concepts.

## 21.5 Phase 4 — Design System and Motion Language
Purpose:
- build consistency,
- deepen product polish,
- make the product feel intentionally designed.

## 21.6 Phase 5 — Guided Intelligence and Steering Support
Purpose:
- help the user decide what to do next,
- summarize project risk and momentum,
- support project steering workflows.

## 21.7 Phase 6 — Multi-Repo and Knowledge Expansion
Purpose:
- support broader territory mapping,
- cross-repo relationships,
- more ambitious project memory views.

---

# 22. Early Candidate Capability Clusters

These are not yet final feature IDs, but likely backlog clusters.

## 22.1 Foundation Cluster
- local repo input model
- artifact parser contracts
- feature/spec/task/audit extraction
- timeline event extraction
- issue/risk model
- source indexing and cache

## 22.2 Observatory Cluster
- home pulse summary
- current-state region summary
- active work map
- risk/health signal layer
- recommended next action module

## 22.3 Map Cluster
- region model
- cluster/group view
- node/link view
- landmark model
- route highlight system

## 22.4 Journey Cluster
- historical trail view
- milestone summary
- turning point display
- rework and drift visibility

## 22.5 Focus Cluster
- feature detail page
- issue detail page
- audit detail page
- decision detail page
- linked artifact context panels

## 22.6 Narrative Cluster
- guided project briefing
- recent changes storyline
- why-this-matters summary mode
- recommended route explanation

## 22.7 Design Language Cluster
- visual identity v1
- motion language v1
- typography hierarchy v1
- color/state semantics v1
- map-layer composition rules

## 22.8 Governance Cluster
- experience audit rubric
- consistency checks
- design anti-pattern checks
- dogfood capture template

---

# 23. Expected Canonical Deliverables Per Major Feature

To support strong loop execution, major features should produce consistent deliverables.

## 23.1 For Product / Capability Features
- feature spec,
- architecture notes,
- implementation,
- test coverage or validation plan,
- completion report,
- follow-up issues.

## 23.2 For Experience / Design Features
- problem statement,
- interaction goals,
- concept rationale,
- design alternatives,
- implemented prototype or UI changes,
- experience review notes,
- follow-up questions.

## 23.3 For Research Features
- research question,
- compared concepts,
- evaluation notes,
- selected direction,
- implications for next features.

## 23.4 For Governance / Audit Features
- audit rubric,
- findings,
- severity mapping,
- remediation items,
- consistency report.

---

# 24. Review and Audit Framework Direction

Because this project is design-heavy, audits must include more than implementation correctness.

## 24.1 Required Audit Dimensions
Every major UX-facing feature should be reviewable across:
- product alignment,
- data truthfulness,
- information clarity,
- interaction quality,
- visual coherence,
- map-metaphor appropriateness,
- dogfood utility,
- maintainability.

## 24.2 Example Review Questions
- Does this feature help users understand the project faster?
- Does this page drift toward a generic backend pattern?
- Does the visual design have structure or only styling?
- Is the map metaphor meaningful here or just superficial?
- Does the feature help with repeated real use?
- Does the source data remain inspectable and trustworthy?
- Are states and signals semantically clear?

## 24.3 Severity Direction
Possible severity examples:
- blocker: misleading state or unusable core flow
- major: generic drift, broken interaction logic, severe clarity failure
- medium: weak hierarchy, inconsistent narrative expression, partial map misuse
- minor: polish gaps, incomplete motion consistency, secondary visual mismatch

---

# 25. Dogfooding Strategy

`amazing-visual-map` should not be treated as a portfolio demo only. It must be used repeatedly with real project artifacts.

## 25.1 Dogfood Questions
Regular dogfooding should ask:
- Did this help me re-enter the project faster?
- Did this help me notice something I would have missed in raw files?
- Did the recommended next action feel useful or generic?
- Did the interface help me think, or only display?
- Which parts felt alive and helpful, and which parts still felt like a backend?

## 25.2 Dogfood Outputs
Dogfooding should generate:
- friction logs,
- missed insight logs,
- design confusion notes,
- stale interaction notes,
- next-iteration suggestions.

## 25.3 Rule
No phase should be considered mature if it has not been used on at least one real project flow.

---

# 26. Technical Direction (High-Level)

## 26.1 Recommended Initial Product Form
- independent repository,
- local-first web app,
- modern frontend stack,
- small local backend / parser service,
- file-based input contract from async-dev repos.

## 26.2 Directional Stack Preference
This document does not fully lock the stack, but the preferred direction is:
- frontend capable of rich interaction and motion,
- local backend capable of reading/parsing project artifacts,
- architecture suitable for iterative visual product development,
- easy local dogfood setup.

## 26.3 Architectural Boundary Rule
`amazing-visual-map` should depend on async-dev through **observable outputs and data contracts**, not deep runtime coupling.

Meaning:
- it reads artifacts,
- it reads project structures,
- it consumes canonical outputs,
- but it is not embedded into async-dev internals.

This preserves independence and makes the product healthier.

---

# 27. Canonical Constraints for Early Implementation

## 27.1 Constraint A — Local-First
Assume local usage first.

## 27.2 Constraint B — Truth Before Flair
Fancy visual systems are welcome, but source truth and comprehension come first.

## 27.3 Constraint C — One Clear Experience Upgrade Per Round
Each loop should have a concrete experience win, not just background refactoring forever.

## 27.4 Constraint D — Repeated Dogfoodability
If a design is too exotic to use repeatedly, it is not a good direction.

## 27.5 Constraint E — Map Identity Must Be Earned
Do not fake the map identity with decoration. Build it through structure, relationships, movement, and navigation logic.

---

# 28. Suggested Initial Canonical Follow-Up Documents

This mother document should be followed by a document stack.

## 28.1 Immediate Follow-Up Doc A
`amazing-visual-map-v1-foundation-spec.md`

Purpose:
- define first executable product scope,
- lock V1 boundaries,
- define initial repo input contract,
- identify first core surfaces.

## 28.2 Immediate Follow-Up Doc B
`amazing-visual-map-skill-pack-plan.md`

Purpose:
- define which skills should be created/adapted first,
- map each skill to async-dev workflow roles,
- define expected responsibilities and inputs/outputs.

## 28.3 Immediate Follow-Up Doc C
`amazing-visual-map-experience-language-and-design-principles.md`

Purpose:
- deepen interaction and visual language,
- define anti-generic rules,
- define map-metaphor usage boundaries,
- define early narrative UX guidelines.

## 28.4 Immediate Follow-Up Doc D
`amazing-visual-map-phase-1-feature-roadmap.md`

Purpose:
- sequence the first feature wave,
- organize work by canonical-loop-friendly batches,
- balance foundation, UI, and design exploration.

## 28.5 Immediate Follow-Up Doc E
`amazing-visual-map-experience-audit-rubric.md`

Purpose:
- define how design-heavy features are reviewed,
- prevent dashboard drift,
- improve consistency and truthfulness.

---

# 29. First Recommended Execution Order

Recommended next-step sequence after this mother document:

1. create and lock the V1 foundation spec,
2. define the initial skill pack plan,
3. define the experience language and design rules,
4. decompose the first phase roadmap,
5. start implementing the first foundational features,
6. establish the first experience audit loop,
7. dogfood on a real project repository,
8. use findings to shape the second wave.

---

# 30. Explicit Instructions for async-dev / Canonical Loop Usage

Use this document as the canonical top-layer source for:
- product identity,
- experience direction,
- skill alignment,
- roadmap philosophy,
- and anti-pattern prevention.

When creating downstream specs, they must remain consistent with the following mandatory requirements:

## 30.1 Mandatory Requirement Set
- The product must remain local-first in early phases.
- The product must remain independent from async-dev internals.
- The product must use map-like thinking structurally, not superficially.
- The product must avoid generic backend/dashboard regression.
- The product must support long-term canonical-loop iteration.
- UX and visual design are first-class product concerns, not decoration work.
- Design research must be tied to real product problems.
- Dogfooding is required for maturity.

## 30.2 Rule for Downstream Feature Specs
Any downstream feature spec must explicitly state:
- which product track it belongs to,
- which user scenario it serves,
- which experience principle it supports,
- which anti-pattern it is preventing or at risk of triggering,
- which skills are required,
- and how it will be validated.

---

# 31. Definition of Success

`amazing-visual-map` is succeeding when:
- it is actually used to inspect real project state,
- users can understand project state faster than by reading raw artifacts,
- project history and relationships become more legible,
- the UI has a distinct and coherent identity,
- the product does not regress into a standard dashboard,
- canonical loop can keep generating meaningful next work,
- design iteration becomes structured and cumulative rather than random,
- and the product helps improve async-dev itself.

---

# 32. Final Strategic Statement

`amazing-visual-map` should be treated not as a side viewer, but as a **map-shaped product for navigating project memory and project evolution**.

Its importance is larger than the UI itself.

If done well, it becomes:
- a useful product,
- a canonical-loop training ground,
- a design-heavy async-dev proving ground,
- and a visible example that async-dev can do more than produce documents and backend-style utilities.

This project should therefore be developed with both seriousness and creative ambition.

---

# 12. Autonomous Canonical Loop Execution Policy

This section upgrades this mother document from a product north-star artifact into an autonomous execution constitution. The goal is to allow amazing-async-dev to continue development with low human interruption while remaining aligned with the core identity of amazing-visual-map.

## 12.1 Policy Intent

amazing-visual-map should not depend on frequent human-authored downstream specs for every iteration. Instead, the canonical loop should derive executable scopes, implementation plans, quality checks, and follow-up iterations from this mother document unless an explicit escalation condition is triggered.

This policy exists to ensure that:
- the project can evolve continuously under canonical loop control;
- the product does not regress into a generic admin/dashboard implementation;
- interaction design, visual identity, and narrative exploration remain first-class concerns;
- the system can autonomously narrow scope into coherent, testable iterations;
- human involvement is reserved for genuinely high-leverage product decisions.

## 12.2 Constitutional Role of This Document

This mother document must be treated as both:

1. the canonical product north-star document;
2. the canonical autonomous execution constitution.

All downstream artifacts must remain compatible with this document unless a formal deviation is explicitly raised and approved.

## 12.3 Default Autonomy Rule

Unless an escalation condition is triggered, amazing-async-dev should proceed without waiting for repeated human confirmation.

The system should:
- derive the first executable foundation spec from this mother document;
- generate downstream planning and implementation artifacts as needed;
- continue through the canonical loop with low interruption;
- prefer small, coherent, reviewable increments over broad speculative builds;
- preserve product identity even when early scope must remain small.

## 12.4 Mandatory Self-Derivation Responsibilities

When running under this mother document, amazing-async-dev is expected to perform the following autonomously:

### A. Derive an Initial Executable Scope
The system must derive a V1 foundation scope that is:
- small enough to be realistically implemented and audited;
- large enough to demonstrate real product identity;
- consistent with local-first, independent-repo, map-like, and narrative-aware principles;
- suitable for dogfooding.

### B. Produce Downstream Execution Artifacts
The system may generate, maintain, and update downstream artifacts such as:
- foundation specs;
- task breakdowns;
- implementation plans;
- audit documents;
- repair plans;
- dogfood reports;
- next-iteration proposals;
- design research notes;
- experience review documents.

### C. Choose Scope by Product Identity Preservation
When multiple scope options are available, the system must choose the smallest coherent scope that still preserves the identity of amazing-visual-map.

This means the chosen first version must not strip away all of the following at once:
- map-like thinking;
- interaction design intent;
- narrative or guided understanding;
- meaningful project-memory interpretation.

### D. Continue Iteratively
After each implementation and audit cycle, the system should continue by deriving the next justified iteration rather than waiting for a new human-written master prompt.

## 12.5 Scope Selection Heuristics

When deriving the first and subsequent iterations, the system should prioritize work using the following order:

1. preserve product identity;
2. maintain coherent information architecture;
3. ensure real data grounding from async-dev project artifacts;
4. enable reviewable user-visible progress;
5. improve comprehension before expanding breadth;
6. delay abstraction and platformization until clearly justified.

The system should prefer:
- one strong product surface over many shallow surfaces;
- one understandable interaction flow over many disconnected panels;
- one real narrative/observatory experience over a large but generic feature set.

## 12.6 Hard Anti-Regression Rules

The system must not silently regress amazing-visual-map into any of the following:
- a generic admin dashboard;
- a conventional issue tracker clone;
- a plain file browser with decorative map language;
- a metrics-only control panel;
- a document index UI with superficial styling;
- a speculative platform with weak dogfooding value.

More specifically, the system must not use the following implementation logic:
- “build a normal dashboard first, add identity later”;
- “ship plain CRUD first, design can wait”;
- “defer narrative/interaction thinking until after core engineering”;
- “replace map-like structure with simple sidebar/table layouts unless absolutely required by V1 survival.”

If a compromise is necessary, the system must preserve at least one visible and credible aspect of the intended product identity in the current iteration.

## 12.7 Design Research as a First-Class Loop Track

Design research is not optional polish work. It is part of the canonical loop.

The system should continuously explore:
- better project-state visualization patterns;
- map-like navigation structures;
- narrative modes of understanding progress and change;
- visual metaphors for memory, history, drift, and tension;
- transitions and motion that reinforce system evolution;
- interaction patterns that reduce cognitive overload.

However, design exploration must remain controlled. Each design-oriented iteration should be tied to a concrete product question, such as:
- how to improve project-state comprehension;
- how to make decision history easier to follow;
- how to reduce information pressure on the home surface;
- how to make next recommended actions feel more guided and contextual.

## 12.8 Required Balance Between Product Tracks

The canonical loop should not only generate engineering work. It should maintain a balanced portfolio across these tracks:
- core capability;
- information architecture;
- interaction/product experience;
- visual language and narrative design;
- quality/governance;
- dogfooding and feedback capture.

A long sequence of purely parser/backend/internal work without meaningful user-visible product progress should be treated as drift and corrected.

Likewise, a long sequence of purely visual redesign work without stronger real project understanding should also be treated as drift.

## 12.9 Human Escalation Boundaries

Human escalation should be rare and used only for decisions with substantial directional impact.

The system should escalate when one or more of the following is true:
- the core product metaphor must change materially;
- the project may shift from local-first web workspace toward a different product category;
- two or more major design directions are equally strong but imply clearly different long-term identities;
- a major architecture shift is required;
- external dependency cost, hosting assumptions, or system boundaries change substantially;
- the intended user model changes materially;
- downstream work would invalidate a major principle in this mother document.

The system should not escalate merely because:
- there are multiple plausible small-scope options;
- a design decision is not perfect;
- the first iteration cannot include every desirable concept;
- a local optimization choice must be made;
- an incremental compromise is needed to keep progress moving.

## 12.10 Default Output Expectation for Autonomous Runs

When operating under this policy, amazing-async-dev should leave behind a clear paper trail that supports later audit and dogfooding. At minimum, autonomous execution should produce artifacts that make the following understandable:
- what was chosen for the current iteration;
- why that scope was selected;
- what was intentionally deferred;
- how the current work preserves product identity;
- what user-visible progress was achieved;
- what product/design/quality questions remain open;
- what the next justified iteration is.

## 12.11 Low-Interruption Iteration Doctrine

The preferred operating mode is low interruption, not no governance.

This means:
- the system should keep moving unless blocked by a true constitutional decision;
- it should record assumptions instead of constantly asking for confirmation;
- it should make reversible choices autonomously;
- it should leave behind enough rationale for later correction;
- it should optimize for learning velocity without breaking product identity.

## 12.12 First-Step Instruction Under This Policy

Immediately after receiving this mother document, the canonical loop should:
1. derive the first executable foundation scope;
2. generate the minimum downstream execution artifacts needed to begin work;
3. implement the first coherent version without waiting for unnecessary human prompts;
4. audit the result against both functional and experience goals;
5. propose and continue into the next justified iteration unless an escalation condition is triggered.

## 12.13 Mother-Document Priority Rule

If any downstream artifact conflicts with this mother document, this mother document wins unless a formal, explicit, human-approved deviation is recorded.

This rule exists to protect the long-term identity of amazing-visual-map from gradual regression into convenience-driven but lower-value forms.

