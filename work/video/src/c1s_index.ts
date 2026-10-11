// C1S 세로 쇼츠 전용 진입점(m1s_index.ts와 같은 이유 — 공용 Root는 다른 편 json을 전부 import해서 다른 담당이 그 json을 쓰는 중이면 번들이 깨진다).
// 렌더: npx remotion render src/c1s_index.ts C1S out/c1s_<편>.mp4 --props=c1s_<편>.json
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {C1S, C1SProps, c1sFrames} from './C1S';
import c1s from '../c1s.json';

const C1SRoot: React.FC = () => React.createElement(Composition as any, {
  id: 'C1S', component: C1S, durationInFrames: c1sFrames(c1s as unknown as C1SProps), fps: 30, width: 1080, height: 1920,
  defaultProps: c1s, calculateMetadata: ({props}: any) => ({durationInFrames: c1sFrames(props as C1SProps)}),
});
registerRoot(C1SRoot);
