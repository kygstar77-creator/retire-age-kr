// C2P(쇼츠 틀 c2person) 전용 진입점 — c1s_index.ts와 같은 이유(공용 Root는 다른 편 json을 전부 import).
// 렌더: npx remotion render src/c2p_index.ts C2P out/<편>.mp4 --props=<편>.json
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {C2P, C2PProps, c2pFrames} from './C2P';
import c2p from '../c2s_jungwoo.json';

const C2PRoot: React.FC = () => React.createElement(Composition as any, {
  id: 'C2P', component: C2P, durationInFrames: c2pFrames(c2p as unknown as C2PProps), fps: 30, width: 1080, height: 1920,
  defaultProps: c2p, calculateMetadata: ({props}: any) => ({durationInFrames: c2pFrames(props as C2PProps)}),
});
registerRoot(C2PRoot);
