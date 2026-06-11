# maple — MSWRemake 리소스 정리

[MSW-Git/MSWRemake](https://github.com/MSW-Git/MSWRemake) (MIT License)의 메이플스토리 월드
리메이크 6종을 **카테고리별로 사용 가능하도록** 재구성한 리소스 모음입니다.

```
maple/
├── README.md          ← 이 문서
├── MSWRemake/         ← 업스트림 원본 클론 (월드별 원래 구조 그대로, 재가져오기용)
└── resource/          ← 카테고리별로 재구성한 리소스 (이 폴더를 사용)
```

## 폴더 구조

```
resource/
├── _common/                    # 전 월드 공통 (중복 제거됨)
│   └── NativeScripts/          # MSW 엔진 내장 API 정의 660개 (.d.mlua)
│       ├── Component/          #   엔진 컴포넌트 정의 (Transform, Sprite, Physics …)
│       ├── Event/              #   엔진 이벤트 정의
│       ├── Logic/              #   엔진 로직/서비스 정의
│       └── Misc/               #   기타 타입 정의
├── chu-chu-burger/             # [Remake] Chu Chu Burger the 1st Branch
├── maple-auto-battler/         # [Remake] Maple Auto Battler
├── maple-duel/                 # [Remake] Maple Duel
├── maple-soul-hero/            # [Remake] Maple Soul Hero
├── miner-simulator/            # [Remake] Miner Simulator
└── monster-farm/               # [Remake] Monster Farm
```

각 월드 폴더는 동일한 카테고리 체계를 따릅니다.
원본 `RootDesk/MyDesk/` 내부의 하위 폴더 경로는 카테고리 안에 그대로 보존되어 있습니다.

| 카테고리 | 확장자 | 내용 |
|---|---|---|
| `scripts/` | `.mlua` `.codeblock` `.scriptfile` | 게임 로직 스크립트 (mlua 소스 + 코드블록 페어) |
| `models/` | `.model` | 게임 오브젝트 프리팹/모델 정의 |
| `ui/` | `.ui` | UI 화면/레이아웃 정의 |
| `maps/` | `.map` | 맵 데이터 |
| `tilesets/` | `.tileset` | 맵 제작용 타일셋 |
| `sprites/` | `.sprite` `.blueprintatlas` | 스프라이트/아틀라스 리소스 |
| `materials/` | `.material` | 렌더링 머티리얼 |
| `datasets/` | `.csv` `.userdataset` `.localedataset` | 밸런스 테이블·유저 데이터셋·로컬라이즈 테이블 |
| `sounds/` | `.sound` | 사운드 리소스 |
| `global/` | `.config` `.logic` `.gamelogic` `.collisiongroupset` `.bodyaction` `.avataraction` 등 | 월드 전역 설정 (충돌 그룹, 커스텀 아바타 액션 등) |

## 월드별 리소스 현황 (파일 수)

| 월드 | scripts | models | ui | maps | tilesets | sprites | materials | datasets | sounds | global |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `chu-chu-burger` | 1,208 | 305 | 57 | 12 | 13 | 45 | 51 | 276 | – | 8 |
| `maple-auto-battler` | 1,690 | 74 | 34 | 2 | 1 | – | 76 | 164 | – | 8 |
| `maple-duel` | 280 | 1,036 | 3 | 2 | – | 23 | 33 | 12 | 1 | 8 |
| `maple-soul-hero` | 1,132 | 944 | 57 | 12 | 11 | 37 | 33 | 204 | – | 11 |
| `miner-simulator` | 549 | 740 | 34 | 44 | – | 198 | 25 | 80 | – | 9 |
| `monster-farm` | 401 | 1,189 | 25 | 3 | 2 | 131 | – | 124 | – | 9 |

총 12,086개 파일 (공통 NativeScripts 660개 포함).

## 월드별 특징 (scripts 주요 구성 기준)

- **chu-chu-burger** — 햄버거 가게 타이쿤. 단계별 폴더 구성(`00. Player` ~ `11. Employment`):
  직원/주방기구/레시피/손님/트레이닝/경영 시스템. 타이쿤류 제작 참고에 적합.
- **maple-auto-battler** — 오토 배틀러. `InGame`/`OutGame` 분리 구조, `UIComponents`,
  `DataStorage`, `DatasetCacheLogic`, 로컬라이즈 테이블(`.localedataset`) 활용 예시.
- **maple-duel** — 카드 게임. 스크립트는 적지만 모델 1,036개로 카드 리소스가 풍부.
  `Components`/`Events`/`Logics` 의 깔끔한 3분할 아키텍처 참고용.
- **maple-soul-hero** — 방치형 RPG. 전투/버프/제작/수집/캐시샵/일일보상 등
  RPG 시스템 모듈이 가장 다양함 (scripts 1,132 + models 944).
- **miner-simulator** — 채광 시뮬레이터. 맵 44개로 멀티 스테이지 맵 구성 참고에 최적.
  업적(`Achievement`)·상호작용 오브젝트 스크립트 다수.
- **monster-farm** — 몬스터 농장. 도감(`Book`/`Collection`)·요리(`Cook`)·
  로컬라이제이션 컴포넌트 패턴 참고용. 모델 1,189개.

## 사용 방법

### 1. 카테고리 리소스 참고/재사용
필요한 카테고리 폴더를 직접 탐색합니다. 예:

```bash
# 솔 히어로의 전투 스크립트 보기
ls "resource/maple-soul-hero/scripts/Battle/"

# 모든 월드의 인벤토리 관련 스크립트 검색
grep -ril "inventory" resource/*/scripts/
```

`.mlua` 는 같은 이름의 `.codeblock` 과 페어로 동작하므로 재사용 시 두 파일을 함께 복사하세요.

### 2. 엔진 API 정의 참조
`resource/_common/NativeScripts/` 의 `.d.mlua` 파일들은 MSW 엔진 내장 컴포넌트·이벤트·로직의
타입 정의입니다. 6개 월드 모두 동일한 사본을 포함하고 있어 1벌로 중복 제거했습니다.

### 3. 월드 전체를 MSW Maker로 가져오기
카테고리 재구성본이 아닌 **`MSWRemake/` 원본**을 사용해야 합니다
([공식 가이드](https://maplestoryworlds-creators.nexon.com/docs?postId=1165)):

1. MapleStory Worlds Maker에서 새 월드 생성
2. **Workspace → WorldConfig → LocalWorkspace** 활성화
3. 로컬 워크스페이스 폴더의 파일을 모두 삭제
4. `MSWRemake/[Remake] <월드명>/` 의 전체 파일을 워크스페이스 폴더로 복사
5. **Workspace → MyDesk 우클릭 → Reimport All**

## 비고

- `resource/` 는 `MSWRemake/` 에서 APFS clone copy(`cp -c`)로 생성되어 추가 디스크를 거의 차지하지 않습니다.
- MSW 에디터 폴더 메타파일(`.directory`, 689개)은 카테고리 뷰에서 제외했습니다. 원본은 `MSWRemake/` 에 그대로 있습니다.
- 원본 라이선스: MIT (`MSWRemake/LICENSE`)
