// 모션 부품 — 점 하나 → 줌아웃(모션 475 #5) 롱폼 첫 장면. TallyFrame 보드 안에서 쓴다.
// ① 1억 점 하나를 크게 확대한 채 시작(말 1) → ② 뒤로 빠지며 갈래 N개가 '?'로 뻗음(말 2) → ③ 날짜 축·'1억'이 갈래를 따라 감(말 3)
// → ④ 갈래가 흐려지고 오른쪽에 '간격' 막대 두 개: 세금 전 길이에서 세금 뒤 길이로 줄어듦(말 4). 막대 길이만 값 비례, 글자는 props 원문 그대로.
// 갈래 끝 위치는 고르게 나눈 자리(값 아님) — 결과 순위를 미리 암시하지 않는다. 숫자를 부품 안에 쓰지 않는다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from '../parts/fm';

export type ZoomOutOpenProps = {
  seed: string;
  dot: string;                 // 점 옆 글자(예: '1억')
  names: string[];             // 갈래 이름(대본에 나오는 순서)
  nameAt: number[];            // 각 갈래가 뻗기 시작하는 프레임(장면 기준)
  from: string; to: string;    // 축 양끝 날짜 글자
  q: number;                   // 줌아웃 시작(말 2 시작)
  travel: number;              // 날짜 축·'1억' 이동 시작(말 3 시작)
  gap: number;                 // 간격 막대 시작(말 4 시작)
  gapHead: string;             // 간격 막대 제목(예: 'SCHD − 예금 차이')
  pre: [string, number];       // [글자, 값] 세금 전
  post: [string, number];      // [글자, 값] 세금 뒤
  cut: string;                 // 줄어든 몫 글자
};

const hash = (s: string) => { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
const ease = Easing.inOut(Easing.cubic);
const fade = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], CL);

export const ZoomOutOpen: React.FC<ZoomOutOpenProps> = (p) => {
  const f = useCurrentFrame();
  const h = hash(p.seed);
  // 갈래는 대본 순서대로 위→아래 고정(순서를 뒤집으면 결과 순위처럼 읽힐 수 있음, 레드팀 10/5). 편마다 바뀌는 건 점 높이·부채 폭.
  const P = {x: 230, y: 545 + ((h >> 1) % 3) * 15};    // 월드 좌표의 점
  const endX = 1000; const spread = 330 + ((h >> 3) % 3) * 10; const top = P.y - spread / 2 - 5; const bot = P.y + spread / 2 + 5;
  const n = p.names.length;
  const ys = p.names.map((_, i) => { const k = i; return n === 1 ? P.y : top + (bot - top) * k / (n - 1); });

  // 카메라: 처음엔 점을 화면 가운데에 크게(zA배), q부터 1배로 빠진다. 말 1 동안도 아주 천천히 빠져 정지 화면이 아니다.
  const zA = 3.4;
  const drift = interpolate(f, [0, p.q], [0, 0.3], CL);
  const pull = interpolate(f, [p.q, p.q + 75], [0, 1], {...CL, easing: ease});
  const pp = Math.min(1, drift + (1 - 0.3) * pull);
  const z = Math.exp(Math.log(zA) * (1 - pp));
  const scr = {x: 860 + (P.x - 860) * pp, y: 560 + (P.y - 560) * pp};
  const tx = scr.x - z * P.x; const ty = scr.y - z * P.y;
  // 간격 단계: 갈래 묶음이 조금 더 빠지며 흐려진다
  const g = interpolate(f, [p.gap, p.gap + 24], [0, 1], {...CL, easing: ease});
  const worldO = 1 - g;   // 간격 막대 단계에선 갈래를 완전히 뺀다(시선 다툼·'맨 위' 말과 자리 어긋남 방지)
  const worldS = 1 - 0.08 * g;

  const pulse = 1 + 0.06 * Math.sin(f / 9) * (1 - pull);
  // 말 1 '통장에 1억이 들어왔다' — 입금 줄이 점 아래로 들어온다(첫 5초 두 번째 움직임)
  const dep = interpolate(f, [55, 75], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const depO = dep * (1 - fade(f, p.q + 10, 16));
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'hidden', clipPath: 'inset(238px 102px 230px 102px round 22px)'}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '0 0',
          transform: `translate(${tx}px, ${ty}px) scale(${z * worldS})`, opacity: worldO}}>
          <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
            {/* 날짜 축 */}
            <line x1={P.x} y1={795} x2={P.x + (endX - P.x) * fade(f, p.travel, 30)} y2={795} stroke={T.line} strokeWidth={4} />
            {p.names.map((_, i) => {
              const a = p.nameAt[i]; const k = interpolate(f, [a, a + 26], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
              const x2 = P.x + (endX - P.x) * k; const y2 = P.y + (ys[i] - P.y) * k;
              return <line key={i} x1={P.x} y1={P.y} x2={x2} y2={y2} stroke={T.ink3} strokeWidth={3.5} strokeDasharray="10 9" strokeLinecap="round" />;
            })}
            <circle cx={P.x} cy={P.y} r={16 * pulse} fill={T.accent} />
            <circle cx={P.x} cy={P.y} r={30 * pulse} fill="none" stroke={T.accent} strokeOpacity={0.35} strokeWidth={3} />
          </svg>
          <div style={{...F, position: 'absolute', left: P.x + 40, top: P.y - 36, fontWeight: 700, fontSize: 52, color: T.ink, whiteSpace: 'nowrap', opacity: 1 - fade(f, p.q + 40, 20)}}>{p.dot}</div>
          <div style={{...F, position: 'absolute', left: P.x - 40, top: P.y - 92, fontWeight: 700, fontSize: 52, color: T.ink, whiteSpace: 'nowrap', opacity: fade(f, p.q + 40, 20)}}>{p.dot}</div>
          <div style={{...F, position: 'absolute', left: P.x + 40, top: P.y + 34 + (1 - dep) * 18, opacity: depO, fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap', display: 'flex', gap: 12, alignItems: 'center'}}>
            <span style={{background: T.soft, color: T.accent, borderRadius: 8, padding: '2px 12px'}}>통장 입금</span>
          </div>
          {/* 갈래 끝: 이름 + ? */}
          {p.names.map((name, i) => {
            const o = fade(f, p.nameAt[i] + 18, 10);
            // '1억'이 닿은 뒤 '?'가 차례로 한 번씩 튄다(영수증을 뽑는 순간, 말 3 끝) — 순서는 대본 순서, 크기 같음
            const b0 = p.travel + 112 + i * 16; const bump = 1 + 0.22 * Math.sin(Math.PI * interpolate(f, [b0, b0 + 14], [0, 1], CL));
            return (
              <div key={i} style={{position: 'absolute', left: endX + 18, top: ys[i] - 30, display: 'flex', alignItems: 'center', gap: 14, opacity: o, transform: `translateX(${(1 - o) * 14}px)`}}>
                <div style={{...F, fontWeight: 700, fontSize: 38, color: T.ink, whiteSpace: 'nowrap'}}>{name}</div>
                <div style={{...F, fontWeight: 700, fontSize: 34, color: '#fff', background: T.ink, borderRadius: 10, width: 52, height: 52, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${bump})`}}>?</div>
              </div>
            );
          })}
          {/* '1억'이 갈래를 따라 같은 속도로 감 — 넣은 돈이 같다는 뜻 */}
          {p.names.map((_, i) => {
            const k = interpolate(f, [p.travel + 20, p.travel + 110], [0, 1], {...CL, easing: ease});
            if (f < p.travel + 20) return null;
            const x = P.x + (endX - P.x) * k * 0.86; const y = P.y + (ys[i] - P.y) * k * 0.86;
            return <div key={i} style={{...F, position: 'absolute', left: x - 34, top: y - 46, fontWeight: 700, fontSize: 26, color: T.accent, background: T.soft, borderRadius: 8, padding: '2px 10px', whiteSpace: 'nowrap', opacity: fade(f, p.travel + 20, 8)}}>{p.dot}</div>;
          })}
          <div style={{...F, position: 'absolute', left: P.x - 60, top: 806, fontWeight: 700, fontSize: 28, color: T.ink2, opacity: fade(f, p.travel, 12), whiteSpace: 'nowrap'}}>{p.from}</div>
          <div style={{...F, position: 'absolute', left: endX - 70, top: 806, fontWeight: 700, fontSize: 28, color: T.ink2, opacity: fade(f, p.travel + 24, 12), whiteSpace: 'nowrap'}}>{p.to}</div>
        </div>
      </div>
      <GapBars {...p} />
    </>
  );
};

// 간격 막대: 세금 전 막대가 다 그려진 뒤, 세금 뒤 막대가 같은 길이에서 줄어든다(줄어든 몫은 빗금으로 남김). 길이는 값 비례, 0 기준선 공유.
const GapBars: React.FC<ZoomOutOpenProps> = (p) => {
  const f = useCurrentFrame();
  const W = 760; const x = (1920 - W) / 2; const y = 360;
  const o = fade(f, p.gap + 10, 12);
  if (f < p.gap) return null;
  const a = interpolate(f, [p.gap + 14, p.gap + 44], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const ratio = p.post[1] / p.pre[1];
  const b = interpolate(f, [p.gap + 70, p.gap + 110], [1, ratio], {...CL, easing: ease});
  const bo = fade(f, p.gap + 60, 10);
  const cutO = fade(f, p.gap + 112, 12);
  const beat = 1 + 0.08 * Math.sin(Math.PI * interpolate(f, [p.gap + 140, p.gap + 158], [0, 1], CL));   // 다 그려진 뒤 줄어든 몫을 한 번 맥박
  return (
    <div style={{position: 'absolute', left: x, top: y, width: W + 40, opacity: o}}>
      <div style={{...F, fontWeight: 700, fontSize: 34, color: T.ink, whiteSpace: 'nowrap'}}>{p.gapHead}</div>
      <div style={{position: 'absolute', left: 0, top: 70, width: 4, height: 300, background: T.ink2}} />
      <div style={{...F, position: 'absolute', left: 20, top: 74, fontWeight: 700, fontSize: 28, color: T.ink2, whiteSpace: 'nowrap'}}>세금 전</div>
      <div style={{position: 'absolute', left: 4, top: 118, height: 62, width: W * a, background: T.ink3, borderRadius: '0 10px 10px 0'}} />
      <div style={{...F, position: 'absolute', left: 20, top: 190, fontWeight: 700, fontSize: 34, color: T.ink2, whiteSpace: 'nowrap', opacity: fade(f, p.gap + 40, 8)}}>{p.pre[0]}</div>
      <div style={{opacity: bo}}>
        <div style={{...F, position: 'absolute', left: 20, top: 248, fontWeight: 700, fontSize: 28, color: T.accent, whiteSpace: 'nowrap'}}>세금 뒤</div>
        <div style={{position: 'absolute', left: 4 + W * ratio, top: 292, height: 62, width: W * (1 - ratio), borderRadius: '0 10px 10px 0', opacity: cutO,
          background: `repeating-linear-gradient(135deg, ${T.soft} 0 10px, #fff 10px 20px)`, border: `2px dashed ${T.accent}`, boxSizing: 'border-box', transform: `scaleY(${beat})`}} />
        <div style={{position: 'absolute', left: 4, top: 292, height: 62, width: W * b, background: T.accent, borderRadius: '0 10px 10px 0'}} />
        <div style={{...F, position: 'absolute', left: 20, top: 364, fontWeight: 700, fontSize: 34, color: T.accent, whiteSpace: 'nowrap', opacity: cutO}}>{p.post[0]}</div>
        <div style={{...F, position: 'absolute', left: 4 + W, top: 364, transform: 'translateX(-100%)', fontWeight: 700, fontSize: 28, color: '#fff', background: T.accent, borderRadius: 8, padding: '0 10px', whiteSpace: 'nowrap', opacity: cutO}}>{p.cut}</div>
      </div>
    </div>
  );
};
