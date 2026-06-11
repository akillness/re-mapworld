# 메이플스토리 글로벌 개발 콘테스트 2026 — 참가/개발 정리

![메이플스토리 월드 로고](https://mod-static.dn.nexoncdn.co.kr/events/_nuxt/bi_msw.uG54b-ew.svg)

> 개발 목표: `성장 + 경쟁 + 서바이벌`을 한 세션 안에서 이해되는 MORPG형 메이플 월드로 구성한다. 콘테스트 심사 기준상 “메이플 IP 해석/확장 40%, 완성도 40%, 지속 가능성 20%”를 직접 겨냥한다.

## 제안 콘셉트

**가칭: Maple Survival Expedition / 메이플 생존 원정대**

- 장르: 세션형 MORPG + 서바이벌 성장 + 비동기 랭킹 경쟁
- 핵심 판타지: 메이플 월드의 사냥·성장·몬스터 수집·장비 파밍을 “위험 지역에서 오래 살아남고 더 깊이 진입하는 원정”으로 재해석
- 플레이 길이: 5~12분 단위 반복 세션 + 누적 성장 메타
- 경쟁 방식: 직접 PK보다 안전한 랭킹/기록/보스 기여도/생존 시간 경쟁 우선
- 운영 방식: 주간 시즌 랭킹, 신규 몬스터/지역/룬 조합 업데이트, 커뮤니티 챌린지

## 공식 참여 흐름

![출품 배너 예시](https://dszw1qtcnsa5e.cloudfront.net/community/20260520/0e47f3f8-ca01-4dc8-83e6-6b4096fff774/image202605201655163.png)
![출품하기 예시](https://dszw1qtcnsa5e.cloudfront.net/community/20260520/6e5a9519-b218-4dac-b63f-97015a6f8d44/image202605201655164.png)

1. 메이플스토리 월드 클라이언트의 `만들기(메이커)`에서 월드 개발.
2. 모집 기간 내 신규 공개 출시.
3. 클라이언트 내 `개발 콘테스트 출품` 배너 클릭.
4. 출품 월드 선택 후 `출품하기` 클릭.
5. 공모전 정책 확인 후 `동의 후 출품` 클릭.
6. 출품 완료 후 취소 불가.

## 현재 폴더 리소스 활용 지도

이 저장소는 `MSW-Git/MSWRemake`의 메이플스토리 월드 리메이크 6종 리소스를 `resource/` 아래에 정리해 둔 상태다. 공식 공지상 오픈 소스로 공개된 리메이크 월드를 활용한 제작 월드는 출품 가능하다.

![리메이크 리소스 공개 공지 이미지](https://dszw1qtcnsa5e.cloudfront.net/community/20260421/5d13021d-5ecc-41f8-8e92-a5dc48b02c61/image202604211735003.png)

| 리소스 폴더 | 개발에 쓸 축 | 바로 볼 만한 경로 |
|---|---|---|
| `resource/maple-soul-hero/` | 방치형 RPG, 전투, 퀘스트, 랭킹, 멀티 전투 | `scripts/Battle/`, `scripts/MultiMode/`, `scripts/Ranking/`, `scripts/Quest/`, `scripts/Stage/` |
| `resource/maple-auto-battler/` | 팀 성장, 자동전투, 라운드/스테이지, 일일미션, 업적 | `scripts/InGame/`, `scripts/OutGame/Ranking/`, `scripts/OutGame/DailyMission/`, `scripts/OutGame/Achievement/` |
| `resource/maple-duel/` | 랭크전/랭킹 UI, 승패 보상, 카드형 경쟁 구조 | `scripts/Components/UIs/RankingModule.*`, `scripts/Components/Managers/RankManager.*` |
| `resource/miner-simulator/` | 채광/자원 파밍, 단계별 맵, 장비/펫/상점, 반복 성장 | `scripts/Components/Player/`, `scripts/Components/Town/`, `maps/` |
| `resource/monster-farm/` | 몬스터 도감, 수집, 조합/퓨전, 요리/농장, 퀘스트 | `scripts/Logic/`, `scripts/Book/`, `scripts/Collection/`, `ui/MonsterBookGroup.ui` |
| `resource/chu-chu-burger/` | 타이쿤, 고객/직원/레시피, 스테이지 패스/상점 | `scripts/Shop/`, `scripts/11. Employment/`, `scripts/04. Recipe/` |
| `resource/_common/NativeScripts/` | MSW 엔진 API 타입 정의 | `Component/`, `Event/`, `Logic/`, `Misc/` |

## 핵심 게임 루프

```text
로비/준비 → 위험 지역 입장 → 사냥/채집/생존 자원 관리 → 엘리트 몬스터/보스 이벤트 → 탈출/전멸 → 보상 정산 → 장비·스킬·몬스터 컬렉션 성장 → 랭킹/시즌 목표 갱신
```

### 성장

- 계정 레벨: 플레이 누적 보상, 지역 해금, 기본 능력 상승.
- 장비/룬: 세션 중 획득, 세션 후 일부 영구 성장으로 전환.
- 몬스터 도감: 처치/포획/퓨전으로 패시브 보너스 획득.
- 생존 숙련도: 오래 생존하거나 위험도를 높여 클리어하면 성장 재화 보너스.

### 경쟁

- 비동기 랭킹: 생존 시간, 최고 위험도, 보스 기여도, 누적 시즌 점수.
- 주간 시즌: 주간 보상과 칭호를 제공하되 과금/강제 PvP 없이 실력·운영 지표 중심.
- 옵트인 협동 경쟁: 같은 맵에서 경쟁하되 직접 방해보다 자원 선택/보스 딜/탈출 타이밍으로 차별화.

### 서바이벌

- 위험도 게이지: 시간이 지날수록 몬스터 밀도, 엘리트 등장, 환경 피해 증가.
- 생존 자원: 포션, 캠프/안전지대, 수리 키트, 이동 주문서 등 메이플식 소모품.
- 탈출 선택: 더 버티면 보상 증가, 실패하면 일부 보상 손실. 핵심 의사결정은 “지금 탈출할까, 한 웨이브 더 갈까?”로 고정.

## MVP 우선순위

| 우선순위 | 기능 | 수용 기준 |
|---:|---|---|
| P0 | 1개 핵심 맵 + 1개 세션 루프 | 입장→전투/생존→탈출/전멸→정산이 끊기지 않는다 |
| P0 | 전투/피해/보상 기본 시스템 | 사냥, 보스, 보상 획득, 세션 종료 보상이 정상 동작한다 |
| P0 | 공개 출시용 메타데이터 | 월드명/설명/장르/이미지/30초 영상/커뮤니티 링크 준비 |
| P1 | 성장 메타 | 계정 레벨, 장비 강화, 몬스터 도감 중 최소 2개 완성 |
| P1 | 랭킹 | 생존 시간 또는 시즌 점수 랭킹 1종 구현 |
| P1 | 튜토리얼/가이드 UI | 첫 60초 안에 목표, 생존 자원, 탈출 조건을 이해시킨다 |
| P2 | 시즌 운영 장치 | 주간 챌린지, 보상표, 공지/커뮤니티 운영 템플릿 |
| P2 | 확장 콘텐츠 | 신규 지역/몬스터/룬 추가가 데이터 중심으로 가능해야 한다 |

## 심사 기준별 개발 포인트

![핵심 재미 확장 사례](https://mod-static.dn.nexoncdn.co.kr/events/_nuxt/con01_deco_tab.i3xxJdRl.png)

| 심사 기준 | 개발 해석 | 해야 할 일 |
|---|---|---|
| IP 해석 및 확장 40% | 메이플의 성장·사냥·몬스터·아이템 파밍을 생존 원정 규칙으로 재조합 | 메이플 친화적 몬스터/지역/아이템 명명, 원작 감성 UI/이펙트 활용 |
| 완성도 40% | 짧은 세션에서도 버그 없이 반복 가능한 핵심 루프 | 세션 종료/재접속/보상 중복/랭킹 반영 안정성 우선 |
| 지속 가능성 20% | 시즌, 랭킹, 도감, 신규 지역으로 운영 가능한 구조 | 데이터셋 기반 밸런스, 주간 목표, 커뮤니티 챌린지 준비 |
| 결승 유저 평가 | 첫 세션 만족도와 부정 신고 최소화 | 강제 경쟁/과도한 실패 손실/불친절한 UI를 피한다 |

## 참가 지원/개발 지원 요소

![AI Toolkit 안내](https://mod-static.dn.nexoncdn.co.kr/events/_nuxt/contest-lounge-07.DFwVjYbE.png)

- 교육 자료, 전문가 Q&A, 전용 커뮤니티가 제공된다.
- 월드 개발 관련 문의는 글로벌 개발 콘테스트 디스코드를 통해 접수한다.
- 공식 페이지는 Claude Code, Codex, Cursor를 활용한 AI Toolkit/바이브 코딩 지원을 안내한다.
- 이 저장소의 리소스 구조는 Hermes가 코드/모델/UI/맵/데이터셋을 빠르게 찾아 재조합하기 위한 기준점으로 사용한다.

## Hermes 개발 착수 기준

1. `join_notice.md`의 출품 조건을 완료 정의에 포함한다.
2. P0 루프는 `maple-soul-hero`의 전투/스테이지/랭킹 구조와 `miner-simulator`의 자원 성장 구조를 먼저 참고한다.
3. 수집/장기 성장은 `monster-farm` 도감/컬렉션 구조를 후순위로 결합한다.
4. 직접 PvP는 MVP에서 제외하고, `maple-duel`의 랭킹/보상 UI 패턴만 가져온다.
5. 모든 기능은 “출품 가능한 신규 공개 월드”를 기준으로 검수한다.
