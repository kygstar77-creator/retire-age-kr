// Tally 움직임 부품 ① 장면 틀 — 제목·형광 부제·흰 보드·정확한 값 칩([자막])·말 자막·출처를 안전 구역 안에만 둔다(2026-10-03 cloud/r1-remake-1003)
// 안전 구역: 오른쪽 아래 25%×20%(x>1440·y>864, 유튜브 끝 화면·구독 버튼 자리)와 맨 아래 5%(y>1026)에는 글자·그림을 두지 않는다.
// 보드(흰 판)는 x 100~1820 · y 236~852, 말 자막은 가운데 · 아래 끝 y 1024(1줄 60px, 한 쪽 18자), 출처 y 864~886. 토큰은 parts/fm(T·F)과 같다.
// 자막 규격 근거 research/longform/caption-spec-1011.md(상위 26편 실측, 10/11 순돌이 지시). 끝 화면 구간은 capX=760으로 옮겨 오른쪽 아래 금지 구역을 비운다.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from '../parts/fm';
import {wordTimings, paginate, activeWord, pageOf, CaptionPage} from '../motion-proto/captionTiming';

export const SAFE = {W: 1920, H: 1080, left: 120, textRight: 1400, brX: 1440, brY: 864, bottom: 1026};
export const BOARD = {x: 100, y: 236, w: 1720, h: 616};

export type TallyLine = {text: string; cap?: string | null; frames: number};
export const tallyStarts = (lines: TallyLine[]) => { const out: number[] = []; let a = 0; for (const l of lines) { out.push(a); a += l.frames; } return out; };
export const tallyAt = (lines: TallyLine[], i: number | null | undefined) => (i == null || i < 0 || i >= lines.length) ? 1e9 : tallyStarts(lines)[i];
export const tallyIdx = (lines: TallyLine[], f: number) => { const st = tallyStarts(lines); let k = -1; st.forEach((a, i) => { if (f >= a) k = i; }); return k; };

// 출처는 자르지 않고 글자를 줄여 한 줄(x 120~1400)에 넣는다 — 한글 1em, 영문·숫자 0.56em로 어림
export const srcSize = (src: string) => { const u = [...('출처 ' + src)].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : 0.56), 0); return Math.max(13, Math.min(19, Math.floor((SAFE.textRight - SAFE.left) / u))); };

// 말 자막 쪽 나누기: 한 쪽 공백 뺀 18자, 5자 이하로 남는 꼬리 쪽은 앞 쪽에 붙인다(caption-spec 4장)
const CAP_MAX = 18, CAP_TAIL = 5;
const nsp = (t: string) => t.replace(/\s/g, '').length;
export const capPages = (text: string): CaptionPage[] => {
  const pages = paginate(text.split(/\s+/).filter(Boolean), CAP_MAX);
  if (pages.length > 1 && nsp(pages[pages.length - 1].text) <= CAP_TAIL) { const b = pages.pop() as CaptionPage; const a = pages.pop() as CaptionPage; pages.push({first: a.first, last: b.last, text: a.text + ' ' + b.text}); }
  return pages;
};
// 한 줄(nowrap)이 상자 maxWidth 1400 안에 들도록: 한글 1em, 그 밖 0.56em, 공백 0.3em로 어림해 60px에서 줄인다
const capSize = (t: string) => { const u = [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.3 : 0.56), 0); return Math.min(60, Math.floor(1330 / Math.max(1, u))); };

export const TallyFrame: React.FC<{title: string; sub?: string | null; source?: string | null; chapter?: string | null; lines: TallyLine[]; children?: React.ReactNode; board?: boolean; capX?: number}> =
  ({title, sub, source, chapter, lines, children, board = true, capX = 960}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 10], [0, 1], CL);
  const hl = interpolate(f, [6, 22], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const k = tallyIdx(lines, f);
  let cap: string | null = null; let capAt = 0;
  for (let i = 0; i <= k; i++) if (lines[i]?.cap) { cap = lines[i].cap as string; capAt = tallyStarts(lines)[i]; }
  const co = interpolate(f, [capAt, capAt + 8], [0, 1], CL);
  const line = k >= 0 ? lines[k] : null; const lo = line ? interpolate(f, [tallyStarts(lines)[k], tallyStarts(lines)[k] + 5], [0, 1], CL) : 0;
  let page = '';
  if (line) { const pages = capPages(line.text); const tm = wordTimings(line.text, line.frames, 0.92); page = pages[pageOf(pages, Math.max(0, activeWord(tm, f - tallyStarts(lines)[k])))]?.text ?? line.text; }
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
        <div style={{position: 'absolute', left: capX - 700, width: 1400, bottom: 56, display: 'flex', justifyContent: 'center', opacity: lo}}>
          <div style={{...F, fontWeight: 700, fontSize: capSize(page), lineHeight: 1.25, color: '#fff', background: T.ink, padding: '10px 32px', borderRadius: 12, whiteSpace: 'nowrap', maxWidth: 1400}}>{page}</div>
        </div>
      ) : null}
      {source ? <div style={{...F, fontWeight: 500, fontSize: srcSize(source), color: T.ink3, position: 'absolute', left: SAFE.left, top: 864, whiteSpace: 'nowrap'}}>출처 {source}</div> : null}
    </AbsoluteFill>
  );
};
