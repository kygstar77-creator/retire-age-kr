// 문턱 위 계단(StepCliff) — P-1 '5. 519만원 위의 계단'(2026-10-13 motion). TallyFrame 자식.
// 가로 = 공제 뒤 월 소득, 세로 = 한 달에 깎이는 돈. 문턱 바로 아래 0원 → 바로 위 15만원으로 '툭' 올라가는 계단을 보인다.
// 정직성: 곡선은 제63조의2 계산식(props.tiers)으로 그리고, 점·글자는 calc_out 그대로(props). 옛 법 곡선은 그리지 않는다(calc_out 5절 '확인 안 함').
// U5: 말 줄마다 판 일부가 바뀐다(beats[i] = 그 줄 시작 프레임). 왼쪽 빈 칸(문턱 아래 0원 구간 위)을 차례로 카드 자리로 쓴다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type StepCliffProps = {
  seed: string;
  xMin: number; xMax: number; yMax: number;            // 만원 단위
  a: number; gap: number; cap: number;                 // A값(만원)·문턱 차(200)·상한(만원)
  tiers: [number, number, number][];                   // [초과액 하한, 그때 감액, 기울기] — 초과액 = 소득 − A
  xticks: number[]; yticks: [number, string][];
  oldText: string; newText: string; plusText: string; zeroText: string;
  axisX: string; axisY: string; notWage: string; formula: string[];
  salary: [string, string]; ask: string; jumpText: string; stair: string;
  pts: {x: number; text: string; at: number}[];
  capText: [string, string]; period: [string, string, string]; slips: [string, string, string, string];
  zone: string;
  beats: number[];   // 줄 시작 프레임 15개(5장 말 줄 순서)
};

const out = Easing.out(Easing.cubic);
const ease = Easing.inOut(Easing.cubic);
const g = (f: number, a: number, d = 18, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const win = (f: number, a: number, b: number, d = 12) => Math.min(g(f, a, d), 1 - g(f, b, d));   // a에 들어와 b에 나감

export const StepCliff: React.FC<StepCliffProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const B = p.beats;
  // 판 y 236~852: 위 254~300은 [자막] 띠 → 그래프 꼭대기 360. 0선 740, 축 글자 아래 752~800.
  const X0 = 300 + Math.round(r('x') * 12), X1 = 1660, Z = 744, YT = 410;   // 위 '정확한 값' 띠가 두 줄이면 y 330까지 → 세로축 제목은 그 아래(레드팀 10/13)
  const X = (v: number) => X0 + (v - p.xMin) / (p.xMax - p.xMin) * (X1 - X0);
  const Y = (v: number) => Z - v / p.yMax * (Z - YT);
  const th = p.a + p.gap;                                   // 새 문턱(만원)
  const cut = (x: number) => {                               // 제63조의2(1·2구간 폐지 뒤) — 상한까지
    const e = x - p.a; if (e < p.gap) return 0;
    let v = 0; for (const [lo, base, k] of p.tiers) if (e >= lo) v = base + (e - lo) * k;
    return Math.min(v, p.cap);
  };
  const xT = X(th), xOld = X(p.a);

  // 진행
  const gAx = g(f, 4, 22);
  const gLine = g(f, B[1], 20);                              // '선' 등장(옛 자리)
  const gMove = g(f, B[2] + 4, 26, ease);                    // 문턱이 오른쪽으로
  const gZero = g(f, B[3], 20);                              // 0원 구간 칠
  const gStep = g(f, B[8], 16);                              // 계단 수직
  const gT3 = g(f, B[8] + 14, 30);                           // 3구간 선
  const gMore = g(f, B[10], 46, ease);                       // 4·5구간까지
  const gCap = g(f, B[11], 20);
  const lineX = xOld + (xT - xOld) * gMove;

  // 곡선 경로: 문턱부터 오른쪽 끝까지, 진행에 따라 잘라 그림
  const xEnd = th + (100 * gT3) + ((p.xMax - th - 100) * gMore);
  const path: string[] = [];
  if (gStep > 0) {
    path.push(`M${xT},${Z}`, `L${xT},${Y(cut(th + 0.001) * gStep)}`);
    if (gT3 > 0) for (let v = th + 1; v <= xEnd; v += 2) path.push(`L${X(v).toFixed(1)},${Y(cut(v)).toFixed(1)}`);
  }

  // 카메라: 줄마다 초점을 옮긴다(선형) + 줄 시작마다 숨(작게)
  const focusKeys: [number, number, number, number][] = [   // [프레임, x, y, 배율]
    [0, 960, 560, 1.0], [B[1], 760, 560, 1.03], [B[2], 820, 560, 1.03], [B[3], xT, 600, 1.06], [B[4], 960, 700, 1.04], [B[5], 640, 520, 1.05],
    [B[6], xT - 60, 520, 1.05], [B[7], xT, 700, 1.09], [B[8], xT, 640, 1.12], [B[9], xT, 640, 1.16], [B[10], 1200, 560, 1.02],
    [B[11], 1350, 460, 1.04], [B[12], 700, 480, 1.04], [B[13], xT, 640, 1.10], [B[14], xT, 640, 1.04], [B[14] + 200, xT, 620, 1.0]];
  const kt = focusKeys.map(q => q[0]); for (let i = 1; i < kt.length; i++) if (kt[i] <= kt[i - 1]) kt[i] = kt[i - 1] + 1;
  const fx = interpolate(f, kt, focusKeys.map(q => q[1]), {...CL, easing: ease});
  const fy = interpolate(f, kt, focusKeys.map(q => q[2]), {...CL, easing: ease});
  const sc = interpolate(f, kt, focusKeys.map(q => q[3]), {...CL, easing: ease});
  const pulse = Math.max(0, ...B.map(a => f < a ? 0 : f < a + 14 ? out((f - a) / 14) : Math.max(0, 1 - (f - a - 14) / 40)));
  const camX = (960 - fx) * 0.12, camY = (560 - fy) * 0.10;
  const pop = (a: number) => interpolate(f, [a, a + 12], [0.85, 1], {...CL, easing: Easing.out(Easing.back(2))});
  const card = {background: T.ink, color: '#fff', borderRadius: 14, padding: '14px 22px', fontWeight: 700, boxShadow: '0 10px 24px rgba(0,0,0,.16)', whiteSpace: 'nowrap' as const};
  const ck = 0.5 + r('c') * 1;   // 카드 기울기(편마다)

  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translate(${camX}px,${camY}px) scale(${sc * (1 + 0.025 * pulse)})`, transformOrigin: `${fx}px ${fy}px`}}>
        <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
          {/* 0원 구간(문턱 아래) */}
          <rect x={X0} y={Z - 60} width={(xT - X0) * gZero} height={60} fill="#e4ecfb" opacity={0.9} />
          {/* 상한 띠 */}
          <line x1={X0} x2={X0 + (X1 - X0) * gCap} y1={Y(p.cap)} y2={Y(p.cap)} stroke={T.ink3} strokeWidth={2} strokeDasharray="10 8" />
          {/* 축 */}
          <line x1={X0} x2={X0 + (X1 - X0) * gAx} y1={Z} y2={Z} stroke={T.ink} strokeWidth={4} />
          <line x1={X0} x2={X0} y1={Z} y2={Z - (Z - YT + 20) * gAx} stroke={T.ink} strokeWidth={3} />
          {p.yticks.map(([v, t], i) => (
            <g key={i} opacity={g(f, 10 + i * 4, 10)}>
              {v > 0 ? <line x1={X0} x2={X1} y1={Y(v)} y2={Y(v)} stroke={T.line} strokeWidth={2} /> : null}
            </g>
          ))}
          {/* 옛 문턱 자리(흐린 실선, 남김) */}
          {gLine > 0 ? <line x1={xOld} x2={xOld} y1={Z} y2={YT - 6} stroke={T.ink3} strokeWidth={3} opacity={(0.25 + 0.5 * gMove) * (1 - g(f, B[4], 14))} strokeDasharray="6 8" /> : null}
          {/* 움직이는 문턱 */}
          {gLine > 0 ? <line x1={lineX} x2={lineX} y1={Z} y2={Z - (Z - YT + 6) * gLine} stroke={T.fall} strokeWidth={5} /> : null}
          {/* 옮김 화살표(+200만원) */}
          {gMove > 0 ? (
            <g opacity={win(f, B[2] + 4, B[4])}>
              <line x1={xOld + 8} x2={lineX - 14} y1={YT + 30} y2={YT + 30} stroke={T.fall} strokeWidth={4} />
              <path d={`M${lineX - 30},${YT + 18} L${lineX - 12},${YT + 30} L${lineX - 30},${YT + 42}`} fill="none" stroke={T.fall} strokeWidth={4} />
            </g>
          ) : null}
          {/* 계단 + 곡선 */}
          {path.length ? <path d={path.join(' ')} fill="none" stroke={T.accent} strokeWidth={7} strokeLinejoin="round" strokeLinecap="round" /> : null}
          {gStep > 0 ? <circle cx={xT} cy={Z} r={9} fill="#fff" stroke={T.fall} strokeWidth={4} /> : null}
          {gStep > 0.9 ? <circle cx={xT} cy={Y(cut(th + 0.001))} r={11} fill={T.accent} /> : null}
          {/* 점: 600·700·800 */}
          {p.pts.map((q, i) => f >= q.at ? <circle key={i} cx={X(q.x)} cy={Y(cut(q.x))} r={10 * pop(q.at)} fill={T.ink} /> : null)}
          {/* 계단 자리 띠(끝 줄) */}
          <rect x={xT - 34} y={YT - 4} width={68} height={Z - YT + 4} fill={T.accent} opacity={0.10 * g(f, B[14], 16) * (0.6 + 0.4 * Math.sin((f - B[14]) / 9))} rx={10} />
          {/* 조문대로 계산하면? — 문턱 자리를 손그림 동그라미로 */}
          {f >= B[7] ? <HandCircle cx={xT} cy={Z - 40} rx={70} ry={64} p={g(f, B[7], 20) * (1 - g(f, B[8] + 30, 14))} /> : null}
        </svg>

        {/* 눈금 글자 — SVG <text>는 카메라 변형 중 렌더 프레임마다 자리가 어긋나 HTML로(10/13 실측) */}
        {p.yticks.map(([v, t], i) => (
          <div key={'y' + i} style={{...F, position: 'absolute', left: X0 - 134, width: 120, textAlign: 'right', top: Y(v) - 16, fontWeight: 700, fontSize: 24, color: T.ink2, opacity: g(f, 10 + i * 4, 10)}}>{t}</div>
        ))}
        {p.xticks.map((v, i) => (
          <div key={'x' + i} style={{...F, position: 'absolute', left: X(v) - 60, width: 120, textAlign: 'center', top: Z + 12, fontWeight: 700, fontSize: 24, color: T.ink3, opacity: g(f, 12 + i * 3, 10)}}>{v}만</div>
        ))}
        {/* 축 이름 */}
        <div style={{...F, position: 'absolute', left: X1 - 420, width: 420, textAlign: 'right', top: Z + 50, opacity: g(f, 14, 10), whiteSpace: 'nowrap'}}>
          <span style={{fontWeight: 700, fontSize: 28, color: T.ink, padding: '2px 10px', borderRadius: 8,
            background: `rgba(255,227,209,${win(f, B[4], B[6], 10)})`, outline: win(f, B[4], B[6], 10) > 0.05 ? `3px solid ${T.accent}` : 'none'}}>{p.axisX} →</span>
        </div>
        <div style={{...F, position: 'absolute', left: X0 + 14, top: YT - 42, opacity: g(f, 16, 10), whiteSpace: 'nowrap', fontWeight: 700, fontSize: 26, color: T.ink2}}>↑ {p.axisY}</div>

        {/* 옛 문턱 이름 */}
        <div style={{...F, position: 'absolute', left: xOld + 12, top: YT + 54, opacity: g(f, B[2], 12) * (1 - g(f, B[4], 10)), whiteSpace: 'nowrap', fontWeight: 700, fontSize: 26, color: T.ink3}}>{p.oldText}</div>
        {/* L1 '어떤 선?' */}
        <div style={{...F, position: 'absolute', left: lineX + 14, top: YT + 90, opacity: win(f, B[1] + 10, B[2] + 6), whiteSpace: 'nowrap', transform: `scale(${pop(B[1] + 10)})`, transformOrigin: 'left center',
          fontWeight: 700, fontSize: 44, color: T.fall}}>← 어떤 선?</div>
        {/* +200만원 */}
        <div style={{...F, position: 'absolute', left: (xOld + xT) / 2 - 120, width: 240, textAlign: 'center', top: YT - 14, opacity: win(f, B[2] + 18, B[4]), whiteSpace: 'nowrap',
          transform: `scale(${pop(B[2] + 18)})`}}>
          <span style={{fontWeight: 700, fontSize: 40, color: T.fall}}>{p.plusText}</span>
        </div>
        {/* 새 문턱 이름(문턱 오른쪽 위) */}
        <div style={{...F, position: 'absolute', left: xT + 16, top: YT + 6, opacity: g(f, B[3], 12), whiteSpace: 'nowrap', transform: `translateX(${(1 - g(f, B[3], 12)) * -14}px)`}}>
          <div style={{fontWeight: 700, fontSize: 50, color: T.fall, letterSpacing: -1, lineHeight: 1.05}}>{p.newText}</div>
          <div style={{fontWeight: 700, fontSize: 26, color: T.ink2}}>이 선부터 깎임</div>
        </div>
        {/* 0원 구간 글자 */}
        <div style={{...F, position: 'absolute', left: X0 + 20, width: xT - X0 - 40, textAlign: 'center', top: Z - 50, opacity: gZero, whiteSpace: 'nowrap', fontWeight: 700, fontSize: 30, color: T.fall}}>{p.zeroText}</div>

        {/* 왼쪽 카드 자리(문턱 아래 위쪽 빈 곳): 줄마다 바뀜 */}
        {/* L4 '월급 그대로 아님' */}
        <div style={{...F, position: 'absolute', left: X0 + 40, top: 420, opacity: win(f, B[4] + 4, B[5]), transform: `scale(${pop(B[4] + 4)}) rotate(${-ck}deg)`, transformOrigin: 'left center',
          ...card, background: '#fff', color: T.ink, border: `3px solid ${T.ink}`, fontSize: 36}}>
          {p.notWage}
        </div>
        {/* L5 식 */}
        <div style={{...F, position: 'absolute', left: X0 + 30, top: 400, opacity: win(f, B[5] + 2, B[6] + 4), transform: `translateY(${(1 - g(f, B[5] + 2, 14)) * 16}px)`, transformOrigin: 'left top', ...card, fontSize: 32, lineHeight: 1.4}}>
          {p.formula.map((t, i) => <div key={i} style={{color: i === p.formula.length - 1 ? T.daccent : '#fff', opacity: g(f, B[5] + 6 + i * 10, 10)}}>{t}</div>)}
        </div>
        {/* L6 세전 연봉 */}
        <div style={{...F, position: 'absolute', left: X0 + 30, top: 420, opacity: win(f, B[6] + 8, B[7] + 6), transform: `scale(${pop(B[6] + 4)})`, transformOrigin: 'left center',
          ...card, background: '#fff', color: T.ink, border: `3px solid ${T.fall}`, fontSize: 28, lineHeight: 1.35}}>
          <div style={{color: T.ink2}}>근로소득만이면 세전(비과세 제외)</div>
          <div style={{fontSize: 44, color: T.fall, letterSpacing: -1}}>{p.salary[0]}</div>
          <div style={{color: T.ink2}}>{p.salary[1]}</div>
        </div>
        {/* L6 연봉 카드 → 문턱 잇는 화살표 */}
        {f >= B[6] + 10 ? (
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: win(f, B[6] + 10, B[7] + 6)}}>
            <path d={`M${X0 + 440},${500} Q${xT - 60},${500} ${xT - 8},${Z - 70}`} fill="none" stroke={T.fall} strokeWidth={4} strokeDasharray={600} strokeDashoffset={600 * (1 - g(f, B[6] + 10, 20))} />
          </svg>
        ) : null}
        {/* L7 물음 */}
        <div style={{...F, position: 'absolute', left: xT - 340, width: 300, textAlign: 'right', top: Z - 150, opacity: win(f, B[7] + 8, B[8] + 30), whiteSpace: 'nowrap', fontWeight: 700, fontSize: 34, color: T.ink}}>{p.ask}</div>
        {/* L8 15만원 */}
        <div style={{...F, position: 'absolute', left: xT - 250, width: 230, textAlign: 'right', top: Y(15) - 40, opacity: g(f, B[8] + 10, 10) * (1 - win(f, B[13] + 2, B[14] + 60)), whiteSpace: 'nowrap',
          transform: `scale(${pop(B[8] + 10) * (1 + 0.12 * interpolate(f, [B[13], B[13] + 10, B[13] + 26], [0, 1, 0], CL))})`, transformOrigin: 'right center'}}>
          <span style={{fontWeight: 700, fontSize: 56, color: T.accent, letterSpacing: -1}}>{p.jumpText}</span>
        </div>
        {/* L9 계단 도장 */}
        <div style={{...F, position: 'absolute', left: xT + 30, top: Y(15) - 20, opacity: g(f, B[9], 10) * (1 - 0.6 * g(f, B[10], 14)) * (1 - win(f, B[13] + 2, B[14] + 60)), transform: `scale(${pop(B[9])}) rotate(${-3 + ck}deg)`, transformOrigin: 'left center',
          ...card, background: T.accent, fontSize: 40, padding: '8px 22px'}}>{p.stair}</div>

        {/* 점 글자 */}
        {p.pts.map((q, i) => (
          <div key={i} style={{...F, position: 'absolute', ...(i === 1 ? {left: X(q.x) + 18, top: Y(cut(q.x)) + 4} : i === 2 ? {left: X(q.x) - 160, top: Y(cut(q.x)) - 50} : {left: X(q.x) + 14, top: Y(cut(q.x)) + 6}), opacity: g(f, q.at + 6, 10), whiteSpace: 'nowrap'}}>
            <span style={{fontWeight: 700, fontSize: 34, color: T.ink}}>{q.text}</span>
          </div>
        ))}
        {/* L11 상한 */}
        <div style={{...F, position: 'absolute', left: X1 - 560, width: 560, textAlign: 'right', top: Y(p.cap) - 84, opacity: gCap, whiteSpace: 'nowrap', transform: `translateY(${(1 - gCap) * 10}px)`}}>
          <div style={{fontWeight: 700, fontSize: 30, color: T.ink2}}>{p.capText[0]}</div>
        </div>

        {/* L12 기간 띠 */}
        <div style={{...F, position: 'absolute', left: X0 + 30, top: 440, width: 500, opacity: win(f, B[12] + 2, B[13]), transform: `translateX(${(1 - g(f, B[12] + 2, 16)) * -30}px)`}}>
          <div style={{...card, padding: '16px 22px'}}>
            <div style={{fontSize: 24, whiteSpace: 'normal'}}>{p.period[2]}</div>
            <div style={{position: 'relative', height: 40, marginTop: 12}}>
              <div style={{position: 'absolute', left: 0, right: 0, top: 16, height: 8, background: '#3a3c44', borderRadius: 4}} />
              <div style={{position: 'absolute', left: 0, width: `${100 * g(f, B[12] + 12, 40, Easing.linear)}%`, top: 12, height: 16, background: T.daccent, borderRadius: 8}} />
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 28, marginTop: 4}}><span>{p.period[0]}</span><span>{p.period[1]}</span></div>
          </div>
        </div>
        {/* L13 바로 아래 / 바로 위 두 장 */}
        {[0, 1].map(i => (
          <div key={i} style={{...F, position: 'absolute', left: i === 0 ? X0 + 60 : xT + 40, top: i === 0 ? 545 : 640, width: 360,
            opacity: win(f, B[13] + 6 + i * 22, B[14] + 60), transform: `translateY(${(1 - g(f, B[13] + 6 + i * 22, 14)) * 18}px) rotate(${(i ? 1 : -1) * ck}deg)`,
            background: '#fff', border: `3px solid ${i ? T.accent : T.fall}`, borderRadius: 14, padding: '12px 18px', boxShadow: '0 10px 24px rgba(0,0,0,.12)', whiteSpace: 'nowrap'}}>
            <div style={{fontWeight: 700, fontSize: 26, color: T.ink2}}>{p.slips[i * 2]}</div>
            <div style={{fontWeight: 700, fontSize: 44, color: i ? T.accent : T.fall, letterSpacing: -1}}>{p.slips[i * 2 + 1]}</div>
          </div>
        ))}
        {/* L14 계단 자리 */}
        <div style={{...F, position: 'absolute', left: xT + 10, top: YT - 30, opacity: g(f, B[14] + 4, 12), whiteSpace: 'nowrap'}}>
          <span style={{fontWeight: 700, fontSize: 30, color: '#fff', background: T.accent, padding: '4px 16px', borderRadius: 8}}>{p.zone}</span>
        </div>
      </div>
    </div>
  );
};
