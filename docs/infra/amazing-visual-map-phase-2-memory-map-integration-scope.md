# amazing-visual-map Phase 2 — Memory-Map Integration Scope

## Document Control
- Project: `amazing-visual-map`
- Document Type: `Phase 2 Scope Specification`
- Derived From: `Polish Phase 1 Assessment + North Star Section 12.7`
- Purpose: `Integrate narrative with visual timeline, enhance memory-map feeling`
- Status: `Active`
- Autonomous Execution: `Enabled`

---

## 1. Derivation Rationale

Phase 2 scope is derived from:
1. **F08**: Narrative text-only, not integrated with visual timeline
2. **North Star Section 12.7**: "visual metaphors for memory, history, drift, and tension"
3. **North Star Section 12.8**: Balance "visual language and narrative design"
4. **User directive**: "richer memory-map feeling across projects, features, and trails"

### 1.1 Why This Is Not Diminishing-Returns Polish

Polish Phase 1 addressed transitions and visual terrain styling. This is different:
- **Memory-Map Integration** adds a NEW interaction mode (timeline-narrative fusion)
- **Visual history** transforms how users perceive project evolution
- This is PRODUCT EXPERIENCE enhancement, not polish churn

### 1.2 Product Identity Preservation

| Check | Status |
|-------|--------|
| Map metaphor | ✅ History as trail/journey visualization |
| Narrative | ✅ Integrated with visual, not text-only |
| Interaction design | ✅ New cross-surface experience |
| Memory feeling | ✅ Project evolution as navigable landscape |

---

## 2. Phase 2 Scope Definition

### 2.1 Included Features

| Feature ID | Name | Purpose |
|------------|------|---------|
| 013 | visual-history | Timeline with embedded narrative waypoints |
| 014 | memory-trail | Project evolution as navigable journey trail |
| 015 | journey-guidance | Contextual guidance across surfaces |

### 2.2 Intentionally Deferred

| Item | Reason |
|------|--------|
| Force-directed positioning | Would require canvas, not CSS-first |
| Multi-repo support | Expansion, not memory enhancement |
| Full spec parsing | Data quality, not visual experience |

---

## 3. Feature 013 — Visual History

### 3.1 Goal
Embed narrative milestones directly on timeline waypoints, making history visual, not text-only.

### 3.2 Acceptance Criteria
- AC1: Timeline waypoints show narrative summaries (not just id/date)
- AC2: Hover waypoint reveals milestone story snippet
- AC3: Click waypoint shows full narrative in context
- AC4: Narrative integrated with timeline position (visual connection)
- AC5: Recent waypoints have motion indicator (pulse/glow)
- AC6: Timeline shows project state progression visually
- AC7: NOT flat text list - visual journey representation

### 3.3 Map Metaphor
- Timeline = Journey trail through project history
- Waypoints = Milestone markers with story
- Narrative = Story embedded in the landscape

---

## 4. Feature 014 — Memory Trail

### 4.1 Goal
Project evolution visualized as navigable trail with state progression markers.

### 4.2 Acceptance Criteria
- AC1: Memory trail shows state transitions (planning→executing→completed)
- AC2: Trail markers indicate phase boundaries
- AC3: Click trail segment focuses on that period
- AC4: Trail reflects actual project evolution from artifacts
- AC5: Memory trail uses journey metaphor, not progress bar
- AC6: Trail connects to timeline waypoints visually

### 4.3 Map Metaphor
- Memory trail = Route through project history
- Phase markers = Landmarks/waypoints
- State progression = Movement along route

---

## 5. Feature 015 — Journey Guidance

### 5.1 Goal
Contextual guidance that helps user understand where they are in the project journey.

### 5.2 Acceptance Criteria
- AC1: Each surface shows "You are here" location indicator
- AC2: Guidance adapts to current project state
- AC3: Suggested next journey step shown contextually
- AC4: Journey path indicator (surface connection visualization)
- AC5: Guidance feels like trail guide, not UI tooltip
- AC6: Cross-surface journey continuity maintained

### 5.3 Map Metaphor
- Journey guidance = Trail guide/path hint
- Location indicator = "You are here" on map
- Next step = Recommended trail segment

---

## 6. Implementation Strategy

**CSS-first, no canvas/D3.js**:
- Timeline waypoints with embedded narrative (CSS styling)
- Memory trail as visual timeline extension
- Journey guidance as contextual indicators

**Bounded scope**:
- 3 features, 30-40 tests
- Visual experience enhancement, not platform expansion

---

## 7. Escalation Check

Per Mother Document Section 12.9:
- Core product metaphor change? NO (enhancing existing metaphor)
- Major architecture shift? NO (CSS styling, no new backend)
- Conflicting directions? NO (memory-map aligned with North Star)
- External dependency? NO

**No escalation. Proceed to Phase 2 implementation autonomously.**

---

## 8. Success Criteria

Phase 2 succeeds when:
- Narrative visible on timeline waypoints (not text-only)
- Memory trail shows state progression visually
- Journey guidance contextual (not generic)
- Viewer feels like navigating project memory
- Map metaphor strengthened
- Tests comprehensive (200+)