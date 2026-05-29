# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **기준 AC** | AC-FR-01-01 (ST-01 / TC-011 계열) |
| **테스트 스위트** | `tests/unit/boundary/test_ac_fr_01_01_invalid_size.py` |
| **마지막 실행** | `.venv` + `pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py` |
| **실행 결과** | 13 collected, **13 passed** (GREEN + refactor regression) |
| **관련 문서** | [docs/TP-ST01-TC011-001.md](docs/TP-ST01-TC011-001.md), [Report/16](Report/16.MagicSquare_REFACTOR_Plan_Report.md) |

---

## 결함 요약

| Severity | 건수 | 설명 |
|----------|------|------|
| **Critical** | 0 | DEF-001~004 종결 (AC-FR-01-01 GREEN) |
| **Major** | 1 | DEF-005 open — `INVALID_SIZE` vs `INPUT_DIMENSION_MISMATCH` (Phase B green) |

---

## 종결 결함 (DEF-001 ~ DEF-004)

| ID | 상태 | 비고 |
|----|------|------|
| **DEF-001** | ✅ 종결 | `grid=None` → `INVALID_SIZE` |
| **DEF-002** | ✅ 종결 | `[]`, 3×4, `[[]]*4` → `INVALID_SIZE` |
| **DEF-003** | ✅ 종결 | `verify_magic_square` 조기 반환, `resolve` 미호출 |
| **DEF-004** | ✅ 종결 | Boundary 단독 경로 Domain 미진입 |

---

## 미결 결함

| ID | Severity | AC ID | 설명 | 수정 방향 |
|----|----------|-------|------|-----------|
| **DEF-005** | Major | AC-FR-01-01 | PRD `InputError` + `INPUT_DIMENSION_MISMATCH` vs 테스트 `INVALID_SIZE` | Phase B: `test_tc008_*` 등 green 후 계약 통일 ([Report/16](Report/16.MagicSquare_REFACTOR_Plan_Report.md) WP-8) |

---

## 변경 이력

| 날짜 | 작성 | 비고 |
|------|------|------|
| 2026-05-29 | QA 리드 | RED 12건 실패 기준 최초 등록 |
| 2026-05-29 | REFACTOR | DEF-001~004 종결; AC-FR 13 passed (inject validate test 추가) |
