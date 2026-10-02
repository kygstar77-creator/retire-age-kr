// N-1 "나 vs 남들 ① 연봉·순자산 줄" — 재료: work/video/n1.json(ep/N-1/n1props.py가 script.md·voice.json·원자료로 만든다)
// 장면 종류 17가지: 빈칸 카드+100칸 띠 · 사람 점 100줄 · 100칸 막대(넘침 끊김) · 자리표+띠 · 연봉-백분위 선+화살표 비교 · 9칸 가로 막대+괄호 ·
// 금액 카운트+띠 쪼개기 · 쌍둥이 막대 · 백분위 눈금자+핀 · 중앙값/평균 막대 · 5칸 띠(점유율) · 좌우 증감 막대 · 12칸 달력 · 카드 3장 · 두 줄 핀 · 계산기 화면 · 로고
// 숫자는 전부 n1.json에서 온다(코드 안에는 눈금·배치 값만). 단계 시점은 data.at(문장 번호, 못 찾으면 −1=안 나옴).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {line as d3line, curveMonotoneX} from 'd3-shape';
import {T, F, CL, FONT_CSS, VScene, at, appear, CountUp, Page, LogoSting, ProgressRail} from './parts/fm';
import {PctStrip, HundredBars, PctRuler, DivergeRows} from './parts/rank';

export type N1Props = {fps: number; rail: string[]; scenes: VScene[]; missing: number; holes: number};
export const n1Frames = (p: N1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: VScene};
const NEVER = 1e9;
const A = (s: VScene, k: number) => (s.data.at?.[k] ?? -1) < 0 ? NEVER : at(s, s.data.at[k]);
const RailCtx = React.createContext<string[]>([]);
const n0 = (v: number) => v.toLocaleString();
const won = (m: number) => m >= 10000 ? (m % 10000 ? `${Math.floor(m / 10000)}억 ${n0(m % 10000)}만원` : `${m / 10000}억원`) : `${n0(m)}만원`;
const sgn = (v: number) => (v > 0 ? '+' : v < 0 ? '−' : '') + n0(Math.abs(v));
const Card: React.FC<{x: number; y: number; w: number; h?: number; o?: number; bg?: string; style?: React.CSSProperties; children?: React.ReactNode}> = ({x, y, w, h, o = 1, bg = T.surface, style, children}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: bg, borderRadius: 20, opacity: o, ...style}}>{children}</div>
);
const Chip: React.FC<{x: number; y: number; o: number; text: string; dark?: boolean; size?: number}> = ({x, y, o, text, dark = true, size = 32}) => (
  <div style={{...F, position: 'absolute', left: x, top: y, opacity: o, fontWeight: 700, fontSize: size, color: dark ? '#fff' : T.ink, background: dark ? T.ink : T.soft,
    borderRadius: 40, padding: '10px 28px', whiteSpace: 'nowrap'}}>{text}</div>
);
const P: React.FC<S & {children: React.ReactNode}> = ({s, children}) => {
  const rail = React.useContext(RailCtx);
  return <Page s={{...s, rail: 0}}>{s.rail ? <ProgressRail n={rail.length} cur={s.rail} labels={rail} on={T.ink} /> : null}{children}</Page>;
};
const Slot: React.FC<{w: number; filled: number; text: string}> = ({w, filled, text}) => (
  <span style={{display: 'inline-block', minWidth: w, textAlign: 'center', borderBottom: `8px solid ${T.accent}`, margin: '0 16px', color: T.accent}}><span style={{opacity: filled}}>{text}</span></span>
);

// ───── 0. 여는 장면: 빈칸 '연봉 ___ → 상위 ?%' + 100칸 띠, 표시가 50% → 35~36% ─────
const Open: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const fill = appear(f, A(s, 1), 20); const slide = interpolate(f, [A(s, 1), A(s, 1) + 40], [50, (d.a + d.b) / 2], CL);
  const tz = appear(f, A(s, 2)); const qs = appear(f, A(s, 3));
  return (
    <P s={{...s, title: '나 vs 남들 · 연봉 줄'}}>
      <div style={{...F, position: 'absolute', left: 200, top: 250, fontWeight: 700, fontSize: 92, color: T.ink, opacity: 1 - qs * 0.0}}>
        연봉<Slot w={330} filled={fill} text={n0(d.avg)} />만원 → 상위<Slot w={230} filled={fill} text={`${d.a}~${d.b}`} />%
      </div>
      <div style={{...F, position: 'absolute', left: 200, top: 380, fontWeight: 700, fontSize: 34, color: T.ink3, opacity: appear(f, 12) * (1 - fill)}}>평균 연봉 4,475만원 = 한가운데?</div>
      <div style={{...F, position: 'absolute', left: 200, top: 380, fontWeight: 700, fontSize: 34, color: T.ink2, opacity: fill}}>평균만 받아도 위쪽 3분의 1 언저리</div>
      <PctStrip x={200} y={560} w={1520} o={appear(f, 4, 20)} mark={slide} markO={appear(f, 24)} label={fill > 0.5 ? `상위 ${d.a}~${d.b}%` : '50%?'}
        hiFrom={0} hiTo={36} hiO={fill} />
      <Card x={1040} y={680} w={680} h={150} o={tz * (1 - qs)} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.dink3, padding: '20px 36px 0'}}>끝에서: 가구 순자산 상위 10% 문턱</div>
        <div style={{...F, fontWeight: 700, fontSize: 64, color: T.daccent, padding: '4px 36px'}}>1년 새 +{n0(d.p90[2])}만원</div>
      </Card>
      {['연봉 3,000만원은?', '1억원은?', '우리 집 순자산은?'].map((t, i) => <Chip key={t} x={200 + i * 420} y={720} o={appear(f, A(s, 3) + i * 12)} text={t} dark={i === 2} size={34} />)}
    </P>
  );
};

// ───── 2a. 사람 점 100줄 ─────
const Crowd: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const g = appear(f, A(s, 1) === NEVER ? Math.floor(s.frames * 0.5) : A(s, 1), 30);
  return (
    <P s={s}>
      <div style={{...F, position: 'absolute', left: 260, top: 250, fontWeight: 700, fontSize: 100, color: T.ink}}><CountUp to={d.n} p={appear(f, 6, 50)} />명</div>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {Array.from({length: 100}).map((_, c) => Array.from({length: 9}).map((__, r) => {
          const o = appear(f, 10 + ((c * 7 + r * 13) % 40), 12); const x = 210 + c * 15.2 + g * Math.floor(c / 10) * 4 - g * 18, y = 470 + r * 30;
          return <circle key={`${c}-${r}`} cx={x} cy={y} r={5.2} fill={c < 10 ? T.accent : c >= 90 ? T.ink3 : T.ink2} opacity={o} />;
        }))}
      </svg>
      <div style={{...F, position: 'absolute', left: 200, top: 760, fontWeight: 700, fontSize: 30, color: T.ink3, opacity: appear(f, 30)}}>← 연봉 높은 순</div>
      <Chip x={1100} y={760} o={g} text={`한 칸 ≈ ${n0(Math.round(d.per / 10000))}만 명`} />
    </P>
  );
};

// ───── 2b. 100칸 막대 — 가운데 칸 깃발 · 0.1% 칸이 뚫고 올라감 · 맨 끝 21만원 ─────
const Bars100: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const X = 220, Y = 740, W = 1480, H = 360, cap = 20000; const cw = W / 100;
  const sy = (v: number) => Y - (Math.min(v, cap) / cap) * H;
  const mid = appear(f, A(s, 1)), top = appear(f, A(s, 2)), shoot = appear(f, A(s, 3), 30), last = appear(f, A(s, 4)), reg = appear(f, A(s, 5));
  return (
    <P s={s}>
      <HundredBars x={X} y={Y} w={W} h={H} vals={d.bars} cap={cap} p={appear(f, 4, 40)} hi={top > 0.5 ? [0, 1, 2, 3, 4] : [49]} hiColor={top > 0.5 ? T.accent : T.ink} dim={mid > 0.5 ? 0.5 : 0} />
      <div style={{position: 'absolute', left: X, top: sy(d.avg), width: W, borderTop: `3px dashed ${T.accent}`, opacity: mid}} />
      <div style={{...F, position: 'absolute', left: X + 62 * cw, top: sy(d.avg) - 46, fontWeight: 700, fontSize: 32, color: T.accent, opacity: mid}}>전체 평균 {n0(d.avg)}만원</div>
      <div style={{position: 'absolute', left: X + 49 * cw + 4, top: sy(d.mid) - 120, opacity: mid}}>
        <div style={{width: 4, height: 110, background: T.ink}} />
        <div style={{...F, position: 'absolute', left: 8, top: -6, fontWeight: 700, fontSize: 38, color: '#fff', background: T.ink, borderRadius: 10, padding: '6px 16px', whiteSpace: 'nowrap'}}>가운데 칸 {n0(d.mid)}만원</div>
      </div>
      {/* 상위 0.1% 칸: 화면 위로 뚫고 올라감 */}
      <div style={{position: 'absolute', left: X, top: interpolate(shoot, [0, 1], [Y - H, 236]), width: cw * 0.6, height: interpolate(shoot, [0, 1], [H, Y - 236]), background: T.accent, opacity: shoot}} />
      <Card x={X + 30} y={250} w={520} h={130} o={shoot} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 26, color: T.dink3, padding: '18px 28px 0'}}>{`상위 0.1% · ${n0(d.top01n)}명 평균`}</div>
        <div style={{...F, fontWeight: 700, fontSize: 56, color: T.daccent, padding: '0 28px'}}>{won(d.top01)}</div>
      </Card>
      <div style={{position: 'absolute', left: X + W - 420, top: Y - 290, opacity: last, textAlign: 'right', width: 420}}>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.fall}}>맨 끝 칸 {n0(d.last)}만원</div>
        <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink2}}>한 해 일부만 일한 사람 포함</div>
      </div>
      <Chip x={X + 640} y={250} o={reg} text="정규직끼리 줄 세우면 아래쪽 값은 더 높다" dark={false} size={30} />
      <div style={{...F, position: 'absolute', left: X, top: Y + 12, fontWeight: 500, fontSize: 24, color: T.ink3}}>상위 1%</div>
      <div style={{...F, position: 'absolute', left: X + W - 120, top: Y + 12, fontWeight: 500, fontSize: 24, color: T.ink3}}>100%</div>
      <div style={{...F, position: 'absolute', left: X + 49 * cw - 20, top: Y + 12, fontWeight: 500, fontSize: 24, color: T.ink3}}>50%</div>
    </P>
  );
};

// ───── 3a. 자리표 — 빈칸 카드 + 줄마다 켜짐 + 아래 띠 표시 ─────
const Lookup: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows: {x: number; a: number; b: number}[] = d.rows;
  let cur = -1; rows.forEach((_, i) => { if (f >= A(s, i + 1)) cur = i; });
  const r = cur >= 0 ? rows[cur] : null; const k = cur >= 0 ? appear(f, A(s, cur + 1), 16) : 0;
  return (
    <P s={s}>
      <Card x={200} y={250} w={640} h={330} o={appear(f, 4)} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 34, color: T.dink3, padding: '34px 44px 0'}}>연봉</div>
        <div style={{...F, fontWeight: 700, fontSize: 104, color: T.dink, padding: '0 44px'}}>{r ? won(r.x) : '____'}</div>
        <div style={{...F, fontWeight: 700, fontSize: 64, color: T.daccent, padding: '6px 44px', opacity: r ? k : 1}}>{r ? `상위 ${r.a}~${r.b}%` : '상위 ?%'}</div>
      </Card>
      {rows.map((q, i) => { const o = appear(f, A(s, i + 1)); const on = i === cur; const hi = i === d.hi;
        return <div key={q.x} style={{position: 'absolute', left: 920, top: 250 + i * 66, width: 800, height: 56, borderRadius: 12, display: 'flex', alignItems: 'center',
          background: hi && o > 0.5 ? T.soft : on ? T.surface : 'transparent', opacity: 0.25 + o * 0.75}}>
          <span style={{...F, fontWeight: 700, fontSize: 36, color: T.ink, width: 300, paddingLeft: 24}}>{won(q.x)}</span>
          <span style={{...F, fontWeight: 700, fontSize: 36, color: on ? T.accent : T.ink2}}>{o > 0.3 ? `상위 ${q.a}% ~ ${q.b}%` : '…'}</span>
        </div>; })}
      <PctStrip x={200} y={700} w={1520} h={50} o={1} mark={r ? (r.a + r.b) / 2 - 0.5 : 50} markO={r ? 1 : 0} label={r ? `${r.a}~${r.b}%` : undefined} hiFrom={0} hiTo={r ? r.b : 0} hiO={r ? 1 : 0} />
    </P>
  );
};

// ───── 3b. 연봉-백분위 선 + 화살표 비교(+2,000만원 27칸 vs +1억원 6칸) ─────
const Climb: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const pts: [number, number][] = d.pts;
  const X0 = 300, X1 = 1680, Y0 = 740, Y1 = 260;
  const px = scaleLinear().domain([60, 0]).range([X0, X1]); const py = scaleLinear().domain([0, 21000]).range([Y0, Y1]);
  const p = appear(f, 6, 50); const m = Math.max(2, Math.ceil(pts.length * p));
  const path = d3line<[number, number]>().x((q) => px(q[1])).y((q) => py(q[0])).curve(curveMonotoneX)(pts.slice(0, m)) || '';
  const P2 = (x: number) => pts.find((q) => q[0] === x)!;
  const ar = [appear(f, A(s, 1)), appear(f, A(s, 2))];
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={X0} x2={X1} y1={Y0} y2={Y0} stroke={T.ink3} strokeWidth={2} />
        {[60, 50, 40, 30, 20, 10, 0].map((q) => <text key={q} x={px(q)} y={Y0 + 40} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{q === 0 ? '상위 0%' : `${q}%`}</text>)}
        <path d={path} fill="none" stroke={T.ink} strokeWidth={6} />
        {pts.slice(0, m).map(([x, q]) => <g key={x}><circle cx={px(q)} cy={py(x)} r={11} fill={T.ink} />
          <text x={px(q) - 18} y={py(x) - 10} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={28} fill={T.ink}>{won(x)}</text></g>)}
        {d.arrows.map(([t, a, b, c]: [string, number, number, string], i: number) => { const pa = P2(a), pb = P2(b); const o = ar[i]; const col = i ? T.fall : T.accent;
          const y = i ? py(a) + 30 : py(a) + 30; const bx = i ? px(pa[1]) - 300 : (px(pa[1]) + px(pb[1])) / 2; const by = i ? py(b) + 40 : py(b) - 240;
          return <g key={t} opacity={o}>
            <line x1={px(pa[1])} x2={px(pa[1]) + (px(pb[1]) - px(pa[1])) * o} y1={y} y2={y} stroke={col} strokeWidth={8} />
            <line x1={px(pb[1])} x2={px(pb[1])} y1={py(a)} y2={py(b)} stroke={col} strokeWidth={4} strokeDasharray="10 8" />
            <rect x={bx - 170} y={by} width={340} height={100} rx={14} fill={col} />
            <text x={bx} y={by + 40} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={30} fill="#fff">{t}</text>
            <text x={bx} y={by + 84} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={38} fill="#fff">{`→ ${c}`}</text>
          </g>; })}
      </svg>
    </P>
  );
};

// ───── 3c. 상위 2~10% 칸 가로 막대 + 괄호(8,215만원) ─────
const Gap: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const rows: [number, number][] = d.rows; const mx = rows[0][1]; const br = appear(f, Math.floor(s.frames * 0.45), 20);
  return (
    <P s={s}>
      {rows.map(([k, v], i) => { const o = appear(f, 6 + i * 5, 20); const hi = i === 0 || i === rows.length - 1;
        return <div key={k} style={{position: 'absolute', left: 200, top: 240 + i * 58, display: 'flex', alignItems: 'center', gap: 20}}>
          <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, width: 140, textAlign: 'right'}}>{`상위 ${k}%`}</span>
          <div style={{width: (v / mx) * 1000 * o, height: 42, borderRadius: 8, background: hi ? T.ink : T.line}} />
          <span style={{...F, fontWeight: 700, fontSize: hi ? 38 : 30, color: hi ? T.ink : T.ink3, opacity: o}}>{n0(v)}</span>
        </div>; })}
      <div style={{position: 'absolute', left: 1500, top: 270, width: 30, height: 8 * 58, border: `5px solid ${T.accent}`, borderLeft: 'none', borderRadius: '0 14px 14px 0', opacity: br}} />
      <div style={{...F, position: 'absolute', left: 1550, top: 470, fontWeight: 700, fontSize: 56, color: T.accent, opacity: br}}>{`+${n0(d.diff)}만원`}</div>
      <div style={{...F, position: 'absolute', left: 1550, top: 540, fontWeight: 700, fontSize: 28, color: T.ink2, opacity: br}}>여덟 칸 사이</div>
    </P>
  );
};

// ───── 4a. 세금 합계 카운트 → 띠 100조각 ─────
const TaxSplit: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c = appear(f, 6, 40); const sp = appear(f, Math.floor(s.frames * 0.45), 30);
  return (
    <P s={s}>
      <div style={{...F, position: 'absolute', left: 200, top: 280, fontWeight: 700, fontSize: 130, color: T.ink}}><CountUp to={d.jo} p={c} />조 <CountUp to={d.eok} p={c} />억원</div>
      {Array.from({length: 100}).map((_, i) => <div key={i} style={{position: 'absolute', left: 200 + i * 15.2 + sp * 0, top: 560 + (sp * ((i * 37) % 11) - sp * 5) * 3, width: 15.2 - 3 * sp, height: 120, background: i < 10 ? T.accent : T.ink,
        opacity: appear(f, 10, 20) * (1 - sp * (i >= 50 ? 0.7 : 0)), borderRadius: 2}} />)}
      <div style={{...F, position: 'absolute', left: 200, top: 740, fontWeight: 700, fontSize: 30, color: T.ink2, opacity: sp}}>100칸으로 쪼개면 — 누가 얼마를 냈나</div>
    </P>
  );
};

// ───── 4b. 쌍둥이 막대(연봉 몫 vs 세금 몫) ─────
const Twin: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows: [string, number, number][] = s.data.rows; const prog = appear(f, A(s, 3));
  return (
    <P s={s}>
      <div style={{position: 'absolute', left: 1360, top: 222, display: 'flex', gap: 30, opacity: appear(f, 6)}}>
        {[['받은 연봉 몫', T.ink2], ['낸 세금 몫', T.accent]].map(([t, c]) => <span key={t} style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2, display: 'flex', alignItems: 'center', gap: 10}}>
          <span style={{width: 26, height: 26, borderRadius: 6, background: c}} />{t}</span>)}
      </div>
      {rows.map(([n, a, b], i) => { const o = appear(f, A(s, i), 24); const y = 290 + i * 170;
        return <div key={n} style={{position: 'absolute', left: 200, top: y, opacity: 0.15 + o * 0.85}}>
          <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, width: 230}}>{n}</div>
          {[[a, T.ink2], [b, T.accent]].map(([v, c], j) => <div key={j} style={{position: 'absolute', left: 250, top: j * 64 - 6, display: 'flex', alignItems: 'center', gap: 16}}>
            <div style={{width: Math.max(4, ((v as number) / 75) * 1150 * o), height: 52, borderRadius: 8, background: c as string}} />
            <span style={{...F, fontWeight: 700, fontSize: j ? 44 : 36, color: c as string}}>{`${v}%`}</span></div>)}
        </div>; })}
      <Chip x={200} y={212} o={prog} text="소득세는 누진 — 한 칸 올라도 실수령액은 연봉만큼 안 는다" size={28} />
    </P>
  );
};

// ───── 5a. 가구 순자산 눈금자(P10~P90) + 중앙값 + 핀 ─────
const Ruler: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const sw = appear(f, 6, 20);
  const ticks: [number, string][] = d.ps.map(([p, v]: [number, number]) => [p, won(v).replace('만원', '만').replace('억원', '억')]);
  const med = appear(f, A(s, 2)); const p1 = appear(f, A(s, 3)), p2 = appear(f, A(s, 3) + 40), p3 = appear(f, A(s, 4)), th = appear(f, A(s, 4) + 30);
  return (
    <P s={s}>
      <div style={{position: 'absolute', left: 200, top: 250, display: 'flex', alignItems: 'center', gap: 24}}>
        <span style={{...F, fontWeight: 700, fontSize: 40, color: T.ink3, textDecoration: sw > 0.5 ? 'line-through' : 'none'}}>개인 연봉</span>
        <span style={{...F, fontWeight: 700, fontSize: 40, color: T.ink3}}>→</span>
        <span style={{...F, fontWeight: 700, fontSize: 48, color: T.fall, opacity: sw}}>가구 순자산</span>
      </div>
      <PctRuler x={240} y={560} w={1440} ticks={ticks} o={[appear(f, 10, 30), appear(f, A(s, 1) === NEVER ? 20 : A(s, 1))]} hiTick={th > 0.5 ? 90 : med > 0.5 ? 50 : undefined} hiO={1}
        pins={[[d.pins[0][0], d.pins[0][1], p1], [d.pins[1][0], d.pins[1][1], p2], [d.pins[2][0], d.pins[2][1], p3, T.accent]]} />
      <Chip x={240} y={760} o={med * (1 - p1)} text="가운데 가구(중앙값) 2억 3,860만원" size={32} />
      <Chip x={1060} y={760} o={th} text="상위 10% 문턱 11억 20만원 — 10억은 그 아래" size={30} />
    </P>
  );
};

// ───── 5b. 중앙값 vs 평균 막대 ─────
const MeanMed: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const o = appear(f, 6, 30); const x2 = appear(f, Math.floor(s.frames * 0.4));
  return (
    <P s={s}>
      {[['중앙값(가운데 가구)', d.med, T.fall], ['평균', d.mean, T.accent]].map(([t, v, c], i) => (
        <div key={i} style={{position: 'absolute', left: 200, top: 300 + i * 180}}>
          <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2}}>{t as string}</div>
          <div style={{display: 'flex', alignItems: 'center', gap: 20, marginTop: 10}}>
            <div style={{width: ((v as number) / d.mean) * 1100 * appear(f, 6 + i * 16, 30), height: 80, borderRadius: 12, background: c as string}} />
            <span style={{...F, fontWeight: 700, fontSize: 52, color: c as string, opacity: o}}>{won(v as number)}</span></div>
        </div>))}
      <Chip x={200} y={720} o={x2} text={`평균 = 중앙값의 ${d.x}배 · 평균 가구는 위에서 20~30% 사이`} size={34} />
    </P>
  );
};

// ───── 5c. 5칸 띠(점유율) — 맨 위 칸 1년 전보다 커짐 ─────
const Share: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const q: number[] = s.data.q; const grow = appear(f, Math.floor(at(s, 0) + 50), 40); const nx = appear(f, A(s, 1));
  const top = s.data.prev5 + (q[4] - s.data.prev5) * grow; const rest = q.slice(0, 4); const sc = 1520 / 100;
  const vals = [...rest.map((v) => v * (100 - top) / rest.reduce((a, b) => a + b, 0)), top];
  let acc = 0;
  return (
    <P s={s}>
      {vals.map((v, i) => { const x = 200 + acc * sc; acc += v; const o = appear(f, 6 + i * 6, 20);
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: x, top: 330, width: Math.max(3, v * sc - 4), height: 170, borderRadius: 10, background: i === 4 ? T.fall : [T.line, T.line, '#cfd6e2', '#a9b6cc'][i], opacity: o}} />
          <div style={{...F, position: 'absolute', left: i < 2 ? x - 10 + i * 40 : x + 14, top: i < 2 ? 520 + i * 40 : 360, fontWeight: 700, fontSize: i === 4 ? 64 : 30, color: i === 4 ? '#fff' : T.ink2, opacity: o, whiteSpace: 'nowrap'}}>
            {i === 4 ? `${top.toFixed(2)}%` : `${q[i]}%`}</div>
          <div style={{...F, position: 'absolute', left: x + 14, top: 600, fontWeight: 500, fontSize: 24, color: T.ink3, opacity: o * (i >= 2 ? 1 : 0)}}>{['', '', '가운데 20%', '그 위 20%', '위쪽 20% 가구'][i]}</div>
        </React.Fragment>; })}
      <Chip x={200} y={680} o={grow * (1 - nx)} text={`위쪽 20% 몫 1년 전 ${s.data.prev5}% → ${q[4]}% (+1.48%p)`} size={32} />
      <Chip x={200} y={680} o={nx} text="더 눈에 띄는 숫자: 문턱이 1년 새 얼마나 움직였나" size={32} dark={false} />
    </P>
  );
};

// ───── 6a. 경계값 1년 증감(좌우 막대) ─────
const Shift: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const rows: [number, number, number, number][] = s.data.rows;
  const st = [A(s, 1), A(s, 2), A(s, 3), A(s, 4)]; let k = -1; st.forEach((a, i) => { if (f >= a) k = i; });
  const hi = [[4], [0], [6, 7], [8]][k] ?? []; const card = appear(f, A(s, 4) + 10);
  return (
    <P s={s}>
      <DivergeRows x0={720} y={250} rowH={62} rows={rows.map(([p, , , dl]) => [`P${p}`, dl])} max={5428} half={860} p={appear(f, 6, 40)} hi={hi} dimOthers={k >= 0 ? 1 : 0}
        fmt={(v) => `${sgn(v)}만원`} />
      <div style={{...F, position: 'absolute', left: 360, top: 830, fontWeight: 500, fontSize: 24, color: T.fall}}>← 내려감</div>
      <div style={{...F, position: 'absolute', left: 760, top: 830, fontWeight: 500, fontSize: 24, color: T.rise}}>올라감 →</div>
      <Card x={1060} y={260} w={680} h={200} o={card} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.dink3, padding: '24px 32px 0'}}>상위 10% 문턱(P90)</div>
        <div style={{...F, fontWeight: 700, fontSize: 38, color: T.dink, padding: '4px 32px', whiteSpace: 'nowrap'}}>{`${won(rows[8][1])} → ${won(rows[8][2])}`}</div>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.daccent, padding: '0 32px'}}>+5.2%</div>
      </Card>
    </P>
  );
};

// ───── 6b. 1년 이동을 12칸으로 ─────
const Month: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const cv = appear(f, A(s, 1));
  return (
    <P s={s}>
      <div style={{...F, position: 'absolute', left: 200, top: 260, fontWeight: 700, fontSize: 96, color: T.ink}}>1년 <span style={{color: T.accent}}>+<CountUp to={d.y} p={appear(f, 6, 30)} />만원</span></div>
      {Array.from({length: 12}).map((_, i) => { const o = appear(f, 40 + i * 6, 14);
        return <div key={i} style={{position: 'absolute', left: 200 + i * 128, top: 430, width: 116, height: 200, borderRadius: 14, background: T.surface, opacity: o, transform: `translateY(${(1 - o) * 20}px)`}}>
          <div style={{...F, fontWeight: 500, fontSize: 24, color: T.ink3, textAlign: 'center', marginTop: 20}}>{`${i + 1}월`}</div>
          <div style={{...F, fontWeight: 700, fontSize: 40, color: T.accent, textAlign: 'center', marginTop: 40}}>{`+${d.m}`}</div>
        </div>; })}
      <div style={{...F, position: 'absolute', left: 200, top: 660, fontWeight: 700, fontSize: 36, color: T.ink2, opacity: appear(f, 120)}}>{`한 달 ${d.m}만원꼴 — 저축 + 집값·주가 변화`}</div>
      <Chip x={200} y={740} o={cv} text="한 해 변화일 뿐 · 내년도 같은 속도라는 뜻 아님 · 표본 조사 오차" dark={false} size={30} />
    </P>
  );
};

// ───── 7a. 정리 카드 3장 ─────
const Sum3: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const cards: [string, string, string][] = s.data.cards;
  return (
    <P s={s}>
      {cards.map(([a, b, c], i) => <Card key={a} x={200 + i * 520} y={280} w={480} h={420} o={appear(f, A(s, i + 1))} bg={i === 2 ? T.ink : T.surface}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: i === 2 ? T.dink3 : T.ink3, padding: '40px 36px 0'}}>{`${i + 1}. ${a}`}</div>
        <div style={{...F, fontWeight: 700, fontSize: 64, color: i === 2 ? T.daccent : T.accent, padding: '20px 36px'}}>{b}</div>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: i === 2 ? T.dink : T.ink2, padding: '0 36px', wordBreak: 'keep-all'}}>{c}</div>
      </Card>)}
    </P>
  );
};

// ───── 7b. 같은 사람, 두 줄에서 다른 자리(왼쪽 = 위쪽) ─────
const TwoPins: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const X = 300, W = 1400;
  const a = appear(f, Math.floor(s.frames * 0.12), 20), b = appear(f, Math.floor(s.frames * 0.42), 20), c = appear(f, Math.floor(s.frames * 0.72));
  const row = (y: number, label: string, col: string, pos: number, pin: string, o: number) => (
    <div style={{position: 'absolute', left: 0, top: y}}>
      <div style={{...F, position: 'absolute', left: 200, top: -80, fontWeight: 700, fontSize: 34, color: col, whiteSpace: 'nowrap'}}>{label}</div>
      <div style={{position: 'absolute', left: X, top: 0, width: W, height: 10, borderRadius: 5, background: T.line}} />
      {[0, 50, 100].map((q) => <div key={q} style={{...F, position: 'absolute', left: X + (q / 100) * W - 70, width: 140, textAlign: 'center', top: 22, fontWeight: 500, fontSize: 22, color: T.ink3}}>{q === 0 ? '위쪽 0%' : q === 100 ? '아래쪽 100%' : '50%'}</div>)}
      <div style={{position: 'absolute', left: X + (pos / 100) * W, top: -60 - (1 - o) * 20, opacity: o}}>
        <div style={{...F, position: 'absolute', left: -150, width: 300, textAlign: 'center', top: -50, fontWeight: 700, fontSize: 32, color: '#fff', background: col, borderRadius: 30, padding: '6px 0'}}>{pin}</div>
        <div style={{position: 'absolute', left: -14, top: 20, width: 28, height: 28, borderRadius: 14, background: col, border: '4px solid #fff'}} />
      </div>
    </div>);
  return (
    <P s={s}>
      {row(340, '개인 연봉 줄 · 5,000만원', T.ink, (d.pay[0] + d.pay[1]) / 2, `위에서 ${d.pay[0]}~${d.pay[1]}%`, a)}
      {row(540, '가구 순자산 줄 · 1억원', T.fall, 100 - d.nw, '아래에서 20~30%', b)}
      <Chip x={200} y={610} o={c} text="순자산 줄은 모든 나이 가구가 섞임 — 젊을수록 아래쪽이 자연스럽다" dark={false} size={28} />
    </P>
  );
};

// ───── 7c. 계산기 화면(입력만, 결과 숫자 짓지 않음) + 끝 안내 ─────
const Cta: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const typed = Math.floor(interpolate(f, [40, 90], [0, 4], CL)); const dg = String(d.x).slice(0, typed); const txt = dg ? n0(Number(dg)) : '';
  const end = appear(f, A(s, 1));
  return (
    <P s={s}>
      <Card x={460} y={250} w={1000} h={440} o={appear(f, 6)} style={{boxShadow: '0 12px 40px rgba(0,0,0,0.08)'}}>
        <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink3, padding: '28px 44px 0'}}>firemap.kr · 계산기</div>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, padding: '30px 44px 10px'}}>내 연봉(세전)</div>
        <div style={{margin: '0 44px', height: 110, borderRadius: 16, border: `4px solid ${T.accent}`, display: 'flex', alignItems: 'center', padding: '0 30px'}}>
          <span style={{...F, fontWeight: 700, fontSize: 72, color: T.ink}}>{txt || ' '}</span>
          <span style={{width: 4, height: 70, background: T.ink, marginLeft: 6, opacity: Math.floor(f / 15) % 2}} />
          <span style={{...F, fontWeight: 700, fontSize: 44, color: T.ink3, marginLeft: 'auto'}}>만원</span>
        </div>
        <div style={{margin: '30px 44px', height: 90, borderRadius: 16, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: appear(f, 100)}}>
          <span style={{...F, fontWeight: 700, fontSize: 40, color: '#fff'}}>실수령액 보기</span></div>
      </Card>
      <Chip x={460} y={740} o={appear(f, 30) * (1 - end)} text="설명란 첫 줄 링크" size={32} />
      <Chip x={460} y={740} o={end} text="다음 나 vs 남들 — 다른 숫자로 줄 세우기 · 투자 권유 아님" size={30} dark={false} />
    </P>
  );
};

const View: React.FC<S> = ({s}) => {
  switch (s.kind) {
    case 'open': return <Open s={s} />; case 'logo': return <LogoSting sub={s.data.sub} />; case 'crowd': return <Crowd s={s} />;
    case 'bars100': return <Bars100 s={s} />; case 'lookup': return <Lookup s={s} />; case 'climb': return <Climb s={s} />; case 'gap': return <Gap s={s} />;
    case 'taxsplit': return <TaxSplit s={s} />; case 'twin': return <Twin s={s} />; case 'ruler': return <Ruler s={s} />; case 'meanmed': return <MeanMed s={s} />;
    case 'share': return <Share s={s} />; case 'shift': return <Shift s={s} />; case 'month': return <Month s={s} />; case 'sum3': return <Sum3 s={s} />;
    case 'twopins': return <TwoPins s={s} />; case 'cta': return <Cta s={s} />;
    default: return <P s={s}>{null}</P>;
  }
};

export const N1: React.FC<N1Props> = ({scenes, rail}) => {
  let acc = 0;
  return (
    <RailCtx.Provider value={rail}>
      <AbsoluteFill style={{background: T.bg}}>
        <style>{FONT_CSS}</style>
        {scenes.map((s, i) => {
          const from = acc; acc += s.frames; let a = 6;
          return (
            <Sequence key={i} from={from} durationInFrames={s.frames}>
              <View s={s} />
              {s.lines.map((l, j) => { const st = a; a += l.frames;
                return l.audio ? <Sequence key={j} from={st} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null; })}
            </Sequence>
          );
        })}
      </AbsoluteFill>
    </RailCtx.Provider>
  );
};
