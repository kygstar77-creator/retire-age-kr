// 영상미 고칠 점 5개 미리보기(2026-10-02 motion) — 숫자는 ep/E-1/facts.txt·e1.json에서 그대로. 공개용 아님(미리보기·심사용).
import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {T, F, FONT_CSS} from './parts/fm';
import {HookNumber, Beat, beatCues, Drift, HeroNumber, PenMark, Wipe} from './parts/beats';

const SEED = 'E-2';
const ROWS: [string, string][] = [['2025Q2', '41.4%'], ['2025Q3', '46.6%'], ['2025Q4', '58.4%'], ['2026Q1', '71.5%'], ['2026Q2', '76.3%']];

const Hook: React.FC = () => (
  <AbsoluteFill style={{background: T.dbg}}>
    <HookNumber to={412.9} digits={1} prefix="+" suffix="%" label="SK하이닉스 1년 주가" color={T.rise} dark x={140} y={260} size={220} />
    <Sequence from={45}><HookNumber to={-54.7} digits={1} suffix="%" label="그 안의 최대 낙폭" color={T.dfall} dark x={140} y={580} size={220} /></Sequence>
    <div style={{...F, fontWeight: 500, fontSize: 22, color: T.dink3, position: 'absolute', left: 140, bottom: 24}}>출처 네이버 금융 일별 시세(000660) · 2025-09-29 → 2026-09-29 종가</div>
  </AbsoluteFill>
);

const Table: React.FC = () => {
  const {fps} = useVideoConfig();
  const cues = beatCues([8, 30, 52, 74, 96], 150, fps); // 문장 시작 5개 = 행 5개, 마지막 행에 초점이 온 뒤 펜(실제 편은 at(s,i))
  return (
    <AbsoluteFill style={{background: T.bg}}>
      <Drift frames={150} seed={SEED}>
        <div style={{...F, fontWeight: 700, fontSize: 52, color: T.ink, position: 'absolute', left: 160, top: 110}}>SK하이닉스 분기 영업이익률</div>
        <Beat cues={cues} n={ROWS.length}>{(_, o) => ROWS.map(([q, v], i) => (
          <div key={q} style={{position: 'absolute', left: 160, top: 230 + i * 130, width: 1100, height: 104, background: T.surface, borderRadius: 18, opacity: o(i),
            display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 48px', boxSizing: 'border-box'}}>
            <span style={{...F, fontWeight: 500, fontSize: 44, color: T.ink2}}>{q}</span>
            <span style={{...F, fontWeight: 700, fontSize: 60, color: T.ink}}>{v}</span>
          </div>))}</Beat>
        <PenMark kind="under" x={1010} y={866} w={220} cue={108} seed={SEED} />
        <PenMark kind="bracket" x={150} y={620} w={0} h={240} cue={124} seed={SEED} />
      </Drift>
      <div style={{...F, fontWeight: 500, fontSize: 22, color: T.ink3, position: 'absolute', left: 160, bottom: 24}}>출처 OpenDART 단일회사 주요계정(연결)</div>
      <Wipe seed={SEED} />
    </AbsoluteFill>
  );
};

const Hero: React.FC = () => (
  <AbsoluteFill>
    <HeroNumber to={80.4} digits={1} suffix="%" top="마이크론 영업이익률 · 2026-05-28 끝난 분기" bottom="여덟 분기 전 19.6%" source="SEC XBRL companyfacts (CIK 723125)" start={6} />
    <Wipe seed={SEED} />
  </AbsoluteFill>
);

export const MotionKit: React.FC = () => (
  <AbsoluteFill style={{background: T.bg}}>
    <style>{FONT_CSS}</style>
    <Sequence durationInFrames={90}><Hook /></Sequence>
    <Sequence from={90} durationInFrames={150}><Table /></Sequence>
    <Sequence from={240} durationInFrames={120}><Hero /></Sequence>
  </AbsoluteFill>
);
