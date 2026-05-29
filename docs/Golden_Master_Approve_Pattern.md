# Golden Master Approve Pattern — Magic Square Solver (GM-1)

| 항목 | 값 |
|------|-----|
| **Task ID** | GM-1 |
| **Baseline file** | `tests/golden_master_expected.txt` |
| **Capture module** | `scripts/golden_master.py` |
| **Generator CLI** | `scripts/generate_golden_master.py` |
| **Regression tests** | `tests/test_golden_master_magic_square.py` |
| **pytest marker** | `@pytest.mark.golden_master` |
| **실행** | `pytest -m golden_master -v` |
| **Solver source** | `scripts/demo_solver.py` (small-first → reverse) |
| **작성일** | 2026-05-29 |

---

## 1. Purpose

Magic Square 2-blank Solver의 **결정적 출력**을 파일 기준선(Golden Master)으로 고정하고,  
구현 변경 시 **회귀(Approval)** 를 자동 검출한다.

- 출력 캡처 방식: **Result DTO serialize** (`SolverResultDTO` → 텍스트 블록)
- `stdout` 캡처는 사용하지 않음 (GUI/CLI 문구 변동과 분리)

---

## 2. Approve Pattern

```text
┌─────────────────┐     capture_all_scenarios()     ┌──────────────────┐
│  Live Solver    │ ──────────────────────────────► │  actual (text)   │
│  solve_two_step │                                 └────────┬─────────┘
└─────────────────┘                                          │
                                                             ▼
                    ┌────────────────────────────────────────────────────┐
                    │  baseline exists?                                  │
                    └────────────┬───────────────────────┬───────────────┘
                          NO     │                       │ YES
                                 ▼                       ▼
                    ┌────────────────────┐    ┌────────────────────────────┐
                    │ auto-write baseline│    │ actual == expected ?     │
                    │ (approve)          │    └──────┬─────────────┬───────┘
                    └────────────────────┘      YES  │             │ NO
                                                     ▼             ▼
                                                  PASS      unified diff
                                                            + FAIL
```

### 2.1 규칙

| 조건 | 동작 |
|------|------|
| `tests/golden_master_expected.txt` **없음** | 현재 출력으로 **자동 생성** 후 PASS |
| baseline **있음** | `actual` vs `expected` **전문 비교** |
| 불일치 | 시나리오별 **unified diff** 출력 후 `AssertionError` |
| 의도적 갱신 | `python scripts/generate_golden_master.py` 또는 `pytest --approve-golden` |

### 2.2 pytest 연동

```powershell
# 회귀 검증 (GM-2 marker)
pytest -m golden_master -v

# 기준선 재승인 (출력 의도적 변경 시)
pytest -m golden_master --approve-golden -v

# 기준 파일만 재생성
python scripts/generate_golden_master.py
```

`--approve-golden` 은 `tests/conftest.py` 의 `pytest_addoption` 으로 등록된다.

---

## 3. Baseline File Structure

각 시나리오는 `[scenario_id]` 헤더로 구분한다.

```text
[normal_success]
Input:
<4 rows, space-separated integers; 0 = blank>

Output:
[r1,c1,n1,r2,c2,n2]

[reverse_success]
Input:
...

Output:
[...]

[invalid_blank_count]
Input:
...

Error:
INVALID_BLANK_COUNT

[duplicate_number]
Input:
...

Error:
DUPLICATE_NUMBER

[no_valid_solution]
Input:
...

Error:
NO_VALID_SOLUTION
```

### 3.1 포맷 규칙

- **Input**: 4행 × 4열, 공백 구분, `0` = 빈칸
- **성공 Output**: 1-index `[r1,c1,n1,r2,c2,n2]`, 콤마 뒤 공백 없음
- **실패 Error**: 고정 코드 문자열 (메시지 전문 아님)

### 3.2 Error Code Mapping

| Solver 조건 | Golden Master 코드 |
|-------------|-------------------|
| 빈칸 ≠ 2 | `INVALID_BLANK_COUNT` |
| non-zero 중복 | `DUPLICATE_NUMBER` |
| small-first·reverse 모두 실패 | `NO_VALID_MAGIC_SQUARE` |

---

## 4. Input Scenarios

| Scenario ID | 의도 | Grid 출처 |
|-------------|------|-----------|
| `normal_success` | Step A (small-first) 성공 | Dürer partial, blanks (1,3)·(3,3) |
| `reverse_success` | Step A 실패 → Step B 성공 | SC-DOM-SOL-001 / G2 |
| `invalid_blank_count` | 빈칸 0개 (완성 격자) | G0 complete |
| `duplicate_number` | non-zero 중복 | G1 + `(2,4)=5` |
| `no_valid_solution` | 유효 입력, 해 없음 | brute-force 탐색 확정 격자 |

격자·기대 payload 는 `scripts/golden_master.py` 의 `SCENARIO_GRIDS` 에 고정한다.

---

## 5. Solver Strategy (Capture 대상)

` solve_two_step()` (`scripts/golden_master.py`):

1. `_parse_partial_grid()` — demo_solver 입력 검증
2. 누락 수 `{a,b}` (`a < b`)에 대해:
   - **small-first**: `(a → blank₁, b → blank₂)`
   - **reverse**: `(b → blank₁, a → blank₂)`
3. 각 시도 후 `_is_complete_magic()` (M=34)
4. 첫 성공 payload 반환; 둘 다 실패 시 `NO_VALID_SOLUTION`

blank 순서는 row-major 탐지 순서(`_parse_partial_grid` blanks 리스트)를 따른다.

---

## 6. Module Responsibilities

| 모듈 | 책임 |
|------|------|
| `scripts/golden_master.py` | DTO, capture, parse, diff, approve |
| `scripts/generate_golden_master.py` | baseline 파일 생성 CLI |
| `tests/test_golden_master_solver.py` | 전문·섹션·픽스처 회귀 |
| `tests/golden_master_expected.txt` | **버전 관리 대상** 기준선 |
| `scripts/demo_solver.py` | 검증·마방진 판정 (변경 없음) |

---

## 7. Version Control

기준 파일은 **반드시** git에 포함한다.

```powershell
git add tests/golden_master_expected.txt
git add scripts/golden_master.py scripts/generate_golden_master.py
git add tests/test_golden_master_solver.py docs/Golden_Master_Approve_Pattern.md
```

출력 변경이 의도적일 때만 `generate_golden_master.py` 또는 `--approve-golden` 으로  
baseline 을 갱신하고, PR 에 **왜 바뀌었는지**를 기록한다.

---

## 8. Limitations

- 프로덕션 `src/` Control `solution()` 미구현 — 현재는 **scripts 데모 솔버** 기준
- Dual-Track E002/E005 envelope 문자열과 Golden Master 코드는 **별 계층** (코드만 고정)
- `stdout` / GUI `format_solve_result()` 는 GM-1 범위 밖

---

*GM-1 완료 후 Track B `D-SOL` green 구현 시 동일 패턴으로 `src/` 솔버 출력을 전환할 수 있다.*
