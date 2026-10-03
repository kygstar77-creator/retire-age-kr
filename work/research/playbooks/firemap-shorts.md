# firemap-shorts 교본

## 경쟁 1등 사례
- SK하이닉스 주가 쇼츠 1위: 0cvYbJ7CdUE 경제스타 84.9만(사람 얼굴·목소리). 우리는 얼굴 대신 종가선 그림 표지로 다르게 간다(cardshorts/e1_hynix_dd/compete.md).

## 잘된 우리 사례
- 순자산 중앙값 자가·전세·월세(DNpdFtZyfE8) 3.8시간 444회 — 통계청 '내 위치' 비교형.
- 주담대 금리 은행 17곳 순위(rank) 325회/20시간.

## 실패 사례
- a1_need100: 카드 한 장이 표지를 겸해 1초 시험 4.2 → 첫 1초 표지 화면(cover/cover_png/cover_chart)을 따로 붙인다.
- 2026-10-03 커밋 때 다른 루틴이 add해 둔 파일(deadfin1003 등)이 내 커밋에 함께 들어감 — add 직전 `git diff --cached --name-only`로 내 파일만인지 본다.

## 체크리스트(공개 회차)
1. today.md 담당 일 → 착수 줄(`date`로 잰 시각)
2. shortsdaily status 막힘 없음
3. 사실표 '공개 전 다시 받는다' 메모가 있으면 원 출처 재조회해 저장본과 diff
4. check 문제 없음 · aitell → .edit.json(by auto, 해시)
5. publish → card·cover png 눈으로 보기 → 문제는 shorts-research.md '고칠 것'
6. 커밋은 cardshorts 파일만, 완료 줄은 today.md·decisions/log.md 둘 다, 상황판 시각도 `date` 값만

## 배운 것
- 2026-10-03: 시세 재조회는 `api.finance.naver.com/siseJson.naver?symbol=<코드>&requestType=1&startTime=..&endTime=..&timeframe=day`로 바로 받힌다(curl, 브라우저 불필요).
- 2026-10-03: 칸에 편을 배정할 때 `log.jsonl`의 facts와 겹치는지 먼저 본다. publish는 같은 사실표 두 번째 쇼츠를 막는다(e1_micron_q4가 E-1 하이닉스 뒤라 19:20에 걸림). 롱폼 사실표 하나로 쇼츠 여러 편 계획은 관문 다 넘겨도 못 나간다.
- 2026-10-03: 썸네일 지정은 `ytupload.service().thumbnails().set(videoId=..., media_body=MediaFileUpload(<편>_cover.png))` — 1080x1920 png 30KB 그대로 200 응답.
