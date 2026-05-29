# GM-2 Golden Master Test — 실행 결과 예시

| 항목 | 값 |
|------|-----|
| **Task ID** | GM-2 |
| **테스트 모듈** | `tests/test_golden_master_magic_square.py` |
| **기준 파일** | `tests/golden_master_expected.txt` |
| **마커** | `@pytest.mark.golden_master` |
| **실행** | `pytest -m golden_master -v` |

---

## PASS (16 selected)

```text
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-8.4.2, pluggy-1.6.0
rootdir: C:\DEV\MagicSquare_XX
configfile: pytest.ini
collecting ... collected 58 items / 42 deselected / 16 selected

tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareFile::test_gm2_full_baseline_approve PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_section_matches_baseline[GM-TC-01] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_section_matches_baseline[GM-TC-02] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_section_matches_baseline[GM-TC-03] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_section_matches_baseline[GM-TC-04] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_section_matches_baseline[GM-TC-05] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_input_grid_fixture[GM-TC-01] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_input_grid_fixture[GM-TC-02] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_input_grid_fixture[GM-TC-03] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_input_grid_fixture[GM-TC-04] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareCases::test_gm2_input_grid_fixture[GM-TC-05] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareContracts::test_gm2_solver_result_contract[contract-GM-TC-01] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareContracts::test_gm2_solver_result_contract[contract-GM-TC-02] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareContracts::test_gm2_solver_result_contract[contract-GM-TC-03] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareContracts::test_gm2_solver_result_contract[contract-GM-TC-04] PASSED
tests/test_golden_master_magic_square.py::TestGoldenMasterMagicSquareContracts::test_gm2_solver_result_contract[contract-GM-TC-05] PASSED

====================== 16 passed, 42 deselected in 0.62s ======================
```

---

## FAIL 예시 (unified diff)

기준선과 실제 출력이 다를 때 섹션 비교 테스트는 아래 형식으로 실패한다.

```text
E   Golden Master mismatch [GM-TC-01] 정상 조합 성공 (small-first):

E   --- [GM-TC-01] diff ---
E   --- expected
E   +++ actual
E   @@ -6,4 +6,4 @@
E
E    Output:
E   -[1,3,2,3,3,7]
E   +[1,3,2,3,3,9]
```

전문 비교(`test_gm2_full_baseline_approve`) 실패 시에는 문서 전체에 대해 동일한
`--- expected` / `+++ actual` / `@@` hunk 형식이 출력된다.

---

## 테스트 케이스 매핑

| Test ID | 시나리오 | 검증 |
|---------|----------|------|
| GM-TC-01 | 정상 조합 성공 | small-first Step A, int[6], 1-index, row-major |
| GM-TC-02 | reverse 조합 성공 | Step A 실패 → Step B, reverse 값 배치 |
| GM-TC-03 | `INVALID_BLANK_COUNT` | Error Contract |
| GM-TC-04 | `DUPLICATE_NUMBER` | Error Contract |
| GM-TC-05 | `NO_VALID_MAGIC_SQUARE` | both-fail, Error Contract |

---

## 재승인 (approve)

```powershell
pytest -m golden_master --approve-golden -v
# 또는
python scripts/generate_golden_master.py
```
