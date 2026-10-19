// 10/19 '클로드 티' 견본 전용 진입점 — 공용 Root는 다른 편 json을 전부 import해서 다른 담당이 그 json을 쓰는 중이면 번들이 깨진다(c1s_index와 같은 이유).
// 롱폼: npx remotion render src/noclaude_index.ts C2 <out.mp4> --props=<c2 형식 json> --frames=a-b
// 쇼츠: npx remotion render src/noclaude_index.ts C1S <out.mp4> --props=<c1s 형식 json>
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {C2, C2Props, c2Frames} from './C2';
import {C1S, C1SProps, c1sFrames} from './C1S';
import c2 from '../c2.json';
import r1s from '../r1s_fx.json';

const Root: React.FC = () => React.createElement(React.Fragment, null,
  React.createElement(Composition as any, {id: 'C2', component: C2, durationInFrames: c2Frames(c2 as unknown as C2Props), fps: 30, width: 1920, height: 1080,
    defaultProps: c2, calculateMetadata: ({props}: any) => ({durationInFrames: c2Frames(props as C2Props)})}),
  React.createElement(Composition as any, {id: 'C1S', component: C1S, durationInFrames: c1sFrames(r1s as unknown as C1SProps), fps: 30, width: 1080, height: 1920,
    defaultProps: r1s, calculateMetadata: ({props}: any) => ({durationInFrames: c1sFrames(props as C1SProps)})}),
);
registerRoot(Root);
