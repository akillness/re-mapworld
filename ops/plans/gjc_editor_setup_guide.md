# 🛠️ gjc 에디터 설정 및 지속 개발 가이드

## 1. 에디터 초기 설정 (Editor Setup)
- **Layer Management**: 배경(Background), 장애물(Obstacle), 캐릭터(Player), UI 레이어 순으로 정렬 확인.
- **Trigger Zones**: 세이프 존 구역에 `TriggerComponent` 추가 및 `SurvivalManager:OnSafeZoneEnter()` 바인딩.
- **UI Canvas**: `DefaultUI` 그룹 내에 새로운 `Image` 컴포넌트(게이지)와 `Text` 컴포넌트(카운트다운) 생성.

## 2. 지속적 코드 확장 (Continuous Dev)
- **gjc**는 매 20분마다 `expanded_spec_v2.md`를 확인하여 신규 기능을 루아 스크립트로 번역함.
- 에디터 내의 변경 사항을 저장할 때마다 `logs/engine_trace.log`에 `[AUTO_SAVE]` 신호를 기록하여 버전 관리 수행.

## 3. 확인 및 루프
- 각 기능 추가 후 **ooo run** 시각적 검증 통과 시 다음 기획 항목으로 이동.
