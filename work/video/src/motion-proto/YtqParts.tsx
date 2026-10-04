// cloud yt-quality 시제품 2개(2026-10-03) — 새 편에서 골라 쓰는 opt-in 부품. 기존 편(A1~R1)은 안 바뀐다.
// ① KaraokeCaption: fm.Caption 자리에 그대로 넣는 단어 강조 자막. 지금 말하는 어절만 밝고 크게, 아직 안 읽은 어절은 흐리게.
//    색은 fm.T 토큰만(강조는 밝기·크기로 — 주황은 손그림·파이어맵 숫자 전용 규칙 유지). 시간은 captionTiming.ts.
// ② SayExact: 말한 반올림 숫자를 크게, 사실표 정확값을 아래 꼬리표로(numberSpeech.ts). 대본 숫자를 줄여도 화면 정확도는 그대로.
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, VScene, lineStarts} from '../parts/fm';
import {wordTimings, paginate, activeWord, pageOf} from './captionTiming';
import type {SpokenNumber} from './numberSpeech';

export const KaraokeCaption: React.FC<{s: VScene; dark?: boolean; maxChars?: number; speechFrac?: number; bottom?: number; size?: number}> =
  ({s, dark, maxChars = 28, speechFrac = 0.92, bottom = 64, size = 40}) => {
    const f = useCurrentFrame(); const st = lineStarts(s); let idx = -1; st.forEach((a, i) => { if (f >= a) idx = i; });
    if (idx < 0) return null;
    const line = s.lines[idx]; const local = f - st[idx];
    const tm = wordTimings(line.text, line.frames, speechFrac);
    const pages = paginate(tm.map((t) => t.word), maxChars);
    const k = activeWord(tm, local); const pg = pages[pageOf(pages, Math.max(0, k))];
    if (!pg) return null;
    const o = interpolate(local, [0, 5], [0, 1], CL);
    return (
      <div style={{position: 'absolute', bottom, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
        <div style={{...F, fontWeight: 700, fontSize: size, lineHeight: 1.35, background: dark ? 'rgba(27,28,33,0.92)' : T.ink,
          padding: '16px 34px', borderRadius: 16, maxWidth: 1480, textAlign: 'center', wordBreak: 'keep-all'}}>
          {tm.slice(pg.first, pg.last + 1).map((t, j) => {
            const i = pg.first + j; const on = i === k; const said = k >= 0 && i < k;
            const pop = on ? interpolate(local, [t.from, t.from + 4], [1, 1.06], {...CL, easing: Easing.out(Easing.quad)}) : 1;
            return <span key={i} style={{display: 'inline-block', marginRight: '0.28em', color: dark ? T.dink : '#fff',
              opacity: on || said ? 1 : 0.45, transform: `scale(${pop})`, transformOrigin: 'center bottom'}}>{t.word}</span>;
          })}
        </div>
      </div>
    );
  };

export const SayExact: React.FC<{n: SpokenNumber; label: string; source?: string; start?: number; x?: number; y?: number; size?: number; color?: string; dark?: boolean}> =
  ({n, label, source, start = 0, x = 140, y = 300, size = 180, color = T.ink, dark}) => {
    const f = useCurrentFrame();
    const o = interpolate(f, [start, start + 10], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
    const tag = interpolate(f, [start + 14, start + 26], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
    return (
      <div style={{position: 'absolute', left: x, top: y}}>
        <div style={{...F, fontWeight: 700, fontSize: size * 0.24, color: dark ? T.dink3 : T.ink3, opacity: o}}>{label}</div>
        <div style={{...F, fontWeight: 700, fontSize: size, color: dark ? T.dink : color, lineHeight: 1.05, opacity: o, transform: `translateY(${(1 - o) * 16}px)`}}>{n.say}</div>
        {n.rounded ? <div style={{...F, fontWeight: 500, fontSize: Math.max(26, size * 0.2), color: dark ? T.dink3 : T.ink2, marginTop: 14, opacity: tag,
          background: dark ? T.dsurface : T.surface, border: `2px solid ${dark ? T.dsurface : T.line}`, borderRadius: 12, padding: '6px 18px', display: 'inline-block'}}>
          정확히 {n.show}{source ? <span style={{color: dark ? T.dink3 : T.ink3}}> · {source}</span> : null}</div> : null}
      </div>
    );
  };
