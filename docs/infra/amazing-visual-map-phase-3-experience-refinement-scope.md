# amazing-visual-map Phase 3 — Experience Refinement and Productization Scope

**Date**: 2026-04-15
**Phase**: Phase 3 (Experience Refinement)
**Direction**: Bounded high-value refinement toward finished product feel
**Status**: Scope Definition

---

## 1. Phase Context

### 1.1 Completed Milestones
- **V1-V4**: Viewer Journey Surfaces A-F (129 tests)
- **Polish Phase 1**: Motion Language, Spatial Terrain, Feature Navigation (169 tests)
- **Phase 2**: Memory-Map Integration - Visual History, Memory Trail, Journey Guidance (194 tests)

### 1.2 Current State
- Feature navigation complete (region click → focus view)
- Narrative integrated with timeline
- Recommended Path adapts to state
- 194 tests passing, comprehensive coverage

### 1.3 Remaining Friction
- F10: Timeline waypoint click shows artifact, not feature (partial - works via region)
- Motion continuity across surface transitions could be smoother
- Spatial clarity could be stronger (regions still grid-positioned)
- Narrative quality could be more structured

---

## 2. Phase 3 Priorities

Per user direction, Phase 3 focuses on:

| Priority | Description | Bounded Scope |
|----------|-------------|---------------|
| P1 | Motion and continuity across surfaces | Cross-surface transition smoothness |
| P2 | Stronger map fidelity and spatial clarity | Visual clustering, connection visibility |
| P3 | Better guided journey / narrative quality | Structured narrative sections |

---

## 3. Derived Features

### Feature 016: Cross-Surface Motion Continuity

**Goal**: Ensure smooth motion feel when navigating between surfaces (project → terrain → focus → timeline).

**Scope**:
- Surface transition indicator (visual breadcrumb trail)
- Smooth panel transitions (focus panel open/close)
- Context preservation across navigation
- Motion timing consistency

**Anti-Regression**:
- NOT generic page transition animation
- NOT loading spinners or progress bars
- Preserve map metaphor (movement = journey)

**Tests**: ~10 tests
- Surface transition has visual indicator
- Focus panel has consistent animation timing
- Navigation preserves context
- Back navigation works with motion feel

---

### Feature 017: Spatial Clarity Enhancement

**Goal**: Strengthen map fidelity - make terrain regions feel more spatially arranged, not grid-boxes.

**Scope**:
- Visual clustering indication (feature groups have subtle clustering)
- Connection path visibility (relationship lines visible, not implied)
- Proximity indication (related regions visually closer)
- Depth/shadow hierarchy for spatial layering

**Anti-Regression**:
- NOT force-directed layout algorithm (complexity too high)
- NOT D3/canvas rendering (CSS-only approach maintained)
- NOT interactive drag-to-rearrange (user need unclear)
- Preserve CSS-only performance

**Tests**: ~12 tests
- Related features have proximity styling
- Connection paths visible between regions
- Regions have depth hierarchy (shadow variation)
- Clustering visual present (subtle grouping)

---

### Feature 018: Structured Narrative Quality

**Goal**: Improve narrative quality from simple text to structured story.

**Scope**:
- Narrative sections: beginning, milestones, current state, recommended next
- Milestone highlighting (first run, completion, blocked events)
- Current state summary (concise, actionable)
- Recommended next step (specific, not generic)

**Anti-Regression**:
- NOT verbose paragraph narrative
- NOT generic progress report style
- Preserve story-like feel
- Keep narrative integrated, not separate panel

**Tests**: ~10 tests
- Narrative has multiple sections
- Milestones highlighted in narrative
- Current state concise and actionable
- Recommended next specific to feature context

---

## 4. Bounded Scope Summary

| Feature | Focus | Tests | Priority |
|---------|-------|-------|----------|
| 016 | Cross-Surface Motion Continuity | ~10 | P1 |
| 017 | Spatial Clarity Enhancement | ~12 | P2 |
| 018 | Structured Narrative Quality | ~10 | P3 |

**Total**: ~32 new tests → ~226 tests expected

---

## 5. Constraints (Verbatim from User)

- Preserve north-star identity
- Preserve map metaphor
- Preserve anti-dashboard direction
- Prefer coherent refinement over feature sprawl
- Keep canonical loop running with low interruption

---

## 6. Diminishing Returns Threshold

**STOP Phase 3 if**:
- Motion additions feel jarring or gratuitous
- Spatial additions require canvas/D3 (complexity threshold)
- Narrative additions feel verbose or bureaucratic
- Tests not adding meaningful coverage
- Dogfood shows no perceptible UX improvement

**CONTINUE to Phase 4 only if**:
- Clear perceptible product feel improvement
- User feedback shows genuine value
- Remaining friction has bounded solution

---

## 7. Implementation Order

1. Feature 016 (Motion Continuity) - foundation for feel
2. Feature 017 (Spatial Clarity) - visual map fidelity
3. Feature 018 (Narrative Quality) - guided journey feel
4. Full test suite run
5. Dogfood and friction capture
6. Assessment: Phase 4 vs diminishing returns

---

## 8. Expected Outcome

Phase 3 should make amazing-visual-map feel:
- Smooth across navigation transitions
- More map-like in spatial arrangement
- More story-aware in narrative guidance

**Goal**: "Finished product experience, not just completed feature set."