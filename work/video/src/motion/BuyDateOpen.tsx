// 롱폼 첫 장면 '산 날 영수증'(BuyDateOpen) — G-1 금값 1천만원 영수증(2026-10-07 motion). TallyFrame 자식.
// 0. 판 전체가 어두운 판(hook): 대본 첫 문장 조각 + 큰 숫자 → 산 날 점 하나로 빨려 들며 걷힘(점 = 그 숫자가 나온 자리)
// 1. 값 선이 그려지고, 산 날 점에서 '1천만원' 덩이가 떨어져 오른쪽 막대 자리로 가며 오늘 값만큼 줄어든다(줄어든 몫은 빗금 유령)
// 2. 두 번째 산 날도 같은 규칙 → 3. 선은 흐려지고 막대 둘에 '산 날만 달랐다' 괄호, 카메라가 막대 쪽으로 다가감
// 정직성: 막대는 0 기준선 공유·높이 = 값/낸 돈 비례(낸 돈 1천만원 = 점선 테두리), 숫자는 굴리지 않는다(중간 가짜 숫자 0). 숫자 글자는 전부 props(g1open.py가 calc_out 대조).
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL} from '../parts/fm';
import {lineXY} from './TallyLineChart';

export type BuyDate = {i: number; v: number; date: string; value: number; text: string; pct: string; at: number};
export type BuyDateOpenProps = {
  seed: string; hookTop: string; hookBig: string; hookOut: number;
  pts: number[]; min: number; max: number; ticks: [number, string][]; xlabels: [number, string][]; draw: number;
  now: [number, string]; paid: number; paidText: string; buys: BuyDate[]; same: number; sameText: string;
};

const ease = Easing.inOut(Easing.cubic);
const out = Easing.out(Easing.cubic);
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);

export const BuyDateOpen: React.FC<BuyDateOpenProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  // 차트 자리(왼쪽) · 막대 자리(오른쪽) — seed로 막대 폭·간격만 조금 바뀐다
  const C = {x: 250, y: 320, w: 840, h: 420};
  const barW = Math.round(150 + r('w') * 30), gap = Math.round(70 + r('g') * 30);
  // 판(카드)은 y 238~849 — 막대 높이 330이면 값 글자(낸 돈 점선 위)까지 판 안에 든다(10/9: 430이면 956만원이 판 위로 넘침)
  const baseY = 760, maxH = 330, bx0 = 1230;
  const bx = (k: number) => bx0 + k * (barW + gap);
  const n = p.pts.length;
  const xy = lineXY(C.x, C.y, C.w, C.h, p.min, p.max, n);
  const draw = interpolate(f, [p.draw, p.draw + 30], [0, 1], {...CL, easing: ease});
  const dim = interpolate(f, [p.same, p.same + 16], [1, 0.32], CL);
  const cam = interpolate(f, [p.same, p.same + 120], [1, 1.07], {...CL, easing: ease});
  const path = p.pts.map((v, i) => { const [x, y] = xy(i, v); return `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`; }).join(' ');
  const [, nowY] = xy(0, p.now[0]);
  const h0 = maxH; // 낸 돈 1천만원 높이
  const first = p.buys[0];
  const [dx0, dy0] = xy(first.i, p.pts[first.i]);

  // 0. hook — 어두운 판이 첫 산 날 점으로 빨려 든다
  const hk = interpolate(f, [p.hookOut, p.hookOut + 18], [0, 1], {...CL, easing: Easing.in(Easing.cubic)});
  const hookOn = hk < 1;

  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${cam})`, transformOrigin: `${bx(1)}px ${baseY - 200}px`}}>
        {/* 값 선 */}
        <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: dim}}>
          {p.ticks.map(([v, t], i) => { const [, ty] = xy(0, v); return (
            <g key={i} opacity={fade(f, p.draw + i * 3)}><line x1={C.x} x2={C.x + C.w} y1={ty} y2={ty} stroke={T.line} strokeWidth={2} />
              <text x={C.x - 14} y={ty + 8} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3}>{t}</text></g>); })}
          {p.xlabels.map(([i, t], k) => { const [lx] = xy(i, p.min); return <text key={k} x={lx} y={C.y + C.h + 34} textAnchor="middle" fontFamily="PD" fontWeight={500} fontSize={22} fill={T.ink3} opacity={fade(f, p.draw + 10)}>{t}</text>; })}
          {/* 점선은 '낸 돈' 한 뜻만(레드팀 10/9) — 오늘 값 가로선·떨어진 세로선은 실선 */}
          <line x1={C.x} x2={C.x + C.w} y1={nowY} y2={nowY} stroke={T.ink} strokeWidth={2} opacity={fade(f, p.draw + 30)} />
          <text x={C.x + C.w} y={nowY + 32} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink} opacity={fade(f, p.draw + 30)}>{p.now[1]}</text>
          <path d={path} fill="none" stroke={T.ink2} strokeWidth={5} strokeLinejoin="round" strokeLinecap="round" style={{clipPath: `inset(0 ${(1 - draw) * 100}% 0 0)`}} />
          {/* 산 날 → 오늘 값 가로선까지 내려온 선(세로축이 16만부터라 길이는 비율이 아니다 — 비율은 오른쪽 막대만 맡는다) */}
          {p.buys.map((b, k) => {
            const [x, y] = xy(b.i, p.pts[b.i]);
            const on = k === 0 ? p.draw + 34 : b.at;
            const s = interpolate(f, [on, on + 12], [0, 1], {...CL, easing: Easing.out(Easing.back(2))});
            const dl = interpolate(f, [on + 8, on + 26], [0, 1], {...CL, easing: out});
            return (
              <g key={k} opacity={f >= on ? 1 : 0}>
                <line x1={x} x2={x} y1={y} y2={y + (nowY - y) * dl} stroke={T.fall} strokeWidth={3} />
                <circle cx={x} cy={y} r={14 * s} fill={T.accent} stroke="#fff" strokeWidth={4} />
                <text x={x + (k === 0 ? 0 : 22)} y={k === 0 ? y - 26 : nowY + 34} textAnchor={k === 0 ? 'middle' : 'start'} fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink} stroke="#fff" strokeWidth={8} paintOrder="stroke" opacity={fade(f, on + 6)}>{b.date}</text>
              </g>
            );
          })}
        </svg>

        {/* 오른쪽 막대 — 낸 돈 1천만원(점선 테두리) 안에서 오늘 값만큼 */}
        {p.buys.map((b, k) => {
          const on = k === 0 ? p.draw + 40 : b.at + 10;
          const [px, py] = xy(b.i, p.pts[b.i]);
          const mv = interpolate(f, [on, on + 26], [0, 1], {...CL, easing: ease});   // 점 → 막대 자리
          const sh = interpolate(f, [on + 26, on + 50], [0, 1], {...CL, easing: out});  // 1천만원 → 오늘 값
          const hv = h0 * (1 - sh) + h0 * (b.value / p.paid) * sh;
          const x = interpolate(mv, [0, 1], [px - barW / 2, bx(k)]);
          const top = interpolate(mv, [0, 1], [py - h0, baseY - h0]);   // 'center bottom' 기준이라 덩이 밑변이 점에서 출발(10/9 레드팀: py−30이면 330px 아래에서 떠 판 밖으로 나감)
          const sc = interpolate(mv, [0, 1], [0.14, 1]);
          if (f < on) return null;
          return (
            <React.Fragment key={k}>
              {/* 낸 돈 유령 */}
              <div style={{position: 'absolute', left: bx(k), top: baseY - h0, width: barW, height: h0, border: `3px dashed ${T.ink3}`, borderRadius: 8, boxSizing: 'border-box', opacity: fade(f, on + 20)}} />
              {/* 줄어든 몫 빗금 */}
              <div style={{position: 'absolute', left: bx(k), top: baseY - h0, width: barW, height: h0 - hv, opacity: sh * 0.9, borderRadius: '8px 8px 0 0',
                background: `repeating-linear-gradient(135deg, ${T.fall}33 0 8px, transparent 8px 18px)`}} />
              {/* 막대(덩이) */}
              <div style={{position: 'absolute', left: x, top: mv < 1 ? top : baseY - hv, width: barW, height: mv < 1 ? h0 : hv,
                transform: `scale(${sc})`, transformOrigin: 'center bottom', borderRadius: 8, opacity: mv < 1 ? 0.85 : 1,   // 날아가는 동안 선·이름표 비침(레드팀 10/9)
                background: k === 0 ? T.accent : T.ink2, boxShadow: '0 10px 24px rgba(0,0,0,.14), 0 2px 4px rgba(0,0,0,.12)'}} />
              {/* 값 글자: 다 줄어든 뒤 — 모든 막대 같은 자리(낸 돈 점선 위), 빗금과 겹치지 않게 */}
              <div style={{...F, position: 'absolute', left: bx(k) - 40, width: barW + 80, textAlign: 'center', top: baseY - h0 - 104, opacity: fade(f, on + 50, 8)}}>
                <div style={{fontWeight: 700, fontSize: 58, color: k === 0 ? T.accent : T.ink, letterSpacing: -1, whiteSpace: 'nowrap'}}>{b.text}</div>
                <div style={{fontWeight: 700, fontSize: 30, color: T.fall, whiteSpace: 'nowrap'}}>{b.pct}</div>
              </div>
              <div style={{...F, position: 'absolute', left: bx(k) - 40, width: barW + 80, textAlign: 'center', top: baseY + 14, fontWeight: 700, fontSize: 26, color: T.ink2, opacity: fade(f, on + 20), whiteSpace: 'nowrap'}}>{b.date} 산 날</div>
            </React.Fragment>
          );
        })}
        <div style={{position: 'absolute', left: bx(0) - 20, width: 2 * barW + gap + 40, top: baseY, height: 4, background: T.ink, opacity: fade(f, p.draw + 40)}} />
        <div style={{...F, position: 'absolute', left: bx(p.buys.length - 1) + barW + 14, top: baseY - h0 - 4, fontWeight: 700, fontSize: 22, lineHeight: 1.3, color: T.ink3, opacity: fade(f, p.draw + 60)}}>점선 =<br />낸 돈<br />{p.paidText}</div>

        {/* 3. 산 날만 달랐다 — 두 막대 아래 괄호 */}
        {f >= p.same ? (() => {
          const g = interpolate(f, [p.same + 12, p.same + 28], [0, 1], {...CL, easing: out});   // 선이 다 흐려진 뒤 결론 글자
          const L = bx(0), R = bx(1) + barW, y = baseY + 46;   // 판 아래 끝(849) 안 — 글자는 흐려진 선그래프 자리로(10/9: 괄호 밑 글자가 판 밖으로 넘침)
          return (
            <>
              <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
                <path d={`M${L} ${y} L${L} ${y + 18} L${R} ${y + 18} L${R} ${y}`} fill="none" stroke={T.accent} strokeWidth={5} strokeLinecap="round"
                  strokeDasharray={2000} strokeDashoffset={2000 * (1 - g)} />
              </svg>
              <div style={{...F, position: 'absolute', left: C.x, width: C.w, textAlign: 'center', top: C.y + C.h / 2 - 40, fontWeight: 700, fontSize: 64, letterSpacing: -1, color: T.accent, opacity: g, transform: `translateY(${(1 - g) * 20}px)`, whiteSpace: 'nowrap', textShadow: '0 0 18px #fff, 0 0 8px #fff'}}>{p.sameText} →</div>
            </>
          );
        })() : null}
      </div>

      {/* 0. hook 판 */}
      {hookOn ? (
        <div style={{position: 'absolute', inset: 0, background: T.dbg, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          transform: `scale(${interpolate(hk, [0, 1], [1, 0.02])})`, transformOrigin: `${dx0}px ${dy0}px`, borderRadius: `${hk * 50}%`, opacity: interpolate(hk, [0.8, 1], [1, 0], CL)}}>
          <div style={{...F, fontWeight: 700, fontSize: 52, color: T.dink, opacity: fade(f, 0, 8), whiteSpace: 'nowrap'}}>{p.hookTop}</div>
          <div style={{...F, fontWeight: 700, fontSize: 210, color: T.daccent, letterSpacing: -4, lineHeight: 1.1, marginTop: 20, whiteSpace: 'nowrap',
            transform: `translateY(${(1 - fade(f, 4, 12)) * 30}px) scale(${interpolate(f, [4, 16], [0.9, 1], {...CL, easing: out})})`, opacity: fade(f, 4, 8)}}>{p.hookBig}</div>
        </div>
      ) : null}
    </div>
  );
};
