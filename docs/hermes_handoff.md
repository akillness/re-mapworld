# Hermes 작업 전달 패킷

## 목표

메이플스토리 글로벌 개발 콘테스트 2026 출품을 목표로, 현재 폴더의 `resource/` 리메이크 리소스를 기반으로 `성장 + 경쟁 + 서바이벌` MORPG 월드의 MVP를 깃 작업으로 진행한다.

## 먼저 읽을 파일

1. `join_notice.md` — 출품 조건, 유의사항, 실격 리스크.
2. `join_develop.md` — 참가 절차, 개발 콘셉트, 리소스 활용 지도.
3. `trend_strategy.md` — 2026 메이플/MORPG 트렌드와 PM/프로덕션 방향.
4. `README.md` — 저장소 리소스 구조와 월드별 특징.

## 공식 링크

- 이벤트 페이지: <https://maplestoryworlds.nexon.com/events/ko/2026globalcontest>
- 참가자 모집 공지: <https://maplestoryworlds.nexon.com/ko/community/5005/2120/3443626>
- FAQ 공지: <https://maplestoryworlds.nexon.com/ko/community/5005/2120/3443627>
- 공모전 정책: <https://guide.nexon.com/ko/game/maplestoryworlds/guides/globalcreatorchallenge/pages/kr>
- 리메이크 리소스 공개 공지: <https://maplestoryworlds.nexon.com/ko/community/5005/2120/3429377>

## 제안 월드 방향

**가칭:** Maple Survival Expedition / 메이플 생존 원정대

**핵심 루프:**

```text
로비/준비 → 위험 지역 입장 → 사냥/채집/생존 자원 관리 → 엘리트/보스 이벤트 → 탈출 또는 전멸 → 보상 정산 → 장비·룬·도감 성장 → 랭킹/시즌 점수 갱신
```

**설계 축:**

- 성장: 계정 레벨, 장비/룬, 몬스터 도감.
- 경쟁: 생존 시간, 최고 위험도, 시즌 점수 랭킹.
- 서바이벌: 위험도 상승, 제한 자원, 탈출 타이밍.

## 리소스 우선순위

| 우선 | 출처 | 사용 목적 |
|---:|---|---|
| 1 | `resource/maple-soul-hero/scripts/Battle/` | 전투, HP/MP/SP 이벤트, 배틀 UI, 보스/스테이지 구조 참고 |
| 2 | `resource/maple-soul-hero/scripts/Ranking/` | 생존 시간/시즌 점수 랭킹 UI와 로직 참고 |
| 3 | `resource/maple-soul-hero/scripts/Stage/` | 스테이지 입장/종료/이동 구조 참고 |
| 4 | `resource/miner-simulator/scripts/Components/Player/` | 자원 파밍, 장비/펫/인벤토리 성장 구조 참고 |
| 5 | `resource/monster-farm/scripts/Logic/` + `Book/` + `Collection/` | 몬스터 도감/수집/보상 구조 참고 |
| 6 | `resource/maple-auto-battler/scripts/OutGame/DailyMission/` | 일일/주간 미션과 반복 접속 루프 참고 |
| 7 | `resource/maple-duel/scripts/Components/UIs/RankingModule.*` | 경쟁 UI 참고. 직접 PvP는 MVP 제외 |

## MVP 작업 순서

### P0 — 출품 가능한 핵심 루프

- [ ] 신규 월드 프로젝트 생성 또는 기존 작업 브랜치 준비.
- [ ] 1개 로비 맵과 1개 위험 지역 맵 구성.
- [ ] 입장 → 생존 전투 → 탈출/전멸 → 보상 정산 루프 구현.
- [ ] 전투 UI, HP/자원 표시, 보상 팝업 최소 구현.
- [ ] 30초 플레이 영상 촬영 가능한 안정 빌드 확보.

### P1 — 콘테스트 심사 대응

- [ ] 메이플 IP 재해석이 보이는 몬스터/지역/아이템 테마 적용.
- [ ] 생존 시간 또는 최고 위험도 랭킹 1종 구현.
- [ ] 계정 레벨/장비/도감 중 2개 성장축 구현.
- [ ] 첫 60초 튜토리얼: 목표, 위험도, 탈출 조건 설명.
- [ ] 월드 기본정보와 장르가 실제 플레이와 일치하도록 작성.

### P2 — 지속 가능성/운영 구조

- [ ] 주간 시즌 점수와 보상표 초안.
- [ ] 신규 위험도/몬스터/룬을 데이터셋으로 추가할 수 있는 구조.
- [ ] 커뮤니티 공지 템플릿과 문의 대응 루틴.
- [ ] 본선 이후 업데이트 계획 문서화.

## 완료 조건

- 월드가 공개 출시 가능한 상태다.
- 플레이 가능 범위 `공개`, 출시 지역 `전체`, 월드 설문지, 30초 영상, 커뮤니티 주소 조건을 충족할 수 있다.
- 출품 전 `join_notice.md` 체크리스트를 모두 통과한다.
- 세션 루프가 3회 연속 실행되어도 보상 중복, 랭킹 누락, 진행 불능이 없다.
- 외부 리소스/IP 사용 내역이 없거나, 공식/직접 제작/AI 사용 가이드 준수 근거가 남아 있다.

## Git 작업 권장 방식

- 브랜치명: `feature/maple-survival-expedition-mvp`
- 커밋 단위:
  1. `docs: add contest brief and handoff docs`
  2. `feat: add survival expedition core loop`
  3. `feat: add growth and ranking systems`
  4. `chore: prepare contest submission metadata`
- 대형 리소스 이동/삭제는 별도 커밋으로 분리한다.
- `MSWRemake/` 원본은 재가져오기용이므로 직접 수정하지 말고, 작업은 새 월드 또는 `resource/` 기반 복사본에서 진행한다.

## 금지/주의

- 콘테스트 모집 기간 전 공개된 월드를 그대로 출품하지 않는다.
- 출품 후 취소가 불가능하므로 테스트 월드와 출품 월드를 혼동하지 않는다.
- 강제 PvP, 과도한 실패 손실, 불명확한 과금 요소는 결승 유저 평가에 불리하므로 MVP에서 제외한다.
- 심사 기간 중 급한 수정이 필요하지 않도록 본선 전 안정판을 확보한다.
