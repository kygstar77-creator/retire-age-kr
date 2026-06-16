import { useEffect, useRef, useState } from 'react';
import { wonStr } from '../../firemap-v2/dailyData.js';
import { computePet } from '../../utils/pet.js';
import { identityIds } from '../../utils/identity.js';
import { fetchWeeklySaveBoard } from '../../utils/firemapSaveApi.js';

const STYLE = `
.fm-petcard{text-align:center}
.fm-pet-art{display:flex;justify-content:center;align-items:flex-end;min-height:150px}
.fm-pet-art svg{width:148px;height:auto;animation:fmPetBob 3s ease-in-out infinite;transform-origin:50% 80%}
.fm-pet-art.evo svg{animation:fmPetPop .8s ease}
@keyframes fmPetBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes fmPetPop{0%{transform:scale(.5) rotate(-10deg);opacity:.3}55%{transform:scale(1.15) rotate(5deg);opacity:1}100%{transform:scale(1)}}
.fm-pet-name{font-weight:800;font-size:18px;color:#18212c;margin:2px 0}
.fm-pet-rank{margin:2px 0 0;font-size:13px;font-weight:800;color:#b45309}
.fm-pet-bar{height:10px;background:#eef0f3;border-radius:99px;overflow:hidden;margin:10px auto 6px;max-width:320px}
.fm-pet-bar-fill{height:100%;background:linear-gradient(90deg,#ff8a3d,#ff5a00);border-radius:99px;transition:width .6s ease}
.fm-pet-cap{font-size:13px;color:#4b5563;margin:2px 0}
.fm-pet-cap b{color:#c2410c}
.fm-pet-total{font-size:12px;color:#8a93a0;margin-top:6px}
.fm-pet-evolve{margin-top:10px;background:#fff4e8;color:#c2410c;font-weight:800;border-radius:12px;padding:9px 12px;font-size:14px;animation:fmPetPop .6s ease}
`;

function Crown() {
  return <path d='M84 10 l9 18 17 -16 17 16 9 -18 -5 30 -42 0 z' fill='#ffd23f' stroke='#e0a92a' strokeWidth='2' strokeLinejoin='round' />;
}

function Raccoon({ idx }) {
  if (idx <= 0) {
    return (
      <g>
        <ellipse cx='110' cy='120' rx='50' ry='62' fill='#f3ead7' stroke='#d8c8a6' strokeWidth='3' />
        <ellipse cx='95' cy='142' rx='7' ry='5' fill='#e7d7b1' />
        <ellipse cx='128' cy='100' rx='6' ry='4' fill='#e7d7b1' />
        <polyline points='80,114 98,104 88,122 110,110 100,128 124,116' fill='none' stroke='#caa86b' strokeWidth='3' strokeLinejoin='round' strokeLinecap='round' />
      </g>
    );
  }
  const gold = idx >= 5;
  const body = gold ? '#f5c451' : '#9aa6b2';
  const dark = gold ? '#c9962a' : '#5b6b7a';
  const belly = gold ? '#fff3cf' : '#eef2f6';
  const scale = [0, 0.78, 0.86, 0.93, 0.99, 1.05][idx] || 1;
  return (
    <g transform={`translate(110 108) scale(${scale}) translate(-110 -108)`}>
      {idx >= 5 && <Crown />}
      <circle cx='158' cy='124' r='18' fill={body} />
      <circle cx='171' cy='104' r='16' fill={dark} />
      <circle cx='181' cy='86' r='13' fill={body} />
      <circle cx='189' cy='70' r='11' fill={dark} />
      <ellipse cx='110' cy='150' rx='48' ry='44' fill={body} />
      <ellipse cx='110' cy='158' rx='30' ry='30' fill={belly} />
      {idx >= 4 && <path d='M82 126 Q110 138 138 126 L136 138 Q110 149 84 138 Z' fill='#ef6b53' />}
      <circle cx='110' cy='84' r='46' fill={body} />
      <circle cx='78' cy='46' r='16' fill={body} /><circle cx='78' cy='48' r='8' fill={dark} />
      <circle cx='142' cy='46' r='16' fill={body} /><circle cx='142' cy='48' r='8' fill={dark} />
      <path d='M70 86 Q110 68 150 86 Q152 106 130 110 Q110 102 90 110 Q68 106 70 86 Z' fill='#3f4b57' />
      <ellipse cx='92' cy='90' rx='10' ry='12' fill='#fff' /><ellipse cx='128' cy='90' rx='10' ry='12' fill='#fff' />
      <circle cx='93' cy='93' r='5' fill='#1c2530' /><circle cx='127' cy='93' r='5' fill='#1c2530' />
      <circle cx='95.5' cy='90' r='1.6' fill='#fff' /><circle cx='129.5' cy='90' r='1.6' fill='#fff' />
      <ellipse cx='110' cy='112' rx='22' ry='16' fill={belly} />
      <ellipse cx='110' cy='104' rx='6' ry='4.5' fill='#2a333d' />
      <path d='M110 108 Q110 117 103 119 M110 108 Q110 117 117 119' stroke='#2a333d' strokeWidth='2' fill='none' strokeLinecap='round' />
      {idx >= 2 && (
        <g>
          <ellipse cx='92' cy='172' rx='9' ry='7' fill={body} />
          <ellipse cx='128' cy='172' rx='9' ry='7' fill={body} />
          <circle cx='110' cy='178' r='15' fill='#f6c945' stroke='#e0a92a' strokeWidth='3' />
          <text x='110' y='184' textAnchor='middle' fontSize='15' fontWeight='800' fill='#b9821a'>₩</text>
        </g>
      )}
      {idx >= 4 && (
        <g>
          <ellipse cx='56' cy='182' rx='14' ry='5' fill='#e0a92a' />
          <ellipse cx='56' cy='176' rx='14' ry='5' fill='#f6c945' />
          <ellipse cx='56' cy='170' rx='14' ry='5' fill='#ffd76b' />
        </g>
      )}
      {idx >= 4 && (
        <g fill='#ffd23f'>
          <path d='M40 58 l3 7 7 3 -7 3 -3 7 -3 -7 -7 -3 7 -3 z' />
          <path d='M180 150 l2.5 6 6 2.5 -6 2.5 -2.5 6 -2.5 -6 -6 -2.5 6 -2.5 z' />
        </g>
      )}
    </g>
  );
}

export default function PetCard() {
  const [pet, setPet] = useState(() => computePet());
  const [evo, setEvo] = useState(null);
  const [weeklyRank, setWeeklyRank] = useState(null);
  const seen = useRef(null);

  useEffect(() => {
    let last = null;
    try { last = localStorage.getItem('fm_pet_stage'); } catch { /* ignore */ }
    const cur = computePet();
    if (last == null) { try { localStorage.setItem('fm_pet_stage', String(cur.idx)); } catch { /* ignore */ } }
    seen.current = last == null ? cur.idx : Number(last);
    setPet(cur);
    const onChange = () => {
      const p = computePet();
      setPet(p);
      if (p.idx > seen.current) {
        seen.current = p.idx;
        try { localStorage.setItem('fm_pet_stage', String(p.idx)); } catch { /* ignore */ }
        setEvo(p.stage.name);
        window.setTimeout(() => setEvo(null), 4200);
      }
    };
    window.addEventListener('fm-savings-changed', onChange);
    return () => window.removeEventListener('fm-savings-changed', onChange);
  }, []);

  useEffect(() => {
    let alive = true;
    const ids = identityIds();
    const run = () => fetchWeeklySaveBoard(10).then((rows) => {
      if (!alive) return;
      const i = (rows || []).findIndex((r) => r.client_id && ids.includes(r.client_id));
      setWeeklyRank(i >= 0 ? i + 1 : null);
    });
    run();
    window.addEventListener('fm-savings-changed', run);
    return () => { alive = false; window.removeEventListener('fm-savings-changed', run); };
  }, []);

  const { idx, stage, next, pct, toNext, total } = pet;
  const rankMark = weeklyRank === 1 ? '👑' : weeklyRank === 2 ? '🥈' : weeklyRank === 3 ? '🥉' : '';
  return (
    <section className='fm-card fm-petcard'>
      <style>{STYLE}</style>
      <p className='fm-pet-name'>{stage.name}{idx >= 5 ? ' 👑' : ''}</p>
      {weeklyRank && weeklyRank <= 3 && <p className='fm-pet-rank'>{rankMark} 이번 주 절약왕 {weeklyRank}위!</p>}
      <div className={`fm-pet-art${evo ? ' evo' : ''}`}>
        <svg viewBox='0 0 220 210' role='img' aria-label={stage.name}>
          <Raccoon idx={idx} />
        </svg>
      </div>
      {next
        ? (
          <>
            <div className='fm-pet-bar'><div className='fm-pet-bar-fill' style={{ width: `${pct}%` }} /></div>
            <p className='fm-pet-cap'>다음 진화 <b>{next.name}</b>까지 <b>{wonStr(toNext)}</b> 더!</p>
          </>
        )
        : <p className='fm-pet-cap'>최종 진화 완료 — 황금 너구리예요 ✨</p>}
      <p className='fm-pet-total'>{total > 0 ? <>지금까지 모은 누적 저축·절약 <b>{wonStr(total)}</b></> : '저축·절약을 기록하면 알이 부화해요'}</p>
      {evo && <div className='fm-pet-evolve'>🎉 진화! <b>{evo}</b>가 됐어요</div>}
    </section>
  );
}
