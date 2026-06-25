import { useState, useEffect } from 'react';
import Header from './Header.jsx';
import CobeGlobe from './CobeGlobe.jsx';
import { QUESTIONS, ARCHETYPES, scoreAnswers, recommendCities } from '../../firemap-v2/cityTypeTest.js';
import { buildScenario } from '../../firemap-v2/scenarios.js';
import { shareToKakao } from '../../utils/kakaoShare.js';
import { track } from '../../firemap-v2/dailyData.js';

const won = (n) => `${Math.round(n / 10000).toLocaleString('ko-KR')}만원`;
const TEST_URL = 'https://firemap.kr/#firetype';

function Cover({ onStart }) {
  return (
    <div className="fm-ft-cover">
      <style>{COVER_CSS}</style>
      <div className="fm-ft-cover-glow" aria-hidden="true" />
      <p className="fm-ft-kick">9문항 · 30초</p>
      <h1 className="fm-ft-title">나는 어떤<br /><span>파이어족</span>일까?</h1>
      <p className="fm-ft-sub">유형 + 나에게 맞는 <b>국내·해외 도시 Top3</b>를 찾아드려요.<br />로그인 없이 바로 시작.</p>
      <button type="button" className="fm-ft-start" onClick={onStart}>테스트 시작하기 →</button>
      <p className="fm-ft-foot">결과는 추정이며 정보 제공용이에요 · 투자조언 아님</p>
    </div>
  );
}

function Quiz({ idx, onPick, onBack }) {
  const q = QUESTIONS[idx];
  const pct = Math.round((idx / QUESTIONS.length) * 100);
  return (
    <div className="fm-ft-quiz">
      <style>{QUIZ_CSS}</style>
      <div className="fm-ft-bar"><div className="fm-ft-bar-in" style={{ width: `${pct}%` }} /></div>
      <p className="fm-ft-step">{idx + 1} / {QUESTIONS.length}</p>
      <h2 className="fm-ft-q">{q.q}</h2>
      <div className="fm-ft-opts">
        {q.opts.map((o, i) => (
          <button type="button" key={i} className="fm-ft-opt" onClick={() => onPick(i)}>{o.t}</button>
        ))}
      </div>
      <button type="button" className="fm-ft-back" onClick={onBack}>← 이전</button>
    </div>
  );
}

function Result({ answers, simulation, onChange, onMove, onRestart }) {
  const { archetype: A, axes } = scoreAnswers(answers);
  const recs = recommendCities(axes, simulation, buildScenario, 3);
  const match = ARCHETYPES[A.match];
  const [reveal, setReveal] = useState(false);
  const [flash, setFlash] = useState('');
  useEffect(() => {
    track('firetype_result', { type: A.id, top: recs[0] && recs[0].city.city, qa: (answers || []).join(''), nq: (answers || []).length });
    try { localStorage.setItem('fm_firetype_done', '1'); } catch { /* 유형 확인 완료 → 홈 권유 팝업 중단 */ }
    const t = setTimeout(() => setReveal(true), 120);
    return () => clearTimeout(t);
  }, []);
  const markers = recs.map((r, i) => ({ location: [r.city.lat, r.city.lon], size: i === 0 ? 0.1 : 0.07 }));
  const top = recs[0];

  const share = async () => {
    track('firetype_share', { type: A.id });
    const title = `나는 ${A.name} (${A.nick}) ☕🔥`;
    const desc = `추천 도시 ${recs.map((r) => r.city.city).join('·')} · 9문항으로 내 파이어 유형 찾기`;
    const ogImg = `https://firemap.kr/og?mode=firetype&tn=${encodeURIComponent(A.name)}&nk=${encodeURIComponent(A.nick)}&ct=${encodeURIComponent(recs.map((r) => r.city.city).join('·'))}`;
    try { await shareToKakao({ title, description: desc, imageUrl: ogImg, linkUrl: TEST_URL }); return; }
    catch (e) { /* 폴백 */ }
    try { await navigator.clipboard.writeText(`${title}\n${desc}\n${TEST_URL}`); setFlash('링크를 복사했어요! 단톡방에 붙여넣어 보세요'); setTimeout(() => setFlash(''), 2500); }
    catch { /* ignore */ }
  };
  const copy = async () => { try { await navigator.clipboard.writeText(TEST_URL); setFlash('링크 복사 완료!'); setTimeout(() => setFlash(''), 2000); track('firetype_share', { type: A.id, via: 'copy' }); } catch { /* ignore */ } };
  const pickCity = (krw) => { if (onChange) { onChange('monthlyLivingCost', krw); if (onMove) onMove('result'); } else if (onMove) onMove('cities'); };

  return (
    <div className="fm-ft-result">
      <style>{RESULT_CSS}</style>
      <section className="fm-ft-hero" style={{ background: `linear-gradient(150deg, ${A.c1}, ${A.c2})` }}>
        <div className="fm-ft-hero-glow" aria-hidden="true" />
        <p className="fm-ft-hero-kick">내 파이어 유형</p>
        <div className={`fm-ft-emoji${reveal ? ' on' : ''}`}>{A.emoji}</div>
        <h1 className="fm-ft-name">{A.name}</h1>
        <p className="fm-ft-nick">“{A.nick}”</p>
        <p className="fm-ft-tag">{A.tagline}</p>
        <div className="fm-ft-sw">
          <span><b>강점</b> {A.strong}</span>
          <span><b>주의</b> {A.watch}</span>
        </div>
        <p className="fm-ft-match">잘 맞는 유형 · <b>{match.emoji} {match.nick}</b></p>
      </section>

      <section className="fm-ft-globe-wrap">
        <p className="fm-ft-sec">🌍 나에게 맞는 도시 Top 3</p>
        <CobeGlobe markers={markers} focus={top ? [top.city.lat, top.city.lon] : null} accent={A.c1} size={280} />
      </section>

      <div className="fm-ft-cards">
        {recs.map((r, i) => (
          <article key={r.city.city} className="fm-ft-card" style={{ borderColor: `${r.city.c1}55` }}>
            <div className="fm-ft-card-top">
              <span className="fm-ft-rank" style={{ background: `linear-gradient(135deg, ${r.city.c1}, ${r.city.c2})` }}>{i + 1}</span>
              <span className="fm-ft-cname"><b>{r.city.flag} {r.city.city}</b><em>{r.city.country} · 월 {won(r.city.krw)}</em></span>
              <span className="fm-ft-score" style={{ color: r.city.c1 }}>{r.score}<i>점</i></span>
            </div>
            <div className="fm-ft-scorebar"><div className="fm-ft-scorebar-in" style={{ width: reveal ? `${r.score}%` : '0%', background: `linear-gradient(90deg, ${r.city.c1}, ${r.city.c2})` }} /></div>
            <div className="fm-ft-parts">
              {Object.entries(r.parts).map(([k, v]) => (
                <span key={k} className="fm-ft-part"><em>{k}</em><i style={{ width: reveal ? `${v}%` : '0%', background: r.city.c1 }} /></span>
              ))}
            </div>
            {r.fireAge && <p className="fm-ft-fire">⏱️ 이 도시면 <b>{r.fireAge}세</b>에 파이어 가능</p>}
            <p className="fm-ft-blurb">{r.city.blurb}</p>
            <button type="button" className="fm-ft-citycta" onClick={() => pickCity(r.city.krw)}>{onChange ? '이 도시로 내 결과 보기' : '지역별 파이어 보기'} →</button>
          </article>
        ))}
      </div>

      {flash && <div className="fm-ft-flash" role="status">{flash}</div>}
      <div className="fm-ft-share">
        <button type="button" className="fm-ft-kakao" onClick={share}>💬 카카오로 공유하기</button>
        <div className="fm-ft-share-row">
          <button type="button" onClick={copy}>🔗 링크 복사</button>
          <button type="button" onClick={onRestart}>↺ 다시 하기</button>
        </div>
      </div>
      <p className="fm-ft-disc">결과·도시 점수는 입력·취향 기반 추정이에요. 실제 비용·비자·의료는 다를 수 있어요 · 투자조언 아님.</p>
    </div>
  );
}

export default function FireTypeTest({ simulation, onChange, onMove, onBack }) {
  const [stage, setStage] = useState('cover'); // 'cover' | 'quiz' | 'result'
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState([]);
  const start = () => { track('firetype_start'); setAnswers([]); setIdx(0); setStage('quiz'); };
  const pick = (oi) => {
    const next = [...answers]; next[idx] = oi; setAnswers(next);
    if (idx + 1 >= QUESTIONS.length) setStage('result'); else setIdx(idx + 1);
  };
  const back = () => { if (idx === 0) setStage('cover'); else setIdx(idx - 1); };
  const restart = () => { setStage('cover'); setIdx(0); setAnswers([]); };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="파이어 유형" onBack={onBack} />
      {stage === 'cover' && <Cover onStart={start} />}
      {stage === 'quiz' && <Quiz idx={idx} onPick={pick} onBack={back} />}
      {stage === 'result' && <Result answers={answers} simulation={simulation} onChange={onChange} onMove={onMove} onRestart={restart} />}
    </main>
  );
}

const COVER_CSS = `
.fm-ft-cover{ position:relative; text-align:center; padding:38px 20px 30px; border-radius:22px; overflow:hidden; background:radial-gradient(120% 90% at 50% 0%, #1b2350, #0b1024 70%); color:#fff; margin:6px 0 12px; }
.fm-ft-cover-glow{ position:absolute; inset:-40% 20% auto 20%; height:60%; background:radial-gradient(circle, #ff7a3c55, transparent 60%); filter:blur(20px); opacity:.6; }
.fm-ft-kick{ font-size:12px; letter-spacing:.06em; color:#ffd9c2; font-weight:800; margin:0 0 10px; position:relative; }
.fm-ft-title{ font-size:30px; line-height:1.22; font-weight:900; margin:0 0 14px; position:relative; }
.fm-ft-title span{ background:linear-gradient(90deg,#ff8a4c,#ffd166); -webkit-background-clip:text; background-clip:text; color:transparent; }
.fm-ft-sub{ font-size:13.5px; line-height:1.6; color:#c7cce0; margin:0 0 22px; position:relative; }
.fm-ft-start{ position:relative; width:100%; max-width:300px; padding:15px; border-radius:14px; border:0; font-size:15.5px; font-weight:800; color:#1a1330; background:linear-gradient(90deg,#ff8a4c,#ffd166); cursor:pointer; box-shadow:0 8px 26px #ff7a3c55; }
.fm-ft-foot{ font-size:11px; color:#8b91ad; margin:14px 0 0; position:relative; }
`;
const QUIZ_CSS = `
.fm-ft-quiz{ padding:8px 2px 20px; }
.fm-ft-bar{ height:7px; border-radius:99px; background:#eee; overflow:hidden; margin:6px 0 14px; }
.fm-ft-bar-in{ height:100%; background:linear-gradient(90deg,#ff5a00,#ffb020); transition:width .35s ease; }
.fm-ft-step{ font-size:12px; font-weight:800; color:#ff5a00; margin:0 0 6px; }
.fm-ft-q{ font-size:21px; font-weight:800; line-height:1.35; margin:0 0 18px; color:#15151b; }
.fm-ft-opts{ display:flex; flex-direction:column; gap:10px; }
.fm-ft-opt{ text-align:left; padding:16px; border-radius:14px; border:1.5px solid #ececec; background:#fff; font-size:14.5px; font-weight:600; color:#23242a; cursor:pointer; transition:transform .08s, border-color .15s, background .15s; }
.fm-ft-opt:hover{ border-color:#ff8a4c; background:#fff7f2; }
.fm-ft-opt:active{ transform:scale(.99); }
.fm-ft-back{ margin:16px auto 0; display:block; background:none; border:0; color:#9aa3bf; font-size:13px; font-weight:700; cursor:pointer; }
`;
const RESULT_CSS = `
.fm-ft-result{ padding:4px 0 22px; }
.fm-ft-hero{ position:relative; overflow:hidden; border-radius:22px; padding:26px 20px 20px; color:#fff; text-align:center; }
.fm-ft-hero-glow{ position:absolute; inset:-50% 10% auto 10%; height:70%; background:radial-gradient(circle,#ffffff66,transparent 60%); filter:blur(18px); }
.fm-ft-hero-kick{ font-size:12px; font-weight:800; opacity:.92; margin:0 0 6px; letter-spacing:.04em; position:relative; }
.fm-ft-emoji{ font-size:64px; line-height:1; margin:4px 0 8px; transform:scale(.4) rotate(-12deg); opacity:0; transition:transform .5s cubic-bezier(.2,1.4,.4,1), opacity .5s; position:relative; }
.fm-ft-emoji.on{ transform:scale(1) rotate(0); opacity:1; }
.fm-ft-name{ font-size:25px; font-weight:900; margin:0 0 2px; position:relative; }
.fm-ft-nick{ font-size:14.5px; font-weight:700; opacity:.95; margin:0 0 10px; position:relative; }
.fm-ft-tag{ font-size:13.5px; line-height:1.55; opacity:.95; margin:0 auto 14px; max-width:300px; position:relative; }
.fm-ft-sw{ display:flex; flex-direction:column; gap:6px; text-align:left; background:#ffffff22; border:1px solid #ffffff33; border-radius:14px; padding:12px 14px; font-size:12.5px; line-height:1.5; position:relative; }
.fm-ft-sw b{ opacity:.85; margin-right:4px; }
.fm-ft-match{ font-size:12.5px; opacity:.92; margin:12px 0 0; position:relative; }
.fm-ft-globe-wrap{ margin:18px 0 6px; padding:16px 0 6px; border-radius:22px; background:radial-gradient(120% 100% at 50% 0%, #141c3e, #0b1024 75%); }
.fm-ft-sec{ text-align:center; font-size:14px; font-weight:800; color:#e7ebff; margin:0 0 8px; }
.fm-ft-cards{ display:flex; flex-direction:column; gap:12px; margin-top:14px; }
.fm-ft-card{ background:#fff; border:1.5px solid #eee; border-radius:18px; padding:14px 14px 12px; }
.fm-ft-card-top{ display:flex; align-items:center; gap:10px; }
.fm-ft-rank{ width:30px; height:30px; flex:0 0 auto; border-radius:50%; color:#fff; font-weight:900; font-size:15px; display:flex; align-items:center; justify-content:center; }
.fm-ft-cname{ flex:1; min-width:0; display:flex; flex-direction:column; }
.fm-ft-cname b{ font-size:15px; color:#15151b; }
.fm-ft-cname em{ font-size:11.5px; color:#8a8f99; font-style:normal; }
.fm-ft-score{ font-size:24px; font-weight:900; }
.fm-ft-score i{ font-size:12px; font-weight:700; font-style:normal; margin-left:1px; }
.fm-ft-scorebar{ height:8px; border-radius:99px; background:#f0f0f3; overflow:hidden; margin:9px 0 8px; }
.fm-ft-scorebar-in{ height:100%; border-radius:99px; transition:width 1s cubic-bezier(.2,.8,.3,1); }
.fm-ft-parts{ display:flex; gap:6px; margin:0 0 8px; }
.fm-ft-part{ flex:1; display:flex; flex-direction:column; gap:3px; align-items:stretch; }
.fm-ft-part em{ font-size:10px; color:#9aa3bf; font-style:normal; text-align:center; }
.fm-ft-part i{ height:5px; border-radius:99px; transition:width .9s ease; opacity:.85; }
.fm-ft-fire{ font-size:12.5px; font-weight:800; color:#c2410c; background:#fff4ec; border-radius:10px; padding:8px 10px; margin:0 0 8px; }
.fm-ft-blurb{ font-size:12px; color:#6b6f76; line-height:1.5; margin:0 0 10px; }
.fm-ft-citycta{ width:100%; padding:10px; border-radius:11px; border:0; background:#1e2859; color:#fff; font-size:13px; font-weight:800; cursor:pointer; }
.fm-ft-flash{ text-align:center; font-size:13px; font-weight:700; color:#0f6e56; background:#e1f5ee; border-radius:12px; padding:10px; margin:14px 0 0; }
.fm-ft-share{ margin:16px 0 0; }
.fm-ft-kakao{ width:100%; padding:14px; border-radius:14px; border:0; background:#FAE100; color:#3c1e1e; font-size:15px; font-weight:800; cursor:pointer; }
.fm-ft-share-row{ display:flex; gap:8px; margin-top:8px; }
.fm-ft-share-row button{ flex:1; padding:11px; border-radius:11px; border:1.5px solid #e6e6e6; background:#fff; font-size:13px; font-weight:700; color:#444; cursor:pointer; }
.fm-ft-disc{ font-size:11px; color:#9aa3bf; line-height:1.5; text-align:center; margin:14px 4px 0; }
`;
