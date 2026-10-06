// 모션 부품 — 거꾸로 묻기(M-1 월배당 첫 장면). TallyFrame 보드 안에서 쓴다.
// ① 보통 방향: 왼쪽 '큰돈' → 오른쪽 '매달 ?'로 화살표(말 fwd) → ② 화살표가 걷히고 오른쪽 카드가 목표 글자로 바뀐 뒤
// 화살표가 거꾸로(오른쪽→왼쪽) 달려 '?' 셋에 닿음(말 rev) → ③ 카메라 1단 줌아웃, '?' 셋이 바닥선 위 막대 자리로 내려앉고 막대가 0에서 자람(말 grow)
// → ④ 말이 가리키는 막대만 주황(말 hi[i]) → ⑤ 카메라 2단 줌인, 한 막대가 '가장 적은 달' 높이로 늘어남(빗금 = 늘어난 몫, 말 low).
// '흰 판 위 깊이': 카드·막대에 두 겹 그림자, 바탕 점 격자는 카메라의 절반만 움직이는 뒷층(시차). 캐릭터·실사 없음.
// 막대 높이만 값 비례(0 기준선 공유), 글자는 props 원문 그대로 — 숫자를 굴리지 않는다(가짜 중간 숫자 0, 교본 10/4).
// seed로 바뀌는 건 의미 없는 칸뿐(막대 폭·간격·화살표 휨·격자 간격) — 순서·높이는 바꾸지 않는다(교본 10/5).
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type ReverseAskProps = {
  seed: string;
  big: string;                  // 왼쪽 '큰돈' 글자
  ask0: string;                 // 처음 오른쪽 카드 글자(예: '매달 ?')
  goal: string;                 // 거꾸로 묻는 목표(예: '매달 100만원')
  goalSub: string;              // 목표 아래 작은 글자(예: '세금·건보료 뗀 뒤')
  bars: [string, number, string][];   // [이름, 값(높이 비례), 값 글자] — 대본 순서
  low: {i: number; v: number; label: string; times: string; tag: string};  // 늘어나는 막대(말이 가리키는 것, 주황)
  also: {i: number; v: number; label: string; times: string}[];   // 같은 규칙으로 함께 늘어나는 막대(잉크, 한 막대만 늘면 나머지가 안전해 보이는 오독 방지 — 심사 10/5)
  note: [number, string][];     // 같은 규칙을 못 쓰는 막대의 이유 칩(예: 분기 지급)
  hook?: string; hookSub?: string;
  stamp?: string; stampSub?: string; stampAt?: number;   // 말 5(기준일·권유 아님): 판 가운데 어두운 도장 판이 내려앉았다 위로 걷힘 — 막대 다 자란 뒤 정지 끊기(레드팀 10/6). 글자는 대본 원문 조각만.   // 첫 화면(0~fwd): 판 가득 큰 목표 숫자 — 첫 30초 힘(심사 10/5 공통 지적: 흰 판·상자 2개). 글자는 대본 원문만.
  fwd: number; nope: number; rev: number; land: number; grow: number; hi: [number, number][]; low0: number;  // 프레임: 보통 방향·거꾸로·막대·[강조 프레임, 막대 번호]·늘어남
};

const hash = (s: string) => { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
const ease = Easing.inOut(Easing.cubic);
const out = Easing.out(Easing.cubic);
const fade = (f: number, a: number, d = 12) => interpolate(f, [a, a + d], [0, 1], CL);
const lift = '0 2px 4px rgba(24,25,29,0.06), 0 18px 40px rgba(24,25,29,0.10)';
const liftHi = '0 3px 6px rgba(255,90,0,0.10), 0 26px 54px rgba(255,90,0,0.16)';

export const ReverseAsk: React.FC<ReverseAskProps> = (p) => {
  const f = useCurrentFrame();
  const h = hash(p.seed);
  const bw = 150 + ((h >> 2) % 3) * 16;           // 막대 폭
  const gapX = 300 + ((h >> 5) % 3) * 20;         // 막대 간격
  const bend = [-40, 0, 40][(h >> 7) % 3];        // 화살표 휨
  const grid = 44 + ((h >> 9) % 3) * 6;           // 바탕 격자 간격

  // 무대(월드 좌표, 1920×1080 판 안)
  const base = 790;                                // 0 기준선
  const vmax = Math.max(p.low.v, ...p.also.map((a) => a.v), ...p.bars.map((b) => b[1]));
  const px = 460 / vmax;                           // 값 1 = px
  const n = p.bars.length;
  const cx0 = 960 - ((n - 1) * gapX) / 2;
  const xs = p.bars.map((_, i) => cx0 + i * gapX);
  const L = {x: 420, y: 470}; const R = {x: 1400, y: 470};   // 왼쪽 '큰돈'·오른쪽 카드 가운데

  // 카메라 2단: 처음 1.16배(화살표 가운데) → grow에서 1배 → low0에서 늘어날 막대 쪽으로 옆 이동만(판 높이 616px라 확대하면 0 기준선·이름이 잘림, 10/5 시험)
  const c1 = interpolate(f, [p.land - 10, p.land + 40], [0, 1], {...CL, easing: ease});
  const c2 = interpolate(f, [p.low0 - 6, p.low0 + 40], [0, 1], {...CL, easing: ease});
  const drift = interpolate(f, [0, p.land], [0, 1], CL);
  // 말 3 '거꾸로'(rev): 카메라가 화살표·물음표 쪽으로 1.32배 당겨 판을 채움(심사 10/6 Claude: 15.7초도 0.7초처럼 판 가득)
  const c0 = interpolate(f, [p.rev - 22, p.rev + 8], [0, 1], {...CL, easing: ease});
  const zA = 1.16 - 0.04 * drift; const zR = zA + (1.32 - zA) * c0;
  const push = interpolate(f, [p.low0 + 84, p.low0 + 360], [0, 1], {...CL, easing: Easing.inOut(Easing.quad)});   // 늘어난 뒤 끝까지 천천히 다가감(끝 8초 정지 끊기)
  const z = (zR + (1 - zR) * c1) * (1 + 0.1 * push);
  const fxA = 900 + 60 * c0;
  const fx = fxA + (960 - fxA) * c1 + (xs[p.low.i] - 960) * 0.45 * c2;   // 화면 가운데에 올 월드 x
  const fy = 470 + (560 - 470) * c1 + 30 * push;   // 다가가는 동안 아래로 보정 — 0 기준선·막대 이름이 판 안에 남게(레드팀 10/6 잘림)
  const tx = 960 - z * fx; const ty = 545 - z * fy;
  const bz = Math.sqrt(z); const btx = (960 - bz * fx) * 0.5; const bty = (545 - bz * fy) * 0.5;  // 뒷층: 절반만

  // 0. 여는 판(hook): 판 가득 목표 숫자 → fwd-24~fwd-6에 앞으로 날아가며 걷히고 무대가 뒤에서 들어옴
  const hk = p.hook ? interpolate(f, [p.fwd - 24, p.fwd - 4], [0, 1], {...CL, easing: ease}) : 1;
  // 말 '큰돈이 없잖아요': '큰돈' 카드가 판을 다 채운 어두운 판으로 커짐(nope~+16) → 줄(+18~+34) → 지폐 떨어짐(+30~) → 원래 자리로 줄어들며 걷힘(+58~+78)
  const sOpen = interpolate(f, [p.nope, p.nope + 16], [0, 1], {...CL, easing: out});
  const sBack = interpolate(f, [p.nope + 58, p.nope + 78], [0, 1], {...CL, easing: ease});
  const sw0 = sOpen * (1 - sBack);
  const sCut = interpolate(f, [p.nope + 18, p.nope + 34], [0, 1], {...CL, easing: out});
  const sFall = interpolate(f, [p.nope + 30, p.nope + 54], [0, 1], {...CL, easing: Easing.in(Easing.quad)});
  // 지폐 쌓임(말 '큰돈을 넣으면'): fwd+20부터 한 장씩 — 숫자 없는 그림
  const BILLS = 7;
  const bill = (k: number) => interpolate(f, [p.fwd + 20 + k * 12, p.fwd + 30 + k * 12], [0, 1], {...CL, easing: out});
  // ① 보통 방향 화살표: fwd~fwd+30 그려짐, rev-30부터 걷힘
  const a1 = interpolate(f, [p.fwd, p.fwd + 30], [0, 1], {...CL, easing: out}) * (1 - fade(f, p.nope + 20, 16));
  // 말 '큰돈이 없잖아요'(nope): 큰돈 카드에 줄이 그어지고 작아지며 흐려짐
  const no = interpolate(f, [p.nope + 58, p.nope + 78], [0, 1], {...CL, easing: out});
  // ② 거꾸로: 카드 글자 바뀜(rev-14), 화살표 rev~rev+34
  const sw = fade(f, p.rev - 16, 10);
  const a2 = interpolate(f, [p.rev, p.rev + 34], [0, 1], {...CL, easing: out});
  const qIn = (k: number) => fade(f, p.rev + 26 + k * 7, 10);
  // ③ '?' 셋이 막대 자리로 내려앉음, 화살표·카드는 위로 걷힘
  const settle = interpolate(f, [p.land, p.land + 36], [0, 1], {...CL, easing: ease});   // 말 '상품 셋' — 막대가 자라는 때(grow)와 나눠 정지 구간을 끊는다
  const topO = 1 - settle;
  const growK = interpolate(f, [p.grow + 10, p.grow + 46], [0, 1], {...CL, easing: out});
  // ④ 강조: 지금 가리키는 막대 번호
  let hiIdx = -1; for (const [a, i] of p.hi) if (f >= a) hiIdx = i;
  if (f >= p.low0 - 6) hiIdx = p.low.i;
  // ⑤ 늘어남
  const ext = interpolate(f, [p.low0 + 24, p.low0 + 74], [0, 1], {...CL, easing: ease});
  const extDone = fade(f, p.low0 + 74, 10);

  const curve = (x1: number, x2: number, y: number, k: number) => {
    const mx = (x1 + x2) / 2; const my = y + bend;
    // 2차 곡선을 k까지만 — 점들을 이어 그린다
    const pts: string[] = [];
    for (let i = 0; i <= 40; i++) { const t = (i / 40) * k; const x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * x2; const yy = (1 - t) ** 2 * y + 2 * (1 - t) * t * my + t * t * y; pts.push(`${x.toFixed(1)},${yy.toFixed(1)}`); }
    const t = Math.max(0.001, k); const ex = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * x2; const ey = (1 - t) ** 2 * y + 2 * (1 - t) * t * my + t * t * y;
    const dx = 2 * (1 - t) * (mx - x1) + 2 * t * (x2 - mx); const dy = 2 * (1 - t) * (my - y) + 2 * t * (y - my); const ang = Math.atan2(dy, dx) * 180 / Math.PI;
    return {d: pts.join(' '), ex, ey, ang};
  };
  const A1 = curve(L.x + 150, R.x - 190, L.y, a1);
  const A2 = curve(R.x - 190, L.x + 300, R.y, a2);

  const card = (x: number, y: number, w: number, hgt: number, hi: boolean, o: number, s = 1): React.CSSProperties => ({
    position: 'absolute', left: x - w / 2, top: y - hgt / 2, width: w, height: hgt, borderRadius: 26, background: T.surface, opacity: o,
    boxShadow: hi ? liftHi : lift, border: `2px solid ${hi ? T.accent : T.line}`, transform: `scale(${s})`,
    display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', ...F,
  });

  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'hidden', clipPath: 'inset(238px 102px 230px 102px round 22px)'}}>
      {/* 뒷층: 점 격자(시차) */}
      <div style={{position: 'absolute', left: -400, top: -400, width: 2720, height: 1880, transformOrigin: '400px 400px',
        transform: `translate(${btx}px, ${bty}px) scale(${bz})`,
        backgroundImage: `radial-gradient(${T.line} 2.2px, transparent 2.4px)`, backgroundSize: `${grid}px ${grid}px`, opacity: 0.9}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '0 0', transform: `translate(${tx}px, ${ty}px) scale(${z})`}}>
        {/* ①② 위층: 큰돈 · 화살표 · 카드 */}
        <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, opacity: topO, transform: `translateY(${-60 * settle}px)`}}>
          <div style={card(L.x, L.y, 320, 280, false, (1 - sw) * (1 - 0.55 * no) * (1 - sOpen * (1 - sBack)), 1 - 0.22 * no)}>
            <div style={{position: 'relative', width: 200, height: BILLS * 17 + 20, marginBottom: 10}}>
              {Array.from({length: BILLS}, (_, k) => (k + 1) / BILLS > 1 - sFall ? null : (
                <div key={k} style={{position: 'absolute', left: ((h >> (k % 8)) % 3) * 6 - 6, bottom: k * 17, width: 200, height: 30, borderRadius: 6, boxSizing: 'border-box',
                  background: T.soft, border: `3px solid ${T.accent}`, opacity: bill(k), transform: `translateY(${(1 - bill(k)) * -26}px)`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 700, fontSize: 18, color: T.accent, lineHeight: 1}}>₩</div>))}
            </div>
            <div style={{fontWeight: 700, fontSize: 60, color: T.ink, position: 'relative'}}>{p.big}
              <div style={{position: 'absolute', left: -14, top: '52%', height: 6, borderRadius: 3, background: T.ink, width: `calc(${no * 100}% + 28px)`, opacity: no > 0.01 ? 1 : 0}} />
            </div>
          </div>
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
            {a1 > 0.01 && <>
              <polyline points={A1.d} fill="none" stroke={T.ink3} strokeWidth={6} strokeLinecap="round" />
              <path d="M -22 -14 L 0 0 L -22 14" fill="none" stroke={T.ink3} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" transform={`translate(${A1.ex},${A1.ey}) rotate(${A1.ang})`} />
            </>}
            {a2 > 0.01 && <>
              <polyline points={A2.d} fill="none" stroke={T.accent} strokeWidth={8} strokeLinecap="round" />
              <path d="M -26 -17 L 0 0 L -26 17" fill="none" stroke={T.accent} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" transform={`translate(${A2.ex},${A2.ey}) rotate(${A2.ang})`} />
            </>}
          </svg>
          <div style={card(R.x, R.y, 360, 190, sw > 0.5, 1, 1 + 0.06 * Math.sin(Math.PI * sw))}>
            <div style={{fontWeight: 700, fontSize: 56, color: sw > 0.5 ? T.accent : T.ink, whiteSpace: 'nowrap'}}>{sw > 0.5 ? p.goal : p.ask0}</div>
            {sw > 0.5 && <div style={{fontWeight: 500, fontSize: 26, color: T.ink2, marginTop: 6, opacity: fade(f, p.rev - 6, 10), whiteSpace: 'nowrap'}}>{p.goalSub}</div>}
          </div>
        </div>
        {/* 0 기준선 */}
        <div style={{position: 'absolute', left: xs[0] - bw, top: base, width: xs[n - 1] - xs[0] + 2 * bw, height: 4, borderRadius: 2, background: T.ink3, opacity: fade(f, p.land + 20, 14)}} />
        {/* '?' 셋 → 막대 */}
        {p.bars.map((b, i) => {
          const q0 = {x: L.x + 90 + (i - (n - 1) / 2) * 110, y: L.y};
          const qx = q0.x + (xs[i] - q0.x) * settle; const qy = q0.y + (base - 70 - q0.y) * settle;
          const hgt = b[1] * px * growK;
          const isLow = i === p.low.i; const al = p.also.find((a) => a.i === i);
          const extH = isLow ? (p.low.v - b[1]) * px * ext : al ? (al.v - b[1]) * px * ext : 0;
          const hi = hiIdx === i; const dim = hiIdx >= 0 && !hi && !(al && f >= p.low0);
          const qO = qIn(i) * (1 - fade(f, p.grow + 4, 10));
          const hold = interpolate(f, [p.land + 36, p.grow], [0, 1], CL);   // 내려앉은 '?'가 바닥선 위에서 천천히 숨 쉼
          return (
            <React.Fragment key={i}>
              <div style={{...F, position: 'absolute', left: qx - 50, top: qy - 60, width: 100, height: 120, display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontWeight: 700, fontSize: 132, color: T.accent, opacity: qO, transform: `scale(${(0.6 + 0.4 * qIn(i)) * (1 + 0.08 * Math.sin(Math.PI * 2 * hold + i))})`}}>?</div>
              <div style={{...F, position: 'absolute', left: xs[i] - 200, width: 400, top: base + 18, textAlign: 'center', whiteSpace: 'nowrap',
                  fontWeight: 700, fontSize: 34, color: dim ? T.ink3 : T.ink2, opacity: fade(f, p.land + 30 + i * 8, 12)}}>{b[0]}</div>
              {growK > 0 && <>
                {/* 늘어난 몫(빗금) — 원래 막대 위에 쌓임 */}
                {extH > 0.5 && <div style={{position: 'absolute', left: xs[i] - bw / 2, top: base - hgt - extH, width: bw, height: extH + 2, borderRadius: '8px 8px 0 0',
                  background: `repeating-linear-gradient(135deg, ${isLow ? T.accent : T.ink3} 0 6px, ${isLow ? T.soft : T.surface} 6px 18px)`, border: `2px dashed ${isLow ? T.accent : T.ink3}`, borderBottom: 'none', boxSizing: 'border-box'}} />}
                <div style={{position: 'absolute', left: xs[i] - bw / 2, top: base - hgt, width: bw, height: hgt, borderRadius: extH > 0.5 ? 0 : '8px 8px 0 0',
                  background: hi ? (isLow && f >= p.low0 - 6 ? T.accent : T.ink) : '#c9ced6', boxShadow: hi && isLow && f >= p.low0 - 6 ? liftHi : lift, opacity: dim ? 0.35 : 1}} />
                {/* 값 글자(막대 다 자란 뒤, 굴리지 않음) */}
                <div style={{...F, position: 'absolute', left: xs[i] - 160, width: 320, top: base - hgt - 74 - (isLow ? extH : 0), textAlign: 'center', whiteSpace: 'nowrap',
                  fontWeight: 700, fontSize: 50, color: T.ink, opacity: fade(f, p.grow + 46, 10) * (dim ? 0.35 : 1) * (isLow || al ? 1 - fade(f, p.low0 + 24, 8) : 1)}}>{b[2]}</div>

              </>}
            </React.Fragment>
          );
        })}
        {/* ⑤ 늘어난 뒤 글자: 원래 값 → 새 값, 배수 칩 */}
        {(() => {
          const i = p.low.i; const top = base - p.low.v * px; const o = extDone;
          return (
            <>
              <div style={{...F, position: 'absolute', left: xs[i] + bw / 2 + 22, top: top - 12, whiteSpace: 'nowrap', fontWeight: 700, fontSize: 64, color: T.accent, opacity: o}}>{p.low.label}</div>
              <div style={{...F, position: 'absolute', left: xs[i] + bw / 2 + 22, top: top + 72, whiteSpace: 'nowrap', opacity: o, transform: `translateX(${(1 - o) * 14}px)`,
                background: T.surface, boxShadow: lift, borderRadius: 14, padding: '8px 18px', border: `2px solid ${T.line}`}}>
                <div style={{fontWeight: 700, fontSize: 40, color: T.ink}}>{p.low.times}</div>
                <div style={{fontWeight: 700, fontSize: 30, color: T.ink2}}>{p.low.tag}</div>
              </div>
              <div style={{...F, position: 'absolute', left: xs[i] + bw / 2 + 22, top: base - p.bars[i][1] * px - 22, whiteSpace: 'nowrap', opacity: fade(f, p.low0 + 30, 10),
                fontWeight: 700, fontSize: 30, color: T.ink3}}>{p.bars[i][2]}</div>
              {p.also.map((al) => { const t2 = base - al.v * px; return (
                <div key={al.i} style={{...F, position: 'absolute', left: xs[al.i] - 160, width: 320, top: t2 - 150, textAlign: 'center', whiteSpace: 'nowrap', opacity: o}}>
                  <div style={{fontWeight: 700, fontSize: 46, color: T.ink}}>{al.label}</div>
                  <div style={{fontWeight: 700, fontSize: 32, color: T.ink2}}>{al.times}</div>
                  <div style={{fontWeight: 700, fontSize: 30, color: T.ink3}}>{p.bars[al.i][2]}</div>
                </div>); })}
              {p.note.map(([ni, txt]) => (
                <div key={ni} style={{...F, position: 'absolute', left: xs[ni] - 200, width: 400, top: base - p.bars[ni][1] * px - 132, textAlign: 'center', whiteSpace: 'nowrap', opacity: o}}>
                  <span style={{background: T.surface, border: `2px solid ${T.line}`, boxShadow: lift, borderRadius: 12, padding: '6px 16px', fontWeight: 700, fontSize: 32, color: T.ink2}}>{txt}</span>
                </div>))}
            </>
          );
        })()}
      </div>
      {/* 판 덮개 둘(화면 좌표): 여는 판 · '큰돈' 판 — 말 1·2에서 화면 절반 이상이 바뀌는 단계 전환 */}
      {(() => {
        const B = {x: 102, y: 238, w: 1716, h: 612};
        const lx = tx + z * L.x; const ly = ty + z * L.y; const lw = z * 320; const lh = z * 280;
        const r = (k: number) => ({left: lx - lw / 2 + (B.x - (lx - lw / 2)) * k, top: ly - lh / 2 + (B.y - (ly - lh / 2)) * k, width: lw + (B.w - lw) * k, height: lh + (B.h - lh) * k});
        return (
          <>
            {p.hook && hk < 1 && (
              <div style={{position: 'absolute', left: B.x, top: B.y, width: B.w, height: B.h, background: T.surface, opacity: 1 - hk, ...F,
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 + 0.9 * hk})`}}>
                <div style={{fontWeight: 700, fontSize: 190, color: T.accent, letterSpacing: -4, lineHeight: 1,
                  transform: `scale(${interpolate(f, [0, 10], [0.86, 1], {...CL, easing: out})})`}}>{p.hook}</div>
                <div style={{fontWeight: 700, fontSize: 64, color: T.ink, marginTop: 34, opacity: fade(f, 8, 10)}}>{p.hookSub}</div>
              </div>
            )}
            {p.stamp && p.stampAt !== undefined && (() => {
              const a = interpolate(f, [p.stampAt, p.stampAt + 12], [0, 1], {...CL, easing: out});
              const b = interpolate(f, [p.stampAt + 96, p.stampAt + 116], [0, 1], {...CL, easing: ease});
              if (a <= 0 || b >= 1) return null;
              return (
                <div style={{position: 'absolute', left: 410, top: 256, width: 1100, height: 250, borderRadius: 26, background: T.ink, ...F,
                  display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: a * (1 - b),
                  transform: `translateY(${-260 * b}px) scale(${1.25 - 0.25 * a})`, boxShadow: '0 30px 80px rgba(24,25,29,0.35)'}}>
                  <div style={{fontWeight: 700, fontSize: 84, color: T.dink, letterSpacing: -2}}>{p.stamp}</div>
                  <div style={{fontWeight: 700, fontSize: 40, color: T.daccent, marginTop: 14, opacity: fade(f, p.stampAt + 16, 10)}}>{p.stampSub}</div>
                </div>);
            })()}
            {sw0 > 0.001 && (
              <div style={{position: 'absolute', ...r(sw0), borderRadius: 26 * (1 - sw0) + 22 * sw0, background: T.ink, overflow: 'hidden', ...F,
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: Math.min(1, sw0 * 3)}}>
                <div style={{position: 'relative', width: 520, height: 210, marginBottom: 18, transform: `scale(${0.35 + 0.65 * sw0})`}}>
                  {Array.from({length: BILLS}, (_, k) => (
                    <div key={k} style={{position: 'absolute', left: ((h >> (k % 8)) % 3) * 14 - 14, bottom: k * 26, width: 520, height: 46, borderRadius: 10, boxSizing: 'border-box',
                      border: `4px solid ${T.daccent}`, background: T.dsurface, display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 700, fontSize: 32, color: T.daccent, lineHeight: 1,
                      transform: `translate(${sFall * (k % 2 ? 1 : -1) * (60 + k * 22)}px, ${sFall * (520 + k * 40)}px) rotate(${sFall * (k % 2 ? 1 : -1) * (14 + k * 4)}deg)`}}>₩</div>))}
                </div>
                <div style={{position: 'relative', fontWeight: 700, fontSize: 170 * (0.35 + 0.65 * sw0), color: T.dink, lineHeight: 1}}>{p.big}
                  <div style={{position: 'absolute', left: -30, top: '40%', height: 16, borderRadius: 8, background: T.daccent, width: `calc(${sCut * 100}% + 60px)`, opacity: sCut > 0.01 ? 1 : 0}} />
                </div>
              </div>
            )}
          </>
        );
      })()}
    </div>
  );
};
