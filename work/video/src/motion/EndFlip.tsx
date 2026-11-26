// 끝날 바꾸면 답이 뒤집힘(EndFlip) — CC-1 7장 '끝날 6개'(2026-11-26 motion). TallyFrame 자식.
// 가운데 세로 칸에 끝날(위→아래 시간순), 왼쪽은 A(커버드콜) 막대가 왼쪽으로, 오른쪽은 B(일반형) 막대가 오른쪽으로 자람.
// 줄은 '말한 순서'대로 열린다(order — 시간순이 아님). 말하지 않은 줄(rest)은 마지막 말 줄 뒤에 같이 열리고, 끝에 '4 · 2' 찍기.
// 주황은 그 순간의 답 하나: 지금 열린 줄의 앞선 쪽 체크 → 끝엔 세기 글자만. 지난 줄 체크는 먹색.
// 들어오기: 날짜는 왼쪽부터 써지듯(줄마다 5프레임 늦게), 값은 '?'에서 막대가 자라며 열림, 세기는 찍기.
// U5: 늘 천천히 다가감(1.00→1.03) + 지금 줄 쪽으로 조금 옮겨 감. bgcheck ⑥: 막대 두께 ≤18px, 눈금 칸 없음.
// 숫자는 전부 props(편 스크립트가 calc 출력과 assert). 반복 방지: seed로 옮겨 가는 방향·막대 두께·가운데 칸 폭.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL} from '../parts/fm';
import {HandCheck, HandUnderline} from '../parts/human';

export type EndRow = {date: string; a: number; b: number};
export type EndFlipProps = {
  seed: string;
  names: [string, string];          // [왼쪽 A, 오른쪽 B]
  rows: EndRow[];                   // 시간순(위→아래)
  order: number[];                  // 말한 순서 — order[k]는 박자 k에 열림
  restAt: number;                   // 말하지 않은 줄이 열리는 박자(소수 = 그 줄 안 비율)
  tallyAt: number;                  // '4 · 2' 찍는 박자
  tallyText: [string, string];      // ['커버드콜 4', '일반형 2'] — 편 스크립트가 rows에서 셈
  unit: string;                     // '%'
  max: number;                      // 막대 끝 값(가장 큰 값보다 조금 크게)
  end: number;                      // 장면 길이(프레임) — 마지막 박자 길이 셈
  beats: number[];
};

const io = Easing.inOut(Easing.cubic), out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const fmt = (v: number, u: string) => `${v.toFixed(1)}${u}`;

export const EndFlip: React.FC<EndFlipProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats;
  const at = (x: number) => { const i = Math.floor(x); const a = B[i] ?? p.end; const n = (B[i + 1] ?? p.end) - a; return a + n * (x - i); };
  const N = p.rows.length;
  const CW = 300 + Math.round(r('cw') * 40);                 // 가운데 날짜 칸 폭
  const XL = 960 - CW / 2, XR = 960 + CW / 2;               // 왼쪽 막대 시작·오른쪽 막대 시작
  const PX = 560 / p.max;                                    // 1단위 px
  const YT = 290, RH = 70, BH = 16 + Math.round(r('bh') * 2);
  const Yc = (i: number) => YT + RH * (i + 0.5);
  const openAt: number[] = p.rows.map((_, i) => { const k = p.order.indexOf(i); return at(k >= 0 ? k : p.restAt) + (k >= 0 ? 8 : (i % 3) * 6); });
  const cur = (() => { let c = -1, best = -1e9; p.rows.forEach((_, i) => { if (p.order.includes(i) && openAt[i] <= f && openAt[i] > best) { best = openAt[i]; c = i; } }); return c; })();
  const restA = at(p.restAt), tA = at(p.tallyAt);
  const tallyO = g(f, tA, 10, Easing.out(Easing.back(1.6)));
  const lateRest = f >= restA;
  // 카메라: 늘 1.00→1.03 + 지금 줄 쪽 위아래로 조금
  const z = interpolate(f, [0, p.end], [1, 1.03], CL);
  const dir = r('dir') > 0.5 ? 1 : -1;
  // 지금 줄 쪽으로 화면이 조금 옮겨 감(줄마다 ±20px) — 막대 한 줄만으론 U5 '새 화면'(4%)이 안 됨(11/26 첫 미리보기 7.0초)
  const tgt = (k: number) => k < 0 ? 0 : Math.max(-2, -(Yc(p.order[k]) - 540) * 0.16 + 12);   // 위로는 거의 안 감 — 11/26 셋째 미리보기: 위로 21px 가면 첫 줄이 머리글에 닿음
  let ty = 0; p.order.forEach((_, k) => { ty += (tgt(k) - tgt(k - 1)) * g(f, openAt[p.order[k]] - 6, 26, io); });
  ty += (0 - tgt(p.order.length - 1)) * g(f, restA, 30, io);
  const oy = 540;
  const ox = 960 + dir * 120 * interpolate(f, [0, p.end], [0, 1], CL);
  const lab = (s: React.CSSProperties) => ({position: 'absolute' as const, ...F, whiteSpace: 'nowrap' as const, ...s});
  const axis = g(f, 4, 26, io);
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translate(${ox * (1 - z)}px, ${oy * (1 - z)}px) scale(${z})`, transformOrigin: '0 0'}}>
      {/* 머리: 두 이름 — 가운데 선 기준(왼쪽 이름은 오른쪽 끝, 오른쪽 이름은 왼쪽 끝) */}
      <div style={lab({right: 1920 - XL + 10, top: YT - 66, fontWeight: 700, fontSize: 42, color: T.ink2, opacity: g(f, 2, 12)})}>{p.names[0]}</div>
      <div style={lab({left: XR + 10, top: YT - 66, fontWeight: 700, fontSize: 42, color: T.ink2, opacity: g(f, 6, 12)})}>{p.names[1]}</div>
      {/* 줄·막대·세기만 지금 줄 쪽으로 옮겨 감 — 이름 둘은 제자리(11/26 둘째 미리보기: 옮겨 가면 이름이 제목에 닿음) */}
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transform: `translateY(${ty}px)`}}>
      <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}}>
        <line x1={XL} x2={XL} y1={YT - 8} y2={YT - 8 + (RH * N + 16) * axis} stroke={T.ink2} strokeWidth={4} strokeLinecap="round" />
        <line x1={XR} x2={XR} y1={YT - 8} y2={YT - 8 + (RH * N + 16) * axis} stroke={T.ink2} strokeWidth={4} strokeLinecap="round" />
        {p.rows.map((q, i) => {
          const s = g(f, openAt[i], 20, io);
          const aw = q.a >= q.b, done = s > 0;
          const fade = 1;   // 11/26 심사: 지난 줄을 옅게 하면 앞선 막대 색이 줄마다 달라 보임 → 하나로
          return done ? <g key={i} opacity={fade}>
            <rect x={XL - Math.max(6, q.a * PX) * s} y={Yc(i) - BH / 2} width={Math.max(6, q.a * PX) * s} height={BH} rx={3} fill={aw ? T.ink : T.ink3} opacity={aw ? 1 : 0.6} />
            <rect x={XR} y={Yc(i) - BH / 2} width={Math.max(6, q.b * PX) * s} height={BH} rx={3} fill={aw ? T.ink3 : T.ink} opacity={aw ? 0.6 : 1} />
          </g> : null;
        })}
      </svg>
      {p.rows.map((q, i) => {
        const w = g(f, 10 + i * 5, 18, io);                    // 날짜: 왼쪽부터 써지듯
        const s = g(f, openAt[i], 20, io), vo = g(f, openAt[i] + 14, 10);
        const aw = q.a >= q.b;
        const isCur = i === cur && !lateRest;
        const ax = XL - Math.max(6, q.a * PX) - 18, bx = XR + Math.max(6, q.b * PX) + 18;
        const ck = g(f, openAt[i] + 22, 14, Easing.inOut(Easing.quad));
        return <React.Fragment key={i}>
          <div style={lab({left: XL, top: Yc(i) - 28, width: CW, textAlign: 'center', fontWeight: 700, fontSize: 40, color: isCur ? T.ink : T.ink2, clipPath: `inset(0 ${(1 - w) * 100}% 0 0)`})}>{q.date}</div>
          {/* 열리기 전 '?' */}
          <div style={lab({right: 1920 - XL + 24, top: Yc(i) - 30, fontWeight: 800, fontSize: 44, color: T.ink3, opacity: w * (1 - s)})}>?</div>
          <div style={lab({left: XR + 24, top: Yc(i) - 30, fontWeight: 800, fontSize: 44, color: T.ink3, opacity: w * (1 - s)})}>?</div>
          {/* 값 — 막대 끝 바깥 */}
          <div style={lab({right: 1920 - ax, top: Yc(i) - 28, fontWeight: aw ? 800 : 600, fontSize: 40, color: aw ? T.ink : T.ink2, opacity: vo})}>{fmt(q.a, p.unit)}</div>
          <div style={lab({left: bx, top: Yc(i) - 28, fontWeight: aw ? 600 : 800, fontSize: 40, color: aw ? T.ink2 : T.ink, opacity: vo})}>{fmt(q.b, p.unit)}</div>
          {/* 앞선 쪽 체크 — 지금 줄만 주황 */}
          <HandCheck x={aw ? ax - 175 : bx + 135} y={Yc(i) - 22} s={36} p={ck} color={isCur ? T.accent : T.ink2} />
          {isCur ? <HandUnderline x={XL + 30} y={Yc(i) + 26} w={CW - 60} p={g(f, openAt[i] + 4, 16, io)} color={T.ink} seed={i + 2} stroke={4} /> : null}
        </React.Fragment>;
      })}
      {/* 끝: 세기 찍기 — 이 순간 주황은 이것 하나 */}
      <div style={lab({left: 0, width: 1920, top: YT + RH * N + 18, textAlign: 'center', fontWeight: 800, fontSize: 66, opacity: tallyO, transform: `scale(${1.25 - 0.25 * g(f, tA, 10)})`, transformOrigin: 'center center'})}>
        <span style={{color: T.accent}}>{p.tallyText[0]}</span><span style={{color: T.ink3}}>{'  ·  '}</span><span style={{color: T.ink2}}>{p.tallyText[1]}</span>
      </div>
      </div>
    </div>
  );
};
