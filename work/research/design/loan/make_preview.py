# 대출 v1 시안 만들기 — 연봉 v5(디자인 통과 7.2) 토큰·CSS를 그대로 가져와 대출 화면만 붙인다. py -3.12 make_preview.py
from pathlib import Path
D = Path(__file__).resolve().parent
s = (D.parent / "tokens-ref/salary-v5/preview.html").read_text(encoding="utf-8")
head = s[s.index('<link rel="stylesheet"'):s.index('</style>')]

LOAN_CSS = r"""
/* ---- 대출 v1 추가(새 색 0·새 수치 0: 기존 토큰만) ---- */
.res .sub{margin-top:var(--s2);font-size:var(--fs-label);color:rgba(255,255,255,.64);line-height:1.5}
.res .sub b{color:#fff;font-weight:600}
.res .goal{margin-top:var(--s3);padding-top:var(--s3);border-top:1px solid rgba(255,255,255,.12);font-size:var(--fs-label);color:#fff;font-weight:600;display:none}
body.b .res .goal{display:block}
.xtra{padding:var(--s4)}
.xtra .hd{display:flex;justify-content:space-between;align-items:baseline}
.xtra .hd .k{font-size:var(--fs-label);color:var(--ink-2)}
.xtra .hd .v{font-size:var(--fs-body);font-weight:700}
.xtra input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:32px;background:transparent;margin:var(--s2) 0 0}
.xtra input[type=range]::-webkit-slider-runnable-track{height:6px;border-radius:3px;background:linear-gradient(var(--ink),var(--ink)) 0/var(--p,10%) 100% no-repeat,var(--field)}
.xtra input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:28px;height:28px;border-radius:50%;background:var(--card);border:2px solid var(--ink);margin-top:-11px;box-shadow:0 1px 4px rgba(0,0,0,.12)}
.xtra .out{margin-top:var(--s2);padding:var(--s3);background:var(--field);border-radius:var(--r-field);font-size:var(--fs-label);color:var(--ink-2);line-height:1.5}
.xtra .out b{color:var(--ink);font-weight:700}
.share{display:block;text-align:center;margin-top:var(--s3);font-size:var(--fs-label);color:var(--ink-3);font-weight:600;text-decoration:none}
.nw{white-space:nowrap}
.res .ex{display:inline-block;margin-left:var(--s1);padding:0 var(--s2);border-radius:var(--r-small);background:rgba(255,255,255,.12);font-size:var(--fs-caption);font-weight:600;color:rgba(255,255,255,.64);vertical-align:1px}
body.b .res .ex{display:none}
.res .sub,.xtra .out{word-break:keep-all}
@media (max-width:359px){.xtra{padding:var(--s3)}.xtra .out{padding:var(--s2) 12px}.xtra input[type=range]{margin:0}.res .sub{font-size:var(--fs-caption)}.res .q{font-size:var(--fs-caption)}}
.mt{width:100%;border-collapse:collapse;font-size:var(--fs-label);margin-bottom:var(--s3)}
.mt td{padding:var(--s2) 0;border-top:1px solid var(--line)}.mt td:last-child{text-align:right;font-weight:600}
.mt tr:first-child td{border-top:0}
"""

BODY = r"""</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute"><symbol id="chev" viewBox="0 0 16 16"><path d="M6 3.5 10.5 8 6 12.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol></svg>
<header class="top"><img src="../quality/ds-v2/icon-192.png" width="24" height="24" alt="" style="border-radius:6px"><b>파이어맵</b><nav class="menu"><a>연봉</a><a>퇴직금</a><a aria-current="page">대출</a></nav></header>
<main class="wrap">
  <h1>대출이자 계산기</h1>
  <div class="grid">
    <section class="card res" aria-live="polite">
      <div class="q">다 갚는 나이 <span class="ex">예시</span></div>
      <div class="n num" id="age">65<small>세</small></div>
      <div class="sub num"><span class="nw">매달 <b id="pay"></b></span> · <span class="nw">총이자 <b id="int"></b></span></div>
      <div class="goal num" id="goal"></div>
    </section>
    <section class="card cond" aria-label="조건">
      <button class="row" type="button"><span class="k">지금 나이</span><span class="v num">35세<svg class="chev"><use href="#chev"/></svg></span></button>
      <button class="row" type="button"><span class="k">대출 조건</span><span class="v num">3억원 · 4.5% · 30년<svg class="chev"><use href="#chev"/></svg></span></button>
    </section>
    <section class="card xtra">
      <div class="hd"><span class="k">매달 더 갚기</span><span class="v num" id="xv">10만원</span></div>
      <input type="range" id="x" min="0" max="1000000" step="10000" value="100000" aria-label="매달 더 갚는 금액">
      <div class="out num" id="xo"></div>
    </section>
    <div class="cta"><a href="#">이 돈이면 몇 살에 은퇴?</a></div>
    <section class="card list">
      <details>
        <summary class="row"><span>상환 방식별 총이자</span><span class="v"><svg class="chev"><use href="#chev"/></svg></span></summary>
        <table class="mt num" id="cmp"></table>
      </details>
      <details>
        <summary class="row"><span>매달 상환표</span><span class="v num" id="mn"></span></summary>
        <table class="mt num" id="sch"></table>
      </details>
      <details>
        <summary class="row"><span>계산 방법</span><span class="v"><svg class="chev"><use href="#chev"/></svg></span></summary>
        <p class="howto">[카피 몫] 월 이자 = 남은 원금 × 연 금리 ÷ 12. 총이자는 상환표 매달 이자의 합. 중도상환수수료는 빼고 계산.</p>
      </details>
    </section>
    <a class="share" href="#">결과 공유</a>
  </div>
  <p class="src">참고용 · 예시 값 · 중도상환수수료 미반영 [문구 최종은 copywriter·editor-web]</p>
</main>
<footer class="foot"><span>파이어맵</span><span>문의 · 개인정보처리방침 · 면책 안내</span></footer>
<script>
// 숫자는 운영 엔진 src/utils/loanRepay.js 식을 그대로 옮김(시안 확인용, 거치 기간 생략)
const pmt=(p,r,n)=>r===0?p/n:(p*r*(1+r)**n)/((1+r)**n-1);
function sched({principal:P,annualRate,months:n,method='equal',extraMonthly:extra=0}){const r=annualRate/100/12;const pay=method==='equal'?pmt(P,r,n):0;const fp=method==='principal'?P/n:0;const rows=[];let bal=P;
for(let m=1;m<=n&&bal>0.5;m++){const i=bal*r;let pr=method==='equal'?pay-i+extra:method==='principal'?fp+extra:extra;if(m===n||pr>=bal-0.5)pr=bal;bal-=pr;const payment=Math.round(pr+i),interest=Math.round(i);rows.push({m,payment,interest});}
return{rows,months:rows.length,first:rows[0].payment,ti:rows.reduce((s,x)=>s+x.interest,0)};}
const I={principal:300000000,annualRate:4.5,months:360},AGE=35,GOAL=55;
const won=v=>v.toLocaleString('ko-KR')+'원';
const man=v=>{const e=Math.floor(v/1e8),m=Math.floor(v%1e8/1e4);return (e?e+'억 ':'')+(m?m.toLocaleString('ko-KR')+'만':'')+'원';};
const ageAt=mo=>AGE+Math.floor(mo/12);
const chev='<svg class="chev"><use href="#chev"/></svg>';
const base=sched(I);
document.getElementById('age').innerHTML=ageAt(base.months)+'<small>세</small>';
document.getElementById('pay').textContent=won(base.first);document.getElementById('int').textContent=man(base.ti);
const k=ageAt(base.months)-GOAL;document.getElementById('goal').textContent=k>0?`은퇴 목표 ${GOAL}세 뒤에도 ${k}년 더 갚아요`:`은퇴 목표 ${GOAL}세 전에 끝나요`;
if(location.hash==='#b')document.body.classList.add('b');
const names={equal:'원리금균등',principal:'원금균등',bullet:'만기일시'};
document.getElementById('cmp').innerHTML=['equal','principal','bullet'].map(m=>`<tr><td>${names[m]}</td><td>${man(sched({...I,method:m}).ti)}</td></tr>`).join('');
const x=document.getElementById('x');
function upd(){const e=+x.value;x.style.setProperty('--p',(e/10000)+'%');document.getElementById('xv').textContent=e?(e/10000).toLocaleString('ko-KR')+'만원':'0원';
const w=sched({...I,extraMonthly:e});const sv=base.months-w.months,si=base.ti-w.ti;
document.getElementById('xo').innerHTML=e?`<span class=nw><b>${ageAt(w.months)}세</b>에 끝나요</span> · <span class=nw>${sv}개월 일찍</span> · <span class=nw>이자 ${man(si)} 덜</span>`:'움직이면 다 갚는 나이가 바뀌어요';
document.getElementById('mn').innerHTML=w.months+'회'+chev;
document.getElementById('sch').innerHTML=w.rows.slice(0,12).map(r=>`<tr><td>${r.m}회</td><td>${won(r.payment)}</td></tr>`).join('')+'<tr><td>…</td><td></td></tr>';}
x.addEventListener('input',upd);upd();
</script>
</body>
</html>
"""

TOP = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>대출이자 계산기 v1</title>
<!-- 대출 v1 시안 (firemap-designer 2026-10-05). make_preview.py로 생성 — 토큰·부품은 연봉 v5(디자인 통과 7.2)와 같음, 새 색·새 수치 0.
     숫자1 = 다 갚는 나이(다크 카드) · 행동1 = '이 돈이면 몇 살에 은퇴?'(주황, 연봉 운영 문구 재사용)
     더 갚기 슬라이더는 잉크색(주황은 행동 1곳만). #b = 파이어 저장값(inputsIsReal) 있는 방문자 상태. -->
"""
(D / "preview.html").write_text(TOP + head + LOAN_CSS + BODY, encoding="utf-8")
print("ok")
