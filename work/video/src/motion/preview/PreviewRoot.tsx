import React from 'react';
import {Composition} from 'remotion';
import {TallyFrame} from '../TallyFrame';
import {ZoomOutOpen, ZoomOutOpenProps} from '../ZoomOutOpen';
import type {RScene} from '../../R1';
import {ReverseAsk, ReverseAskProps} from '../ReverseAsk';
import {BuyDateOpen, BuyDateOpenProps} from '../BuyDateOpen';
import {WaterfallPieces, WaterfallPiecesProps} from '../WaterfallPieces';
import {AsymClimb, AsymClimbProps} from '../AsymClimb';

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
  </>
);
