# 🛠️ MapleStory Worlds 엔진 활용 및 프로세스 추적 가이드

## 1. 월드 제작 및 실행 (Workflow)
1. **월드 만들기**: [MSW 제작 페이지](https://maplestoryworlds.nexon.com/ko/make)에 접속하여 신규 월드 프로젝트를 생성합니다.
2. **클라이언트 실행**: 제작된 월드를 '클라이언트 실행' 버튼을 통해 로컬 엔진 툴에서 구동합니다.
3. **프로세스 확인**: 작업 관리자에 `mapleworld` 프로세스가 추가되었는지 확인합니다. 이 프로세스가 활성화되어야 실시간 코드 이식이 가능합니다.

## 2. 프로세스 추적 및 개발 로그 (Monitoring)
- **대상**: `mapleworld.exe` (또는 관련 프로세스)
- **로그 활용**: 
    - `mapleworld` 화면의 시각적 변화를 `ops/plans/process_analysis_log.md`에 기록.
    - 엔진 내부의 디버그 콘솔 로그를 `logs/engine_trace.log`로 추출하여 `gjc`에게 전달.

## 3. 실시간 코드 적용 (Live Update)
- `/tmp/MapleSurvivalExpedition/scripts/`에 작성된 루아 스크립트를 엔진 툴의 스크립트 에디터에 복사-붙여넣기 하거나, 파일 시스템 동기화를 통해 반영합니다.
- **Option C** (위험도 상승 + 세이프 존) 로직이 `mapleworld` 프로세스 상에서 정상 동작하는지 20분 주기로 체크합니다.

## 4. 지속 개발 규칙
- 모든 수정 사항은 반드시 **gjc 분석 시스템**을 거쳐 화면 분석 내용과 동기화되어야 함.
- 동작 검증 완료 시 `[VERIFIED]` 로그를 남기고 메인 브랜치에 머지함.
