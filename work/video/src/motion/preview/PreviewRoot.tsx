import React from 'react';
import {Composition} from 'remotion';
import {TallyFrame} from '../TallyFrame';
import {ZoomOutOpen, ZoomOutOpenProps} from '../ZoomOutOpen';
import type {RScene} from '../../R1';
import {ReverseAsk, ReverseAskProps} from '../ReverseAsk';

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

export const PreviewRoot: React.FC = () => (
  <>
  <Composition id="OpenZoom" component={OpenZoom as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P).scene.frames})} />
  <Composition id="M1Open" component={M1Open as unknown as React.FC<Record<string, unknown>>} durationInFrames={300} fps={30} width={1920} height={1080}
    defaultProps={{} as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as P2).scene.frames})} />
  </>
);
