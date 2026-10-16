// 10/17 롱폼 화면 기준 견본 전용 진입점(공용 Root를 건드리지 않음)
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {LongStd, LONGSTD_FRAMES} from './LongStdSample';
const Root: React.FC = () => React.createElement(Composition as any, {id: 'LongStd', component: LongStd, durationInFrames: LONGSTD_FRAMES, fps: 30, width: 1920, height: 1080, defaultProps: {}});
registerRoot(Root);
