// 디자인 기준 v3 견본 전용 진입점(공용 Root를 건드리지 않음)
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {DSLong} from './DSSample';
const Root: React.FC = () => React.createElement(Composition as any, {id: 'DSLong', component: DSLong, durationInFrames: 300, fps: 30, width: 1920, height: 1080, defaultProps: {}});
registerRoot(Root);
