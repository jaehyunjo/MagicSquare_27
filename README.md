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
│   └── 06.MagicSquare_RED_AC_FR_01_01_Report.md     ← RED 단계 (AC-FR-01-01) 실행 보고서
└── Prompting/
    ├── 01.cursor_4x4_magic_square_problem_definit_prompt.md   ← 문제 정의 대화·프롬프트
    ├── 02.cursor_4x4_magic_square_tdd_spec_workflow_prompt.md ← TDD·브랜치·spec 대화
    ├── 04.cursor_magic_square_user_journey_user_story_scenario_transcript.md
    └── 05.cursor_ac_fr_01_01_red_test_plan_coverage_transcript.md ← RED·플랜·커버리지 대화
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
| [docs/TP-ST01-TC011-001.md](docs/TP-ST01-TC011-001.md) | 테스트 플랜 (AC-FR-01-01 / TC-011) |
| [defect_list.md](defect_list.md) | RED 결함 목록 (DEF-001~005) |
| [Prompting/01.cursor_4x4_magic_square_problem_definit_prompt.md](Prompting/01.cursor_4x4_magic_square_problem_definit_prompt.md) | 문제 정의(STEP 1~5) 프롬프트·응답 transcript |
| [Prompting/02.cursor_4x4_magic_square_tdd_spec_workflow_prompt.md](Prompting/02.cursor_4x4_magic_square_tdd_spec_workflow_prompt.md) | 브랜치·spec·TDD 설계 실행 프롬프트·응답 transcript |
| [Prompting/05.cursor_ac_fr_01_01_red_test_plan_coverage_transcript.md](Prompting/05.cursor_ac_fr_01_01_red_test_plan_coverage_transcript.md) | RED·테스트 플랜·venv·커버리지·결함 대화 transcript |
| `.cursor/magicsquare-rules.yaml` | 프로젝트 규칙 템플릿 (8개 최상위 키) |

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 정의 (STEP 1~5) | ✅ 완료 |
| TDD 설계 문서 (`spec`) | ✅ `Report/02...` |
| PRD (`spec`) | ✅ `Report/03...` |
| 보고서·Prompting transcript | ✅ `Report/`, `Prompting/` |
| 구현·테스트·실행 방법 | ⏳ RED 진행 — [Report/06](Report/06.MagicSquare_RED_AC_FR_01_01_Report.md), [테스트 실행](#테스트-실행-가상환경--커버리지) |
| RED 보고서·Transcript | ✅ `Report/06...`, `Prompting/05...` |

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

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ — [테스트 실행 §4](#4-테스트--커버리지-출력-필수-관행) (`scripts/run-coverage.ps1`)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] [defect_list.md](defect_list.md) 생성 및 발견 결함 기록 (DEF-001~005, RED 12 failed)
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 다음 단계 (예정)

1. **범위(1차/2차)** 및 **비목표** 목록 확정  
2. **TDD 판정 시나리오** 정리 (유효 / 무효 / 부분 / 입력 오류)  
3. 구현·구조 설계 (별도 문서·브랜치에서 진행)

---

## 라이선스 · 기여

미정. 프로젝트가 확장되면 이 섹션을 갱신합니다.
