// R1만 따로 번들하는 진입점(클라우드처럼 Weekly·Tour 원본이 없는 곳에서도 렌더되게). PC는 원래 src/index.ts(Root.tsx)를 그대로 써도 된다.
//   npx remotion render src/motion/TallyRoot.tsx R1 out/r1.mp4 --props=r1.json  → 720p 미리보기는 ffmpeg -vf scale=1280:720
//   (--scale=0.6667은 높이 720.036이라 렌더가 거부되고, 2/3 축소 감싸개 컴포지션은 Sequence 배치가 어긋나 버림)
import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {R1, R1Props, r1Frames, R1Thumb} from '../R1';
import r1 from '../../r1.json';

const TallyRoot: React.FC = () => {
  const rp = r1 as unknown as R1Props;
  return (
    <>
    <Composition id="R1" component={R1 as unknown as React.FC<Record<string, unknown>>} durationInFrames={r1Frames(rp)} fps={rp.fps}
      width={1920} height={1080} defaultProps={rp as unknown as Record<string, unknown>}
      calculateMetadata={({props: pp}) => ({durationInFrames: r1Frames(pp as unknown as R1Props)})} />
    <Composition id="R1Thumb" component={R1Thumb as unknown as React.FC<Record<string, unknown>>} durationInFrames={1} fps={30} width={1280} height={720}
      defaultProps={{net: [['SCHD', '1억 1,599만', '+15.99%'], ['S&P500', '1억 1,023만', '+10.23%'], ['금', '1억 337만', '+3.37%'], ['예금', '1억 218만', '+2.18%']]}} />
    </>
  );
};
registerRoot(TallyRoot);
