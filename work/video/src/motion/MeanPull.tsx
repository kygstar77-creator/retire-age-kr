// 평균이 끌려간다(MeanPull) — N-3 '7. 평균 4,475만원과 상위 25%'(2026-10-29 motion). TallyFrame 자식.
// 돈 자(0 ~ xMax 만원) 위에 깃발 둘: 평균(먹)·가운데(회색). 자 오른쪽 끝 너머에서 상위 1% 추가 내려앉고 줄이 평균 깃발에 걸려 팽팽해진다.
// 평균 깃발은 자리를 옮기지 않는다(옮기면 '1%를 빼면 평균이 얼마'라는 사실표에 없는 숫자가 생긴다) — 줄에 끌려 기울고 화살표만 앞을 가리킨다.
// 가운데 깃발은 그대로 서 있다. 두 깃발 사이 폭에 답 하나(주황) + 손 밑줄. N1·N2 '100명 줄'(사람 점)과 다른 꼴(반복 템플릿 신호 피하기).
// 글자는 전부 HTML(카메라 안 SVG 글자 어긋남 10/13). 판 전체 1.00→1.04 다가가기(U5 10/19). 숫자 글자는 props만(편별 props 스크립트가 calc·대본 assert).
// 시각 at = 말 줄 번호 + 줄 안 비율(1.4 = 둘째 줄 40% 자리).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random, spring, useVideoConfig} from 'remotion';
import {T, F, CL} from '../parts/fm';
import {HandUnderline} from '../parts/human';

export type MeanPullProps = {
  seed: string;
  xMax: number; ticks: number[];                         // 만원
  mean: {v: number; label: string; text: string; at: number};
  mid: {v: number; label: string; text: string; at: number; stay: string};
  top: {label: string; text: string; at: number; pull: number};   // 추가 내려앉는 때(at) · 줄이 팽팽해지는 때(pull)
  gap: {text: string; at: number};
  unit: string;
  beats: number[];
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});

export const MeanPull: React.FC<MeanPullProps> = (p) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats; const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? 1e9; const n = (B[i + 1] ?? a + 150) - a; return a + n * (x - i); };
  const sp = (a: number, damping = 12) => spring({frame: f - a, fps, config: {damping}});
  // 자: y = ZY. 왼쪽 X0 ~ 오른쪽 X1, 그 너머 끊김 표시 뒤에 추(TX)
  const ZY = 540 + Math.round(r('y') * 30), X0 = 190, X1 = 1330, TX = 1600;   // ZY 640→540: 아래 답 글자가 출처 줄에 닿음(10/29 눈 검사)
  const X = (v: number) => X0 + v / p.xMax * (X1 - X0);
  const endF = (B[B.length - 1] ?? 0) + 150;
  const push = interpolate(f, [0, endF], [1, 1.04], CL);
  // 자는 왼쪽부터 써지듯
  const ruler = g(f, 2, 26, Easing.inOut(Easing.cubic));
  const mA = at(p.mean.at), dA = at(p.mid.at), tA = at(p.top.at), pA = at(p.top.pull), gA = at(p.gap.at);
  const mIn = sp(mA, 10), dIn = sp(dA, 10);
  const tIn = sp(tA, 9);                                    // 추가 위에서 툭 떨어짐
  const rope = g(f, tA + 10, 22);                           // 줄이 추에서 깃발로 그어짐
  const taut = g(f, pA, 20, Easing.inOut(Easing.quad));     // 팽팽해짐
  const shake = f > pA ? Math.sin((f - pA) / 2.2) * Math.exp(-(f - pA) / 18) * 6 : 0;
  const gapO = g(f, gA, 12);
  // 답이 열릴 땐 줄이 느슨해지고 깃발이 바로 선다 — 차이 전체가 추(1%) 탓으로 읽히지 않게(10/29 심사: 1%를 빼도 평균은 중간값보다 한참 위)
  const off = g(f, gA - 6, 16);
  const lean = (taut * 13 + shake) * (1 - off);             // 평균 깃발 오른쪽(앞)으로 기욺(도)
  const mx = X(p.mean.v), dx = X(p.mid.v);
  const POLE = 230;
  const Flag: React.FC<{x: number; o: number; color: string; label: string; text: string; tilt: number; side: 1 | -1}> = ({x, o, color, label, text, tilt, side}) => (
    <div style={{position: 'absolute', left: x, top: ZY - POLE, width: 0, height: POLE, transformOrigin: '0 100%', transform: `translateY(${(1 - o) * -60}px) rotate(${tilt}deg)`, opacity: Math.min(1, o * 1.4)}}>
      <div style={{position: 'absolute', left: -3, top: 0, width: 6, height: POLE, background: color, borderRadius: 3}} />
      <div style={{position: 'absolute', [side > 0 ? 'left' : 'right']: 3, top: 4, padding: '8px 16px 10px', background: color, color: '#fff', clipPath: side > 0 ? 'polygon(0 0, 100% 0, 92% 50%, 100% 100%, 0 100%)' : 'polygon(0 0, 100% 0, 100% 100%, 0 100%, 8% 50%)', whiteSpace: 'nowrap', textAlign: side > 0 ? 'left' : 'right'}}>
        <div style={{...F, fontWeight: 700, fontSize: 30, lineHeight: 1.1, paddingRight: side > 0 ? 18 : 0, paddingLeft: side > 0 ? 0 : 18}}>{label}</div>
        <div style={{...F, fontWeight: 800, fontSize: 54, lineHeight: 1.05, letterSpacing: -1, paddingRight: side > 0 ? 18 : 0, paddingLeft: side > 0 ? 0 : 18}}>{text}</div>
      </div>
    </div>
  );
  // 줄 끝: 장대 30% 높이(깃발 천 아래 — 줄이 글자를 긋지 않게)
  const hookY = ZY - POLE * 0.3; const rad = lean * Math.PI / 180;
  const hx = mx + Math.sin(rad) * POLE * 0.3, hy = ZY - Math.cos(rad) * POLE * 0.3;
  const wx = TX - 90, wy = ZY - 70;                         // 추 왼쪽 고리
  const sag = (1 - taut + off * 0.6) * 120;                             // 처진 줄 → 팽팽
  const ropePath = `M ${wx} ${wy} Q ${(wx + hx) / 2} ${Math.max(wy, hookY) + sag} ${hx} ${hy}`;
  const AY = ZY - POLE - 40;
  const sideM: 1 | -1 = 1, sideD: 1 | -1 = -1;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${push})`, transformOrigin: '50% 60%'}}>
      {/* 자 */}
      <div style={{position: 'absolute', left: X0, top: ZY - 3, width: (X1 - X0) * ruler, height: 6, background: T.ink, borderRadius: 3}} />
      {p.ticks.map((t, i) => {
        const o = g(f, 2 + 26 * (X(t) - X0) / (X1 - X0), 8);
        return <React.Fragment key={i}>
          <div style={{position: 'absolute', left: X(t) - 2, top: ZY, width: 4, height: 18, background: T.ink, opacity: o}} />
          <div style={{position: 'absolute', left: X(t) - 100, top: ZY + 26, width: 200, textAlign: 'center', opacity: o, ...F, fontWeight: 700, fontSize: 30, color: T.ink2}}>{t === 0 ? '0' : t.toLocaleString()}</div>
        </React.Fragment>;
      })}
      <div style={{position: 'absolute', left: X1 - 150, top: ZY + 66, width: 300, textAlign: 'center', opacity: g(f, 24, 10), ...F, fontWeight: 700, fontSize: 26, color: T.ink3}}>{p.unit}</div>
      {/* 끊김 표시 — 자 너머는 멀다 */}
      <div style={{position: 'absolute', left: X1 + 40, top: ZY - 26, opacity: g(f, tA - 6, 10), ...F, fontWeight: 800, fontSize: 52, color: T.ink3, letterSpacing: -6}}>/ /</div>
      <div style={{position: 'absolute', left: X1 + 120, top: ZY - 3, width: (TX - 60 - X1 - 120) * g(f, tA - 4, 14), height: 6, background: T.ink3, borderRadius: 3, opacity: 0.6}} />
      {/* 가운데 깃발(그대로) */}
      <Flag x={dx} o={dIn} color={T.ink2} label={p.mid.label} text={p.mid.text} tilt={0} side={sideD} />
      <div style={{position: 'absolute', left: dx - 260, top: ZY - POLE - 64, width: 250, textAlign: 'right', opacity: g(f, pA + 14, 12) * (1 - off), ...F, fontWeight: 700, fontSize: 30, color: T.ink2}}>{p.mid.stay}</div>
      {/* 평균 깃발(끌려 기욺) */}
      <Flag x={mx} o={mIn} color={T.ink} label={p.mean.label} text={p.mean.text} tilt={lean} side={sideM} />
      {/* 줄 */}
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible', pointerEvents: 'none'}}>
        <path d={ropePath} fill="none" stroke={T.ink2} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - rope} opacity={1 - off * 0.7} />
        {/* 당기는 쪽 화살표(깃발 위, 팽팽해진 뒤) */}
                <polyline points={`${mx + 40},${AY} ${mx + 150},${AY}`} fill="none" stroke={T.ink} strokeWidth={6} strokeLinecap="round" opacity={taut * (1 - off)} />
        <polyline points={`${mx + 132},${AY - 14} ${mx + 152},${AY} ${mx + 132},${AY + 14}`} fill="none" stroke={T.ink} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" opacity={taut * (1 - off)} />
      </svg>
      {/* 추 — 상위 1% */}
      <div style={{position: 'absolute', left: TX - 90, top: ZY - 150 - (1 - tIn) * 260, width: 230, opacity: Math.min(1, tIn * 2)}}>
        <div style={{width: 230, height: 150, background: T.ink, clipPath: 'polygon(14% 0, 86% 0, 100% 100%, 0 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center', ...F, fontWeight: 800, fontSize: 46, color: '#fff'}}>{p.top.label}</div>
      </div>
      <div style={{position: 'absolute', left: TX - 150, top: ZY + 26, width: 350, textAlign: 'center', opacity: g(f, tA + 12, 12), ...F, fontWeight: 800, fontSize: 40, color: T.ink, whiteSpace: 'nowrap'}}>{p.top.text}</div>
      {/* 두 깃발 사이 — 답 */}
      <div style={{position: 'absolute', left: dx, top: ZY + 112, width: (mx - dx) * gapO, height: 0, borderTop: `5px solid ${T.accent}`}} />
      <div style={{position: 'absolute', left: dx - 3, top: ZY + 100, width: 5, height: 26, background: T.accent, opacity: gapO}} />
      <div style={{position: 'absolute', left: mx - 2, top: ZY + 100, width: 5, height: 26, background: T.accent, opacity: g(f, gA + 10, 6)}} />
      <div style={{position: 'absolute', left: (dx + mx) / 2 - 400, top: ZY + 132 + (1 - gapO) * 16, width: 800, textAlign: 'center', opacity: gapO, ...F, fontWeight: 800, fontSize: 92, color: T.accent, letterSpacing: -2, whiteSpace: 'nowrap'}}>{p.gap.text}</div>
      <HandUnderline x={(dx + mx) / 2 - 170} y={ZY + 248} w={340} p={g(f, gA + 12, 18)} seed={3} />
    </div>
  );
};
