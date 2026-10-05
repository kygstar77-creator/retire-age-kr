// Tally 움직임 부품 ① 장면 틀 — 제목·형광 부제·흰 보드·정확한 값 칩([자막])·말 자막·출처를 안전 구역 안에만 둔다(2026-10-03 cloud/r1-remake-1003)
// 안전 구역: 오른쪽 아래 25%×20%(x>1440·y>864, 유튜브 끝 화면·구독 버튼 자리)와 맨 아래 5%(y>1026)에는 글자·그림을 두지 않는다.
// 보드(흰 판)는 x 100~1820 · y 236~852, 말 자막은 x 120~1400 · 아래 끝 y 984, 출처는 y 996~1018. 토큰은 parts/fm(T·F)과 같다.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from '../parts/fm';

export const SAFE = {W: 1920, H: 1080, left: 120, textRight: 1400, brX: 1440, brY: 864, bottom: 1026};
export const BOARD = {x: 100, y: 236, w: 1720, h: 616};

export type TallyLine = {text: string; cap?: string | null; frames: number};
export const tallyStarts = (lines: TallyLine[]) => { const out: number[] = []; let a = 0; for (const l of lines) { out.push(a); a += l.frames; } return out; };
export const tallyAt = (lines: TallyLine[], i: number | null | undefined) => (i == null || i < 0 || i >= lines.length) ? 1e9 : tallyStarts(lines)[i];
export const tallyIdx = (lines: TallyLine[], f: number) => { const st = tallyStarts(lines); let k = -1; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };

// 출처는 자르지 않고 글자를 줄여 한 줄(x 120~1400)에 넣는다 — 한글 1em, 영문·숫자 0.56em로 어림
export const srcSize = (src: string) => { const u = [...('출처 ' + src)].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : 0.56), 0); return Math.max(13, Math.min(19, Math.floor((SAFE.textRight - SAFE.left) / u))); };

export const TallyFrame: React.FC<{title: string; sub?: string | null; source?: string | null; chapter?: string | null; lines: TallyLine[]; children?: React.ReactNode; board?: boolean}> =
  ({title, sub, source, chapter, lines, children, board = true}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 10], [0, 1], CL);
  const hl = interpolate(f, [6, 22], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const k = tallyIdx(lines, f);
  let cap: string | null = null; let capAt = 0;
  for (let i = 0; i <= k; i++) if (lines[i]?.cap) { cap = lines[i].cap as string; capAt = tallyStarts(lines)[i]; }
  const co = interpolate(f, [capAt, capAt + 8], [0, 1], CL);
  const line = k >= 0 ? lines[k] : null; const lo = line ? interpolate(f, [tallyStarts(lines)[k], tallyStarts(lines)[k] + 5], [0, 1], CL) : 0;
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: SAFE.left, top: 40, width: 1500, opacity: o}}>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 18}}>
          {chapter ? <div style={{...F, fontWeight: 700, fontSize: 30, color: '#fff', background: T.accent, borderRadius: 10, padding: '2px 14px'}}>{chapter}</div> : null}
          <div style={{...F, fontWeight: 700, fontSize: 60, color: T.ink, lineHeight: 1.15, letterSpacing: -1, whiteSpace: 'nowrap'}}>{title}</div>
        </div>
        {sub ? (
          <div style={{position: 'relative', display: 'inline-block', marginTop: 12}}>
            <div style={{position: 'absolute', left: -6, top: 4, bottom: 2, width: `calc(${hl * 100}% + 12px)`, background: T.soft, borderRadius: 6}} />
            <div style={{...F, position: 'relative', fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{sub}</div>
          </div>
        ) : null}
      </div>
      <div style={{position: 'absolute', right: 110, top: 54, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={26} /><span style={{...F, fontWeight: 700, fontSize: 28, color: T.ink2}}>파이어맵</span>
      </div>
      {board ? <div style={{position: 'absolute', left: BOARD.x, top: BOARD.y, width: BOARD.w, height: BOARD.h, background: '#fff', border: `2px solid ${T.line}`, borderRadius: 24, opacity: o}} /> : null}
      {children}
      {cap ? (
        <div style={{position: 'absolute', left: 130, top: 252, maxWidth: 1660, opacity: co, transform: `translateY(${(1 - co) * -8}px)`,
          background: T.ink, borderRadius: 10, padding: '7px 16px', display: 'flex', gap: 12, alignItems: 'baseline'}}>
          <span style={{...F, fontWeight: 700, fontSize: 20, color: T.daccent, whiteSpace: 'nowrap'}}>{/\d/.test(cap) ? '정확한 값' : '참고'}</span>
          <span style={{...F, fontWeight: 700, fontSize: 24, color: '#fff', lineHeight: 1.3, wordBreak: 'keep-all'}}>{cap}</span>
        </div>
      ) : null}
      {line ? (
        <div style={{position: 'absolute', left: SAFE.left, bottom: 1080 - 984, maxWidth: SAFE.textRight - SAFE.left, opacity: lo}}>
          <div style={{...F, fontWeight: 700, fontSize: 38, lineHeight: 1.32, color: '#fff', background: T.ink, padding: '12px 28px', borderRadius: 16, wordBreak: 'keep-all'}}>{line.text}</div>
        </div>
      ) : null}
      {source ? <div style={{...F, fontWeight: 500, fontSize: srcSize(source), color: T.ink3, position: 'absolute', left: SAFE.left, top: 996, whiteSpace: 'nowrap'}}>출처 {source}</div> : null}
    </AbsoluteFill>
  );
};
