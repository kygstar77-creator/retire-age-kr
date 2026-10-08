import React from 'react';
import {Composition} from 'remotion';
import {Weekly, WeeklyProps} from './Weekly';
import props from '../props.json';
import {Tour, TourProps, totalFrames, FPS} from './Tour';
import tour from '../tour.json';
import {A1, A1Props, a1Frames} from './A1';
import a1 from '../a1.json';
import {E1, E1Props, e1Frames} from './E1';
import e1 from '../e1.json';
import {D1, D1Props, d1Frames} from './D1';
import d1 from '../d1.json';
import {E2, E2Props, e2Frames} from './E2';
import e2 from '../e2.json';
import {N1, N1Props, n1Frames} from './N1';
import n1 from '../n1.json';
import {R1, R1Props, r1Frames} from './R1';
import r1 from '../r1.json';
import {M1, M1Props, m1Frames} from './M1';
import m1 from '../m1.json';
import {G1, G1Props, g1Frames} from './G1';
import g1 from '../g1.json';
import {C1, C1Props, c1Frames} from './C1';
import c1 from '../c1.json';
import {MotionKit} from './MotionKit';
import {ShortIntro, ShortIntroProps, introFrames} from './motion/ShortIntro';
import introE2 from '../intro_e2_interest.json';
import {ShortIntroBars, ShortIntroBarsProps, introBarsFrames} from './motion/ShortIntroBars';
import introBars from '../intro_bars_template.json';

export const Root: React.FC = () => {
  const p = props as unknown as WeeklyProps;
  const total = p.scenes.reduce((a, s) => a + s.frames, 0);
  const tp = tour as unknown as TourProps;
  const ap = a1 as unknown as A1Props;
  const ep1 = e1 as unknown as E1Props;
  const dp1 = d1 as unknown as D1Props;
  const ep2 = e2 as unknown as E2Props;
  const np1 = n1 as unknown as N1Props;
  const rp1 = r1 as unknown as R1Props;
  const mp1 = m1 as unknown as M1Props;
  const gp1 = g1 as unknown as G1Props;
  const cp1 = c1 as unknown as C1Props;
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
    <Composition id="E1" component={E1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={e1Frames(ep1)} fps={ep1.fps}
      width={1920} height={1080} defaultProps={ep1 as unknown as Record<string, unknown>} />
    <Composition id="D1" component={D1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={d1Frames(dp1)} fps={dp1.fps}
      width={1920} height={1080} defaultProps={dp1 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: d1Frames(pp as unknown as D1Props)})} />
    <Composition id="E2" component={E2 as unknown as React.FC<Record<string, unknown>>} durationInFrames={e2Frames(ep2)} fps={ep2.fps}
      width={1920} height={1080} defaultProps={ep2 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: e2Frames(pp as unknown as E2Props)})} />
    <Composition id="N1" component={N1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={n1Frames(np1)} fps={np1.fps}
      width={1920} height={1080} defaultProps={np1 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: n1Frames(pp as unknown as N1Props)})} />
    <Composition id="R1" component={R1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={r1Frames(rp1)} fps={rp1.fps}
      width={1920} height={1080} defaultProps={rp1 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: r1Frames(pp as unknown as R1Props)})} />
    <Composition id="M1" component={M1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={m1Frames(mp1)} fps={mp1.fps}
      width={1920} height={1080} defaultProps={mp1 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: m1Frames(pp as unknown as M1Props)})} />
    <Composition id="G1" component={G1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={g1Frames(gp1)} fps={gp1.fps}
      width={1920} height={1080} defaultProps={gp1 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: g1Frames(pp as unknown as G1Props)})} />
    <Composition id="C1" component={C1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={c1Frames(cp1)} fps={cp1.fps}
      width={1920} height={1080} defaultProps={cp1 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: c1Frames(pp as unknown as C1Props)})} />
    <Composition id="ShortIntro" component={ShortIntro as unknown as React.FC<Record<string, unknown>>} durationInFrames={introFrames(introE2 as ShortIntroProps)} fps={30}
      width={1080} height={1920} defaultProps={introE2 as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: introFrames(pp as unknown as ShortIntroProps)})} />
    <Composition id="ShortIntroBars" component={ShortIntroBars as unknown as React.FC<Record<string, unknown>>} durationInFrames={introBarsFrames(introBars as ShortIntroBarsProps)} fps={30}
      width={1080} height={1920} defaultProps={introBars as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: introBarsFrames(pp as unknown as ShortIntroBarsProps)})} />
    <Composition id="MotionKit" component={MotionKit} durationInFrames={360} fps={30} width={1920} height={1080} />
    </>
  );
};
