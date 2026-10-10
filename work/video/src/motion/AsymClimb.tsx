// 내려온 폭 vs 올라갈 폭(AsymClimb) — G-1 '6. 산 값까지의 산수'(2026-10-10 motion). TallyFrame 자식.
// 같은 0 기준선 위에 1g 값 막대 두 개: 왼쪽 = 1월 고점 값(위 몫이 '내려온 폭'으로 빗금), 오른쪽 = 오늘 값(위에 '올라야 할 폭'이 쌓여 고점 선까지).
// 핵심: 두 폭은 높이가 같다(같은 원) — 그런데 기준 막대가 달라 −33.66% / +50.7%. 차액 숫자는 화면에 만들지 않고 높이로만 보인다.
// 정직성: 막대 높이 = 1g 값 비례(0부터), 글자 = calc_out 그대로(props). 숫자는 굴리지 않는다. 빗금 = '내려온 폭' 한 뜻, 점선은 쓰지 않는다.
// 움직임: 사건마다 다가갔다 물러남(선형 감쇠) + 말이 가리키는 칸으로 옆 이동 + 끝 도장 뒤 천천히 다가감.
import React from 'react';
import {interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type AsymClimbProps = {
  seed: string; top: number; now: number;
  peakText: string; nowText: string; peakName: string; nowName: string;
  downText: string; upText: string; downBase: string; upBase: string;
  intro: number; drop: number; slide: number; climb: number; base: number; short: number;
  shortText: string; shortLack: string; fee: [string, number]; calm?: string;
};

const out = Easing.out(Easing.cubic);
const ease = Easing.inOut(Easing.cubic);
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);

export const AsymClimb: React.FC<AsymClimbProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  // 판 y 236~852: 위 254~300은 [자막] 띠 → 고점 글자는 340 아래. 0선 760, 칸 이름은 그 아래 772~840.
  const Z = 760, YT = 404 + Math.round(r('y') * 10);
  const k = (Z - YT) / p.top;
  const Y = (v: number) => Z - v * k;
  const barW = Math.round(190 + r('w') * 20);
  const LX = 690 + Math.round(r('l') * 16), RX = 1170 + Math.round(r('r') * 16);   // 막대 가운데 x — 1차는 600/1110이라 오른쪽 3분의 1이 비었다
  const MX = (LX + RX) / 2;
  const yNow = Y(p.now), yTop = Y(p.top);
  const shortV = p.now * (1 + Math.abs(parseFloat(p.downText.replace('−', '-'))) / 100);   // 34%만 오르면 닿는 높이(글자 없음)
  const ySh = Y(shortV);

  // 진행값
  const gL = interpolate(f, [p.intro + 6, p.intro + 34], [0, 1], {...CL, easing: out});        // 고점 막대 자람
  const gD = interpolate(f, [p.drop, p.drop + 24], [0, 1], {...CL, easing: ease});             // 위 몫이 빗금으로
  const gS = interpolate(f, [p.slide, p.slide + 26], [0, 1], {...CL, easing: ease});           // 오늘 막대 오른쪽으로
  const gC = interpolate(f, [p.climb, p.climb + 30], [0, 1], {...CL, easing: out});            // 올라야 할 폭 쌓임
  const gB = interpolate(f, [p.base, p.base + 20], [0, 1], {...CL, easing: out});              // 기준 괄호·같은 폭
  const gH = interpolate(f, [p.short, p.short + 28], [0, 1], {...CL, easing: out});            // 34%만 오르면
  const gF = interpolate(f, [p.fee[1], p.fee[1] + 16], [0, 1], {...CL, easing: out});         // 도장

  // 카메라: 말이 가리키는 칸으로 옆 이동(키 사이 선형) + 사건마다 숨
  const keys: [number, number][] = [[p.intro, LX], [p.drop, LX], [p.slide, MX], [p.climb, RX], [p.base, MX], [p.short, RX], [p.fee[1], RX + 120], [p.fee[1] + 400, RX + 120]];
  const kt = keys.map(q => q[0]); for (let i = 1; i < kt.length; i++) if (kt[i] <= kt[i - 1]) kt[i] = kt[i - 1] + 1;
  const focus = interpolate(f, kt, keys.map(q => q[1]), CL);
  const camX = (960 - focus) * 0.14;
  const ev0 = [p.intro + 6, p.drop, p.slide, p.climb, p.base, p.short, p.fee[1]].sort((a, b) => a - b);
  const ev = ev0.flatMap((a, i) => i + 1 < ev0.length && ev0[i + 1] - a > 150 ? [a, Math.round((a + ev0[i + 1]) / 2)] : [a]);
  const pulse = Math.max(0, ...ev.map(a => f < a ? 0 : f < a + 26 ? out((f - a) / 26) : Math.max(0, 1 - Math.min(1, (f - a - 26) / 140))));
  // 도장 뒤 말이 5초쯤 이어짐 → 도장 쪽으로 천천히 다가감(선형, 꼬리 정지 방지)
  const cam = f < p.fee[1] ? interpolate(f, [p.intro, p.fee[1]], [1.0, 1.04], CL) : interpolate(f, [p.fee[1], p.fee[1] + 170], [1.04, 1.08], CL);   // 1.12면 17초대 왼쪽 '−33.66%'가 판 가장자리에 닿음(레드팀 2차)
  const oy = f < p.fee[1] ? (yTop + Z) / 2 : interpolate(f, [p.fee[1], p.fee[1] + 60], [(yTop + Z) / 2, 640], {...CL, easing: ease});

  // 왼쪽 막대: 0~오늘은 잉크, 오늘~고점은 처음엔 잉크 → 빗금(파랑)으로
  const lTop = Y(p.top * gL);
  const slideX = LX + (RX - LX) * gS;
  const dimRed = 1 - 0.55 * gH;   // 레드팀 10/10: 빨강을 거의 지우면 '+50.7%' 막대가 사라져 보인다 → 옅게 남김
  // 끝 비교: 도장 뒤 말이 5초 이어짐(레드팀 '후반 정적') → 두 % 글자를 차례로 한 번씩 짚는다
  const tap = (a: number) => interpolate(f, [a, a + 10, a + 26], [0, 1, 0], CL);
  const tapD = tap(p.fee[1] + 60), tapU = tap(p.fee[1] + 95);

  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translateX(${camX}px) scale(${cam * (1 + 0.05 * pulse)})`, transformOrigin: `${focus}px ${oy}px`}}>
        <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}}>
          <defs>
            <pattern id="asymHatch" width={18} height={18} patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width={18} height={18} fill="#e4ecfb" />
              <line x1={0} y1={0} x2={0} y2={18} stroke={T.fall} strokeWidth={7} />
            </pattern>
          </defs>
          {/* 0 기준선 */}
          <line x1={LX - barW / 2 - 140} x2={RX + barW / 2 + 140} y1={Z} y2={Z} stroke={T.ink} strokeWidth={4}
            strokeDasharray={2000} strokeDashoffset={2000 * (1 - interpolate(f, [p.intro, p.intro + 20], [0, 1], {...CL, easing: out}))} />
          <text x={LX - barW / 2 - 150} y={Z + 8} textAnchor="end" fontFamily="PD" fontWeight={700} fontSize={26} fill={T.ink2} opacity={fade(f, p.intro + 10)}>0원</text>

          {/* 고점 선(가는 실선) — 두 칸을 가로지름 */}
          <line x1={LX - barW / 2 - 20} x2={LX - barW / 2 - 20 + (RX - LX + barW + 60) * interpolate(f, [p.drop, p.drop + 30], [0, 1], {...CL, easing: out})} y1={yTop} y2={yTop}
            stroke={T.ink3} strokeWidth={2} opacity={gD > 0 ? 1 : 0} />
          {/* 오늘 선 — 같은 폭을 보일 때만 */}
          <line x1={LX + barW / 2} x2={LX + barW / 2 + (RX - LX - barW) * gB} y1={yNow} y2={yNow} stroke={T.ink3} strokeWidth={2} opacity={gB > 0 ? 1 - 0.7 * gH : 0} />

          {/* 왼쪽: 고점에 산 금 */}
          {f >= p.intro + 6 ? (
            <>
              <rect x={LX - barW / 2} y={Math.max(lTop, yNow)} width={barW} height={Z - Math.max(lTop, yNow)} fill={T.ink} rx={4} />
              {lTop < yNow ? (
                <>
                  <rect x={LX - barW / 2} y={lTop} width={barW} height={yNow - lTop} fill={T.ink} rx={6} opacity={1 - gD} />
                  <rect x={LX - barW / 2} y={lTop} width={barW} height={yNow - lTop} fill="url(#asymHatch)" rx={6} opacity={gD} stroke={T.fall} strokeWidth={3} />
                </>
              ) : null}
              {/* 기준 강조: 막대 전체(0~고점) 테두리 */}
              <rect x={LX - barW / 2 - 8} y={yTop - 8} width={barW + 16} height={Z - yTop + 8} fill="none" stroke={T.fall} strokeWidth={5} rx={10}
                opacity={gB * (1 - 0.6 * gH)} strokeDasharray={3000} strokeDashoffset={3000 * (1 - gB)} />
            </>
          ) : null}

          {/* 오른쪽: 오늘 값 막대(왼쪽에서 옮겨 옴) */}
          {f >= p.slide ? (
            <>
              <rect x={slideX - barW / 2} y={yNow} width={barW} height={Z - yNow} fill={T.ink} rx={4} opacity={0.35 + 0.65 * gS} />
              {/* 올라야 할 폭 */}
              {gC > 0 ? <rect x={RX - barW / 2} y={yNow - (yNow - yTop) * gC} width={barW} height={(yNow - yTop) * gC} fill={T.rise} rx={6} opacity={dimRed} /> : null}
              <rect x={RX - barW / 2 - 8} y={yNow - 8} width={barW + 16} height={Z - yNow + 8} fill="none" stroke={T.rise} strokeWidth={5} rx={10}
                opacity={gB * (1 - 0.6 * gH)} strokeDasharray={3000} strokeDashoffset={3000 * (1 - gB)} />
            </>
          ) : null}

          {/* 같은 폭: 두 칸 사이 양방향 화살표 */}
          {gB > 0 ? (
            <g opacity={gB * (1 - gH)}>{/* '34%만 오르면' 글자와 겹쳐서(1차) 완전히 걷는다 */}
              <line x1={MX} x2={MX} y1={yNow - (yNow - yTop) * gB} y2={yNow} stroke={T.ink} strokeWidth={4} />
              <path d={`M${MX - 12},${yTop + 16} L${MX},${yTop} L${MX + 12},${yTop + 16}`} fill="none" stroke={T.ink} strokeWidth={4} opacity={gB > 0.9 ? 1 : 0} />
              <path d={`M${MX - 12},${yNow - 16} L${MX},${yNow} L${MX + 12},${yNow - 16}`} fill="none" stroke={T.ink} strokeWidth={4} />
            </g>
          ) : null}

          {/* 34%만 오르면: 오늘 막대 위 테두리만 있는 몫 → 그 위 고점까지 빈 곳이 '모자라요' */}
          {gH > 0 ? (
            <>
              <rect x={RX - barW / 2 + 10} y={yNow - (yNow - ySh) * gH} width={barW - 20} height={(yNow - ySh) * gH} fill="none" stroke={T.ink} strokeWidth={4} rx={4} />{/* 속이 비어 아래 빨강이 비침(흰 몫+모자란 몫 = 빨강 전체) */}
              <rect x={RX - barW / 2 + 10} y={yTop} width={barW - 20} height={ySh - yTop} fill={T.accent} rx={4}   // 빗금은 '내려온 폭' 한 뜻만(레드팀 10/10) — 모자란 몫은 무늬 없는 주황 면
                opacity={interpolate(f, [p.short + 24, p.short + 38], [0, 1], CL)} />
            </>
          ) : null}
        </svg>

        {/* 고점 막대 위 이름·값 */}
        <div style={{...F, position: 'absolute', left: LX - 220, width: 440, textAlign: 'center', top: yTop - 64, opacity: fade(f, p.intro + 24, 10), whiteSpace: 'nowrap',
          transform: `translateY(${(1 - fade(f, p.intro + 24, 10)) * 10}px)`}}>
          <span style={{fontWeight: 700, fontSize: 44, color: T.ink, letterSpacing: -1}}>{p.peakText}</span>
        </div>
        {/* 왼쪽 막대 안 '오늘 값' 높이 표시는 오른쪽 막대 글자로 — 왼쪽은 내려온 폭 글자 */}
        <div style={{...F, position: 'absolute', left: LX - barW / 2 - 330, width: 300, textAlign: 'right', top: (yTop + yNow) / 2 - 52, opacity: fade(f, p.drop + 14, 10), whiteSpace: 'nowrap',
          transform: `translateX(${(1 - fade(f, p.drop + 14, 10)) * 16}px)`}}>
          <div style={{fontWeight: 700, fontSize: 62, color: T.fall, letterSpacing: -1, lineHeight: 1.05, transform: `scale(${1 + 0.14 * tapD})`, transformOrigin: 'right center'}}>{p.downText}</div>
          <div style={{fontWeight: 700, fontSize: 30, color: T.ink2}}>내려온 폭</div>
        </div>
        {/* 오늘 값 글자 — 옮겨지는 막대를 따라감 */}
        {f >= p.slide ? (
          <div style={{...F, position: 'absolute', left: slideX - 220, width: 440, textAlign: 'center', top: yNow + 14, opacity: fade(f, p.slide + 10, 10) * (1 - gC), whiteSpace: 'nowrap'}}>
            <span style={{fontWeight: 700, fontSize: 36, color: '#fff'}}>{p.nowText}</span>
          </div>
        ) : null}
        {f >= p.climb ? (
          <div style={{...F, position: 'absolute', left: RX - 220, width: 440, textAlign: 'center', top: yNow + 14, opacity: fade(f, p.climb + 10, 10), whiteSpace: 'nowrap'}}>
            <span style={{fontWeight: 700, fontSize: 36, color: '#fff'}}>{p.nowText}</span>
          </div>
        ) : null}
        {/* 올라야 할 폭 글자 */}
        <div style={{...F, position: 'absolute', left: RX + barW / 2 + 30, top: (yTop + yNow) / 2 - 52, opacity: fade(f, p.climb + 18, 10) * Math.max(0.6, dimRed + tapU), whiteSpace: 'nowrap',
          transform: `translateX(${(1 - fade(f, p.climb + 18, 10)) * -16}px) translateY(${gH * 96}px)`}}>{/* '모자라요' 자리를 비켜 아래로 */}
          <div style={{fontWeight: 700, fontSize: 72, color: T.rise, letterSpacing: -1, lineHeight: 1.05, transform: `scale(${1 + 0.14 * tapU})`, transformOrigin: 'left center'}}>{p.upText}</div>
          <div style={{fontWeight: 700, fontSize: 30, color: T.ink2}}>산 값까지 올라야 할 폭</div>
        </div>
        {/* 같은 폭 글자(화살표 옆, 숫자 없음) */}
        <div style={{...F, position: 'absolute', left: MX - 120, width: 240, textAlign: 'center', top: (yTop + yNow) / 2 - 22, opacity: fade(f, p.base + 12, 10) * (1 - gH), whiteSpace: 'nowrap'}}>
          <span style={{fontWeight: 700, fontSize: 32, color: T.ink, background: '#fff', padding: '4px 12px', borderRadius: 8}}>같은 폭</span>
        </div>
        {/* 칸 이름 + 기준(같은 폭인데 나누는 값이 다르다) */}
        {[[LX, p.peakName, p.downBase, T.fall, p.intro + 20], [RX, p.nowName, p.upBase, T.rise, p.slide + 16]].map(([x, name, base, col, a], i) => (
          <div key={i} style={{...F, position: 'absolute', left: (x as number) - 260, width: 520, textAlign: 'center', top: Z + 14, whiteSpace: 'nowrap', opacity: fade(f, a as number, 10)}}>
            <div style={{fontWeight: 700, fontSize: 30, color: T.ink}}>{name as string}</div>
            <div style={{fontWeight: 700, fontSize: 30, color: col as string, opacity: gB, transform: `translateY(${(1 - gB) * -8}px)`}}>{base as string}</div>
          </div>
        ))}

        {/* 34%만 오르면 / 모자라요 */}
        <div style={{...F, position: 'absolute', left: MX - 200, width: 360, textAlign: 'right', top: (ySh + yNow) / 2 - 24, opacity: fade(f, p.short + 12, 10), whiteSpace: 'nowrap'}}>
          <span style={{fontWeight: 700, fontSize: 36, color: T.ink}}>{p.shortText} →</span>
        </div>
        <div style={{...F, position: 'absolute', left: RX + barW / 2 + 30, top: (yTop + ySh) / 2 - 34, opacity: fade(f, p.short + 30, 10), whiteSpace: 'nowrap',
          transform: `scale(${interpolate(f, [p.short + 30, p.short + 42], [0.85, 1], {...CL, easing: Easing.out(Easing.back(2))})})`, transformOrigin: 'left center'}}>
          <span style={{fontWeight: 700, fontSize: 52, color: T.accent, letterSpacing: -1}}>← {p.shortLack}</span>
        </div>

        {/* 도장: 수수료·팔 때 값 차이 뺀 숫자(대본 원문 조각) */}
        {f >= p.fee[1] ? (
          <div style={{...F, position: 'absolute', left: RX + barW / 2 + 30, top: 690, width: 440, opacity: gF, transform: `translateY(${(1 - gF) * 20}px) rotate(${-1.5 + r('s') * 1}deg)`,
            background: T.ink, color: '#fff', borderRadius: 14, padding: '14px 22px', fontWeight: 700, fontSize: 30, lineHeight: 1.3, boxShadow: '0 10px 24px rgba(0,0,0,.18)'}}>
            {p.fee[0]}
          </div>
        ) : null}
      </div>
    </div>
  );
};
