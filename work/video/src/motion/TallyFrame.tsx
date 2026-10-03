// Tally 움직임 부품 ① 장면 틀 — 제목·정확한 값 칩([자막])·말 자막·출처를 안전 구역 안에만 둔다(2026-10-03 cloud/r1-remake-1003)
// 안전 구역: 오른쪽 아래 25%×20%(x>1440·y>864, 유튜브 끝 화면·구독 버튼 자리)와 맨 아래 5%(y>1026)에는 글자를 두지 않는다.
// 글자는 전부 x 120~1400 안에서 왼쪽 정렬, 아래 끝은 y 1022 위. 토큰은 parts/fm(T·F)과 같다.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from '../parts/fm';

export const SAFE = {W: 1920, H: 1080, left: 120, textRight: 1400, brX: 1440, brY: 864, bottom: 1026};

export type TallyLine = {text: string; cap?: string | null; frames: number};
export const tallyStarts = (lines: TallyLine[]) => { const out: number[] = []; let a = 0; for (const l of lines) { out.push(a); a += l.frames; } return out; };
// i번째 문장이 시작하는 프레임(없으면 아주 늦게 = 안 나옴)
export const tallyAt = (lines: TallyLine[], i: number | null | undefined) => (i == null || i < 0 || i >= lines.length) ? 1e9 : tallyStarts(lines)[i];
export const tallyIdx = (lines: TallyLine[], f: number) => { const st = tallyStarts(lines); let k = -1; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };

// 출처는 자르지 않고 글자를 줄여 한 줄(x 120~1400)에 넣는다 — 한글 1em, 영문·숫자 0.56em로 어림
export const srcSize = (src: string) => { const u = [...('출처 ' + src)].reduce((a, c) => a + (/[\u3131-\uD79D]/.test(c) ? 1 : 0.56), 0); return Math.max(13, Math.min(19, Math.floor((SAFE.textRight - SAFE.left) / u))); };

export const TallyFrame: React.FC<{title: string; sub?: string | null; source?: string | null; chapter?: string | null; lines: TallyLine[]; children?: React.ReactNode; dark?: boolean}> =
  ({title, sub, source, chapter, lines, children, dark}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 10], [0, 1], CL);
  const k = tallyIdx(lines, f);
  // 정확한 값 칩: 지금 문장까지 나온 [자막] 중 가장 최근 것(장면 안에서 유지)
  let cap: string | null = null; let capAt = 0;
  for (let i = 0; i <= k; i++) if (lines[i]?.cap) { cap = lines[i].cap as string; capAt = tallyStarts(lines)[i]; }
  const co = interpolate(f, [capAt, capAt + 8], [0, 1], CL);
  const line = k >= 0 ? lines[k] : null; const lo = line ? interpolate(f, [tallyStarts(lines)[k], tallyStarts(lines)[k] + 5], [0, 1], CL) : 0;
  const bg = dark ? T.dbg : T.bg; const ink = dark ? T.dink : T.ink;
  return (
    <AbsoluteFill style={{background: bg}}>
      <style>{FONT_CSS}</style>
      <div style={{position: 'absolute', left: SAFE.left, top: 56, width: SAFE.textRight - SAFE.left, opacity: o}}>
        {chapter ? <div style={{...F, fontWeight: 700, fontSize: 26, color: T.accent, marginBottom: 6}}>{chapter}</div> : null}
        <div style={{...F, fontWeight: 700, fontSize: 58, color: ink, lineHeight: 1.15, wordBreak: 'keep-all'}}>{title}</div>
        {sub ? <div style={{...F, fontWeight: 500, fontSize: 28, color: dark ? T.dink3 : T.ink3, marginTop: 8, wordBreak: 'keep-all'}}>{sub}</div> : null}
      </div>
      <div style={{position: 'absolute', right: 110, top: 70, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={26} /><span style={{...F, fontWeight: 700, fontSize: 28, color: dark ? T.dink3 : T.ink2}}>파이어맵</span>
      </div>
      {children}
      {cap ? (
        <div style={{position: 'absolute', left: SAFE.left, top: 268, maxWidth: SAFE.textRight - SAFE.left, opacity: co,
          background: dark ? T.dsurface : '#fff', border: `3px solid ${T.accent}`, borderRadius: 14, padding: '10px 20px', display: 'flex', gap: 14, alignItems: 'baseline'}}>
          <span style={{...F, fontWeight: 700, fontSize: 22, color: T.accent, whiteSpace: 'nowrap'}}>{/\d/.test(cap) ? '정확한 값' : '참고'}</span>
          <span style={{...F, fontWeight: 700, fontSize: 28, color: ink, wordBreak: 'keep-all', lineHeight: 1.3}}>{cap}</span>
        </div>
      ) : null}
      {line ? (
        <div style={{position: 'absolute', left: SAFE.left, bottom: 1080 - 984, maxWidth: SAFE.textRight - SAFE.left, opacity: lo}}>
          <div style={{...F, fontWeight: 700, fontSize: 38, lineHeight: 1.32, color: '#fff', background: dark ? 'rgba(242,243,245,0.12)' : T.ink,
            padding: '12px 28px', borderRadius: 16, wordBreak: 'keep-all'}}>{line.text}</div>
        </div>
      ) : null}
      {source ? <div style={{...F, fontWeight: 500, fontSize: srcSize(source), color: dark ? T.dink3 : T.ink3, position: 'absolute', left: SAFE.left,
        top: 996, whiteSpace: 'nowrap'}}>출처 {source}</div> : null}
    </AbsoluteFill>
  );
};
