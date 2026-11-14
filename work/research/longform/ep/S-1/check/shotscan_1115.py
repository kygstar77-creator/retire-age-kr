# S-1 shot_plan 경쟁 장면 — 제미나이가 YouTube URL로 영상을 직접 봄(다운로드 없음). 2026-11-15 youtube-loop
import sys, os, json
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
_args = sys.argv[1:]; sys.argv = sys.argv[:1]  # ytbreak은 import 때 argv 영상을 통째로 쪼갬 — 비운다
import ytbreak
VIDS = _args or ['UeYfy8Fww2w', 'Jeo-92g8a4g', 'QLadzq-tb4A', 'g0fWUHvOexQ']
P = ('이 영상의 화면(그림)만 본다. 실적 숫자·주가 움직임·과거 비교를 화면에 어떻게 보여 줬는지 장면 5개를 고른다. '
     '각 줄: "m:ss — 화면에 보인 것(종류: 실사/AI 생성 인물·장면/표/막대·선 그래프/달력/큰 숫자 카드/뉴스·남의 캡처/움직이는 그래픽 중) — 어떻게 움직였나". '
     '시각은 실제로 확인한 것만, 모르면 쓰지 말 것. 말한 내용 요약은 쓰지 않는다. 한국어, 5줄만.')
out = os.path.join(os.path.dirname(__file__), 'shotscan_1115.txt')
with open(out, 'a', encoding='utf-8') as f:
    for v in VIDS:
        try:
            m, r = ytbreak.ask(v, P, 4000); r = 'model ' + str(m) + chr(10) + str(r)
        except Exception as e:
            r = f'실패 {e}'
        f.write(f'\n## {v}\n{r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)}\n'); f.flush()
        print(v, 'done')
