// D-1 "퇴직 후 건강보험료 — 배당·이자·연금 얼마부터 붙나" — 재료: work/video/d1.json(ep/D-1/d1props.py가 script.md·voice.json·facts.txt로 만든다)
// 장면 종류 16가지: 숫자 카드 두 장(여는)·로고·목록·갈림길 흐름도·칸 채우는 계산식·조문 카드+이하/초과 칸·절벽 막대·ETF 화살표 도식·연금 쌓은 막대·달력 줄·체크리스트·
// 36개월 기간 띠·재산 입력 칸·3단계 카드·정리 카드 5장·계산기 카드. 숫자는 전부 d1.json에서 온다(코드에는 배치 값만). 단계 시점은 data.at(문장 번호, 못 찾으면 −1=안 나옴).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {T, F, CL, FONT_CSS, VScene, at, appear, HandCircle, CountUp, Caption, Page, LogoSting, ProgressRail} from './parts/fm';
import {CondTag, Flow, Tokens, CliffBars, MonthRows, PeriodBand, StepCards, CheckList} from './parts/explain';

type DScene = VScene & {tag?: string | null};
export type D1Props = {fps: number; rail: string[]; scenes: DScene[]; missing: number; holes: number};
export const d1Frames = (p: D1Props) => p.scenes.reduce((a, s) => a + s.frames, 0);
type S = {s: DScene; rail: string[]};
const NEVER = 1e9;
const idx = (s: VScene, k: number) => s.data.at?.[k] ?? -1;
const A = (s: VScene, k: number) => (idx(s, k) < 0 ? NEVER : at(s, idx(s, k)));
// 문장 k의 중간(fr=0~1) — 문장이 긴데 그림이 멈춰 있지 않게
const M = (s: VScene, k: number, fr: number) => (idx(s, k) < 0 ? NEVER : at(s, idx(s, k)) + Math.round(fr * (s.lines[idx(s, k)]?.frames ?? 0)));
const won = (v: number) => `${v.toLocaleString()}원`;
const Card: React.FC<{x: number; y: number; w: number; h: number; o?: number; bg?: string; border?: string; children?: React.ReactNode}> = ({x, y, w, h, o = 1, bg = T.surface, border, children}) => (
  <div style={{position: 'absolute', left: x, top: y + (1 - o) * 24, width: w, height: h, background: bg, borderRadius: 22, opacity: o, border: border ? `4px solid ${border}` : 'none', boxSizing: 'border-box'}}>{children}</div>
);
const Chip: React.FC<{x: number; y: number; o: number; tone?: 'ink' | 'rise' | 'line' | 'soft'; size?: number; children: React.ReactNode}> = ({x, y, o, tone = 'ink', size = 32, children}) => (
  <div style={{...F, position: 'absolute', left: x, top: y + (1 - o) * 16, opacity: o, fontWeight: 700, fontSize: size, whiteSpace: 'nowrap', borderRadius: 40, padding: '10px 28px',
    background: tone === 'ink' ? T.ink : tone === 'rise' ? T.rise : tone === 'soft' ? T.soft : T.line, color: tone === 'line' || tone === 'soft' ? T.ink : '#fff'}}>{children}</div>
);
const P: React.FC<S & {children: React.ReactNode}> = ({s, rail, children}) => (
  <Page s={{...s, rail: 0}}>
    {s.rail ? <ProgressRail n={5} cur={s.rail} labels={rail} on={T.ink} /> : null}
    {s.tag ? <CondTag text={s.tag} /> : null}
    {children}
  </Page>
);

// ───── 0. 여는 장면: 숫자 카드 두 장 — 1,000만원 / 1,001만원 → 22,800원 / 67,850원 ─────
const Open: React.FC<S> = ({s}) => {
  const f = useCurrentFrame(); const d = s.data;
  const c0 = appear(f, A(s, 0) === NEVER ? 6 : A(s, 0)), c1 = appear(f, M(s, 0, 0.55)), q = appear(f, A(s, 1));
  const v0 = appear(f, A(s, 2), 24), v1 = appear(f, M(s, 2, 0.5), 30), dy = appear(f, A(s, 3)), py = appear(f, A(s, 4)), law = appear(f, A(s, 5));
  const card = (i: number, o: number, v: number) => {
    const [amt, prem] = d.cards[i]; const x = i === 0 ? 240 : 1010; const hot = i === 1;
    return (
      <div key={i} style={{position: 'absolute', left: x, top: 150 + (1 - o) * 24, width: 670, height: 540, background: T.dsurface, borderRadius: 26, opacity: o,
        border: `4px solid ${hot && v > 0.5 ? T.rise : 'transparent'}`, boxSizing: 'border-box'}}>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.dink3, position: 'absolute', left: 50, top: 44}}>{d.label}</div>
        <div style={{...F, fontWeight: 700, fontSize: 116, color: T.dink, position: 'absolute', left: 46, top: 88, lineHeight: 1.1}}>{amt}</div>
        <div style={{position: 'absolute', left: 50, right: 50, top: 270, height: 3, background: '#2a2c33', opacity: q}} />
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.dink3, position: 'absolute', left: 50, top: 300, opacity: q}}>{d.unit}</div>
        <div style={{...F, fontWeight: 700, fontSize: 120, position: 'absolute', left: 46, top: 346, lineHeight: 1.1, color: hot ? T.rise : T.dink, opacity: q}}>
          {v > 0.01 ? <><CountUp to={prem} p={v} />원</> : <span style={{color: T.dink3}}>?</span>}</div>
      </div>
    );
  };
  return (
    <AbsoluteFill style={{background: T.dbg}}>
      {s.tag ? <CondTag text={s.tag} dark /> : null}
      {card(0, c0, v0)}{card(1, c1, v1)}
      <div style={{...F, position: 'absolute', left: 900, top: 262, width: 120, textAlign: 'center', fontWeight: 700, fontSize: 30, color: T.dink3, opacity: c1, whiteSpace: 'nowrap'}}>+1만원</div>
      <div style={{...F, position: 'absolute', left: 240, top: 728, opacity: dy, transform: `translateY(${(1 - dy) * 16}px)`, fontWeight: 700, fontSize: 38, color: '#fff', background: T.rise, borderRadius: 40, padding: '12px 30px', whiteSpace: 'nowrap'}}>
        1년 차이 +{won(d.diff_y)}</div>
      <div style={{...F, position: 'absolute', left: 1010, top: 728, opacity: py, transform: `translateY(${(1 - py) * 16}px)`, fontWeight: 700, fontSize: 34, color: T.dink, background: T.dsurface, borderRadius: 40, padding: '14px 30px', whiteSpace: 'nowrap'}}>
        국민연금 월 150만원이면 1년 +{won(d.pen_y)}</div>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}><HandCircle cx={1330} cy={572} rx={300} ry={78} p={law} /></svg>
      <div style={{...F, fontWeight: 500, fontSize: 18, color: T.dink3, position: 'absolute', left: 120, right: 110, bottom: 20}}>출처 {s.source}</div>
      <Caption s={s} dark />
    </AbsoluteFill>
  );
};

// ───── 1. 오늘 볼 다섯 가지 ─────
const Agenda: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const items: string[] = s.data.items;
  const st = [A(s, 1), M(s, 1, 0.55), A(s, 2), M(s, 2, 0.4), M(s, 2, 0.7)];
  return (
    <P s={s} rail={rail}>
      {items.map((t, i) => { const o = appear(f, st[i] === NEVER ? 20 + i * 20 : st[i]);
        return (
          <div key={t} style={{position: 'absolute', left: 220, top: 245 + i * 116, display: 'flex', alignItems: 'center', gap: 34, opacity: o, transform: `translateX(${(1 - o) * -30}px)`}}>
            <div style={{width: 88, height: 88, borderRadius: 20, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <span style={{...F, fontWeight: 700, fontSize: 50, color: '#fff'}}>{i + 1}</span></div>
            <span style={{...F, fontWeight: 700, fontSize: 60, color: T.ink}}>{t}</span>
          </div>); })}
    </P>
  );
};

// ───── 2. 갈림길 흐름도: 퇴직 → ① 피부양자 0원 / ② 지역가입자 소득+재산 ─────
const Fork: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame();
  const o0 = appear(f, A(s, 0)), o1 = appear(f, A(s, 1)), e = appear(f, M(s, 1, 0.3), 20), t = appear(f, A(s, 2)), t2 = appear(f, M(s, 2, 0.45)), b = appear(f, A(s, 3)), b2 = appear(f, M(s, 3, 0.5)), me = appear(f, A(s, 4), 24);
  return (
    <P s={s} rail={rail}>
      <Flow
        nodes={[
          {x: 210, y: 250, w: 360, h: 130, title: '회사 다닐 때', sub: '월급 기준 보험료', o: o0, tone: 'line'},
          {x: 210, y: 470, w: 360, h: 170, title: '퇴직', o: o1, tone: 'ink', big: true},
          {x: 760, y: 280, w: 460, h: 170, title: '① 피부양자', sub: '가족 중 직장가입자 밑으로', o: t},
          {x: 1330, y: 280, w: 460, h: 170, title: '본인 보험료 0원', o: t2, tone: 'line', big: true},
          {x: 760, y: 590, w: 460, h: 170, title: '② 지역가입자', sub: '피부양자 조건이 안 맞으면', o: b},
          {x: 1330, y: 590, w: 460, h: 170, title: '소득 + 재산', sub: '으로 보험료 계산', o: b2, tone: 'ink', big: true},
        ]}
        edges={[
          {pts: [[390, 380], [390, 466]], o: o1},
          {pts: [[570, 555], [665, 555], [665, 365], [754, 365]], o: e},
          {pts: [[570, 555], [665, 555], [665, 675], [754, 675]], o: e},
          {pts: [[1220, 365], [1324, 365]], o: t2},
          {pts: [[1220, 675], [1324, 675]], o: b2},
        ]} />
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <rect x={738} y={570} width={1074} height={210} rx={30} fill="none" stroke={T.accent} strokeWidth={6} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - me} /></svg>
      <Chip x={1290} y={796} o={me} tone="soft" size={28}>오늘 계산은 이 길(지역가입자) 기준</Chip>
    </P>
  );
};

// ───── 3. 계산식 한 칸씩: (연소득 ÷ 12) × 7.19% + 재산 점수 × 211.5원 → + 장기요양 13.14% → 소득 종류 칩 ─────
const Formula: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  const t0 = appear(f, A(s, 0)), a = appear(f, A(s, 1)), a2 = appear(f, M(s, 1, 0.55)), b = appear(f, A(s, 2)), b2 = appear(f, M(s, 2, 0.5)), c = appear(f, A(s, 3)), law = appear(f, A(s, 4));
  const kinds = appear(f, A(s, 5)), nontax = appear(f, M(s, 5, 0.65)), q = appear(f, A(s, 6));
  return (
    <P s={s} rail={rail}>
      <Card x={200} y={240} w={1600} h={250} o={t0}>
        <div style={{...F, position: 'absolute', left: 40, top: 22, fontWeight: 700, fontSize: 26, color: T.ink3}}>월 건강보험료 =</div>
      </Card>
      <Tokens x={240} y={300} size={52} toks={[
        {t: '(', o: a, op: true}, {t: '연소득 ÷ 12', o: a, tone: 'ink', w: 360, sub: '소득월액'}, {t: ')', o: a, op: true},
        {t: '×', o: a2, op: true}, {t: `${d.rate}%`, o: a2, w: 200, sub: '보험료율', tone: 'soft'},
        {t: '+', o: b, op: true}, {t: '재산 점수', o: b, w: 260, sub: '재산분'}, {t: '×', o: b2, op: true}, {t: `${d.pt}원`, o: b2, w: 230, tone: 'soft', sub: '점수당'},
      ]} />
      <Tokens x={240} y={530} size={44} toks={[{t: '+', o: c, op: true}, {t: '장기요양', o: c, w: 230}, {t: '=', o: c, op: true}, {t: `건보료 × ${d.ltc}`, o: c, w: 380, tone: 'soft'}]} />
      <Chip x={1290} y={252} o={law} tone="line" size={24}>7.19%·211.5원 = 2026년 값 · 시행령 제44조</Chip>
      <div style={{...F, position: 'absolute', left: 1020, top: 560, fontWeight: 500, fontSize: 24, color: T.ink3, opacity: c}}>장기요양 0.9448% ÷ 7.19% — 공단 모의계산 안내문</div>
      <div style={{position: 'absolute', left: 200, top: 680, display: 'flex', alignItems: 'center', gap: 14, opacity: kinds}}>
        <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, marginRight: 10}}>소득에 들어가는 것</span>
        {d.kinds.map((k: string, i: number) => { const hot = i < 2 && q > 0.5;
          return <span key={k} style={{...F, fontWeight: 700, fontSize: 32, padding: '8px 22px', borderRadius: 30, background: hot ? T.rise : T.ink, color: '#fff', opacity: appear(f, A(s, 5) + i * 6)}}>{k}</span>; })}
        <span style={{...F, fontWeight: 700, fontSize: 30, padding: '8px 22px', borderRadius: 30, background: T.line, color: T.ink3, opacity: nontax, textDecoration: 'line-through'}}>비과세 소득</span>
      </div>
      <Chip x={200} y={770} o={q} tone="rise" size={30}>이자·배당은 똑같이 다 들어가지 않는다 →</Chip>
    </P>
  );
};

// ───── 4a. 조문 카드 + 이하/초과 두 칸 ─────
const Statute: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data; const h = appear(f, A(s, 0)), qo = appear(f, A(s, 1), 20), r0 = appear(f, M(s, 1, 0.6)), r1 = appear(f, A(s, 2)), r1b = appear(f, M(s, 2, 0.5));
  return (
    <P s={s} rail={rail}>
      <div style={{position: 'absolute', left: 200, top: 240 + (1 - h) * 20, width: 1600, height: 300, background: T.surface, borderRadius: 22, borderTop: `8px solid ${T.ink}`, opacity: h}}>
        <div style={{...F, fontWeight: 700, fontSize: 28, color: T.ink3, padding: '26px 44px 0'}}>{d.head}</div>
        <div style={{position: 'absolute', left: 40, top: 70, fontFamily: 'PD', fontWeight: 700, fontSize: 120, color: T.line, lineHeight: 1}}>“</div>
        <div style={{...F, position: 'absolute', left: 120, right: 60, top: 96, fontWeight: 700, fontSize: 52, color: T.ink, lineHeight: 1.4, wordBreak: 'keep-all', whiteSpace: 'pre-line', opacity: qo}}>{d.quote}</div>
      </div>
      {d.rows.map(([k, v, hot]: [string, string, boolean], i: number) => { const o = i ? r1 : r0;
        return <Card key={k} x={200 + i * 820} y={580} w={780} h={220} o={o} border={hot ? T.rise : undefined}>
          <div style={{...F, position: 'absolute', left: 44, top: 30, fontWeight: 700, fontSize: 34, color: T.ink3}}>{`이자 + 배당 ${k}`}</div>
          <div style={{...F, position: 'absolute', left: 44, top: 86, right: 30, fontWeight: 700, fontSize: 52, color: hot ? T.rise : T.ink, wordBreak: 'keep-all', lineHeight: 1.25, opacity: hot ? r1b : 1}}>{v}</div>
        </Card>; })}
    </P>
  );
};

// ───── 4b. 절벽 막대 6개: 1,000만원 → 1,001만원에서 뚝 솟는다 ─────
const Cliff: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  const p = [appear(f, A(s, 1), 24), appear(f, M(s, 1, 0.5), 24), appear(f, A(s, 3), 24), appear(f, A(s, 4), 24), appear(f, A(s, 5), 24), appear(f, M(s, 5, 0.5), 24)];
  return (
    <P s={s} rail={rail}>
      <div style={{...F, position: 'absolute', left: 260, top: 236, fontWeight: 700, fontSize: 28, color: T.ink2, opacity: appear(f, A(s, 0))}}>가로: 1년 이자 + 배당(금융소득) · 세로: 월 건보료</div>
      <CliffBars x={260} y={800} w={1500} h={430} rows={d.rows} p={p} jumpAt={d.jumpAt} jumpP={appear(f, M(s, 3, 0.4), 24)} jumpLabel={d.jump}
        floor={d.floor} floorP={appear(f, A(s, 2), 24)} floorLabel={d.floorLabel} fmt={won} />
      <Chip x={260} y={300} o={appear(f, A(s, 6))} tone="rise" size={34}>{`1,000만 → 1,001만: ${d.year}`}</Chip>
    </P>
  );
};

// ───── 4c. ETF → 분배금 → 배당소득 → 금융소득 합계 (해외주식형 매매차익 점선) ─────
const Etf: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame();
  const d0 = appear(f, A(s, 0)), e1 = appear(f, A(s, 1)), e1b = appear(f, M(s, 1, 0.4)), ex = appear(f, A(s, 2)), ov = appear(f, A(s, 3)), ovb = appear(f, M(s, 3, 0.4)), it = appear(f, A(s, 4)), sum = appear(f, M(s, 4, 0.5));
  return (
    <P s={s} rail={rail}>
      <Flow
        nodes={[
          {x: 200, y: 270, w: 320, h: 160, title: '국내 상장 ETF', o: e1},
          {x: 600, y: 270, w: 280, h: 160, title: '분배금', o: e1b},
          {x: 960, y: 270, w: 320, h: 160, title: '배당소득', sub: '소득세법', o: d0, tone: 'ink', big: true},
          {x: 1370, y: 270, w: 420, h: 160, title: '금융소득 합계', sub: '이자 + 배당 → 1,000만원 넘나?', o: sum, tone: 'soft'},
          {x: 200, y: 580, w: 520, h: 150, title: '국내 상장주식 매매 손익', sub: 'ETF 이익 계산에서 뺀다', o: ex, tone: 'line'},
          {x: 860, y: 580, w: 500, h: 150, title: '해외주식형 ETF 매매차익', sub: '팔아서 남긴 차익도', o: ovb},
          {x: 1440, y: 580, w: 350, h: 150, title: '예금 이자', o: it},
        ]}
        edges={[
          {pts: [[520, 350], [594, 350]], o: e1b},
          {pts: [[880, 350], [954, 350]], o: e1b},
          {pts: [[1280, 350], [1364, 350]], o: sum},
          {pts: [[1110, 580], [1110, 436]], o: ovb, dashed: true},
          {pts: [[1615, 580], [1615, 436]], o: sum},
        ]} />
      <Chip x={200} y={510} o={ex} tone="line" size={26}>배당소득에서 제외</Chip>
      <Chip x={200} y={770} o={ov} tone="ink" size={28}>국내 주식형 ETF: 매매차익 빠짐 · 해외주식형 등: 매매차익도 배당소득</Chip>
    </P>
  );
};

// ───── 5. 국민연금: 1,800만원 중 절반만 반영 → 쌓은 막대 두 개 61,000원 / 128,860원 ─────
const Pension: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  const b0 = appear(f, A(s, 0)), half = appear(f, A(s, 1), 24), lab = appear(f, A(s, 2)), pr = appear(f, A(s, 3)), L = appear(f, A(s, 4), 24), R = appear(f, A(s, 5), 24), R2 = appear(f, M(s, 5, 0.5)), yr = appear(f, A(s, 6)), circ = appear(f, A(s, 7), 24);
  const X = 220, W = 1180, Y = 300;
  const base = 800, H = 250, mx = d.half + d.fin[1]; const hh = (v: number) => (v / mx) * H;
  const bar = (x: number, fin: number, counted: boolean, o: number, prem: number, name: string) => (
    <g opacity={Math.min(1, o * 3)}>
      <rect x={x} y={base - hh(d.half) * o} width={220} height={hh(d.half) * o} rx={6} fill={T.ink} />
      <text x={x + 110} y={base - hh(d.half) / 2 + 10} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill="#fff" opacity={o}>{`연금 ${d.half.toLocaleString()}만`}</text>
      <rect x={x} y={base - (hh(d.half) + hh(fin)) * o} width={220} height={hh(fin) * o} rx={6} fill={counted ? T.rise : 'none'} stroke={counted ? 'none' : T.ink3} strokeWidth={3} strokeDasharray={counted ? undefined : '10 8'} />
      <text x={x + 110} y={base - hh(d.half) - hh(fin) / 2 - 6} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={counted ? '#fff' : T.ink3} opacity={o}>{`금융 ${fin.toLocaleString()}만`}</text>
      <text x={x + 110} y={base - hh(d.half) - hh(fin) / 2 + 26} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={counted ? '#fff' : T.ink3} opacity={o}>{counted ? '전액 합산' : '합산 안 함'}</text>
      <text x={x + 110} y={base - hh(d.half) - hh(fin) - 18} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={40} fill={counted ? T.rise : T.ink} opacity={o}>{won(prem)}</text>
      <text x={x + 110} y={base + 38} textAnchor="middle" fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink2}>{name}</text>
    </g>
  );
  return (
    <P s={s} rail={rail}>
      <div style={{...F, position: 'absolute', left: X, top: Y - 56, fontWeight: 700, fontSize: 30, color: T.ink2, opacity: b0}}>{`국민연금 1년 ${d.pen.toLocaleString()}만원`}</div>
      <div style={{position: 'absolute', left: X, top: Y, width: W, height: 90, borderRadius: 12, background: T.line, opacity: b0}} />
      <div style={{position: 'absolute', left: X, top: Y, width: (W / 2) * half, height: 90, borderRadius: 12, background: T.ink, opacity: b0}} />
      <div style={{...F, position: 'absolute', left: X + 30, top: Y + 22, fontWeight: 700, fontSize: 36, color: '#fff', opacity: half}}>50% 반영</div>
      <div style={{...F, position: 'absolute', left: X + W / 2 + 30, top: Y + 22, fontWeight: 700, fontSize: 36, color: T.ink3, opacity: half}}>반영 안 함</div>
      <div style={{...F, position: 'absolute', left: X, top: Y + 104, fontWeight: 700, fontSize: 32, color: T.ink, opacity: lab}}>{`보험료에 들어가는 소득 ${d.half.toLocaleString()}만원`}</div>
      <Card x={1450} y={250} w={350} h={190} o={pr}>
        <div style={{...F, position: 'absolute', left: 32, top: 26, fontWeight: 700, fontSize: 28, color: T.ink3}}>월 건보료</div>
        <div style={{...F, position: 'absolute', left: 30, top: 70, fontWeight: 700, fontSize: 70, color: T.ink}}><CountUp to={d.p0} p={pr} />원</div>
      </Card>
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={440} x2={1080} y1={base} y2={base} stroke={T.ink3} strokeWidth={2} opacity={L} />
        {bar(480, d.fin[0], false, L, d.p0, `+ 금융 ${d.fin[0].toLocaleString()}만원`)}
        {bar(820, d.fin[1], true, R, d.p1, `+ 금융 ${d.fin[1].toLocaleString()}만원`)}
      </svg>
      <Chip x={1180} y={560} o={R2} tone="rise" size={38}>{d.diff}</Chip>
      <Chip x={1180} y={650} o={yr} tone="ink" size={32}>{d.year}</Chip>
      <Chip x={1180} y={740} o={circ} tone="soft" size={28}>연금이 있으면 절벽이 더 크다</Chip>
    </P>
  );
};

// ───── 6. 달력 줄: 2026년에 받은 소득 → 2027년 11월분(배당·이자) / 1월분(연금) ─────
const Calendar: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame();
  const r0 = appear(f, A(s, 0), 24), div = appear(f, A(s, 1), 24), pen = appear(f, A(s, 2), 30), ex = appear(f, A(s, 3), 24), q = appear(f, A(s, 4));
  const x = 470, cell = 110, y = 290, gap = 190;
  return (
    <P s={s} rail={rail}>
      <MonthRows x={x} y={y} cell={cell} rowGap={gap} years={['2026년', '2027년 배당·이자', '2027년 연금']} spans={[
        {row: 0, from: 0, to: 11, tone: 'soft', o: r0, label: '2026년에 받은 배당·이자·연금'},
        {row: 1, from: 10, to: 11, tone: 'ink', o: div, label: '배당·이자 등: 11월분부터 (→ 2028년 10월분까지)', right: true, below: true},
        {row: 2, from: 0, to: 11, tone: 'fall', o: pen, label: '연금소득만: 1월분 ~ 12월분'},
      ]} />
      <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}} opacity={ex}>
        <path d={`M ${x + 6 * cell} ${y + 70} C ${x + 6 * cell} ${y + 140}, ${x + 10.5 * cell} ${y + 100}, ${x + 10.5 * cell} ${y + gap - 10}`} fill="none" stroke={T.rise} strokeWidth={5}
          pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ex} />
        <polygon points={`${x + 10.5 * cell},${y + gap - 4} ${x + 10.5 * cell - 12},${y + gap - 26} ${x + 10.5 * cell + 12},${y + gap - 26}`} fill={T.rise} opacity={ex > 0.9 ? 1 : 0} />
      </svg>
      <Chip x={470} y={780} o={q} tone="line" size={30}>고지서가 예상과 다르면 → 몇 년도 소득으로 계산됐는지부터</Chip>
      <Chip x={470} y={780} o={Math.min(ex, 1 - q)} tone="rise" size={30}>예: 2026년에 받은 배당 → 2027년 11월분 고지서부터</Chip>
    </P>
  );
};

// ───── 7a. 피부양자 체크리스트 2칸 ─────
const Check: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  const o = appear(f, A(s, 0)); const s0 = appear(f, A(s, 1)), s1 = appear(f, A(s, 2)), s1b = appear(f, A(s, 3)), out = appear(f, A(s, 4));
  return (
    <P s={s} rail={rail}>
      <CheckList x={200} y={250} w={1600} rowH={230} items={d.items} o={[o, appear(f, M(s, 0, 0.5))]} sub={[s0, s1b]} check={[appear(f, M(s, 1, 0.3), 16), appear(f, M(s, 2, 0.4), 16)]} />
      <div style={{position: 'absolute', left: 1240, top: 610, opacity: s1 * (1 - s1b)}}>
        <span style={{...F, fontWeight: 700, fontSize: 30, color: T.ink3}}>5억 4,000만원을 넘으면?</span></div>
      <Chip x={200} y={775} o={out} tone="rise" size={32}>하나라도 넘으면 → 지역가입자</Chip>
    </P>
  );
};

// ───── 7b. 36개월 기간 띠(임의계속가입) ─────
const Band: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  const p = interpolate(f, [A(s, 0), M(s, 0, 0.7)], [0, 1], CL); const law = appear(f, M(s, 0, 0.7)), cmp = appear(f, A(s, 1)), cmp2 = appear(f, M(s, 1, 0.3)), note = appear(f, M(s, 1, 0.65));
  return (
    <P s={s} rail={rail}>
      <PeriodBand x0={260} x1={1700} y={350} n={d.months} p={f < A(s, 0) ? 0 : p} start="퇴직 다음 날" end={`${d.months}개월을 넘지 않는 범위`} />
      <Chip x={260} y={490} o={law} tone="line" size={28}>임의계속가입자 · 국민건강보험법 시행령 제77조①</Chip>
      <Card x={260} y={570} w={560} h={160} o={cmp}>
        <div style={{...F, position: 'absolute', left: 36, top: 28, fontWeight: 700, fontSize: 28, color: T.ink3}}>공단 모의계산</div>
        <div style={{...F, position: 'absolute', left: 36, top: 76, fontWeight: 700, fontSize: 46, color: T.ink}}>지역보험료</div></Card>
      <div style={{...F, position: 'absolute', left: 850, top: 610, fontWeight: 700, fontSize: 52, color: T.ink3, opacity: cmp2}}>vs</div>
      <Card x={960} y={570} w={560} h={160} o={cmp2}>
        <div style={{...F, position: 'absolute', left: 36, top: 28, fontWeight: 700, fontSize: 28, color: T.ink3}}>공단 모의계산</div>
        <div style={{...F, position: 'absolute', left: 36, top: 76, fontWeight: 700, fontSize: 46, color: T.ink}}>임의계속보험료</div></Card>
      <Chip x={260} y={752} o={note} tone="line" size={26}>어느 쪽이 적은지는 사람마다 · 신청 자격·기한은 공단에 확인</Chip>
    </P>
  );
};

// ───── 8a. 재산 입력 칸 재현 — 집이 있으면 / 전월세 ─────
const Field: React.FC<{label: string; unit?: string; o: number; op?: string}> = ({label, unit = '원', o, op}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: 16, height: 84, opacity: o}}>
    <span style={{...F, width: 70, fontWeight: 700, fontSize: 38, color: T.ink3, textAlign: 'center'}}>{op || ''}</span>
    <div style={{flex: 1, height: 72, borderRadius: 14, border: `3px solid ${T.line}`, background: T.bg, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 22px'}}>
      <span style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2}}>{label}</span><span style={{...F, fontWeight: 500, fontSize: 28, color: T.ink3}}>{unit}</span></div>
  </div>
);
const Property: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame();
  const zero = appear(f, A(s, 0)), own = appear(f, A(s, 1)), own2 = appear(f, M(s, 1, 0.5)), rent = appear(f, A(s, 2)), rent2 = appear(f, M(s, 2, 0.45)), rent3 = appear(f, M(s, 2, 0.75)), pts = appear(f, A(s, 3));
  return (
    <P s={s} rail={rail}>
      <Chip x={200} y={236} o={zero} tone="line" size={28}>앞의 표는 재산 0 — 집이 있으면 재산분이 더 붙는다</Chip>
      <Card x={200} y={320} w={780} h={430} o={own}>
        <div style={{...F, position: 'absolute', left: 36, top: 28, fontWeight: 700, fontSize: 36, color: T.ink}}>집이 있으면</div>
        <div style={{position: 'absolute', left: 20, right: 36, top: 100}}>
          <Field label="재산세 과세표준(6월 1일)" o={own} />
          <Field label="1억원 공제" unit="" op="−" o={own2} />
          <Field label="점수를 매길 금액" op="=" o={own2} />
        </div></Card>
      <Card x={1020} y={320} w={780} h={430} o={rent}>
        <div style={{...F, position: 'absolute', left: 36, top: 28, fontWeight: 700, fontSize: 36, color: T.ink}}>집이 없으면(전월세)</div>
        <div style={{position: 'absolute', left: 20, right: 36, top: 100}}>
          <Field label="보증금" o={rent} />
          <Field label="월세 × 40" op="+" o={rent2} />
          <Field label="합계 × 30% = 재산" op="→" unit="" o={rent3} />
        </div></Card>
      <Chip x={200} y={780} o={pts} tone="soft" size={28}>재산 점수표 60등급 — 금액은 공단 모의계산에서 직접</Chip>
    </P>
  );
};

// ───── 8b. 공단 모의계산 입력 3단계 ─────
const Steps: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  return (
    <P s={s} rail={rail}>
      <StepCards x={200} y={270} w={480} h={430} gap={80} steps={d.steps} o={[appear(f, A(s, 0)), appear(f, A(s, 1)), appear(f, M(s, 2, 0.5))]} />
      <Chip x={200} y={740} o={appear(f, M(s, 0, 0.6))} tone="line" size={28}>소득과 재산 과세표준을 넣으면 바로 계산</Chip>
    </P>
  );
};

// ───── 9a. 정리 카드 5장 ─────
const Summary: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const cards = s.data.cards;
  return (
    <P s={s} rail={rail}>
      {cards.map(([h, m, sub]: string[], i: number) => { const o = appear(f, A(s, i) === NEVER ? 10 + i * 20 : A(s, i)); const x = 200 + (i % 3) * 540, y = 240 + Math.floor(i / 3) * 290;
        return <Card key={h} x={x} y={y} w={510} h={265} o={o}>
          <div style={{position: 'absolute', left: 30, top: 26, width: 50, height: 50, borderRadius: 25, background: T.ink, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <span style={{...F, fontWeight: 700, fontSize: 28, color: '#fff'}}>{i + 1}</span></div>
          <div style={{...F, position: 'absolute', left: 96, top: 32, fontWeight: 700, fontSize: 30, color: T.ink3}}>{h}</div>
          <div style={{...F, position: 'absolute', left: 30, right: 26, top: 96, fontWeight: 700, fontSize: 34, color: T.ink, lineHeight: 1.3, wordBreak: 'keep-all'}}>{m}</div>
          <div style={{...F, position: 'absolute', left: 30, right: 26, bottom: 24, fontWeight: 500, fontSize: 26, color: T.ink2, wordBreak: 'keep-all'}}>{sub}</div>
        </Card>; })}
    </P>
  );
};

// ───── 9b. 계산기 카드 — 생활비 칸에 '+ 건보료', firemap.kr ─────
const Calc: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame(); const d = s.data;
  const c = appear(f, A(s, 0)), plus = appear(f, A(s, 1)), res = appear(f, M(s, 1, 0.45)), disc = appear(f, A(s, 2));
  const row = (k: string, i: number, hot = false) => (
    <div key={k} style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: 96, padding: '0 36px', borderBottom: i < 3 ? `2px solid ${T.line}` : 'none'}}>
      <span style={{...F, fontWeight: 700, fontSize: 34, color: hot ? T.ink : T.ink2}}>{k}</span>
      <div style={{display: 'flex', alignItems: 'center', gap: 14}}>
        <div style={{width: 200, height: 54, borderRadius: 12, background: T.bg, border: `3px solid ${hot ? T.ink : T.line}`}} />
        {hot ? <span style={{...F, fontWeight: 700, fontSize: 32, color: '#fff', background: T.accent, borderRadius: 30, padding: '6px 20px', opacity: plus, whiteSpace: 'nowrap'}}>+ 건보료</span> : null}
      </div>
    </div>
  );
  return (
    <P s={s} rail={rail}>
      <Card x={200} y={250} w={860} h={420} o={c}>
        <div style={{height: 20}} />
        {['나이', '모은 돈', '매달 저축'].map((k, i) => row(k, i))}{row('월 생활비', 3, true)}
      </Card>
      <Card x={1120} y={250} w={680} h={420} o={res}>
        <div style={{...F, position: 'absolute', left: 44, top: 40, fontWeight: 700, fontSize: 32, color: T.ink3}}>생활비에 건보료를 더하면</div>
        <div style={{...F, position: 'absolute', left: 44, top: 110, right: 40, fontWeight: 700, fontSize: 50, color: T.ink, lineHeight: 1.3, wordBreak: 'keep-all'}}>은퇴 나이가 몇 년 달라지는지</div>
        <div style={{...F, position: 'absolute', left: 44, bottom: 40, fontWeight: 700, fontSize: 64, color: T.accent}}>{d.url}</div>
      </Card>
      <Chip x={200} y={720} o={disc} tone="line" size={26}>2026년 법령·공단 계산식 기준 · 경감·다른 소득에 따라 달라짐 · 정확한 금액은 공단 모의계산·고객센터</Chip>
      <Chip x={200} y={720} o={c * (1 - plus)} tone="soft" size={28}>건보료 = 매달 나가는 고정 지출</Chip>
    </P>
  );
};

const Bullets: React.FC<S> = ({s, rail}) => {
  const f = useCurrentFrame();
  return <P s={s} rail={rail}>{s.lines.slice(0, 6).map((l, i) => <div key={i} style={{...F, fontWeight: 700, fontSize: 40, color: T.ink, position: 'absolute', left: 200, right: 200, top: 250 + i * 95,
    opacity: appear(f, at(s, i)), wordBreak: 'keep-all'}}>{l.text}</div>)}</P>;
};

const View: React.FC<S> = (p) => {
  switch (p.s.kind) {
    case 'open': return <Open {...p} />; case 'logo': return <LogoSting sub={p.s.data.sub} />; case 'agenda': return <Agenda {...p} />;
    case 'fork': return <Fork {...p} />; case 'formula': return <Formula {...p} />; case 'statute': return <Statute {...p} />; case 'cliff': return <Cliff {...p} />;
    case 'etf': return <Etf {...p} />; case 'pension': return <Pension {...p} />; case 'calendar': return <Calendar {...p} />; case 'check': return <Check {...p} />;
    case 'band': return <Band {...p} />; case 'property': return <Property {...p} />; case 'steps': return <Steps {...p} />; case 'summary': return <Summary {...p} />;
    case 'calc': return <Calc {...p} />;
    default: return <Bullets {...p} />;
  }
};

export const D1: React.FC<D1Props> = ({scenes, rail}) => {
  let acc = 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      {scenes.map((s, i) => {
        const from = acc; acc += s.frames; let a = 6;
        return (
          <Sequence key={i} from={from} durationInFrames={s.frames}>
            <View s={s} rail={rail} />
            {s.lines.map((l, j) => { const st = a; a += l.frames;
              return l.audio ? <Sequence key={j} from={st} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null; })}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
