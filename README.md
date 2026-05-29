# MagicSquare_XX

4×4 마방진(Magic Square)을 다루는 학습·실험 프로젝트입니다.  
현재 단계는 **문제 정의(Problem Definition)** 이며, 구현·설계·알고리즘 선정은 아직 시작하지 않았습니다.

---

## 프로젝트 목적

| 구분 | 내용 |
|------|------|
| **표면 목표** | 4×4 격자에 1~16을 배치해 행·열·대각의 합을 맞추는 것처럼 보이는 문제 |
| **실제 목표** | “마방진” **판정 기준**을 고정하고, 임의의 배치에 그 기준을 **일관되게 적용·반복**할 수 있는지 다루는 것 |
| **훈련 방향** | 명세화, 불변량, 경계·계약, 역할 분리, TDD 기반 검증 우선 사고 |

손으로 한 번 합을 맞추는 수준을 넘어, **규칙·불변량·경계를 명세 가능한 형태로 다루는 능력**을 검증하는 것이 핵심입니다.

---

## 진짜 문제 정의 (요약)

### 잘못된 정의 (피할 표현)

> 4×4 격자에 1~16을 넣어 행·열·대각 합이 같게 만드는 프로그램을 만든다.

— 산출물·완성에만 묶이고, 판정·반복·역할 분리가 빠집니다.

### 정확한 정의

> 4×4 격자에 대한 **“마방진” 판정 기준을 먼저 고정**하고,  
> 임의의 배치(완전·부분·잘못된 입력 포함)에 대해 그 기준을 **일관되게 적용·반복·기록**할 수 있는지를 다루는 문제.  
> 완전한 배치를 얻는 것은, 필요 시 **판정 기준을 만족하는 산출물을 확보**하는 행위로만 한정한다.

---

## 핵심 Invariant

도메인(4×4, 1~16, 행·열·대각을 마법 선으로 둔 경우):

| ID | 불변 조건 |
|----|-----------|
| **I-1** | 1~16 각 **정확히 한 번** |
| **I-2** | 정의된 모든 마법 선의 합이 **서로 같음** (마법 상수 **34**) |
| **I-3** | 마법 상수는 격자 크기·숫자 집합에 **논리적으로 결정** |
| **I-4** | 판정 규칙 집합은 **판정마다 동일** |

시스템·과정:

| ID | 불변 조건 |
|----|-----------|
| **I-5** | 동일 배치·동일 기준 → **동일 판정** |
| **I-6** | 완전 배치 확보 결과는 **항상 I-1~I-3 만족** |
| **I-7** | 잘못된 입력은 **조용히 “거의 맞음” 처리되지 않음** |
| **I-8** | 부분 배치 시 부분 판정 규칙 **사전 정의·일관** (도입 시) |

우선순위: `I-4 → I-1~I-3 → I-5, I-7 → I-6(선택) → I-8(선택)`

---

## 문제 인식 흐름 (STEP 1 ~ 5)

```text
STEP 1  관찰      제약·검증·맥락 — “만든다”가 아닌 상황 서술
STEP 2  Why #1    “완성”의 이유와 생성/검증·부분 상태 긴장
STEP 3  Why #2    프로그램 = 반복·자동 검증·오류 방지·규칙 외화
STEP 4  Why #3    TDD = 통제·불변량·명확한 입출력 계약
STEP 5  정의      판정 기준 중심의 진짜 문제 + Invariant + 사고 능력
```

| STEP | 핵심 질문 | 발견 |
|------|-----------|------|
| 1 | 무엇을 다루는 상황인가? | 16칸 배치 + 다중 합 제약; 생성·검증·활용이 갈림 |
| 2 | 왜 완성해야 하는가? | “완성 = 증거”는 검증만으로도 성립 가능; 생성과 혼선 위험 |
| 3 | 왜 프로그램인가? | 반복 가능성, 검증 자동화, 오류 방지, 규칙 기반 사고 |
| 4 | 왜 TDD인가? | 통제 대상·불변량·입출력 계약을 먼저 고정 |
| 5 | 진짜 문제는? | 판정 기준 중심; I-1~I-8; 명세·분리·반증 사고 |

---

## 설계 원칙 (문제 정의 단계에서 확정)

1. **판정(검증)을 생성보다 먼저** 다룬다.
2. **생성 · 검증 · 표현** 역할을 분리한다.
3. **입력·출력 계약**(격자 표현, 완전/부분, 판정 결과)을 명확히 한다.
4. **불변량(I-1~I-8)** 을 깨지 않는지가 성공 기준이다.
5. 구현이 정의를 대체하지 않도록, **의미를 먼저 고정**한다 (TDD 맥락).

---

## 아직 정하지 않은 것

- 1차 범위: 검증만 / 생성 포함 / UI·교육 기능
- “마법 선”에 포함할 선(대각 외 추가 여부)
- 부분 배치(I-8) 지원 여부
- 사용 언어·런타임·저장소 구조

---

## 저장소 구조

```text
MagicSquare_XX/
├── README.md                          ← 이 파일 (프로젝트 개요)
├── .venv/                             ← 로컬 가상환경 (git 제외, 테스트는 여기서 실행)
├── requirements-dev.txt               ← pytest, pydantic, pytest-cov
├── pytest.ini                         ← pythonpath=src
├── .coveragerc                        ← 커버리지 측정 설정
├── scripts/
│   ├── setup-venv.ps1                 ← 가상환경 생성·의존성 설치
│   ├── run-coverage.ps1               ← 테스트 + 커버리지 (터미널 + HTML)
│   ├── open-coverage-html.ps1         ← htmlcov/index.html 브라우저에서 열기
│   └── open-coverage-liveserver.ps1   ← Live Server로 htmlcov/ 서빙
├── src/magicsquare/                   ← ECB 구현 (boundary / control / domain / entity)
├── tests/                             ← pytest (unit / integration)
├── docs/                              ← 테스트 플랜 등 (예: TP-ST01-TC011-001.md)
├── defect_list.md                     ← RED 단계 결함 목록 (AC-FR-01-01)
├── .cursor/
│   └── magicsquare-rules.yaml         ← 규칙 템플릿 뼈대 (키만, 값 비움)
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md   ← STEP 1~5 전체 보고서
│   ├── 02.MagicSquare_TDD_Design_Report.md          ← TDD 설계 (spec 산출물)
│   ├── 03.MagicSquare_PRD_Report.md                 ← PRD (구현 전 제품 요구사항)
│   ├── 04.MagicSquare_CursorRules_Report.md         ← Cursor 규칙 설계 보고서
│   ├── 05.MagicSquare_UserJourney_UserStories_Scenarios_Report.md
│   ├── 06.MagicSquare_RED_AC_FR_01_01_Report.md     ← RED 단계 (AC-FR-01-01) 실행 보고서
│   ├── 07.MagicSquare_RED_DualTrack_FR01_05_Report.md ← Dual-Track RED 설계 (FR-01~05)
│   ├── 08.MagicSquare_RED_DualTrack_FullRED_UIN0103_Report.md ← Full RED (U-IN-01~03)
│   ├── 09.MagicSquare_DualTrack_RED_TestPlan_Design_Report.md ← Dual-Track TestPlan SSOT
│   ├── 10.MagicSquare_RED_DualTrack_Skeleton_Report.md ← RED Skeleton (24건)
│   ├── 11.MagicSquare_GREEN_Stabilize_AC_FR_01_01_Report.md ← GREEN 1슬라이스 (grid=None)
│   └── 12.MagicSquare_RED_GREEN_Todo_Checklist_Report.md ← RED/GREEN To-Do SSOT
└── Prompting/
    ├── 01.cursor_4x4_magic_square_problem_definit_prompt.md   ← 문제 정의 대화·프롬프트
    ├── 02.cursor_4x4_magic_square_tdd_spec_workflow_prompt.md ← TDD·브랜치·spec 대화
    ├── 04.cursor_magic_square_user_journey_user_story_scenario_transcript.md
    ├── 05.cursor_ac_fr_01_01_red_test_plan_coverage_transcript.md ← RED·플랜·커버리지 대화
    ├── 06.cursor_dual_track_red_fr01_05_transcript.md ← Dual-Track RED FR-01~05 대화
    ├── 07.cursor_dual_track_red_skeleton_transcript.md ← RED Skeleton·Export 대화
    ├── 08.cursor_stabilize_green_ac_fr_01_01_transcript.md ← stabilize/green·Report/11 Export
    └── 09.cursor_red_green_todo_export_transcript.md ← RED/GREEN To-Do·Report/12 Export
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | 관찰, Why 분석, 진짜 문제 정의, Invariant, 종합 요약 (상세) |
| [Report/02.MagicSquare_TDD_Design_Report.md](Report/02.MagicSquare_TDD_Design_Report.md) | TDD 설계: 계약, Slice, TC-001~018, red/green/refactor Playbook |
| [Report/03.MagicSquare_PRD_Report.md](Report/03.MagicSquare_PRD_Report.md) | PRD: Vision, Scope, Contracts, Stories, AC, Architecture, Verification |
| [Report/04.MagicSquare_CursorRules_Report.md](Report/04.MagicSquare_CursorRules_Report.md) | Cursor 프로젝트 룰 설계·정리 보고서 |
| [Report/05.MagicSquare_UserJourney_UserStories_Scenarios_Report.md](Report/05.MagicSquare_UserJourney_UserStories_Scenarios_Report.md) | User Journey, Stories, Scenarios, Verification |
| [Report/06.MagicSquare_RED_AC_FR_01_01_Report.md](Report/06.MagicSquare_RED_AC_FR_01_01_Report.md) | RED 단계: 테스트 플랜·pytest·커버리지·결함 목록 |
| [Report/07.MagicSquare_RED_DualTrack_FR01_05_Report.md](Report/07.MagicSquare_RED_DualTrack_FR01_05_Report.md) | Dual-Track RED 설계표 (FR-01~05, Track A/B 27건) |
| [Report/08.MagicSquare_RED_DualTrack_FullRED_UIN0103_Report.md](Report/08.MagicSquare_RED_DualTrack_FullRED_UIN0103_Report.md) | Full RED (U-IN-01~03, 12 pytest) |
| [Report/09.MagicSquare_DualTrack_RED_TestPlan_Design_Report.md](Report/09.MagicSquare_DualTrack_RED_TestPlan_Design_Report.md) | Dual-Track RED TestPlan SSOT |
| [Report/10.MagicSquare_RED_DualTrack_Skeleton_Report.md](Report/10.MagicSquare_RED_DualTrack_Skeleton_Report.md) | RED Skeleton 실행 (24 pytest) |
| [Report/11.MagicSquare_GREEN_Stabilize_AC_FR_01_01_Report.md](Report/11.MagicSquare_GREEN_Stabilize_AC_FR_01_01_Report.md) | GREEN 1슬라이스 (`stabilize/green`, grid=None 6 passed) |
| [Report/12.MagicSquare_RED_GREEN_Todo_Checklist_Report.md](Report/12.MagicSquare_RED_GREEN_Todo_Checklist_Report.md) | RED/GREEN To-Do 체크리스트 SSOT |
| [docs/TP-ST01-TC011-001.md](docs/TP-ST01-TC011-001.md) | 테스트 플랜 (AC-FR-01-01 / TC-011) |
| [defect_list.md](defect_list.md) | RED 결함 목록 (DEF-001~005) |
| [Prompting/01.cursor_4x4_magic_square_problem_definit_prompt.md](Prompting/01.cursor_4x4_magic_square_problem_definit_prompt.md) | 문제 정의(STEP 1~5) 프롬프트·응답 transcript |
| [Prompting/02.cursor_4x4_magic_square_tdd_spec_workflow_prompt.md](Prompting/02.cursor_4x4_magic_square_tdd_spec_workflow_prompt.md) | 브랜치·spec·TDD 설계 실행 프롬프트·응답 transcript |
| [Prompting/05.cursor_ac_fr_01_01_red_test_plan_coverage_transcript.md](Prompting/05.cursor_ac_fr_01_01_red_test_plan_coverage_transcript.md) | RED·테스트 플랜·venv·커버리지·결함 대화 transcript |
| [Prompting/06.cursor_dual_track_red_fr01_05_transcript.md](Prompting/06.cursor_dual_track_red_fr01_05_transcript.md) | Dual-Track RED FR-01~05 설계·Export 대화 transcript |
| [Prompting/07.cursor_dual_track_red_skeleton_transcript.md](Prompting/07.cursor_dual_track_red_skeleton_transcript.md) | RED Skeleton·Report Export 대화 transcript |
| [Prompting/08.cursor_stabilize_green_ac_fr_01_01_transcript.md](Prompting/08.cursor_stabilize_green_ac_fr_01_01_transcript.md) | stabilize/green ECB GREEN·Report/11 Export transcript |
| [Prompting/09.cursor_red_green_todo_export_transcript.md](Prompting/09.cursor_red_green_todo_export_transcript.md) | RED/GREEN To-Do·Report/12 Export transcript |
| `.cursor/magicsquare-rules.yaml` | 프로젝트 규칙 템플릿 (8개 최상위 키) |

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 정의 (STEP 1~5) | ✅ 완료 |
| TDD 설계 문서 (`spec`) | ✅ `Report/02...` |
| PRD (`spec`) | ✅ `Report/03...` |
| 보고서·Prompting transcript | ✅ `Report/`, `Prompting/` |
| 구현·테스트·실행 방법 | ⏳ GREEN 1슬라이스 — [Report/11](Report/11.MagicSquare_GREEN_Stabilize_AC_FR_01_01_Report.md), 브랜치 `stabilize/green` |
| RED 보고서·Transcript | ✅ `Report/06~10`, `Prompting/05~07` |
| GREEN 보고서·Transcript | ✅ `Report/11`, `Prompting/08` |

---

## 테스트 실행 (가상환경 · 커버리지)

**본 프로젝트의 pytest는 시스템 Python이 아니라 프로젝트 루트의 `.venv` 가상환경에서 실행합니다.**  
커버리지 측정·리포트 출력도 동일하게 가상환경의 `pytest-cov`를 사용합니다.

### 1. 최초 1회 — 가상환경 준비

PowerShell(프로젝트 루트):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-venv.ps1
```

`requirements-dev.txt` 기준으로 `pytest`, `pydantic`, `pytest-cov`가 `.venv`에 설치됩니다.

### 2. 가상환경 활성화 (권장)

```powershell
.\.venv\Scripts\Activate.ps1
```

프롬프트에 `(.venv)`가 보이면 활성화된 상태입니다.

### 3. 테스트만 실행

```powershell
pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -v
```

활성화 없이 한 번에 실행할 때:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -v
```

> **RED 단계:** 구현 전이면 테스트가 **의도적으로 실패**할 수 있습니다(`NotImplementedError` 등). 수집·실행 자체가 되면 환경은 정상입니다.

### 4. 테스트 + 커버리지 출력 (필수 관행)

터미널 요약과 **HTML 리포트**를 함께 생성합니다. HTML은 반드시 `htmlcov/`에 기록됩니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-coverage.ps1
```

또는 (가상환경 활성화 후):

```powershell
pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -v `
  --cov=magicsquare.boundary --cov=magicsquare.control --cov=magicsquare.domain `
  --cov-config=.coveragerc --cov-report=term-missing --cov-report=html:htmlcov
```

| 출력 | 설명 |
|------|------|
| 터미널 `term-missing` | 모듈별 Cover % 및 미커버 라인 |
| **`htmlcov/index.html`** | **브라우저용 HTML 커버리지 리포트** (파일·라인 하이라이트) |

커버리지 설정은 [`.coveragerc`](.coveragerc)를 따릅니다. `htmlcov/`·`.coverage`는 git에 포함하지 않습니다.

### 5. HTML 커버리지 보기

1. 위 [§4](#4-테스트--커버리지-출력-필수-관행)를 실행해 `htmlcov/index.html`을 생성합니다.
2. 브라우저에서 엽니다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\open-coverage-html.ps1
```

**Live Server로 보기** (파일 경로 대신 로컬 HTTP 서버 — 권장):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\open-coverage-liveserver.ps1
```

브라우저에서 `http://127.0.0.1:5500/index.html` 이 열립니다. 종료는 해당 터미널에서 `Ctrl+C`.

`htmlcov`가 없으면 `open-coverage-html.ps1` / `open-coverage-liveserver.ps1`이 먼저 `run-coverage.ps1`을 실행합니다.

수동으로 열 때: 프로젝트 루트의 **`htmlcov\index.html`** 을 더블클릭하거나, 탐색기 주소창에 전체 경로를 붙여 넣습니다.

```text
MagicSquare_XX/htmlcov/index.html   ← 파일별·라인별 커버리지 (녹색/빨강)
```

### 6. 주의

- **시스템 `python` / 전역 `pytest`로 실행하지 마세요.** 패키지 버전·`src` 경로가 어긋날 수 있습니다.
- 의존성을 바꾼 뒤에는 `.venv`에서 `pip install -r requirements-dev.txt`를 다시 실행하세요.

---

## RED 단계 — 이해 요약 · 체크리스트

### RED가 뭔지 (이 프로젝트 기준)

RED는 **구현보다 먼저 “실패하는 테스트”를 고정**하는 단계다.

- 테스트에 **assert(기대값)** 가 있어야 하고, `pytest`로 돌리면 **의도적으로 실패**해야 RED가 끝난 것이다.
- 실패 이유가 **미구현**(`NotImplementedError`, `pytest.fail("RED: ...")`)이면 정상이다. 테스트를 통과시키려고 assert를 지우거나 skip 하면 안 된다.
- RED에서는 **`src/`에 동작 구현을 넣지 않는다.** 스텁(항상 실패)만 허용된다.
- 커밋 접두사: `test:` — “이 계약을 나중에 green이 만족해야 한다”는 증거를 남긴다.

### 트랙이 두 갈래인 이유

| 트랙 | RED가 의미하는 것 | 테스트 위치 | 실패 방식 |
|------|-------------------|-------------|-----------|
| **ECB (판정·Slice S0)** | AC-FR-01-01 / TC-011 — `INVALID_SIZE`, `"Grid must be 4x4."` | `tests/unit/boundary/test_ac_fr_01_01_invalid_size.py` | **Full RED** — assert 있음, `NotImplementedError` |
| **Dual-Track DDD** | FR-01~05 UI·솔버 — E003/E001/E002… envelope | `tests/boundary/`, `tests/entity/` | **Skeleton RED** — `pytest.fail("RED: ...")` 만, assert 아직 없음 |

**헷리리기 쉬운 점:** Dual-Track용 `src/boundary/`(`InputValidator`)는 RED·green 설계와 **별 트랙**이다. ECB green(`stabilize/green`, `magicsquare.boundary.validation`)과 **같은 브랜치·커밋에 섞지 않는다.**

### 검사 순서 (RED 테스트도 이 순서로 쌓음)

FR-01 §8.5 기준: **`null` → `size` → 빈칸 개수 → 값 범위 → 중복**  
지금 Full RED 12건은 앞의 **`null` + `size` 거부**만 다룬다 (AC-FR-01-01).

---

### RED 공통 — 완료 조건

- [x] spec·PRD·TDD Slice 문서 확정 (`Report/02`, `03`, `docs/TP-ST01-TC011-001.md`)
- [x] RED 실행 보고·결함 목록 (`Report/06`, [defect_list.md](defect_list.md) DEF-001~005)
- [x] Dual-Track TestPlan SSOT (`Report/09`)
- [x] `develop`에 RED 테스트·RED 스텁 머지 완료 (`feature/dual-track-tdd` → PR #4/#5)

---

### ECB Full RED — AC-FR-01-01 (12 pytest, assert 포함)

모듈: `tests/unit/boundary/test_ac_fr_01_01_invalid_size.py`  
정렬: **null 먼저 → size → 통합 scope 마지막** (green 때도 같은 묶음 순서)

#### null (`grid=None`) — U-IN-01 / TC-011 V-01

- [x] `test_none_grid_boundary_resolve_zero_calls` — Boundary만, `resolve` 0회
- [x] `test_none_grid_exact_message_prd_section_81_wording` — 메시지 문자 단위
- [x] `test_none_grid_orchestrator_resolve_zero_calls` — Control 경로, `resolve` 0회
- [x] `test_none_grid_resolve_called_fails_isolation` — `resolve` 호출 시 테스트 실패
- [x] `test_none_grid_returns_invalid_size_and_message` — `INVALID_SIZE` + 메시지
- [x] `test_none_grid_returns_validation_failure_model_type` — `ValidationFailure` 타입

#### size (`[]`, 3×4, 빈 4행) — U-IN-02~03 / TC-011 V-02

- [x] `test_boundary_shape_returns_invalid_size_failure[empty_list]`
- [x] `test_empty_list_returns_invalid_size_code`
- [x] `test_boundary_shape_returns_invalid_size_failure[four_empty_rows]`
- [x] `test_boundary_shape_returns_invalid_size_failure[three_by_four]`
- [x] `test_three_by_four_returns_invalid_size_code`
- [x] `test_scope_only_invalid_size_not_other_ac_codes` — `None`·`[]`·`[[]]*4`·3×4만, 다른 AC 코드 금지

**RED DoD:** 위 12건 수집·실행 시 전부 실패(스텁 `NotImplementedError`) → ✅ (`Report/08`)

---

### Dual-Track Skeleton RED (24 pytest, assert 없음)

Skeleton은 “자리만 잡은 RED”다. **green 전에** 각 항목을 Full RED처럼 assert로 바꾸는 단계가 따로 있다.

#### Track A — Boundary / UI (`tests/boundary/`)

- [x] U-IN-04~08 — `test_u_in_04` … `test_u_in_08` (E002/E004/E005 자리)
- [x] U-OUT-01~03 — `test_u_out_01` … `test_u_out_03`
- [x] U-FLOW-02 — `test_u_flow_02_*` (invalid 시 `execute` 0회)

#### Track B — Entity / Logic (`tests/entity/`)

- [x] D-LOC-01, D-MIS-01
- [x] D-VAL-01~06
- [x] D-SOL-01~04 (G2/G3 TBD 주석)

**RED DoD:** 24건 전부 `pytest.fail("RED: ...")` → ✅ (`Report/10`)

---

### RED에서 아직 안 한 것 (의도적 Out of Scope)

- [ ] Dual-Track Skeleton → **Full RED** (실제 assert·E00x 메시지 고정)
- [ ] TC-008, TC-009, TC-010, TC-016 등 **Slice S0/S4 추가 RED** (Report/02)
- [ ] I-1 / I-2 / `Valid` 판정 RED (TC-001~007, S2~S4)
- [ ] DEF-005: PRD `INPUT_DIMENSION_MISMATCH` vs 테스트 `INVALID_SIZE` 문서 합의

> **참고:** ECB **green(구현)** 은 [GREEN To-Do](#green-단계-to-do-리스트) · [Report/12](Report/12.MagicSquare_RED_GREEN_Todo_Checklist_Report.md)를 따른다 ([Report/11](Report/11.MagicSquare_GREEN_Stabilize_AC_FR_01_01_Report.md)).

---

## GREEN 단계 To-Do 리스트

> SSOT: [Report/12.MagicSquare_RED_GREEN_Todo_Checklist_Report.md](Report/12.MagicSquare_RED_GREEN_Todo_Checklist_Report.md)  
> 브랜치: **`stabilize/green`** (`develop` 기준) · 커밋 접두사: **`feat:`**  
> 금지: refactor, Slice 밖 기능, 테스트 완화·skip, Dual-Track `src/boundary/` 혼입

### GREEN이 뭔지 (한 줄)

**RED 실패 TC를 통과시키는 최소 코드만** `entity → control → boundary` 순으로 넣는다. 구조 개선은 **refactor** 단계에서 한다.

### 공통

- [x] `develop` pull 후 `stabilize/green` 브랜치 생성
- [ ] `stabilize/green` → `develop` merge (AC-FR-01-01 12건 전부 green 후)
- [ ] [defect_list.md](defect_list.md) DEF-001~002 종결 (validate 구현 완료 시)
- [ ] 커버리지 실행·HTML 확인 ([§4](#4-테스트--커버리지-출력-필수-관행))

---

### ECB — AC-FR-01-01 (`tests/unit/boundary/test_ac_fr_01_01_invalid_size.py`)

모듈: `magicsquare.boundary.validation`, `magicsquare.control.orchestrator`  
정렬: **null → size → scope** (RED와 동일 순서로 `feat:` 커밋)

#### G-01 · `grid=None` — `feat: grid=None INVALID_SIZE` ✅ (`6fc9679`)

- [x] `test_none_grid_boundary_resolve_zero_calls`
- [x] `test_none_grid_exact_message_prd_section_81_wording`
- [x] `test_none_grid_orchestrator_resolve_zero_calls`
- [x] `test_none_grid_resolve_called_fails_isolation`
- [x] `test_none_grid_returns_invalid_size_and_message`
- [x] `test_none_grid_returns_validation_failure_model_type`

**검증:** `pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -k none_grid -v` → 6 passed

#### G-02 · `[]` 빈 리스트 — `feat: empty grid [] returns INVALID_SIZE`

- [ ] `test_boundary_shape_returns_invalid_size_failure[empty_list]`
- [ ] `test_empty_list_returns_invalid_size_code`

**검증:** `-k "none_grid or empty_list"` → 8 passed

#### G-03 · shape ≠ 4×4 — `feat: non-4x4 shape returns INVALID_SIZE`

- [ ] `test_boundary_shape_returns_invalid_size_failure[four_empty_rows]`
- [ ] `test_boundary_shape_returns_invalid_size_failure[three_by_four]`
- [ ] `test_three_by_four_returns_invalid_size_code`

**검증:** size 관련 5건 + none 6건 → 11 passed

#### G-04 · scope 통합 — `feat: scope guard INVALID_SIZE for dimension inputs`

- [ ] `test_scope_only_invalid_size_not_other_ac_codes`

**DoD:** `pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -v` → **12 passed**

---

### ECB — Slice S0/S4 이후 (RED 추가 후 green)

Report/02 TC · 별도 `feat:` 슬라이스. **AC-FR-01-01 12건 완료 전에는 착수하지 않음.**

- [ ] TC-008 / TC-016 — 3×3, 4×5 차원 `InputError`
- [ ] TC-009 — 4×4 내 null 셀 `INCOMPLETE_GRID`
- [ ] TC-010 — 비정수 `INPUT_NON_INTEGER`
- [ ] TC-001~003 — `Valid` (S3/S4)
- [ ] TC-004~007, TC-012~015 — `Invalid` I-1/I-2
- [ ] TC-017 — 결정성 I-5

---

### Dual-Track DDD (별 트랙 · 별 브랜치)

Skeleton RED만 있음 → **Full RED 전환 후** 아래 green 착수.

- [ ] Skeleton → Full RED (assert·E00x 메시지)
- [ ] DT-G-01 — U-IN-01 null → E003
- [ ] DT-G-02 — U-IN-02~03 size → E001
- [ ] DT-G-03 — U-IN-04~05 빈칸 → E002
- [ ] DT-G-04 — U-IN-06~07 범위 → E004
- [ ] DT-G-05 — U-IN-08 중복 → E005
- [ ] DT-G-06~07 — U-OUT, U-FLOW
- [ ] DT-G-08~12 — D-LOC ~ D-SOL (G2/G3 fixture 확정 후)

---

### GREEN 진행 스냅샷

| 스위트 | passed | failed | 비고 |
|--------|--------|--------|------|
| AC-FR-01-01 (12) | 6 | 6 | G-01 완료, G-02~04 대기 |
| Dual-Track Skeleton (24) | 0 | 24 | green 대상 아님 |

---

## 다음 단계 (예정)

1. **범위(1차/2차)** 및 **비목표** 목록 확정  
2. **TDD 판정 시나리오** 정리 (유효 / 무효 / 부분 / 입력 오류)  
3. 구현·구조 설계 (별도 문서·브랜치에서 진행)

---

## 라이선스 · 기여

미정. 프로젝트가 확장되면 이 섹션을 갱신합니다.
