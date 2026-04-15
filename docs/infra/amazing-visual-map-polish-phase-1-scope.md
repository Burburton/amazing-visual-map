# Amazing Visual Map Polish Phase 1 — Motion, Spatial, Navigation

## Document Control
- Project: `amazing-visual-map`
- Document Type: `Polish Scope Specification`
- Derived From: `V3/V4 Friction Logs`
- Purpose: `Enhance viewer continuity, spatial identity, and cross-surface navigation`
- Status: `Active`
- Autonomous Execution: `Enabled`

---

## 1. Derivation Rationale

Polish Phase 1 addresses friction from V3/V4 dogfood:
- **F03, F04**: Static display, no motion language for transitions
- **F05**: Terrain uses simple grid, not true spatial positioning
- **F07**: No quick way to jump between related features in focus view
- **F08**: Narrative text-only, not integrated with visual timeline

### 1.1 Polish Goals

| Goal | Friction Addressed | Outcome |
|------|-------------------|---------|
| Motion Language | F03, F04 | Transitions feel continuous and intentional |
| Spatial Terrain | F05 | Terrain looks like a map, not a grid |
| Feature Navigation | F07, F08 | Cross-surface movement is coherent |

### 1.2 Anti-Regression Check

Polish must NOT:
- ❌ Add generic dashboard transitions (fade/slide only)
- ❌ Make terrain into canvas-heavy visualization
- ❌ Add conventional navigation breadcrumbs

Polish must:
- ✅ Motion expresses map metaphor (approaching, departing, traversing)
- ✅ Spatial positioning reflects relationships (proximity = relatedness)
- ✅ Navigation feels like journey between territories

---

## 2. Polish Scope Definition

### 2.1 Included Features

| Feature ID | Name | Purpose |
|------------|------|---------|
| 010 | motion-language | CSS transitions expressing movement metaphor |
| 011 | spatial-terrain | Relationship-based positioning, visual terrain |
| 012 | feature-navigation | Cross-surface journey navigation |

### 2.2 Intentionally Deferred

| Item | Reason |
|------|--------|
| Canvas rendering | Over-engineering for V1 polish |
| Animation library | CSS transitions sufficient |
| Full spec parsing | Not polish, is feature enhancement |

---

## 3. Feature 010 — Motion Language

### 3.1 Goal
Add CSS transitions that express map metaphor: approaching regions, departing views, traversing surfaces.

### 3.2 Acceptance Criteria
- AC1: Focus panel opens with "approach" transition (scale/slide)
- AC2: Focus panel closes with "depart" transition
- AC3: Terrain regions highlight on hover with "proximity" effect
- AC4: Timeline waypoints pulse on hover (movement indicator)
- AC5: Project selector buttons transition with "territory switch" feel
- AC6: Search results appear with "discovery" fade-in
- AC7: Status indicators animate state changes
- AC8: No generic fade/slide — transitions express metaphor

### 3.3 Map Metaphor Expression
- **Approach**: Coming closer to a region (scale up, slide in)
- **Depart**: Leaving a region (scale down, slide out)
- **Proximity**: Hovering near a region (glow, border intensify)
- **Traversal**: Moving between surfaces (directional slide)
- **Discovery**: Finding something (reveal, fade-in)

### 3.4 Implementation Notes
- CSS transitions on focus panel (transform, opacity)
- Hover effects on terrain regions (border, shadow)
- Timeline waypoint pulse animation
- Search result staggered fade-in
- Use CSS keyframes for pulsing

---

## 4. Feature 011 — Spatial Terrain

### 4.1 Goal
Position terrain regions based on relationships, not simple grid. Add visual terrain elements (paths, clusters).

### 4.2 Acceptance Criteria
- AC1: Regions positioned by relationship proximity (related = closer)
- AC2: Paths/lines connect related regions
- AC3: Region clusters visually grouped
- AC4: Terrain background has subtle texture/gradient
- AC5: Regions have visual boundaries (not just boxes)
- AC6: Hover shows region connections
- AC7: Not a flat grid — feels like a territory map
- AC8: Performance acceptable (no heavy canvas)

### 4.3 Map Metaphor Expression
- **Position**: Proximity reflects relatedness
- **Paths**: Connections between regions (roads/trails)
- **Clusters**: Feature groups (districts)
- **Terrain**: Background texture (ground/landscape)

### 4.4 Implementation Notes
- Calculate positions from connections (simple force-directed or clustering)
- CSS for paths (SVG lines or border trick)
- Background gradient for terrain feel
- Region styling: rounded, shadowed, bordered

---

## 5. Feature 012 — Feature Navigation

### 5.1 Goal
Enable coherent cross-surface navigation: from terrain → focus → related features → timeline → back.

### 5.2 Acceptance Criteria
- AC1: Focus view shows "Related Features" section
- AC2: Click related feature → navigate to its focus view
- AC3: Navigation breadcrumbs show current location
- AC4: Back button returns to previous surface (terrain/timeline)
- AC5: Timeline waypoint click → opens focus for that feature
- AC6: Search result click → opens focus view
- AC7: Navigation feels like journey, not tab switching
- AC8: Location context preserved across navigation

### 5.3 Map Metaphor Expression
- **Journey**: Moving between territories
- **Path**: Navigation trail through surfaces
- **Landmarks**: Current location breadcrumbs
- **Return**: Backtracking to previous territory

### 5.4 Implementation Notes
- Add related features section in focus response
- Track navigation history (simple JS array)
- Breadcrumbs UI in focus panel header
- Wire clicks to focus navigation
- Preserve project context across navigation

---

## 6. Implementation Order

1. Feature 010 (motion-language) — Enhance feel immediately
2. Feature 011 (spatial-terrain) — Strengthen identity
3. Feature 012 (feature-navigation) — Complete journey

Each → spec → implementation → tests → commit → continue

---

## 7. Dogfood Validation

Polish Phase 1 must:
- Transitions feel intentional, not generic
- Terrain looks like a map, not a grid
- Navigation feels like journey, not tabs
- Performance remains good
- Map metaphor preserved

---

## 8. Success Criteria

Polish Phase 1 succeeds when:
- Motion language functional (transitions express metaphor)
- Spatial terrain enhanced (positioning, paths)
- Feature navigation functional (cross-surface movement)
- Viewer feels more continuous and alive
- No regression into generic dashboard
- Dogfood shows improved experience