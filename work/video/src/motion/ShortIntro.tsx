// 쇼츠 첫 2초(2026-10-04 motion) — 정지 표지 1초 대신: 질문 제목 + 숫자가 내려앉고(0~1초) → 숫자 밑 바닥이 차트 기준선이 되고 숫자가 제 막대 이름표가 된다(1~2초).
// v2(심사 6.9 반려 뒤): 제목(갈고리)을 0프레임부터(경쟁 5편 모두 첫 프레임에 질문형 큰 글씨 — 레드팀), 가짜 숫자 0, 막대는 기준선에서만 자람.
// 색·글꼴은 cardshort.py와 같다(바탕 #101218 · 노랑 #FFD000 · 흰 #F6F6FA · 회색 #969CAA · 숫자 Black Han Sans) — 이어 붙는 카드와 끊기지 않게.
// 숫자는 props(spec·facts.txt 원문)로만 받는다. 이 파일 안에 숫자 없음.
import React from 'react';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {RollNumber, seeded} from './RollNumber';
import {CardToBar} from './CardToBar';

const C = {bg: '#101218', card: '#1f2230', y: '#FFD000', w: '#F6F6FA', g: '#969CAA', muted: '#5b6070'};
const CL = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const FONTS = `
@font-face{font-family:'BHS';src:url('${staticFile('fonts/BlackHanSans.ttf')}')}
@font-face{font-family:'PD';font-weight:700;src:url('${staticFile('fonts/pd700.ttf')}')}
@font-face{font-family:'PD';font-weight:500;src:url('${staticFile('fonts/pd500.ttf')}')}`;

export type ShortIntroProps = {
  seed: string; chip: string; title: string;                  // title = spec 제목 그대로(0프레임부터)
  hook: {label: string; text: string; unit: string};
  a: {label: string; value: number; text: string};            // hook 숫자가 될 막대
  b: {label: string; value: number; text: string};            // 비교 막대
  unit: string; source: string;
  numW: number;                                               // 큰 숫자 폭(px, 스틸로 잰 값) — 바닥 선 길이
  aFirst?: boolean;                                           // 없으면 seed. 이어지는 카드의 순서와 맞출 때 지정
  morphAt?: number; frames?: number;
};
export const introFrames = (p: ShortIntroProps) => p.frames ?? 60;

export const ShortIntro: React.FC<ShortIntroProps> = (p) => {
  const f = useCurrentFrame(); const m = p.morphAt ?? 34;
  const NUM = {x: 120, y: 640, size: 250};
  const FLOOR = {x: NUM.x, y: NUM.y + NUM.size * 1.08 + 12, w: p.numW, h: 12};
  const floorP = interpolate(f, [14, 22], [0, 1], CL);
  const cardO = interpolate(f, [m - 5, m], [1, 0], CL);   // 숫자가 움직이기 전에 카드는 다 사라진다(겹침 0)
  const aFirst = p.aFirst ?? seeded(p.seed, 7) < 0.5;
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <style>{FONTS}</style>
      <div style={{position: 'absolute', left: 64, top: 150, display: 'flex', gap: 18}}>
        <span style={{background: '#ff6a00', color: C.w, fontFamily: 'PD', fontWeight: 700, fontSize: 36, padding: '8px 22px', borderRadius: 10}}>파이어맵</span>
        <span style={{background: C.y, color: C.bg, fontFamily: 'PD', fontWeight: 700, fontSize: 36, padding: '8px 22px', borderRadius: 10}}>{p.chip}</span>
      </div>
      <div style={{position: 'absolute', left: 64, top: 250, right: 64, fontFamily: 'BHS', fontSize: 96, color: C.w, lineHeight: 1.12, whiteSpace: 'pre-line'}}>{p.title}</div>
      {/* 0~m: 카드 + 내려앉는 숫자 + 바닥 선 */}
      <div style={{position: 'absolute', left: 64, top: 520, width: 952, height: 520, background: C.card, borderRadius: 28, opacity: cardO}} />
      <div style={{position: 'absolute', left: NUM.x, top: 560, fontFamily: 'PD', fontWeight: 700, fontSize: 56, color: C.w, opacity: cardO}}>{p.hook.label}</div>
      <div style={{position: 'absolute', left: NUM.x + p.numW + 28, top: NUM.y + NUM.size * 1.08 - 66, fontFamily: 'PD', fontWeight: 700, fontSize: 52, color: C.g, opacity: cardO}}>{p.hook.unit}</div>
      {/* 비교 상대를 첫 화면부터 작게(심사관 10/4: '<'가 무엇과 무엇인지 0초에 보이게) */}
      <div style={{position: 'absolute', left: NUM.x, top: 960, fontFamily: 'PD', fontWeight: 700, fontSize: 48, color: C.g, opacity: cardO}}>{p.b.label} {p.b.text}</div>
      {f < m && <>
        <div style={{position: 'absolute', left: NUM.x, top: NUM.y}}><RollNumber text={p.hook.text} size={NUM.size} color={C.y} font="BHS" seed={p.seed} /></div>
        <div style={{position: 'absolute', left: FLOOR.x, top: FLOOR.y, width: FLOOR.w * floorP, height: FLOOR.h, background: C.y, borderRadius: 4}} />
      </>}
      {f >= m && <CardToBar floor={FLOOR} num={NUM} a={p.a} b={p.b} unit={p.unit} baseY={1420} maxH={600} barW={300} gapX={150} left={165} start={m}
        accent={C.y} muted={C.muted} ink={C.w} ink2={C.g} font="PD" numFont="BHS" aFirst={aFirst} />}
      <div style={{position: 'absolute', left: 64, right: 64, top: 1660, fontFamily: 'PD', fontWeight: 500, fontSize: 30, color: C.g, lineHeight: 1.35}}>{p.source}</div>
    </AbsoluteFill>
  );
};
