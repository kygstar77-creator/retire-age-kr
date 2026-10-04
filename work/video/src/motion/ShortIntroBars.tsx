// 쇼츠 첫 2초 v2 '두 막대(0초에 비교가 보임)' (2026-10-05 motion) — ShortIntro v1의 0초 프레임이 1초 시험 6.0 미통과(A: 422만 읽히고 398은 회색·아래 45% 빈칸·'<' 꺾쇠) → 0프레임에 결론·막대 두 개·두 숫자 같은 크기(130px)·0 기준선을 다 둔다.
// 움직임은 0.5초 뒤부터: 긴 막대 끝에서 짧은 막대 끝으로 '차이' 표시선이 내려온다. 가짜 중간 숫자 0, 막대 길이 = 값/큰 값.
// 색은 cardshort.py 표지(v8)와 같다. 숫자는 props(spec·facts 원문)로만 받는다. 이 파일 안에 숫자 없음.
import React from 'react';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';

const C = {bg: 'rgb(38,44,56)', y: '#FFD000', w: '#F6F6FA', g: 'rgb(150,158,175)', lg: 'rgb(200,205,215)', ink: 'rgb(20,22,28)'};
const CL = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const FONTS = `@font-face{font-family:'BHS';src:url('${staticFile('fonts/BlackHanSans.ttf')}')}`;

export type ShortIntroBarsProps = {
  seed: string; head: string; verdict: string[];            // head = 맨 위 제목, verdict = 결론 줄들(노랑)
  a: {label: string; value: number; text: string};          // 큰 막대(노랑)
  b: {label: string; value: number; text: string};          // 작은 막대(회색)
  unit: string; note: string; noteAccent: string;           // 아래 두 줄: '단위 …' / '… ' + 강조어
  frames?: number;
};
export const introBarsFrames = (p: ShortIntroBarsProps) => p.frames ?? 60;

export const ShortIntroBars: React.FC<ShortIntroBarsProps> = (p) => {
  const f = useCurrentFrame();
  const M = 64, BW = 1080 - 2 * M, BH = 340;
  const max = Math.max(p.a.value, p.b.value);
  const bars = [{...p.a, col: C.y}, {...p.b, col: C.g}].sort((x, y) => y.value - x.value);
  const y0 = 800, gap = 420;
  const w = (v: number) => Math.round(BW * v / max);
  const mark = interpolate(f, [15, 33], [0, 1], {...CL, easing: Easing.out(Easing.cubic)}); // 0~15프레임(0.5초)은 정지 = 0초 프레임이 곧 완성 화면
  const x2 = M + w(bars[1].value), x1 = M + w(bars[0].value);
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <style>{FONTS}</style>
      <div style={{position: 'absolute', left: M, top: 100, fontFamily: 'BHS', fontSize: 124, color: C.w, whiteSpace: 'pre'}}>{p.head}</div>
      <div style={{position: 'absolute', left: M, top: 310, fontFamily: 'BHS', fontSize: 170, color: C.y, lineHeight: 1.18, whiteSpace: 'pre-line'}}>{p.verdict.join('\n')}</div>
      {bars.map((b, k) => (
        <div key={k} style={{position: 'absolute', left: M, top: y0 + k * gap, width: w(b.value), height: BH, background: b.col}}>
          <span style={{position: 'absolute', left: 36, top: 70, fontFamily: 'BHS', fontSize: 150, color: C.ink, whiteSpace: 'nowrap'}}>{b.label} {b.text}</span>
        </div>
      ))}
      <div style={{position: 'absolute', left: M, top: y0 - 20, width: 6, height: 2 * BH + gap - BH + 40, background: C.lg}} />
      {/* 398 위치 선: 짧은 막대 끝을 긴 막대 위로 올려 긋는다(0.5초 뒤 내려옴) */}
      <div style={{position: 'absolute', left: x2 - 4, top: y0 + (gap + BH) * (1 - mark), width: 8, height: (gap + BH) * mark, background: C.w}} />
      <div style={{position: 'absolute', left: M, top: 700, fontFamily: 'BHS', fontSize: 60, color: C.lg, whiteSpace: 'pre'}}>{p.unit} · {p.note}<span style={{color: C.y}}>{p.noteAccent}</span></div>
    </AbsoluteFill>
  );
};
