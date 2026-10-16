// 10/17 롱폼 화면 기준 견본 — 판(큰 제목·아이콘)↔꽉 찬 실사(TallyBroll)↔표를 번갈아 56초.
// 판끼리 이어 붙이면 화면 전체 컷으로 안 잡힌다(배경이 같아 ffmpeg scene 0.3 아래) — 판이 이어진 구간 합이 20초를 넘으면 사이에 실사를 끼운다. bgcheck 롱폼 관문 통과 확인용(올리지 않음).
// 숫자는 g1s_why props(편집 통과 값) 그대로. 실사는 P-1에 쓴 Pexels 영상(credits: research/longform/ep/P-1/stock/credits.json).
// 렌더: npx remotion render src/longstd_index.ts LongStd out/longstd_sample.mp4
import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {T, F} from './parts/fm';
import {TallyFrame, TallyLine} from './motion/TallyFrame';
import {TallyBroll} from './motion/TallyBroll';
import {TallyBars} from './motion/TallyBars';

const L = (text: string, sec: number): TallyLine => ({text, frames: Math.round(sec * 30)});
const BIG: React.FC<{v: string; s: string; c?: string}> = ({v, s, c = T.accent}) => (
  <div style={{position: 'absolute', left: 100, width: 1720, top: 330, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
    <div style={{...F, fontWeight: 800, fontSize: 200, lineHeight: 1, color: c, letterSpacing: -6}}>{v}</div>
    <div style={{...F, fontWeight: 700, fontSize: 44, color: T.ink2, marginTop: 24}}>{s}</div>
  </div>
);
const scenes: {sec: number; el: React.ReactNode}[] = [
  {sec: 12, el: <TallyFrame title="금값은 올랐는데" art={{kind: 'icon', icon: 'Coins', license: 'lucide ISC'}} source="금 선물 GC=F(야후) · 한국은행 ECOS" lines={[L('국제 금값은 1년 동안 올랐어요', 6), L('달러로 보면 6.65% 올랐습니다', 6)]}>
    <BIG v="+6.65%" s="달러로 본 금값 · 지난 1년" c={T.rise} /></TallyFrame>},
  {sec: 6, el: <TallyBroll src="stock/7593893.mp4" license="Pexels 7593893 무료(Pavel Danilyuk)" say="내 계좌는 왜 다를까" lines={[L('그런데 내 계좌를 열어 보면 이야기가 달라요', 6)]} />},
  {sec: 14, el: <TallyFrame title="세 조각으로 나누면" art={{kind: 'icon', icon: 'ChartColumn', license: 'lucide ISC'}} source="KRX 금시장 종가 · 2025-10-02 → 2026-10-02" lines={[L('달러 값, 환율, 웃돈 세 조각으로 나눠 봅니다', 7), L('환율과 웃돈이 금값 오른 몫을 다 먹었어요', 7)]}>
    <TallyBars bars={[['달러 금값', 6.65, '+6.65%'], ['환율', -3.38, '−3.38%'], ['웃돈', -7.26, '−7.26%']].map(([label, value, valueText]) => ({label: label as string, value: Math.abs(value as number), valueText: valueText as string, start: 0, color: (value as number) < 0 ? T.fall : T.rise}))}
      x={260} y={330} w={1400} h={460} max={8} min={0} dir="h" labelSize={40} valueSize={60} /></TallyFrame>},
  {sec: 6, el: <TallyBroll src="stock/18835800.mp4" license="Pexels 18835800 무료(indra projects)" side="right" say="계산은 한 번만" lines={[L('직접 한 번 계산해 볼게요', 6)]} />},
  {sec: 10, el: <TallyFrame title="내 금 1년 계산표" art={{kind: 'icon', icon: 'Calculator', license: 'lucide ISC'}} source="g1s_why 계산 · 편집 통과 값" lines={[L('세 조각을 곱해 보면 내 금은 4.43% 내렸어요', 10)]}>
    <div style={{position: 'absolute', left: 360, top: 320, width: 1200, ...F}}>
      {[['달러 금값', '+6.65%'], ['환율', '−3.38%'], ['웃돈', '−7.26%'], ['내 금', '−4.43%']].map(([a, b], i) => (
        <div key={i} style={{display: 'flex', justifyContent: 'space-between', padding: '14px 24px', borderBottom: `2px solid ${T.line}`, fontSize: 56, fontWeight: 700, color: i === 3 ? T.accent : T.ink}}><span>{a}</span><span>{b}</span></div>))}
    </div></TallyFrame>},
  {sec: 8, el: <TallyFrame title="내 금은 −4.43%" art={{kind: 'icon', icon: 'TrendingDown', license: 'lucide ISC', color: T.fall}} source="g1s_why 계산 · 편집 통과 값" lines={[L('금값이 올라도 내 금은 내릴 수 있어요', 4), L('그래서 살 때 웃돈부터 봐야 합니다', 4)]}>
    <BIG v="−4.43%" s="작년에 산 금 · 1년" c={T.fall} /></TallyFrame>},
];
export const LongStd: React.FC = () => {
  let a = 0;
  return <AbsoluteFill style={{background: T.bg}}>{scenes.map((s, i) => { const from = a; a += s.sec * 30; return <Sequence key={i} from={from} durationInFrames={s.sec * 30}>{s.el}</Sequence>; })}</AbsoluteFill>;
};
export const LONGSTD_FRAMES = scenes.reduce((x, s) => x + s.sec * 30, 0);
