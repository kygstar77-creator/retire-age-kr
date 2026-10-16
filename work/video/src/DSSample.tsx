// 10/16 디자인 기준 v3 견본(롱폼) — TallyFrame bg(실사 배경) 모양 확인용. 숫자는 g1s_why props(편집 통과 값) 그대로.
// 렌더: npx remotion still src/ds_index.ts DSLong out.png --props=<json> --frame=N
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {T, F} from './parts/fm';
import {TallyFrame, TallyBg} from './motion/TallyFrame';
import {TallyBars} from './motion/TallyBars';

export type DSProps = {mode: 'board' | 'big'; bg: TallyBg; title: string; sub: string; source: string; lines: {text: string; frames: number}[]; bars: [string, number, string][]; big: string; bigSub: string};
export const DSLong: React.FC<DSProps> = (p) => (
  <AbsoluteFill>
    <TallyFrame title={p.title} sub={p.sub} source={p.source} lines={p.lines} board={p.mode === 'board'} bg={p.bg}>
      {p.mode === 'board' ? <TallyBars bars={p.bars.map(([label, value, valueText]) => ({label, value, valueText, start: 0, color: value < 0 ? T.fall : T.accent}))} x={260} y={330} w={1400} h={460} max={8} min={-8} dir="h" labelSize={36} valueSize={52} /> :
        <div style={{position: 'absolute', left: 120, top: 300, background: '#fff', borderRadius: 28, padding: '28px 44px 32px', boxShadow: '0 20px 60px rgba(0,0,0,0.45)'}}>
          <div style={{...F, fontWeight: 800, fontSize: 168, lineHeight: 1, color: T.accent, letterSpacing: -4}}>{p.big}</div>
          <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, marginTop: 14}}>{p.bigSub}</div>
        </div>}
    </TallyFrame>
  </AbsoluteFill>
);
