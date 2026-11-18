// 11/18 motion 상시 장 띠·순위 범례 미리보기 전용 진입점(공용 Root는 다른 편 json을 전부 import — noclaude_index와 같은 이유).
// npx remotion still src/strip_index.ts StripPreview <out.png> --props='{"mode":"strip"}' --frame=60
import React from 'react';
import {registerRoot, Composition, AbsoluteFill} from 'remotion';
import {TallyFrame} from './motion/TallyFrame';
import {ChapterStrip} from './motion/ChapterStrip';
import {RankLegend} from './motion/RankLegend';
import {T, F} from './parts/fm';

// 숫자: ep/KOSPI-1/calc2_out.txt(무리 첫날 16줄)·script.md 3장만
const CH = [{n: 1, name: '올해 코스피'}, {n: 2, name: '서킷브레이커와 사이드카'}, {n: 3, name: '지난 31년, 크게 빠진 날 그 뒤'}, {n: 4, name: '전날 값을 되찾기까지'},
  {n: 5, name: '크게 빠진 해엔 크게 오른 날도'}, {n: 6, name: '1천만원을 넣었다면'}, {n: 7, name: '함정'}, {n: 8, name: '정리'}];
const ITEMS = [{label: '2001-09-12', value: '−12.02%'}, {label: '2024-08-05', value: '−8.77%'}, {label: '2020-03-19', value: '−8.39%'},
  {label: '2002-06-26', value: '−7.15%'}, {label: '2007-08-16', value: '−6.93%'}, {label: '2000-01-05', value: '−6.87%'}];
const e = React.createElement;
const Preview: React.FC<{mode: string}> = ({mode}) => {
  const legend = mode === 'legend';
  return e(AbsoluteFill, null,
    e(TallyFrame, {title: legend ? '묶음 첫날, 크게 빠진 순' : '하루 5% 넘게 빠진 날', source: 'ECOS 코스피 일별 종가(1995~2026-11-13), 파이어맵 계산', board: false,
      lines: [{text: legend ? '코로나가 번지던 때도 하루 8% 이상 빠졌고요.' : '하루 5% 넘게 빠진 날은 대개 몰려서 왔어요.', frames: 300}]},
      legend
        ? e('div', {style: {position: 'absolute', left: 180, width: 1200, top: 330, textAlign: 'center'}},
            e('div', {style: {...F, fontWeight: 700, fontSize: 64, color: T.ink2}}, '2020-03-19'),
            e('div', {style: {...F, fontWeight: 700, fontSize: 220, color: T.accent, letterSpacing: -6, lineHeight: 1.05}}, '−8.39%'))
        : e('div', {style: {position: 'absolute', left: 180, width: 1560, top: 300, textAlign: 'center'}},
            e('div', {style: {...F, fontWeight: 700, fontSize: 60, color: T.ink2}}, '60거래일 안은 한 묶음으로'),
            e('div', {style: {...F, fontWeight: 700, fontSize: 240, color: T.ink, letterSpacing: -6, lineHeight: 1.05}}, '16묶음'))),
    e(ChapterStrip, {chapters: CH, starts: [-999, -998, 0], total: 8, topic: '코스피 크게 빠진 날, 그 뒤'}),
    legend ? e(RankLegend, {items: ITEMS, title: '첫날 하락률 순', on: [[0, 0], [20, 2]]}) : null,
  );
};
const Root: React.FC = () => e(Composition as any, {id: 'StripPreview', component: Preview, durationInFrames: 120, fps: 30, width: 1920, height: 1080, defaultProps: {mode: 'strip'}});
registerRoot(Root);
