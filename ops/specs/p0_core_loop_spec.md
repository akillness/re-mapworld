# P0: 핵심 생존 루프 스펙

## 1. 맵 구조
- **Lobby**: 준비 및 보상 정산 (Maple Soul Hero 로직 활용)
- **Expedition Zone**: 위험 지역. 중앙에 세이프 존 존재.

## 2. 위험도 시스템
- 10초마다 1% 상승.
- 세이프 존 진입 시 상승 중단 및 초당 2% HP 회복.
- 위험도 100% 시 보스 'Dark Slime' 소환.

## 3. 탈출 조건
- 보스 처치 시 30초간 탈출 포탈 유지.
- 포탈 미탑승 시 전멸 처리 (보상 50% 손실).

## 4. 참조 리소스
- `resource/maple-soul-hero/scripts/Battle/`: HP/MP 시스템
- `resource/maple-soul-hero/scripts/Stage/`: 맵 이동
