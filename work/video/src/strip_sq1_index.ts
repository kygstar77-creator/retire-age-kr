// 11/22 motion SQ-1 상시 장 띠(오른쪽) 미리보기 전용 진입점 — strip_index.ts(KOSPI-1, 오른쪽)와 같은 틀. 장 이름은 ep/SQ-1/sq1_strip.json(script.md '## [n.]' 그대로). 숫자 없음.
// npx remotion still src/strip_sq1_index.ts StripSQ1 <out.png> (오른쪽 — 왼쪽은 채널 꼬리표와 겹침) --frame=60 --public-dir=<작은 public>
import React from 'react';
import {registerRoot, Composition, AbsoluteFill} from 'remotion';
import {TallyFrame} from './motion/TallyFrame';
import {ChapterStrip} from './motion/ChapterStrip';
import J from '../../research/longform/ep/SQ-1/sq1_strip.json';
const e = React.createElement;
const Preview: React.FC = () => e(AbsoluteFill, null,
  e(TallyFrame, {title: '섞는 비율별 지난 15년과 5년', source: '야후 파이낸스 수정 종가, 파이어맵 계산', board: false,
    lines: [{text: '그럼 한쪽만 살지, 둘을 섞을지.', frames: 300}]}),
  e(ChapterStrip, {chapters: (J as any).strip.chapters, starts: [-999, -998, 0], total: 8, topic: (J as any).strip.topic}));
const Root: React.FC = () => e(Composition as any, {id: 'StripSQ1', component: Preview, durationInFrames: 120, fps: 30, width: 1920, height: 1080});
registerRoot(Root);
