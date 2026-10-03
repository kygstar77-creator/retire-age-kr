// R-1 "1억의 1년 영수증"(X-SERIES-1 ①) — 재료: work/video/r1.json(ep/R-1/r1props.py가 script.md·voice.json·calc2_out·원자료로 만든다)
// 장면 종류 17가지: 같은 높이 막대 4개+도장 · 영수증 인쇄+빠지는 조각 · 환율 두 카드+막대 내려앉음 · 영수증+동전 · 세금 식 토큰 · 12달 달력+영수증 ·
// 영수증 두 장 · 금 막대 올랐다 눌림 · 순위표 두 장 연결 · 간격 막대 · 금리 선(기준금리 겹침) · 공시 점 띠 · 줄다리기 · 눈금자 핀 · 요약 카드 · 계산기 · 로고
// 숫자는 전부 r1.json에서 온다(코드 안에는 눈금·배치 값만). 단계 시점은 data.at(문장 번호, 못 찾으면 −1=안 나옴).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {scaleLinear} from 'd3-scale';
import {line as d3line, curveMonotoneX} from 'd3-shape';
import {T, F, CL, FONT_CSS, VScene, at, appear, CountUp, Page, LogoSting, ProgressRail} from './parts/fm';
import {ReceiptPaper, Stamp, DotStrip, Coins, RLine} from './parts/receipt';

export type R1Props = {fps: number; rail: string[]; scenes: VScene[]; missing: number; holes: number};
export const r1Frames = (p: R1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: VScene};
const NEVER = 1e9;
const A = (s: VScene, k: number) => (s.data.at?.[k] ?? -1) < 0 ? NEVER : at(s, s.data.at[k]);
const RailCtx = React.createContext<string[]>([]);
const n0 = (v: number) => Math.round(v).toLocaleString();
const man = (v: number) => { const m = Math.round(v / 1e4); const e = Math.floor(m / 1e4), r = m % 1e4; return e ? (r ? `${e}억 ${r.toLocaleString()}만원` : `${e}억원`) : `${r.toLocaleString()}만원`; };
const Card: React.FC<{x: number; y: number; w: number; h?: number; o?: number; bg?: string; style?: React.CSSProperties; children?: React.ReactNode}> = ({x, y, w, h, o = 1, bg = T.surface, style, children}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: bg, borderRadius: 20, opacity: o, ...style}}>{children}</div>
);
const Chip: React.FC<{x: number; y: number; o: number; text: string; dark?: boolean; size?: number; color?: string}> = ({x, y, o, text, dark = true, size = 32, color}) => (
  <div style={{...F, position: 'absolute', left: x, top: y, opacity: o, fontWeight: 700, fontSize: size, color: dark ? '#fff' : T.ink, background: color ?? (dark ? T.ink : T.soft),
    borderRadius: 40, padding: '10px 28px', whiteSpace: 'nowrap'}}>{text}</div>
);
const P: React.FC<S & {children: React.ReactNode}> = ({s, children}) => {
  const rail = React.useContext(RailCtx);
  return <Page s={{...s, rail: 0}}>{s.rail ? <ProgressRail n={rail.length} cur={s.rail} labels={rail} on={T.ink} /> : null}{children}</Page>;
};
// 단계 k의 시작(못 찾은 단계는 앞 단계 + gap 프레임)
const cue = (s: VScene, k: number, gap = 22) => { let t = 6; for (let i = 0; i <= k; i++) { const a = A(s, i); t = a === NEVER ? t + gap : Math.max(a, i ? t + gap : a); } return t; };
const Txt: React.FC<{x: number; y: number; o?: number; size?: number; color?: string; w?: number; align?: 'left' | 'center' | 'right'; weight?: number; children: React.ReactNode}> =
  ({x, y, o = 1, size = 32, color = T.ink, w, align = 'left', weight = 700, children}) => (
  <div style={{...F, position: 'absolute', left: x, top: y, width: w, textAlign: align, opacity: o, fontWeight: weight, fontSize: size, color, whiteSpace: 'nowrap'}}>{children}</div>
);

// ───── 0. 여는 장면: 같은 높이 막대 4개 '1억' + 기준일 도장 → 물음표 → '세금이 간격 307만원 줄임' ─────
const Open4: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const q = appear(f, A(s, 1)); const g = appear(f, A(s, 2)); const r = appear(f, A(s, 3));
  const X = 180, W = 180, GAP = 100, BASE = 800, H = 400;
  return (
    <P s={s}>
      {d.bars.map((b: [string, number, number, number], i: number) => {
        const x = X + i * (W + GAP); const o = appear(f, 4 + i * 5, 16);
        return <React.Fragment key={b[0]}>
          <div style={{position: 'absolute', left: x, top: BASE - H * o, width: W, height: H * o, borderRadius: '16px 16px 0 0', background: i === 0 ? T.ink2 : T.ink}} />
          <Txt x={x} y={BASE - H - 60} w={W} align="center" size={40} o={o}>1억</Txt>
          <Txt x={x} y={BASE + 18} w={W} align="center" size={34} color={T.ink2} o={o}>{b[0]}</Txt>
          <Txt x={x} y={BASE - H / 2 - 60} w={W} align="center" size={110} color="#fff" o={q * (1 - r * 0.6)}>?</Txt>
        </React.Fragment>;
      })}
      <Stamp x={1330} y={210} o={appear(f, 18)} text="2025.10.2 → 2026.10.2" color={T.accent} size={34} />
      <Card x={1290} y={430} w={500} h={250} o={g} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.dink3, padding: '26px 34px 0'}}>세금이 줄인 간격</div>
        <div style={{...F, fontWeight: 700, fontSize: 74, color: T.daccent, padding: '6px 34px'}}>−{man(d.gap)}</div>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.dink, padding: '0 34px'}}>예금 ↔ 1등 · 순위는?</div>
      </Card>
      <Chip x={1290} y={720} o={r} text="영수증 한 줄씩 →" size={32} dark={false} />
    </P>
  );
};

// ───── 영수증 + 오른쪽 막대(빨간 조각이 떨어짐) — 예금 1년 전·지금 공용 ─────
const Receipt: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c = [0, 1, 2, 3].map((k) => cue(s, k));
  const lines: RLine[] = d.rows.map((r: [string, number, string], i: number) => ({label: r[0], v: r[1], tone: r[2] as RLine['tone'], o: appear(f, c[i + 1])}));
  lines.push({label: d.netLabel ?? '통장', v: d.net, tone: 'net', o: appear(f, c[3])});
  if (d.mon) lines.push({label: '한 달로 나누면', text: `월 ${n0(d.mon)}`, tone: 'note', o: appear(f, c[3] + 30)});
  const tax = -d.rows[1][1]; const gain = d.rows[0][1]; const drop = appear(f, c[2] + 6, 30);
  const BX = 1330, BASE = 800, BH = 440, sc = BH / gain;   // 오른쪽 막대 = 이자 몫만(원금 1억 위로)
  return (
    <P s={s}>
      <ReceiptPaper x={330} y={230} w={820} head={d.head} lines={lines} o={appear(f, c[0], 22)} size={38} />
      {d.split ? <div style={{position: 'absolute', left: 340, top: 230 + 110 + lines.length * 72 + 70, opacity: appear(f, c[2] + 18)}}>
        {d.split.map((t: string, i: number) => <Chip key={t} x={i * 260} y={0} o={1} text={t} dark={false} size={26} />)}</div> : null}
      <div style={{position: 'absolute', left: BX, top: BASE - BH * appear(f, c[1], 24), width: 180, height: BH * appear(f, c[1], 24) - tax * sc * drop, background: T.ink, borderRadius: '14px 14px 0 0'}} />
      <div style={{position: 'absolute', left: BX, top: BASE - BH + drop * 260, width: 180, height: tax * sc, background: T.rise, borderRadius: 10,
        opacity: appear(f, c[2]) * (1 - interpolate(f, [c[2] + 30, c[2] + 46], [0, 1], CL)), transform: `rotate(${drop * 14}deg)`}} />
      <Txt x={BX - 40} y={BASE + 16} w={260} align="center" size={28} color={T.ink2} o={appear(f, c[1])}>원금 1억 위 이자 몫</Txt>
      <Txt x={BX + 200} y={BASE - BH + 10} size={30} color={T.rise} o={appear(f, c[2] + 20)}>−{n0(tax)}</Txt>
      {d.pct ? <Chip x={BX - 30} y={BASE - BH - 90} o={appear(f, c[3] + 10)} text={`1년에 +${d.pct.toFixed(2)}%`} color={T.accent} size={34} /> : null}
    </P>
  );
};

// ───── 2. 환율: 두 카드 1,406 → 1,359.6 · 달러 자산 막대 3개가 같은 만큼 내려앉음 · 환전 수수료 빈 줄 ─────
const Fx: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1), c2 = cue(s, 2), c3 = cue(s, 3);
  const sink = appear(f, c2 + 10, 30); const X = 1130, BASE = 760, W = 150, GAP = 70;
  const sy = scaleLinear().domain([90_000_000, 100_000_000]).range([0, 380]);   // 9,500만원부터 그린 축(아래를 자름)
  const h = sy(100_000_000 - d.loss * sink);
  return (
    <P s={s}>
      {[[String('2025.10.2'), d.a], ['2026.10.2', d.b]].map(([t, v], i) => (
        <Card key={i} x={160 + i * 470} y={260} w={420} h={200} o={appear(f, i ? c1 + 14 : c1)} bg={i ? T.ink : T.surface}>
          <div style={{...F, fontWeight: 700, fontSize: 28, color: i ? T.dink3 : T.ink3, padding: '26px 30px 0'}}>{t} · 1달러</div>
          <div style={{...F, fontWeight: 700, fontSize: 70, color: i ? T.dink : T.ink, padding: '6px 30px', whiteSpace: 'nowrap'}}>{Number(v).toLocaleString(undefined, {minimumFractionDigits: i ? 1 : 0})}원</div>
        </Card>))}
      <Txt x={590} y={330} size={54} color={T.ink3} o={appear(f, c1 + 14)}>→</Txt>
      <Chip x={180} y={500} o={appear(f, c1 + 30)} text={`달러 값 ${d.pct.toFixed(2).replace('-', '−')}%`} color={T.fall} size={36} />
      {d.names.map((n: string, i: number) => { const x = X + i * (W + GAP); const o = appear(f, c2 - 10 + i * 4);
        return <React.Fragment key={n}>
          <div style={{position: 'absolute', left: x, top: BASE - sy(100_000_000), width: W, height: sy(100_000_000), border: `3px dashed ${T.ink3}`, borderRadius: '12px 12px 0 0', opacity: o * sink}} />
          <div style={{position: 'absolute', left: x, top: BASE - h, width: W, height: h, background: T.ink, borderRadius: '12px 12px 0 0', opacity: o}} />
          <Txt x={x - 20} y={BASE + 14} w={W + 40} align="center" size={28} color={T.ink2} o={o}>{n}</Txt>
        </React.Fragment>; })}
      <Txt x={X - 10} y={BASE - sy(100_000_000) - 56} size={28} color={T.ink3} o={appear(f, c2)}>1억(제자리였다면) · 축은 9,000만원부터</Txt>
      <Chip x={X} y={BASE - 210} o={sink} text={`환율만으로 −${n0(d.loss)}`} color={T.fall} size={34} />
      <Card x={160} y={620} w={760} h={96} o={appear(f, c3)} style={{background: `repeating-linear-gradient(135deg, ${T.bg} 0 10px, ${T.surface} 10px 20px)`}}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink3, padding: '28px 30px'}}>환전 수수료 — 증권사마다 다름</div>
      </Card>
      <Stamp x={660} y={612} o={appear(f, c3 + 12)} text="확인 안 함" />
    </P>
  );
};

// ───── 3a. S&P500 영수증 + 동전 4개(분배금) ─────
const Receipt2: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 60);
  const lines: RLine[] = [
    {label: '달러 종가', text: `${d.usd[0]} → ${d.usd[1]}`, tone: 'note', o: appear(f, 30)},
    {label: '달러 기준', text: `+${d.usd[2].toFixed(2)}%`, tone: 'in', o: appear(f, 50)},
    {label: '원화로 판 돈', v: d.sell, tone: 'in', o: appear(f, c1)},
    {label: '차익', v: d.gain, tone: 'in', o: appear(f, c1 + 20)},
  ];
  return (
    <P s={s}>
      <ReceiptPaper x={330} y={230} w={860} head={d.head} lines={lines} o={appear(f, 6, 22)} size={38} />
      <Coins x={1340} y={640} n={d.n} f={f} start={c1 + 40} label={`분배금 ${d.n}번 +${n0(d.dist)}`} />
      <Txt x={1340} y={700} size={26} color={T.ink3} o={appear(f, c1 + 80)}>세전 · 분기마다 · 끝날 환율로 원화</Txt>
      <Txt x={1340} y={750} size={34} color={T.rise} o={appear(f, c1 + 100)}>미국 원천징수 15% −{n0(d.wht)}</Txt>
    </P>
  );
};

// ───── 3b. 세금 식: 차익 − 250만 = 과세 몫 × 22% = 양도세 ─────
const TaxCalc: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 50), c2 = cue(s, 2, 50); const base = d.gain - d.ded;
  const tok = (t: string, sub: string, x: number, o: number, tone: string, w = 330) => (
    <div key={t + x} style={{position: 'absolute', left: x, top: 330 + (1 - o) * 20, width: w, opacity: o}}>
      <div style={{...F, fontWeight: 700, fontSize: 52, color: tone, textAlign: 'center'}}>{t}</div>
      <div style={{...F, fontWeight: 500, fontSize: 26, color: T.ink3, textAlign: 'center', marginTop: 8}}>{sub}</div>
    </div>);
  const op = (t: string, x: number, o: number) => <Txt key={t + x} x={x} y={330} size={52} color={T.ink3} o={o}>{t}</Txt>;
  return (
    <P s={s}>
      {tok(n0(d.gain), '차익', 100, appear(f, 10), T.ink)}
      {op('−', 440, appear(f, 24))}
      {tok(n0(d.ded), '1년 기본공제', 490, appear(f, 28), T.ink2, 300)}
      {op('=', 800, appear(f, 44))}
      {tok(n0(base), '세금 매기는 몫', 850, appear(f, 48), T.ink)}
      {op('×', 1185, appear(f, c1))}
      {tok(`${d.rate}%`, '세율', 1230, appear(f, c1 + 4), T.rise, 160)}
      {op('=', 1400, appear(f, c2))}
      {tok(`−${n0(d.tax)}`, '양도소득세', 1450, appear(f, c2 + 6), T.rise, 300)}
      <Chip x={1100} y={500} o={appear(f, c1 + 20)} text="소득세 20% + 지방소득세 2%" dark={false} size={28} />
      <Chip x={100} y={600} o={appear(f, c2 + 20)} text="다른 데서 낸 해외 주식 차익이 없다고 친 값" size={28} />
    </P>
  );
};

// ───── 3c. 12달 달력(5월 확정신고) + 남는 돈 영수증(양도세·분배금 원천징수), 보수 메모 ─────
const Calendar: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1), c2 = cue(s, 2), c3 = cue(s, 3);
  const may = appear(f, 30);
  const lines: RLine[] = [
    {label: '양도소득세(5월에 냄)', v: -d.tax, tone: 'tax', o: appear(f, c1)},
    {label: '분배금 원천징수 15%', v: -d.wht, tone: 'tax', o: appear(f, c2)},
    {label: '세금 뒤', v: d.net, tone: 'net', o: appear(f, c2 + 40)},
  ];
  return (
    <P s={s}>
      <Card x={180} y={240} w={620} h={470} o={appear(f, 6)}>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, padding: '26px 34px 10px'}}>판 다음 해</div>
        {Array.from({length: 12}).map((_, i) => { const on = i === 4;
          return <div key={i} style={{position: 'absolute', left: 34 + (i % 4) * 140, top: 90 + Math.floor(i / 4) * 120, width: 124, height: 104, borderRadius: 14,
            background: on ? interpolate(may, [0, 1], [0, 1]) > 0.5 ? T.accent : T.line : T.bg, display: 'flex', alignItems: 'center', justifyContent: 'center',
            transform: on ? `scale(${1 + may * 0.08})` : undefined}}>
            <span style={{...F, fontWeight: 700, fontSize: 34, color: on && may > 0.5 ? '#fff' : T.ink3}}>{i + 1}월</span></div>; })}
      </Card>
      <Chip x={200} y={735} o={may} text="5월 · 직접 확정신고" color={T.accent} size={30} />
      <ReceiptPaper x={900} y={240} w={840} head="S&P500 · 세금 뒤" lines={lines} o={appear(f, c1 - 8, 18)} size={36} />
      <Chip x={900} y={690} o={appear(f, c2 + 50)} text={`+${d.pct.toFixed(2)}% · 세금 둘 다 뺀 뒤`} color={T.accent} size={30} />
      <Chip x={900} y={770} o={appear(f, c3)} text="운용 보수는 이미 가격에 들어가 있음" dark={false} size={28} />
    </P>
  );
};

// ───── 4a. 영수증 두 장: SCHD 인쇄, 금은 다음 차례 ─────
const Duo: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 60);
  const mk = (side: any, o0: number, step: number): RLine[] => [
    ...side[1].map((r: [string, number], i: number) => ({label: r[0], v: r[1], tone: r[1] < 0 ? 'tax' : 'in', o: appear(f, o0 + i * step)}) as RLine),
    {label: '세금 뒤', v: side[2], tone: 'net', o: appear(f, o0 + side[1].length * step)}];
  return (
    <P s={s}>
      <ReceiptPaper x={200} y={230} w={720} head={d.L[0]} lines={mk(d.L, 30, (c1 - 30) / d.L[1].length)} o={appear(f, 6, 22)} size={34} />
      <Chip x={220} y={720} o={appear(f, c1 + 30)} text={`+${d.L[3].toFixed(2)}% · 세금 다 뺀 뒤`} color={T.accent} size={30} />
      <ReceiptPaper x={1020} y={230} w={720} head={d.R[0]} lines={mk(d.R, NEVER, 1)} o={appear(f, 16, 22)} dim={0.45} size={34} />
      <Txt x={1020} y={720} size={30} color={T.ink3} o={appear(f, 30)}>금 — 다음에 같은 계산</Txt>
    </P>
  );
};

// ───── 4b. 금: 달러로 +7.15% 올랐다 → 환율에 눌려 원화 차익 → 양도세 → 통장 ─────
const GoldFx: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 40), c2 = cue(s, 2, 60);
  const BASE = 720, X = 360, W = 240, sc = 380 / d.usdpct;   // 높이 = %
  const up = appear(f, 10, 30); const press = appear(f, c1 + 10, 36); const wonPct = d.gain / 1e6;
  const hNow = sc * (d.usdpct * up - (d.usdpct - wonPct) * press);
  return (
    <P s={s}>
      <div style={{position: 'absolute', left: X, top: BASE - sc * d.usdpct, width: W, height: sc * d.usdpct, border: `3px dashed ${T.ink3}`, borderRadius: '14px 14px 0 0', opacity: press}} />
      <div style={{position: 'absolute', left: X, top: BASE - hNow, width: W, height: hNow, background: '#c9a227', borderRadius: '14px 14px 0 0'}} />
      <Txt x={X + W + 30} y={BASE - sc * d.usdpct - 10} size={40} o={up}>달러 기준 +{d.usdpct.toFixed(2)}%</Txt>
      <div style={{position: 'absolute', left: X - 30, top: BASE - sc * d.usdpct - 70 + press * (sc * (d.usdpct - wonPct)), width: W + 60, height: 46, borderRadius: 12, background: T.fall, opacity: press,
        display: 'flex', alignItems: 'center', justifyContent: 'center'}}><span style={{...F, fontWeight: 700, fontSize: 28, color: '#fff'}}>환율 {d.fxpct.toFixed(2).replace('-', '−')}%</span></div>
      <Txt x={X + W + 30} y={BASE - sc * wonPct + 10} size={40} color={T.ink} o={press}>원화 차익 {n0(d.gain)}</Txt>
      <Txt x={X} y={BASE + 16} w={W} align="center" size={30} color={T.ink2}>금 ETF(GLD)</Txt>
      <ReceiptPaper x={1160} y={300} w={600} head="금 · 세금 뒤" o={appear(f, c2 - 6, 18)} size={34}
        lines={[{label: '분배금', text: '없음', tone: 'note', o: appear(f, c2)}, {label: '양도세', v: -d.tax, tone: 'tax', o: appear(f, c2 + 16)}, {label: '세금 뒤', v: d.net, tone: 'net', o: appear(f, c2 + 32)}]} />
    </P>
  );
};

// ───── 5a. 순위표 두 장(세전 → 세금 뒤), 같은 이름끼리 선 '안 바뀜' ─────
const Ranks: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1), c2 = cue(s, 2);
  const LX = 200, RX = 1100, Y = 270, RH = 100, W = 620;
  const col = (rows: [string, number][], x: number, head: string, o: number, dark: boolean) => (
    <Card x={x} y={Y - 70} w={W} h={70 + rows.length * RH + 20} o={o} bg={dark ? T.ink : T.surface}>
      <div style={{...F, fontWeight: 700, fontSize: 28, color: dark ? T.dink3 : T.ink3, padding: '20px 30px 0'}}>{head}</div>
      {rows.map((r, i) => <div key={r[0]} style={{position: 'absolute', left: 30, right: 30, top: 70 + i * RH, height: RH - 14, display: 'flex', alignItems: 'center', borderTop: i ? `2px solid ${dark ? T.dsurface : T.line}` : undefined}}>
        <span style={{...F, fontWeight: 700, fontSize: 40, color: dark ? T.daccent : T.accent, width: 60}}>{i + 1}</span>
        <span style={{...F, fontWeight: 700, fontSize: 38, color: dark ? T.dink : T.ink}}>{r[0]}</span>
        <span style={{...F, fontWeight: 700, fontSize: 34, color: dark ? T.dink : T.ink2, marginLeft: 'auto'}}>{n0(r[1])}</span></div>)}
    </Card>);
  const link = appear(f, c1, 24);
  return (
    <P s={s}>
      {col(d.L, LX, '세전(분배금 포함)', appear(f, 6), false)}
      {col(d.R, RX, '세금·환율 뒤 통장', appear(f, 30), true)}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {d.L.map((_: any, i: number) => <line key={i} x1={LX + W} x2={LX + W + (RX - LX - W) * link} y1={Y + 30 + i * RH} y2={Y + 30 + i * RH} stroke={T.accent} strokeWidth={6} strokeLinecap="round" />)}
      </svg>
      <Chip x={RX - 210} y={Y + 2 * RH - 10} o={appear(f, c1 + 24)} text="안 바뀜" color={T.accent} size={34} />
      <Chip x={LX} y={Y + 4 * RH + 20} o={appear(f, c2)} text="2025.10.2 하루에 넣은 경우 · 과거 값" dark={false} size={28} />
      <Chip x={RX} y={Y + 4 * RH + 20} o={appear(f, c2 + 24)} text="예금은 가격이 오르내리지 않음" dark={false} size={28} />
    </P>
  );
};

// ───── 5b. 간격 막대: 예금 vs SCHD, 세전 간격 → 세금 뒤 간격(1억 위 몫만) ─────
const GapBars: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = Math.max(cue(s, 1, 90), Math.floor(s.frames * 0.42)), c2 = Math.max(cue(s, 2, 70), Math.floor(s.frames * 0.7));
  const BASE = 790, H = 460, top = d.pre[1] - 1e8; const sy = (v: number) => ((v - 1e8) / top) * H;
  const t = appear(f, c1, 30);
  const v0 = d.pre[0] + (d.net[0] - d.pre[0]) * t, v1 = d.pre[1] + (d.net[1] - d.pre[1]) * t; const gap = d.gap[0] + (d.gap[1] - d.gap[0]) * t;
  const bar = (x: number, v: number, c: string, name: string) => <>
    <div style={{position: 'absolute', left: x, top: BASE - sy(v), width: 220, height: sy(v), background: c, borderRadius: '14px 14px 0 0'}} />
    <Txt x={x - 40} y={BASE + 16} w={300} align="center" size={32} color={T.ink2}>{name}</Txt>
    <Txt x={x - 40} y={BASE - sy(v) - 52} w={300} align="center" size={34}>{n0(v)}</Txt></>;
  return (
    <P s={s}>
      {bar(360, v0, T.ink2, '예금')}{bar(760, v1, T.ink, 'SCHD')}
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={1010} x2={1010} y1={BASE - sy(v1)} y2={BASE - sy(v0)} stroke={T.accent} strokeWidth={6} />
        <line x1={995} x2={1025} y1={BASE - sy(v1)} y2={BASE - sy(v1)} stroke={T.accent} strokeWidth={6} />
        <line x1={995} x2={1025} y1={BASE - sy(v0)} y2={BASE - sy(v0)} stroke={T.accent} strokeWidth={6} />
      </svg>
      <Txt x={1050} y={BASE - (sy(v1) + sy(v0)) / 2 - 70} size={30} color={T.ink3}>{t < 0.5 ? '세전 간격' : '세금 뒤 간격'}</Txt>
      <Txt x={1050} y={BASE - (sy(v1) + sy(v0)) / 2 - 30} size={64} color={T.accent}>{n0(gap)}</Txt>
      <Chip x={1050} y={BASE - 100} o={appear(f, c2)} text={`세금이 줄인 간격 ${man(d.gap[0] - d.gap[1])}`} color={T.ink} size={32} />
      <Txt x={1050} y={240} size={26} color={T.ink3} weight={500}>막대는 원금 1억 위로 늘어난 몫만</Txt>
    </P>
  );
};

// ───── 6a. 금리 선 2020.1~2026.8 + 기준금리 점선 + 점 세 개 ─────
const RateLine: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1), c2 = cue(s, 2, 80);
  const X = 200, Y = 740, W = 1500, H = 440; const all = d.s as [string, number][]; const n = all.length;
  const sx = (i: number) => X + (i / (n - 1)) * W; const sy = scaleLinear().domain([0, 5.5]).range([Y, Y - H]);
  const idx = (t: string) => all.findIndex((r) => r[0] === t);
  const p = appear(f, 8, 70); const m = Math.max(2, Math.round(n * p));
  const path = d3line<[string, number]>().x((_, i) => sx(i)).y((r) => sy(r[1])).curve(curveMonotoneX)(all.slice(0, m)) || '';
  const base = (d.base as [string, number][]).filter((r) => idx(r[0]) >= 0);
  const bpath = d3line<[string, number]>().x((r) => sx(idx(r[0]))).y((r) => sy(r[1]))(base) || '';
  const dotO = [appear(f, c2), appear(f, 80), appear(f, 90)];
  return (
    <P s={s}>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {[0, 1, 2, 3, 4, 5].map((v) => <g key={v}><line x1={X} x2={X + W} y1={sy(v)} y2={sy(v)} stroke={T.line} strokeWidth={2} />
          <text x={X - 16} y={sy(v) + 9} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{v}%</text></g>)}
        {['2020', '2021', '2022', '2023', '2024', '2025', '2026'].map((y) => { const i = idx(y + '01'); return i < 0 ? null :
          <text key={y} x={sx(i)} y={Y + 40} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{y}</text>; })}
        <path d={bpath} stroke={T.ink3} strokeWidth={4} strokeDasharray="10 8" fill="none" opacity={appear(f, c1)} />
        <path d={path} stroke={T.ink} strokeWidth={6} fill="none" strokeLinejoin="round" />
        {d.dots.map((r: [string, number], k: number) => { const i = idx(r[0]); const o = dotO[k]; const [yy, mm] = [r[0].slice(0, 4), +r[0].slice(4)];
          return <g key={r[0]} opacity={o}><circle cx={sx(i)} cy={sy(r[1])} r={12} fill={k === 2 ? T.accent : T.ink} />
            <rect x={sx(i) - 105} y={sy(r[1]) - 78} width={210} height={50} rx={25} fill={k === 2 ? T.accent : T.ink} />
            <text x={sx(i)} y={sy(r[1]) - 43} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={28} fill="#fff">{`${yy}.${mm} ${r[1].toFixed(2)}%`}</text></g>; })}
      </svg>
      <Chip x={1180} y={240} o={appear(f, c1 + 10)} text="점선 = 한국은행 기준금리 · 지금 3%" dark={false} size={28} />
    </P>
  );
};

// ───── 6c. 공시 점 띠: 은행 39 · 저축은행 320, 실제 가입 평균 3.39% 선 ─────
const Dots: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 60), c2 = cue(s, 2, 60);
  const X = 420, W = 1300, dom: [number, number] = [1.8, 4.3]; const sx = (v: number) => X + ((v - dom[0]) / (dom[1] - dom[0])) * W;
  const o2 = appear(f, c2);
  return (
    <P s={s}>
      <DotStrip x={X} y={350} w={W} dom={dom} vals={d.rows[0][1]} label={d.rows[0][0]} o={appear(f, 10, 50)} seed={3} />
      <DotStrip x={X} y={570} w={W} dom={dom} vals={d.rows[1][1]} label={d.rows[1][0]} o={appear(f, c1, 60)} seed={5} band={90} color={T.ink3} />
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        {[2, 2.5, 3, 3.5, 4].map((v) => <text key={v} x={sx(v)} y={705} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={24} fill={T.ink3}>{v.toFixed(1)}%</text>)}
        <line x1={sx(d.avg)} x2={sx(d.avg)} y1={270} y2={680} stroke={T.fall} strokeWidth={4} strokeDasharray="10 8" opacity={o2} />
      </svg>
      <Chip x={sx(d.avg) - 330} y={205} o={o2} text={`실제 신규 가입 평균 ${d.avg}% — 다른 숫자`} color={T.fall} size={28} />
      <Chip x={sx(4.1) - 300} y={730} o={appear(f, c2 + 40)} text="4.1% = 변동금리" dark={false} size={24} />
    </P>
  );
};

// ───── 7. 줄다리기: 세후 이자 vs 물가만큼 필요 ─────
const Tug: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 60), c2 = cue(s, 2, 60);
  const pull = appear(f, c1 - 30, 40); const kx = 960 + 120 * pull;
  return (
    <P s={s}>
      <Card x={160} y={260} w={560} h={190} o={appear(f, 8)}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink3, padding: '24px 32px 0'}}>세후 이자 (3.39%)</div>
        <div style={{...F, fontWeight: 700, fontSize: 70, color: T.ink, padding: '6px 32px'}}>{n0(d.net)}</div></Card>
      <Card x={1200} y={260} w={560} h={190} o={appear(f, 20)} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.dink3, padding: '24px 32px 0'}}>물가만큼 필요 (지난 1년 +3.09%)</div>
        <div style={{...F, fontWeight: 700, fontSize: 70, color: T.dink, padding: '6px 32px'}}>{n0(d.cpi)}</div></Card>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <path d={`M 300 560 Q ${(300 + kx) / 2} ${575 + 10 * Math.sin(f / 6)} ${kx} 560 Q ${(kx + 1620) / 2} ${575 - 10 * Math.sin(f / 6)} 1620 560`} stroke={T.ink2} strokeWidth={10} fill="none" />
        <line x1={960} x2={960} y1={510} y2={610} stroke={T.line} strokeWidth={4} strokeDasharray="8 8" />
        <circle cx={kx} cy={560} r={22} fill={T.rise} />
      </svg>
      <Txt x={kx - 200} y={620} w={400} align="center" size={56} color={T.rise} o={pull}>{n0(d.diff).replace('-', '−')}</Txt>
      <Chip x={160} y={720} o={appear(f, c1 + 20)} text={`물가만큼 지키려면 세전 ${d.need}% 넘게`} color={T.accent} size={30} />
      <Chip x={1100} y={720} o={appear(f, c2)} text="지난 1년 물가 · 앞으로 1년 아님" dark={false} size={28} />
    </P>
  );
};

// ───── 8. 눈금자 핀 세 개(원금) + 금리 오르면 당겨지는 핀 ─────
const Pins: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const X = 200, W = 1520, Y = 560, MAX = 65000; const sx = (m: number) => X + (m / MAX) * W;
  const alt = appear(f, cue(s, 4), 30);
  return (
    <P s={s}>
      <div style={{position: 'absolute', left: X, top: Y, width: W, height: 12, borderRadius: 6, background: T.line}} />
      {[0, 10000, 20000, 30000, 40000, 50000, 60000].map((m) => <Txt key={m} x={sx(m) - 60} y={Y + 30} w={120} align="center" size={24} color={T.ink3} weight={500}>{m ? `${m / 10000}억` : '0'}</Txt>)}
      {d.pins.map((p: [string, number, string], i: number) => { const o = appear(f, cue(s, i + 1), 16); const up = i % 2 === 0;
        return <div key={p[0]} style={{position: 'absolute', left: sx(p[1]), top: Y + 6, opacity: o}}>
          <div style={{position: 'absolute', left: -3, top: up ? -150 + (1 - o) * -40 : 0, width: 6, height: 150, background: i === 0 ? T.ink : T.accent}} />
          <div style={{position: 'absolute', left: -14, top: -14, width: 28, height: 28, borderRadius: 14, background: i === 0 ? T.ink : T.accent, border: '4px solid #fff'}} />
          <div style={{...F, position: 'absolute', left: -200, width: 400, textAlign: 'center', top: up ? -260 : 170, fontWeight: 700, fontSize: 44, color: i === 0 ? T.ink : T.accent}}>{p[0]}</div>
          <div style={{...F, position: 'absolute', left: -200, width: 400, textAlign: 'center', top: up ? -200 : 230, fontWeight: 700, fontSize: 26, color: T.ink2}}>{p[2]}</div>
        </div>; })}
      <div style={{position: 'absolute', left: sx(d.pins[1][1] + (d.alt[0] - d.pins[1][1]) * alt), top: Y - 30, opacity: alt}}>
        <div style={{position: 'absolute', left: -14, top: 0, width: 28, height: 28, borderRadius: 14, border: `4px dashed ${T.rise}`}} /></div>
      <Chip x={sx(d.alt[0]) - 120} y={Y - 110} o={alt} text={d.alt[1]} color={T.rise} size={28} />
    </P>
  );
};

// ───── 9a. 요약 카드: 4줄 막대 + 지금 예금 카드 ─────
const Sum4: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const c1 = cue(s, 1, 90); const top = d.rows[0][1] - 1e8;
  return (
    <P s={s}>
      <Card x={160} y={230} w={980} h={560} o={appear(f, 6)}>
        {d.rows.map((r: [string, number, number], i: number) => { const o = appear(f, 14 + i * 14, 20);
          return <div key={r[0]} style={{position: 'absolute', left: 36, right: 36, top: 36 + i * 128, height: 110, opacity: o}}>
            <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink2}}>{i + 1}. {r[0]}</div>
            <div style={{position: 'absolute', left: 0, top: 54, height: 34, width: 520 * ((r[1] - 1e8) / top) * o, background: i === 0 ? T.accent : T.ink, borderRadius: 8}} />
            <div style={{...F, position: 'absolute', right: 0, top: 6, fontWeight: 700, fontSize: 44, color: T.ink}}>{man(r[1])}</div>
            <div style={{...F, position: 'absolute', right: 0, top: 62, fontWeight: 500, fontSize: 26, color: T.ink3}}>+{r[2].toFixed(2)}%</div>
          </div>; })}
      </Card>
      <Card x={1200} y={230} w={560} h={560} o={appear(f, c1)} bg={T.ink}>
        <div style={{...F, fontWeight: 700, fontSize: 30, color: T.dink3, padding: '36px 40px 0'}}>지금 예금</div>
        <div style={{...F, fontWeight: 700, fontSize: 64, color: T.dink, padding: '10px 40px 0'}}>{d.now[0]}%</div>
        <div style={{...F, fontWeight: 500, fontSize: 26, color: T.dink3, padding: '0 40px'}}>8월 신규 평균</div>
        <div style={{...F, fontWeight: 700, fontSize: 52, color: T.daccent, padding: '30px 40px 0'}}>월 {n0(d.now[1])}</div>
        <div style={{...F, fontWeight: 500, fontSize: 26, color: T.dink3, padding: '0 40px'}}>세후 이자 ÷ 12</div>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.dink, padding: '30px 40px 0'}}>물가만큼 = 세전 {d.now[2]}%</div>
      </Card>
    </P>
  );
};

// ───── 9b. 계산기 화면(자산 칸에 1억 입력만, 결과 숫자 짓지 않음) ─────
const Cta: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data; const typed = Math.floor(interpolate(f, [30, 70], [0, 5], CL)); const dg = String(d.x).slice(0, typed);
  return (
    <P s={s}>
      <Card x={460} y={240} w={1000} h={440} o={appear(f, 6)} style={{boxShadow: '0 12px 40px rgba(0,0,0,0.08)'}}>
        <div style={{...F, fontWeight: 700, fontSize: 26, color: T.ink3, padding: '28px 44px 0'}}>firemap.kr · 은퇴 나이 계산기</div>
        <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, padding: '30px 44px 10px'}}>지금 모은 자산</div>
        <div style={{margin: '0 44px', height: 110, borderRadius: 16, border: `4px solid ${T.accent}`, display: 'flex', alignItems: 'center', padding: '0 30px'}}>
          <span style={{...F, fontWeight: 700, fontSize: 72, color: T.ink}}>{dg ? Number(dg).toLocaleString() : ' '}</span>
          <span style={{width: 4, height: 70, background: T.ink, marginLeft: 6, opacity: Math.floor(f / 15) % 2}} />
          <span style={{...F, fontWeight: 700, fontSize: 44, color: T.ink3, marginLeft: 'auto'}}>만원</span>
        </div>
        <div style={{margin: '30px 44px', height: 90, borderRadius: 16, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: appear(f, 90)}}>
          <span style={{...F, fontWeight: 700, fontSize: 40, color: '#fff'}}>은퇴 나이 보기</span></div>
      </Card>
      <Chip x={460} y={720} o={appear(f, 30)} text="설명란 링크 · 투자 권유 아님" size={30} dark={false} />
    </P>
  );
};

const View: React.FC<S> = ({s}) => {
  switch (s.kind) {
    case 'open4': return <Open4 s={s} />; case 'logo': return <LogoSting sub={s.data.sub} />; case 'receipt': return <Receipt s={s} />;
    case 'fx': return <Fx s={s} />; case 'receipt2': return <Receipt2 s={s} />; case 'taxcalc': return <TaxCalc s={s} />; case 'calendar': return <Calendar s={s} />;
    case 'duo': return <Duo s={s} />; case 'goldfx': return <GoldFx s={s} />; case 'ranks': return <Ranks s={s} />; case 'gapbars': return <GapBars s={s} />;
    case 'rateline': return <RateLine s={s} />; case 'dots': return <Dots s={s} />; case 'tug': return <Tug s={s} />; case 'pins': return <Pins s={s} />;
    case 'sum4': return <Sum4 s={s} />; case 'cta': return <Cta s={s} />;
    default: return <P s={s}>{null}</P>;
  }
};

export const R1: React.FC<R1Props> = ({scenes, rail}) => {
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
export const _unused = {CountUp};
