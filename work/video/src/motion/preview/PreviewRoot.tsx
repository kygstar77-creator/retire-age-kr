import React from 'react';
import {Composition} from 'remotion';
import {TallyFrame} from '../TallyFrame';
import {ZoomOutOpen, ZoomOutOpenProps} from '../ZoomOutOpen';
import type {RScene} from '../../R1';
import {ReverseAsk, ReverseAskProps} from '../ReverseAsk';
import {BuyDateOpen, BuyDateOpenProps} from '../BuyDateOpen';
import {WaterfallPieces, WaterfallPiecesProps} from '../WaterfallPieces';
import {AsymClimb, AsymClimbProps} from '../AsymClimb';
import {StockShot, StockShotProps} from '../StockShot';
import {StepCliff, StepCliffProps} from '../StepCliff';
import {BuybackDays, BuybackDaysProps} from '../BuybackDays';
import {Series} from 'remotion';
import {FxDates, FxDatesProps} from '../FxDates';
import {tallyStarts} from '../TallyFrame';
import {HedgeFlip, HedgeFlipProps} from '../HedgeFlip';
import {EvenLadder, EvenLadderProps} from '../EvenLadder';
import {DaysBelow, DaysBelowProps} from '../DaysBelow';
import {EqStack, EqStackProps} from '../EqStack';
import {LoanSteps, LoanStepsProps} from '../LoanSteps';
import {BalancePath, BalancePathProps} from '../BalancePath';
import {EqRow, EqRowProps} from '../EqRow';
import {CapStop, CapStopProps} from '../CapStop';
import {MeanPull, MeanPullProps} from '../MeanPull';

type P = {scene: RScene; zoom: ZoomOutOpenProps};
const OpenZoom: React.FC<P> = ({scene, zoom}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <ZoomOutOpen {...zoom} />
  </TallyFrame>
);

type P2 = {scene: RScene; rev: ReverseAskProps};
const M1Open: React.FC<P2> = ({scene, rev}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <ReverseAsk {...rev} />
  </TallyFrame>
);

type P3 = {scene: RScene; open: BuyDateOpenProps};
const G1Open: React.FC<P3> = ({scene, open}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <BuyDateOpen {...open} />
  </TallyFrame>
);

type P4 = {scene: RScene; wf: WaterfallPiecesProps};
const G1Waterfall: React.FC<P4> = ({scene, wf}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <WaterfallPieces {...wf} />
  </TallyFrame>
);

type P5 = {scene: RScene; asym: AsymClimbProps};
const G1Asym: React.FC<P5> = ({scene, asym}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <AsymClimb {...asym} />
  </TallyFrame>
);

type P6 = {shots: StockShotProps[]};
const StockReel: React.FC<P6> = ({shots}) => (
  <Series>{shots.map((sh, i) => <Series.Sequence key={i} durationInFrames={sh.dur}><StockShot {...sh} /></Series.Sequence>)}</Series>
);

type P7 = {scene: RScene; step: StepCliffProps};
const P1Step: React.FC<P7> = ({scene, step}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <StepCliff {...step} />
  </TallyFrame>
);

type P8 = {scene: RScene; buy: BuybackDaysProps};
const W2Buy: React.FC<P8> = ({scene, buy}) => (
  <TallyFrame title={scene.title} sub={scene.sub} source={scene.source} chapter={scene.chapter} lines={scene.lines}>
    <BuybackDays {...buy} />
  </TallyFrame>
);

type P9 = {s1: RScene; s2: RScene; fx: Omit<FxDatesProps, 'phase'>};
const X1Fx: React.FC<P9> = ({s1, s2, fx}) => (
  <Series>
    <Series.Sequence durationInFrames={s1.frames}>
      <TallyFrame title={s1.title} sub={s1.sub} source={s1.source} chapter={s1.chapter} lines={s1.lines}><FxDates {...fx} phase="line" /></TallyFrame>
    </Series.Sequence>
    <Series.Sequence durationInFrames={s2.frames}>
      <TallyFrame title={s2.title} sub={s2.sub} source={s2.source} chapter={s2.chapter} lines={s2.lines}><FxDates {...fx} phase="bars" /></TallyFrame>
    </Series.Sequence>
  </Series>
);

// X-1 v3 새 장면 세 개(10/17 motion) — 질문 2 HedgeFlip · 질문 1 EvenLadder · 질문 5 DaysBelow
type V3S<D> = RScene & {data: D};
type P10 = {hedge: V3S<Omit<HedgeFlipProps, 'beats'>>; even: V3S<Omit<EvenLadderProps, 'beats'>>; below: V3S<Omit<DaysBelowProps, 'beats'>>};
const v3Frame = (s: RScene, child: React.ReactNode) => <TallyFrame title={s.title} sub={s.sub} source={s.source} chapter={s.chapter} lines={s.lines}>{child}</TallyFrame>;
const X1V3: React.FC<P10> = ({hedge, even, below}) => (
  <Series>
    <Series.Sequence durationInFrames={hedge.frames}>{v3Frame(hedge, <HedgeFlip {...hedge.data} beats={tallyStarts(hedge.lines)} />)}</Series.Sequence>
    <Series.Sequence durationInFrames={even.frames}>{v3Frame(even, <EvenLadder {...even.data} beats={tallyStarts(even.lines)} />)}</Series.Sequence>
    <Series.Sequence durationInFrames={below.frames}>{v3Frame(below, <DaysBelow {...below.data} beats={tallyStarts(below.lines)} />)}</Series.Sequence>
  </Series>
);

// H-2 5장 견본 방식 장면 셋(10/18 motion) — rule LoanSteps · cash EqStack · edge LoanSteps
type P11 = {rule: V3S<Omit<LoanStepsProps, 'beats'>>; cash: V3S<Omit<EqStackProps, 'beats'>>; edge: V3S<Omit<LoanStepsProps, 'beats'>>};
const H2Eq: React.FC<P11> = ({rule, cash, edge}) => (
  <Series>
    <Series.Sequence durationInFrames={rule.frames}>{v3Frame(rule, <LoanSteps {...rule.data} beats={tallyStarts(rule.lines)} />)}</Series.Sequence>
    <Series.Sequence durationInFrames={cash.frames}>{v3Frame(cash, <EqStack {...cash.data} beats={tallyStarts(cash.lines)} />)}</Series.Sequence>
    <Series.Sequence durationInFrames={edge.frames}>{v3Frame(edge, <LoanSteps {...edge.data} beats={tallyStarts(edge.lines)} />)}</Series.Sequence>
  </Series>
);

// C-2 '28년 통장 잔액' 선 그래프(10/19 벤치마크 지시) — BalancePath · 재료 ep/C-2/motion_preview/balprops.py
type P12 = {scene: RScene; data: BalancePathProps};
const C2Balance: React.FC<P12> = ({scene, data}) => v3Frame(scene, <BalancePath {...data} />);

// T-1 2장 가로식 장면 셋(10/19 motion) — ratio·year·gap EqRow · 재료 ep/T-1/motion_preview/rowprops.py
type P13 = {ratio: V3S<Omit<EqRowProps, 'beats'>>; year: V3S<Omit<EqRowProps, 'beats'>>; gap: V3S<Omit<EqRowProps, 'beats'>>};
const T1Row: React.FC<P13> = ({ratio, year, gap}) => (
  <Series>
    {[ratio, year, gap].map((s, i) => <Series.Sequence key={i} durationInFrames={s.frames}>{v3Frame(s, <EqRow {...s.data} beats={tallyStarts(s.lines)} />)}</Series.Sequence>)}
  </Series>
);

// P-3 가로식 장면 셋(10/27 motion) — calc·rise·mix EqRow plain · 재료 ep/P-3/motion_preview/rowprops.py
type P14 = {calc: V3S<Omit<EqRowProps, 'beats'>>; rise: V3S<Omit<EqRowProps, 'beats'>>; mix: V3S<Omit<EqRowProps, 'beats'>>};
const P3Row: React.FC<P14> = ({calc, rise, mix}) => (
  <Series>
    {[calc, rise, mix].map((s, i) => <Series.Sequence key={i} durationInFrames={s.frames}>{v3Frame(s, <EqRow {...s.data} beats={tallyStarts(s.lines)} />)}</Series.Sequence>)}
  </Series>
);

// N-3 움직이는 판 둘(10/29 motion) — cap CapStop(3장 연금 상한) · mean MeanPull(7장 평균 끌려감)
type P15 = {cap: V3S<Omit<CapStopProps, 'beats'>>; mean: V3S<Omit<MeanPullProps, 'beats'>>};
const N3Motion: React.FC<P15> = ({cap, mean}) => (
  <Series>
    <Series.Sequence durationInFrames={cap.frames}>{v3Frame(cap, <CapStop {...cap.data} beats={tallyStarts(cap.lines)} />)}</Series.Sequence>
    <Series.Sequence durationInFrames={mean.frames}>{v3Frame(mean, <MeanPull {...mean.data} beats={tallyStarts(mean.lines)} />)}</Series.Sequence>
  </Series>
);

export const PreviewRoot: React.FC = () => (
  <>
  <Composition id="OpenZoom" component={OpenZoom as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P).scene.frames})} />
  <Composition id="M1Open" component={M1Open as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P2).scene.frames})} />
  <Composition id="G1Open" component={G1Open as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P3).scene.frames})} />
  <Composition id="G1Waterfall" component={G1Waterfall as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P4).scene.frames})} />
  <Composition id="G1Asym" component={G1Asym as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P5).scene.frames})} />
  <Composition id="StockReel" component={StockReel as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P6).shots.reduce((a, b) => a + b.dur, 0)})} />
  <Composition id="P1Step" component={P1Step as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P7).scene.frames})} />
  <Composition id="W2Buy" component={W2Buy as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P8).scene.frames})} />
  <Composition id="X1Fx" component={X1Fx as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P9).s1.frames + (props as unknown as P9).s2.frames})} />
  <Composition id="X1V3" component={X1V3 as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => { const q = props as unknown as P10; return {durationInFrames: q.hedge.frames + q.even.frames + q.below.frames}; }} />
  <Composition id="H2Eq" component={H2Eq as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => { const q = props as unknown as P11; return {durationInFrames: q.rule.frames + q.cash.frames + q.edge.frames}; }} />
  <Composition id="C2Balance" component={C2Balance as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P12).scene.frames})} />
  <Composition id="T1Row" component={T1Row as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => { const q = props as unknown as P13; return {durationInFrames: q.ratio.frames + q.year.frames + q.gap.frames}; }} />
  <Composition id="P3Row" component={P3Row as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => { const q = props as unknown as P14; return {durationInFrames: q.calc.frames + q.rise.frames + q.mix.frames}; }} />
  <Composition id="N3Motion" component={N3Motion as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => { const q = props as unknown as P15; return {durationInFrames: q.cap.frames + q.mean.frames}; }} />
  </>
);
