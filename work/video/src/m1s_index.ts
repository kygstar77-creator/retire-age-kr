// M1S 세로 쇼츠 전용 진입점 — 공용 Root는 다른 편 props(json)를 전부 import해서, 다른 담당이 그 json을 다시 쓰는 중이면 번들이 깨진다(10/10 c1.json 빈 파일).
// 렌더: npx remotion render src/m1s_index.ts M1S out/m1s_<편>.mp4 --props=m1s_<편>.json
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {M1S, M1SProps, m1sFrames} from './M1S';
import m1s from '../m1s.json';

const M1SRoot: React.FC = () => React.createElement(Composition as any, {
  id: 'M1S', component: M1S, durationInFrames: m1sFrames(m1s as unknown as M1SProps), fps: 30, width: 1080, height: 1920,
  defaultProps: m1s, calculateMetadata: ({props}: any) => ({durationInFrames: m1sFrames(props as M1SProps)}),
});
registerRoot(M1SRoot);
