# 조직도 PNG 만들기 (비주얼 디자이너, 2026-09-30) — HTML을 그려 Playwright로 1080×1920 캡처한다.
#   py -3.12 work/research/design/org-chart/make_org_chart.py  → 같은 폴더 org-chart.png, org-chart.html
# 인원·근무 시각은 예약 작업(cron) 실측 2026-09-30 23:50 기준. agents.md와 다르면 cron이 맞다.
import pathlib, sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

HERE = pathlib.Path(__file__).resolve().parent
FONT = (HERE.parents[3] / 'public' / 'fonts' / 'PretendardVariable.woff2').as_uri()

# (본부, [(자리, 역할 한 줄, 근무)])
TEAMS = [
    ('콘텐츠', [
        ('유튜브·카페 총괄', '기획·대본·카페 운영', '4시간마다'),
        ('영상 PD', '롱폼 제작·예약 공개', '4시간마다'),
        ('쇼츠 PD', '쇼츠 하루 1편', '19:20'),
        ('카페·블로그 작가', '카페 글 하루 5편', '하루 5회'),
        ('카피라이터', '제목·썸네일 문구', '07:20+호출'),
        ('문장 편집자', '사람 말투로 다듬기', '06:50+호출'),
    ]),
    ('제품', [
        ('제품 개발', '계산기·웹앱 개발', '11:10·17:10'),
        ('전담 디자이너', '웹 화면 설계', '일 10:20+호출'),
        ('디자인 개선', '디자인 리뷰·조정', '하루 3회'),
    ]),
    ('디자인실', [
        ('비주얼 디자이너', '썸네일·인포그래픽', '월 09:10+호출'),
        ('모션 디자이너', '영상 속 그래픽', '월 11:20+호출'),
        ('일러스트레이터', '사물·아이콘 그림', '수 13:40+호출'),
    ]),
    ('운영·품질', [
        ('감사관', '독립 감사·정지 스위치', '07:40·19:40'),
        ('발행 감시', '발행 누락 감시', '하루 4회 :45'),
        ('생산·개선', '자료조사·도구 고치기', '14:30·22:30'),
        ('보고 비서', '일일 보고', '12:30'),
    ]),
    ('성장·수익', [
        ('성장·유입', '유입·검색 노출', '10:40·16:40'),
        ('사업개발', '수익 전략 재계산', '월 10:15'),
    ]),
    ('브랜드', [
        ('브랜드 디렉터', '브랜드 가이드', '10:00'),
        ('브랜드 리서처', '시청자·회원 조사', '08:30'),
    ]),
    ('신사업·지원', [
        ('신사업본부장', '신사업 · 새 사업 출시', '13:10·20:10'),
        ('예술가', '크리에이티브 · 뻔함 점검', '11:40'),
        ('총무·인사팀', '도구·한도·직원 관리', '07:00·19:00'),
        ('AI 연구소장', '새 AI 도구 시험', '월·목 09:30'),
    ]),
]
LEFT = ['콘텐츠', '운영·품질', '브랜드']
FLOW = ['경쟁 비교', '카피라이터', '문장 편집자', '디자이너 시안', '제작', '심사·레드팀', '발행', '감사·클릭률', '밤 회의']
STAFF = sum(len(p) for _, p in TEAMS) + 2  # + 전체 회의 의장, 운영실장


def team_html(name, people):
    rows = ''.join(
        f'<div class="p"><div class="l1"><b>{n}</b><span class="t">{t}</span></div><div class="r">{r}</div></div>'
        for n, r, t in people)
    return f'<section class="team"><h3>{name}<em>{len(people)}</em></h3>{rows}</section>'


def build():
    left = ''.join(team_html(n, p) for n, p in TEAMS if n in LEFT)
    right = ''.join(team_html(n, p) for n, p in TEAMS if n not in LEFT)
    flow = ''.join(f'<span class="f"><em>{i + 1}</em>{s}</span>' for i, s in enumerate(FLOW))
    staff_in_units = sum(len(p) for _, p in TEAMS)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url("{FONT}") format("woff2");font-weight:100 900}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;background:#f6f7f9;color:#18191d;font-family:P,sans-serif;padding:30px 32px 0;
  font-variant-numeric:tabular-nums;letter-spacing:0;overflow:hidden}}
header{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px}}
h1{{font-size:52px;font-weight:700;line-height:1.2}}
.meta{{font-size:28px;color:#5d616b}} .meta b{{color:#ff5a00;font-weight:700}}
.card{{background:#fff;border-radius:20px;padding:10px 20px}}
.k{{font-size:28px;color:#6b6f78;line-height:1.25}}
.v{{font-size:34px;font-weight:700;line-height:1.25}}
.boss{{background:#18191d;color:#f2f3f5;border-radius:20px;padding:14px 22px 16px}}
.boss .k{{color:#a9adb6}}
.pair{{display:grid;grid-template-columns:1fr 56px 1.25fr;align-items:center}}
.arrow{{font-size:40px;color:#ff5a00;text-align:center;font-weight:700}}
.o{{color:#ff5a00}}
.advl{{display:flex;align-items:center;gap:10px;margin-top:12px;padding-top:12px;border-top:1px solid #33343b;flex-wrap:nowrap}}
.advl .k{{white-space:nowrap}}
.chip{{font-size:28px;background:#26272e;border-radius:12px;padding:3px 12px;font-weight:600;white-space:nowrap}}
.chip i{{font-style:normal;color:#a9adb6;font-weight:400}}
.stem{{width:3px;height:24px;background:#ff5a00;margin:0 auto}}
.row3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}}
.row3 .v{{font-size:30px}}
.bus{{position:relative;height:14px}}
.bus:before{{content:"";position:absolute;left:25%;right:25%;top:0;height:3px;background:#ff5a00}}
.bus:after{{content:"";position:absolute;left:calc(50% - 1.5px);top:0;width:3px;height:14px;background:#ff5a00}}
.lab{{text-align:center;margin-bottom:12px}}
.lab span{{display:inline-block;font-size:28px;font-weight:700;background:#18191d;color:#fff;border-radius:999px;padding:4px 20px}}
.lab b{{color:#ff5a00}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}}
.col{{display:flex;flex-direction:column;gap:12px}}
.team{{background:#fff;border-radius:20px;padding:10px 20px 4px}}
h3{{font-size:28px;font-weight:700;color:#ff5a00;margin-bottom:0;display:flex;justify-content:space-between}}
h3 em{{font-style:normal;color:#6b6f78;font-weight:600}}
.p{{padding:3px 0 4px;border-top:1px solid #eceef1}}
.team h3+.p{{border-top:0}}
.l1{{display:flex;justify-content:space-between;align-items:baseline;gap:8px;white-space:nowrap}}
.l1 b{{font-size:30px;font-weight:700;line-height:1.2}}
.t{{font-size:28px;color:#6b6f78;font-weight:400}}
.r{{font-size:28px;color:#33363d;line-height:1.2;white-space:nowrap}}
footer{{margin-top:22px}}
footer h2{{font-size:30px;font-weight:700;margin-bottom:8px}}
.flow{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px 30px}}
.f{{position:relative;font-size:28px;font-weight:600;background:#fff;border-radius:12px;padding:5px 12px;white-space:nowrap}}
.f em{{font-style:normal;color:#ff5a00;margin-right:8px;font-weight:700}}
.f:after{{content:"→";position:absolute;right:-24px;top:5px;color:#ff5a00;font-weight:700}}
.f:nth-child(3n):after,.f:last-child:after{{content:""}}
</style></head><body>
<header><h1>파이어맵 조직도</h1><div class="meta">직원 <b>{STAFF}</b>명 · 9/30 기준</div></header>
<div class="boss">
  <div class="pair">
    <div><div class="k">대표</div><div class="v">사장님</div><div class="k">결재·결제만</div></div>
    <div class="arrow">→</div>
    <div><div class="k">공동대표·지휘</div><div class="v o">순돌이</div><div class="k">조직·전략·직원 관리·보고</div></div>
  </div>
  <div class="advl"><span class="k">참모 5</span><span class="chip">전략·사용자·법 <i>제미나이</i></span><span class="chip">검증 <i>Claude</i></span><span class="chip">반론 <i>GPT-6 Astra</i></span></div>
</div>
<div class="stem"></div>
<div class="row3">
  <div class="card"><div class="v">레드팀</div><div class="k">반론 · 큰 결정 전</div></div>
  <div class="card"><div class="v">전체 회의</div><div class="k">의장 · 매일 21:15</div></div>
  <div class="card"><div class="v">운영실장</div><div class="k">호출 배차 · 매시 :05</div></div>
</div>
<div class="stem"></div>
<div class="lab"><span>순돌이 아래 부서 직원 <b>{staff_in_units}</b>명</span></div>
<div class="cols"><div class="col">{left}</div><div class="col">{right}</div></div>
<footer><h2>결과물 만드는 순서</h2><div class="flow">{flow}</div></footer>
</body></html>"""


def main():
    html = HERE / 'org-chart.html'
    html.write_text(build(), encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto(html.as_uri())
        pg.wait_for_timeout(400)
        over = pg.evaluate('''() => {const f=document.querySelector('footer').getBoundingClientRect();
          const bad=[...document.querySelectorAll('.l1,.r,.f')].filter(e=>e.scrollWidth>e.clientWidth+1||e.getBoundingClientRect().right>1080).length;
          return {footerBottom: Math.round(f.bottom), overflowItems: bad}}''')
        print(over)
        pg.screenshot(path=str(HERE / 'org-chart.png'))
        b.close()


if __name__ == '__main__':
    main()
