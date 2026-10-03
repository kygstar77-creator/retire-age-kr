# cloud/r1-remake-1003 — R-1 '1억의 1년 영수증' 최종본 (2026-10-03)

PC가 할 일: `script.v6.md`를 `script.md`로 복사 → 한 회차·한 모델·tempo 1.0으로 녹음 → `r1props.py --script script.md` → 렌더(`src/index.ts`의 R1 또는 `src/motion/TallyRoot.tsx`). 썸네일은 `TallyRoot.tsx`의 `R1Thumb`.

## 파일
| 무엇 | 경로 |
|---|---|
| 대본 최종(말 192문장, 정확한 값은 `[자막]` 줄, 본문 계산기 없음 — RULES X-CALC-VID) | `work/research/longform/ep/R-1/script.v6.md` |
| 사실표(아래쪽 `[add-1003 …]` 줄 = cloud/content-depth-1003 보강안 2부, 줄마다 원래 출처 유지) | `work/research/longform/ep/R-1/facts.txt` |
| 미리보기 mp4 (1280×720, 목소리 없음, 문장 길이 = 글자 ÷ 5.65초) | `work/research/longform/ep/R-1/preview/r1_v6_preview_720p.mp4` |
| 장면 대표 프레임 28장 | `work/research/longform/ep/R-1/preview/stills/00_open.png` … `27_end.png` |
| 썸네일 1280×720 | `work/research/longform/ep/R-1/thumb_r1_final.png` |
| 비교판(우리 장면·썸네일 vs 참고 영상 같은 종류 장면, 링크 포함) | `work/research/longform/ep/R-1/preview/board_r1_v6.png` |
| 화면 코드 | `work/video/src/R1.tsx`, 부품 `work/video/src/motion/Tally*.tsx`(틀·숫자 굴러가기·막대·영수증·강조·표시·선 그래프) |
| 화면 재료 생성 | `work/research/longform/ep/R-1/r1props.py` → `work/video/r1.json` |
| 테스트 17개 | `work/tests/test_r1_script_v6.py` · `work/tests/test_r1_visual_v6.py` |
| 고정 댓글 초안·설명란 첫 줄 | 설명란: `ep/R-1/meta.json` desc 첫 줄(시리즈 재생목록 안내), 계산기 링크는 설명란 한 줄 · 고정 댓글만 |

실측(`speechcompare_script.py`): 숫자 73.9/1,000단어 · 숫자 2개 이상 문장 10% · 예상 12.65분(4,289자) · 렌더 12.69분.

고정 댓글 초안(사람이 PC에서 올림):
> 📌 영수증 숫자 원문은 설명란 '출처'에 있어요(한국은행 ECOS·금감원 비교공시·법령·거래소 종가). 지나간 1년 값이고 미래를 보장하지 않습니다.
> 내 돈이 1억이 아니라면, 은퇴 나이가 몇 년 당겨지는지 여기서 넣어 볼 수 있어요 → https://firemap.kr/?utm_source=youtube&utm_medium=pinned&utm_campaign=r-1
> 다음 영수증으로 어떤 돈을 뜯어볼까요?

## 참고 영상과 비교해 남은 차이(솔직하게)
1. **판의 밀도**: 소수몽키 판은 사진·캡처·표·손글씨 표시가 한 판에 4~6개 겹친다. 우리는 표시를 문장마다 하나씩 더하지만 판마다 2~3개라 아직 여백이 많다(특히 예금·SCHD 영수증 장면 왼쪽).
2. **사진·실사 없음**: 참고 영상은 실사 영상·인물 사진·기사 캡처로 장면 사이를 바꾼다. 우리는 규칙상(남의 사진·캡처 금지) 그래프와 도형뿐이라 장면 전환의 '그림 변화'가 작다.
3. **썸네일**: 참고 썸네일은 얼굴·일러스트 + 노랑/흰 두 줄 초대형 글자다. 우리는 막대 그림 + 두 줄 글자로 글자 크기는 비슷하지만 사람·그림이 없어 눈길이 약하다.
4. **진행자 존재감**: 소수몽키는 오른쪽에 진행자 화면이 늘 있다. 우리는 목소리뿐이다.
5. **장면 길이**: 문턱(53초)·예금 영수증(45초)·세금(44초)은 참고 영상의 판 교체 간격(20~28초, study/2026-09-30.md)보다 길다 — 판 안 표시가 바뀌긴 한다.
6. 참고 화면은 유튜브가 막혀 새로 못 받았고, 저장소의 낮은 해상도 프레임으로만 비교했다.
7. 목소리가 없어서 말과 화면 표시가 맞물리는 시점은 글자 수 추정이다 — 녹음 뒤 `r1props.py`를 다시 돌리면 실제 길이로 맞춰진다.
