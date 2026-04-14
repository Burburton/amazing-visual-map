# V1 Dogfood Friction Log

## Session Info
- Date: 2026-04-15
- Repo: amazing-async-dev
- Scanner Version: V1
- Artifacts Found: 55

---

## Friction Categories

### A. Data Quality Issues

| ID | Issue | Severity | Evidence | Impact |
|----|-------|----------|----------|--------|
| F01 | Multiple runstate.md across projects | MEDIUM | 4 runstate files found, unclear which is "current" | Observatory confusion |
| F02 | Parse failures in exec-results | LOW | 2 failed/partial: exec-live-test-001, exec-018-batch-operations | Data gaps |
| F03 | Inconsistent artifact naming | LOW | Some exec-results named exec-018-* not exec-YYYYMMDD-* | Date extraction fails |

### B. Missing Capabilities

| ID | Issue | Severity | Evidence | Impact |
|----|-------|----------|----------|--------|
| F04 | No project-level grouping | HIGH | All 55 artifacts mixed together, no project filter in output | Can't distinguish projects |
| F05 | Feature ↔ exec-pack relationship missing | MEDIUM | feature_id exists in metadata but not in relationships | No feature traceability |
| F06 | No timeline visualization | HIGH | Mother document specifies "trail/route" metaphor | V1 missing core experience |
| F07 | No map/terrain view | HIGH | Mother document core metaphor | V1 missing core identity |
| F08 | No search/discovery | MEDIUM | Mother document Surface F | Deferred to V2 |

### C. UX/Experience Issues

| ID | Issue | Severity | Evidence | Impact |
|----|-------|----------|----------|--------|
| F09 | Observatory UI not verified | HIGH | HTML exists but not tested with real data | Unknown real UX |
| F10 | No cross-project navigation | MEDIUM | Multiple projects detected but no way to switch | Limited exploration |

### D. Mother Document Alignment

| ID | Issue | Severity | Evidence | Impact |
|----|-------|----------|----------|--------|
| F11 | Section 14.2 Surface B missing | HIGH | "Project Map / Terrain View" not implemented | Major identity gap |
| F12 | Section 14.3 Surface C missing | HIGH | "Journey / Timeline View" not implemented | Core narrative missing |
| F13 | Section 14.4 Surface D missing | MEDIUM | "Focus View" not implemented | Detail inspection gap |
| F14 | Map metaphor expression limited | MEDIUM | Regions/trail/path-hint exist but minimal | Identity preservation OK |

---

## Positive Findings

| ID | Finding | Evidence |
|----|---------|----------|
| P01 | Scanner works on real repo | 55 artifacts found, 53 parsed successfully |
| P02 | Feature extraction works | 17 feature specs detected |
| P03 | Date extraction from exec-YYYYMMDD works | Recent activity correctly sorted |
| P04 | Relationships for exec-pack ↔ exec-result work | Basic linking functional |
| P05 | Dark theme preserved | HTML contains observatory dark colors |
| P06 | No table/card-grid regression | Tests verify anti-patterns avoided |

---

## V2 Scope Derivation

From friction analysis, V2 should address:

### Priority 1 (HIGH friction → immediate)
1. **Feature 004**: Project-level grouping and filtering
2. **Feature 005**: Timeline/Trail visualization (Surface C)
3. **Feature 006**: Terrain/Map view (Surface B)

### Priority 2 (MEDIUM friction → next iteration)
4. **Feature 007**: Focus View (Surface D)
5. **Feature 008**: Feature ↔ exec-pack relationship extraction
6. **Feature 009**: Cross-project navigation

### Priority 3 (Polish)
7. **Feature 010**: Search/Discovery (Surface F)
8. **Feature 011**: Parse failure recovery

---

## Recommendation

**V2 Focus**: Complete the core map experience (Surface B + C)

Mother document Sections 14.2-14.3 define the core identity:
- Project Map / Terrain View (Surface B)
- Journey / Timeline View (Surface C)

V1 provided foundation (scanner, model, observatory home). V2 must deliver the **map identity** that mother document defines as core.

**V2 Scope**: 3 features (004-006) delivering the core map metaphor.

---

## Escalation Check

Per Section 12.9, check escalation conditions:
- Core product metaphor change? NO (still map/observatory)
- Major architecture shift? NO
- Conflicting major design directions? NO
- External dependency cost change? NO
- User model change? NO

**No escalation required. Proceed to V2 derivation autonomously.**