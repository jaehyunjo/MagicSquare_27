# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_XX |
| **기준 AC** | AC-FR-01-01 (ST-01 / TC-011 계열) |
| **테스트 스위트** | `tests/unit/boundary/test_ac_fr_01_01_invalid_size.py` |
| **마지막 실행** | `.venv` + `scripts/run-coverage.ps1` |
| **실행 결과** | 12 collected, **12 failed** (RED) |
| **관련 문서** | [docs/TP-ST01-TC011-001.md](docs/TP-ST01-TC011-001.md), [Report/03.MagicSquare_PRD_Report.md](Report/03.MagicSquare_PRD_Report.md) §8.1 |

---

## 결함 요약

| Severity | 건수 | 설명 |
|----------|------|------|
| **Critical** | 2 | Boundary·Control 핵심 API 미구현으로 AC-FR-01-01 전 테스트 실패 |
| **Major** | 1 | PRD 계약 코드(`INPUT_DIMENSION_MISMATCH`)와 테스트 기대(`INVALID_SIZE`) 불일치 |

---

## 결함 상세

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| **DEF-001** | Critical | AC-FR-01-01 | 1. `.venv` 활성화 2. `pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -v` 3. `grid = None`으로 `validate_grid_input(grid)` 호출 (`test_none_grid_returns_invalid_size_and_message`) | `ValidationFailure(code="INVALID_SIZE", message="Grid must be 4x4.")` 반환 | `NotImplementedError`: `RED: validate_grid_input not implemented` | `src/magicsquare/boundary/validation.py`에 RED 스텁만 존재; `grid is None` 분기·차원 검증 로직 없음 | `validate_grid_input`에 None/빈 입력 거부 구현; `INVALID_SIZE` + PRD 메시지 반환 |
| **DEF-002** | Critical | AC-FR-01-01 | 1. 동일 pytest 실행 2. `grid = []` 또는 `grid = [[]]*4` 또는 `grid = [[1,2,3,4]]*3`로 `validate_grid_input(grid)` (`test_boundary_shape_*`, `test_empty_list_*`, `test_three_by_four_*`, `test_scope_*`) | 각 입력마다 `ValidationFailure`, `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | 동일 `NotImplementedError` (DEF-001과 동일 스텁) | 4×4 row-major 16튜플 성립 전 검증 없음; 빈 리스트·행/열 불일치 처리 누락 | 길이 0·행≠4·열≠4·빈 행 검사 후 동일 `ValidationFailure` 반환 |
| **DEF-003** | Critical | AC-FR-01-01 | 1. `grid = None`, `resolve` mock/spy 주입 2. `verify_magic_square(grid, resolve=resolve_spy)` (`test_none_grid_orchestrator_resolve_zero_calls`, `test_none_grid_resolve_called_fails_isolation`) | `ValidationFailure(INVALID_SIZE)`; `resolve_spy.assert_not_called()` | `NotImplementedError`: `RED: verify_magic_square not implemented` | `src/magicsquare/control/orchestrator.py` RED 스텁; Boundary 조기 종료·Domain 격리 미구현 | `verify_magic_square`에서 `validate_grid_input` 호출 → 실패 시 즉시 반환, `resolve` 미호출 |
| **DEF-004** | Critical | AC-FR-01-01 | 1. `grid = None` 2. `patch("magicsquare.domain.resolver.resolve")` 후 `validate_grid_input(grid)` only (`test_none_grid_boundary_resolve_zero_calls`) | Boundary만으로 실패 반환; `resolve` 0회 | `NotImplementedError` (DEF-001) — Boundary 단계에서 예외로 중단 | DEF-001 해결 시 Boundary 경로는 Domain 미진입 자동 충족; Control(DEF-003)과 회귀 확인 | DEF-001 구현 후 spy 0회 재검증 |
| **DEF-005** | Major | AC-FR-01-01 | 1. [Report/03](Report/03.MagicSquare_PRD_Report.md) §8.1 표 확인 2. 테스트 `INVALID_SIZE_CODE`·README RED To-Do와 대조 | PRD §8.1: `InputError` + `INPUT_DIMENSION_MISMATCH` (빈·길이 0·차원 불일치) | 테스트·README: `INVALID_SIZE` + `"Grid must be 4x4."` | spec(TC-011)과 제품 README/테스트 계약 명칭 분기; green 전 코드·문서 정합 필요 | 팀 합의 후 (A) PRD 코드로 테스트/README 정렬 또는 (B) PRD·TC 문서에 `INVALID_SIZE` alias 명시 |

---

## 실패 테스트 ↔ 결함 매핑

| pytest 테스트 ID | 결함 ID |
|------------------|---------|
| `test_none_grid_returns_invalid_size_and_message` | DEF-001 |
| `test_none_grid_exact_message_prd_section_81_wording` | DEF-001 |
| `test_none_grid_returns_validation_failure_model_type` | DEF-001 |
| `test_boundary_shape_returns_invalid_size_failure[empty_list]` | DEF-002 |
| `test_boundary_shape_returns_invalid_size_failure[four_empty_rows]` | DEF-002 |
| `test_boundary_shape_returns_invalid_size_failure[three_by_four]` | DEF-002 |
| `test_empty_list_returns_invalid_size_code` | DEF-002 |
| `test_three_by_four_returns_invalid_size_code` | DEF-002 |
| `test_none_grid_orchestrator_resolve_zero_calls` | DEF-003 |
| `test_none_grid_boundary_resolve_zero_calls` | DEF-004 |
| `test_none_grid_resolve_called_fails_isolation` | DEF-003 |
| `test_scope_only_invalid_size_not_other_ac_codes` | DEF-002 |

---

## 수정 우선순위 (green 제안)

1. **DEF-005** — 계약 명칭 합의 (구현 전 1회)
2. **DEF-001** + **DEF-002** — `validate_grid_input` 구현
3. **DEF-003** — `verify_magic_square` 오케스트레이션
4. **DEF-004** — DEF-001·003 완료 후 격리 테스트 재실행

**완료 기준:** `pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py` 12 passed; README «모든 결함 수정 후 회귀 테스트 통과» 체크.

---

## 변경 이력

| 날짜 | 작성 | 비고 |
|------|------|------|
| 2026-05-29 | QA 리드 | RED 12건 실패 기준 최초 등록 |
