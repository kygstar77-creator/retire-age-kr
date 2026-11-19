// 11/19 motion StripOver 미리보기 전용 진입점(공용 Root 안 건드림 — strip_index.ts와 같은 이유).
// 시험 재료는 이미 렌더된 H-5 장면 틀(h5.json)로 장 시작·어두운 바탕 판정만 본다. 실제 적용 편은 KOSPI-1.
// npx remotion still src/stripover_index.ts StripOverPreview <out.png> --props=<json> --frame=N
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {H5} from './H5';
import {StripOver} from './motion/StripOver';
import hh5 from './../h5.json';

const e = React.createElement;
const Preview: React.FC<any> = (q) => e(StripOver, {inner: H5 as any, p: hh5, strip: q.strip, legend: q.legend});
const total = (hh5 as any).scenes.reduce((a: number, s: any) => a + s.frames, 0);
const Root: React.FC = () => e(Composition as any, {id: 'StripOverPreview', component: Preview, durationInFrames: total, fps: 30, width: 1920, height: 1080, defaultProps: {strip: null, legend: null}});
registerRoot(Root);
