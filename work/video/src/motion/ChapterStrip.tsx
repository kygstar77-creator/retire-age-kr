// 상시 장 띠 — 영상 내내 오른쪽 위에 '지금 몇 장, 무슨 장'을 작게 둔다(2026-11-18 motion).
// 근거: registry B-57(경쟁 롱폼 8편 중 5편 상시 장·위치 표시 — 일개미 왼쪽 위 장 띠·돈되는집 오른쪽 위 띠·퇴근길 오른쪽 위 탭 등).
// 금지 목록 지킴: 알약·둥근 칸·테두리 상자·진행 막대 없음. 종이 위 글자 + 손 밑줄 한 줄. 실사(bg) 위에선 흰 글자+그림자.
// 쓰는 법: 편 컴포넌트 맨 위(모든 장면 위)에 <ChapterStrip chapters={p.strip} at={장 시작 프레임 배열} dark={지금 장면이 실사인가} />
//   chapters: [{n: 1, name: '올해 코스피'}, ...] · starts: 각 장이 시작하는 전체 프레임(0번 장 = 여는 말은 띠 없음)
// 바꾼 장 첫 18프레임은 이름이 왼쪽에서 써지듯 열리고 밑줄이 다시 그어진다(장 카드+띠링과 같은 박자).
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS} from '../parts/fm';
import {HandUnderline} from '../parts/human';

export type StripChapter = {n: number; name: string};
const SH = '0 2px 6px rgba(0,0,0,0.75)';
export const ChapterStrip: React.FC<{chapters: StripChapter[]; starts: number[]; total?: number; dark?: boolean; side?: 'right' | 'left'; topic?: string | null; top?: number; fs?: number}> =
  ({chapters, starts, total, dark = false, side = 'right', topic = null, top = 10, fs = 24}) => {
  const f = useCurrentFrame();
  let k = -1; starts.forEach((a, i) => { if (f >= a) k = i; });
  if (k < 0) return null;
  const ch = chapters[k]; const a = starts[k];
  const reveal = interpolate(f, [a, a + 18], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const line = interpolate(f, [a + 8, a + 26], [0, 1], CL);
  const n = total ?? chapters.length;
  const ink = dark ? '#ffffff' : T.ink2;
  const w = Math.round([...ch.name].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 24 : /\s/.test(c) ? 7 : 14), 0));
  return (
    <div style={{position: 'absolute', top, [side]: 120, display: 'flex', flexDirection: 'column', alignItems: side === 'right' ? 'flex-end' : 'flex-start'}}>
      <style>{FONT_CSS}</style>
      {topic ? <div style={{...F, fontWeight: 500, fontSize: 18, color: dark ? '#e8eaee' : T.ink3, textShadow: dark ? SH : undefined, marginBottom: 2}}>{topic}</div> : null}
      <div style={{display: 'flex', alignItems: 'baseline', gap: 10, whiteSpace: 'nowrap', clipPath: `inset(-10px ${(1 - reveal) * 100}% -24px -10px)`}}>
        <span style={{...F, fontWeight: 700, fontSize: fs, color: dark ? T.daccent : T.accent, textShadow: dark ? SH : undefined}}>{ch.n}장</span>
        <span style={{...F, position: 'relative', fontWeight: 700, fontSize: fs, color: ink, textShadow: dark ? SH : undefined}}>{ch.name}
          <HandUnderline x={0} y={fs + 6} w={Math.round(w * fs / 24)} p={line} stroke={4} seed={k + 3} color={dark ? T.daccent : T.accent} /></span>
        <span style={{...F, fontWeight: 500, fontSize: Math.round(fs * 0.75), color: dark ? '#e8eaee' : T.ink3, textShadow: dark ? SH : undefined}}>{ch.n}/{n}</span>
      </div>
    </div>
  );
};
