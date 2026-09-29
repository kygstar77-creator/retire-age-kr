import React from 'react';
import {Composition} from 'remotion';
import {Weekly, WeeklyProps} from './Weekly';
import props from '../props.json';
import {Tour, TourProps, totalFrames, FPS} from './Tour';
import tour from '../tour.json';
import {A1, A1Props, a1Frames} from './A1';
import a1 from '../a1.json';

export const Root: React.FC = () => {
  const p = props as unknown as WeeklyProps;
  const total = p.scenes.reduce((a, s) => a + s.frames, 0);
  const tp = tour as unknown as TourProps;
  const ap = a1 as unknown as A1Props;
  return (
    <>
    <Composition
      id="Weekly"
      component={Weekly as unknown as React.FC<Record<string, unknown>>}
      durationInFrames={total}
      fps={p.fps}
      width={1920}
      height={1080}
      defaultProps={p as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => {
        const q = pp as unknown as WeeklyProps;
        return {durationInFrames: q.scenes.reduce((a, s) => a + s.frames, 0)};
      }}
    />
    <Composition id="Tour" component={Tour as unknown as React.FC<Record<string, unknown>>} durationInFrames={totalFrames(tp)} fps={FPS}
      width={1920} height={1080} defaultProps={tp as unknown as Record<string, unknown>} />
    <Composition id="A1" component={A1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={a1Frames(ap)} fps={ap.fps}
      width={1920} height={1080} defaultProps={ap as unknown as Record<string, unknown>} />
    </>
  );
};
