// 세 조각 폭포 막대(WaterfallPieces) — G-1 '3. 세 조각'(2026-10-09 motion). TallyFrame 자식.
// 0 기준선(산 날 값)에서 달러 금값 → 환율 → KRX 웃돈 막대가 앞 막대 끝에 이어 붙어 오르내리고, 마지막에 0부터 '= 내 금' 합계 막대가 같은 끝까지.
// 정직성: 막대 길이 = 곱을 로그로 나눈 %p(합이 정확히 전체 — 끝 막대와 셋째 막대 끝이 같은 높이), 글자 = calc_out 곱 비율 그대로(props). 숫자는 굴리지 않는다.
// 움직임: 말 따라 다음 막대 칸으로 카메라가 천천히 옮겨 가고(정지 방지), 결론 때 첫 막대는 흐려지고 둘째·셋째 위에 괄호.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, HandCircle} from '../parts/fm';

export type WfStep = {name: string; sub: string; pp: number; text: string; at: number};
export type WaterfallPiecesProps = {
  seed: string; min: number; max: number; zeroText: string;
  steps: WfStep[]; total: WfStep & {won: string}; prem: [string, number][]; hit: number; note: [string, number]; intro: number;
};

const ease = Easing.inOut(Easing.cubic);
const out = Easing.out(Easing.cubic);
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);

export const WaterfallPieces: React.FC<WaterfallPiecesProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  // 판(BOARD) y 236~852 안: 판 위 끝 254~300은 [자막] 띠 자리(1차: +6.65%가 띠에 가림) → 위 +max = 350, 아래 min = 742, 칸 이름은 그 아래
  const top = 400, bot = 742, x0 = 330, colW = Math.round(330 + r('c') * 20), barW = Math.round(150 + r('w') * 24);
  const k = (bot - top) / (p.max - p.min);
  const Y = (v: number) => top + (p.max - v) * k;
  const zy = Y(0);
  const cx = (i: number) => x0 + i * colW + colW / 2;
  const all = [...p.steps, p.total];
  // 누적 끝값
  const ends: number[] = []; p.steps.reduce((a, s) => { ends.push(a + s.pp); return a + s.pp; }, 0);
  const starts = [0, ...ends.slice(0, -1)];
  const grow = (at: number) => interpolate(f, [at, at + 22], [0, 1], {...CL, easing: out});

  // 카메라: 말이 가리키는 칸으로 천천히 이동 — 키 프레임 사이를 선형으로 이어 늘 조금씩 움직인다
  const keys = [[p.intro, 1.5], ...all.map((s, i) => [s.at, i] as [number, number]), [p.note[1], 1.5], [p.note[1] + 400, 1.5]] as [number, number][];
  const kt = keys.map(q => q[0]), kc = keys.map(q => q[1]);
  for (let i = 1; i < kt.length; i++) if (kt[i] <= kt[i - 1]) kt[i] = kt[i - 1] + 1;
  const focus = interpolate(f, kt, kc, CL);
  const camX = (960 - cx(focus)) * 0.12;   // 0.2면 넷째 칸 때 왼쪽 '산 값' 글자가 판 밖으로 잘림(2차)
  // 말마다 숨 쉬듯 다가갔다 물러남(2차: 팬만으로는 9.2~14초 4.8초 정지) — 새 막대·꼬리표가 나올 때 0→1(30프레임), 다음 150프레임에 걸쳐 0
  const ev0 = [...all.map(s => s.at), ...p.prem.map(q => q[1]), p.hit].sort((x, y) => x - y);
  // 한 문장이 길어 사건 사이가 6초 넘게 비면(환율 문장 6.4초) 가운데에 한 번 더 숨 — 3차·4차 10초대 정지 3.2~3.8초
  const ev = ev0.flatMap((a, i) => i + 1 < ev0.length && ev0[i + 1] - a > 180 ? [a, Math.round((a + ev0[i + 1]) / 2)] : [a]);
  const pulse = Math.max(0, ...ev.map(a => f < a ? 0 : f < a + 30 ? Easing.out(Easing.cubic)((f - a) / 30) : Math.max(0, 1 - Math.min(1, (f - a - 30) / 160))));
  // 결론 뒤에도 4초 넘게 말이 이어져 정지가 생김(1차 4.0초) → 결론부터 괄호 쪽으로 따로 다가간다
  const cam = f < p.note[1] ? interpolate(f, [p.intro, p.note[1]], [1.0, 1.04], CL) : interpolate(f, [p.note[1], p.note[1] + 150], [1.04, 1.09], {...CL, easing: ease});
  const dimFirst = interpolate(f, [p.note[1], p.note[1] + 14], [1, 0.3], CL);

  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translateX(${camX}px) scale(${cam * (1 + 0.06 * pulse)})`, transformOrigin: `${f < p.note[1] ? cx(focus) : interpolate(f, [p.note[1], p.note[1] + 150], [960, cx(1.2)], {...CL, easing: ease})}px ${f < p.note[1] ? zy : interpolate(f, [p.note[1], p.note[1] + 150], [zy, top], {...CL, easing: ease})}px`}}>
        <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
          {/* 0 기준선 = 산 날 값 */}
          <line x1={x0 - 20} x2={x0 + colW * 4} y1={zy} y2={zy} stroke={T.ink} strokeWidth={4} opacity={fade(f, p.intro, 12)}
            strokeDasharray={2000} strokeDashoffset={2000 * (1 - grow(p.intro))} />
          <text x={x0 - 30} y={zy + 8} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={24} fill={T.ink2} opacity={fade(f, p.intro + 8)}>0</text>
          <text x={x0 - 30} y={zy + 38} textAnchor="end" fontFamily="PD" fontWeight={500} fontSize={20} fill={T.ink3} opacity={fade(f, p.intro + 8)}>{p.zeroText.split(' = ')[0]}</text>
          {/* 이어 붙이는 가는 선(앞 막대 끝 → 다음 막대 시작) */}
          {p.steps.map((s, i) => {
            const nx = i + 1 < p.steps.length ? p.steps[i + 1].at : p.total.at;
            const g = interpolate(f, [nx - 8, nx + 6], [0, 1], {...CL, easing: out});
            const y = Y(ends[i]);
            return <line key={i} x1={cx(i) + barW / 2} x2={cx(i) + barW / 2 + (colW - barW) * g} y1={y} y2={y} stroke={T.ink3} strokeWidth={2} opacity={g > 0 ? 1 : 0} />;
          })}
        </svg>

        {all.map((s, i) => {
          const isT = i === all.length - 1;
          const a = isT ? 0 : starts[i], b = isT ? s.pp : ends[i];
          const g = grow(s.at);
          if (f < s.at) return null;
          const cur = a + (b - a) * g;
          const yTop = Y(Math.max(a, cur)), yBot = Y(Math.min(a, cur));
          const up = b > a;
          const color = isT ? T.accent : up ? T.rise : T.fall;
          const op = i === 0 ? dimFirst : 1;
          // 값 글자: 오르는 막대는 위, 내리는 막대는 아래 끝
          const ly = up ? Y(b) - 98 : Y(b) + 12;   // 레드팀 10/9: 곱 % 글자 아래 '막대 %p'를 밝힌다(더하면 −3.99%라 어긋나 보임)
          return (
            <React.Fragment key={i}>
              <div style={{position: 'absolute', left: cx(i) - barW / 2, top: yTop, width: barW, height: Math.max(2, yBot - yTop), background: color, opacity: op,
                borderRadius: up ? '8px 8px 2px 2px' : '2px 2px 8px 8px', boxShadow: '0 8px 20px rgba(0,0,0,.12)'}} />
              <div style={{...F, position: 'absolute', left: cx(i) - colW / 2, width: colW, textAlign: 'center', top: ly, opacity: fade(f, s.at + 16, 8) * op,
                transform: `translateY(${(1 - fade(f, s.at + 16, 8)) * (up ? 12 : -12)}px)`}}>
                <div style={{fontWeight: 700, fontSize: isT ? 64 : 56, letterSpacing: -1, color: isT ? T.accent : T.ink, whiteSpace: 'nowrap', lineHeight: 1.1}}>{s.text}</div>
                {isT ? null : <div style={{fontWeight: 500, fontSize: 22, color: T.ink3, whiteSpace: 'nowrap'}}>막대 {s.pp > 0 ? '+' : '−'}{Math.abs(s.pp).toFixed(1)}%p</div>}
              </div>
              {/* 칸 이름 */}
              <div style={{...F, position: 'absolute', left: cx(i) - colW / 2, width: colW, textAlign: 'center', top: bot + 26, opacity: fade(f, s.at, 10) * (i === 0 ? 0.4 + 0.6 * dimFirst : 1), whiteSpace: 'nowrap'}}>
                <div style={{fontWeight: 700, fontSize: 32, color: isT ? T.accent : T.ink}}>{s.name}</div>
                <div style={{fontWeight: 500, fontSize: 20, color: T.ink3, marginTop: 2}}>{s.sub}</div>
              </div>
            </React.Fragment>
          );
        })}

        {/* 합계 옆: 1천만원 → 오늘 값(calc_out 영수증 KRX 칸) */}
        <div style={{...F, position: 'absolute', left: cx(3) - colW / 2, width: colW, textAlign: 'center', top: zy - 66, fontWeight: 700, fontSize: 30, color: T.ink2,
          opacity: fade(f, p.total.at + 26, 10), whiteSpace: 'nowrap'}}>{p.total.won}</div>

        {/* 웃돈 그때 → 지금 꼬리표(셋째 칸 위) */}
        <div style={{...F, position: 'absolute', left: cx(2) - colW / 2, width: colW, textAlign: 'center', top: Y(starts[2]) - 110, whiteSpace: 'nowrap'}}>
          {p.prem.map(([t, at], j) => (
            <span key={j} style={{display: 'inline-block', fontWeight: 700, fontSize: 26, padding: '6px 12px', borderRadius: 10, margin: '0 4px',
              background: j === 0 ? '#fde4e4' : '#e4ecfb', color: j === 0 ? T.rise : T.fall,   // 주황은 합계 색 — 그때 웃돈(높았다)은 빨강 계열(레드팀 10/9)
               opacity: fade(f, at, 8), transform: `scale(${interpolate(f, [at, at + 10], [0.8, 1], {...CL, easing: Easing.out(Easing.back(2))})})`}}>{j ? '→ ' : ''}{t}</span>
          ))}
        </div>
        {/* '이 웃돈이 빠진 것만으로도' — 셋째 값 글자에 손 동그라미 */}
        {p.steps[2] && f >= p.hit ? (
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, opacity: dimFirst < 1 ? 0 : 1}}>
            <HandCircle cx={cx(2)} cy={Y(ends[2]) + 50} rx={124} ry={56} p={interpolate(f, [p.hit, p.hit + 22], [0, 1], CL)} />
          </svg>
        ) : null}

        {/* 결론: 0선 아래 빈 자리(첫째·둘째 칸)에 두 줄 — 1차는 판 위 끝 [자막] 띠·+6.65%와 겹쳤다 */}
        {f >= p.note[1] ? (() => {
          const g = interpolate(f, [p.note[1] + 6, p.note[1] + 24], [0, 1], {...CL, easing: out});
          const [l1, l2] = p.note[0].split(' 환율');
          return (
            <div style={{...F, position: 'absolute', left: x0 + 10, top: zy + 34, fontWeight: 700, fontSize: 50, lineHeight: 1.18, letterSpacing: -1, color: T.accent,
              opacity: g, transform: `translateY(${(1 - g) * 14}px)`, whiteSpace: 'nowrap', textShadow: '0 0 14px #fff, 0 0 6px #fff'}}>
              <div>{l1}</div><div>{l2 !== undefined ? '환율' + l2 : ''}</div>
              <div style={{height: 6, width: 560 * g, background: T.accent, borderRadius: 3, marginTop: 8}} />
            </div>
          );
        })() : null}
      </div>
    </div>
  );
};
