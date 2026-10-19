// '사람 편집자' 부품 — 10/19 사장님 "내용 영상도 클로드 티를 벗어야 해" · "휙 휙 소리 별로, 챕터 바뀔 때 수페TV처럼 띠링"
// 근거·금지 목록: work/research/visual/no-claude-look-1019.md (클로드 티 목록) · design-spec-1016.md 11절
//   · 바탕: 구겨진 종이 결(public/human/paper_crumple*.jpg — work/video/public/human/paper.py로 자체 합성, 외부 그림 0)
//   · 강조: 손으로 그린 동그라미(fm HandCircle)·밑줄(HandUnderline)·체크(HandCheck) — 둥근 상자·알약 꼬리표·연주황 띠 대신
//   · 소리: 장면 바뀔 때 '휙'은 기본 끔. 장(챕터)이 바뀔 때만 '띠링'(public/human/chime.wav, chime.py 자체 합성 두 음 올라감 0.72초),
//     말이 쉬는 틈(앞 줄 꼬리 무음)에 넣는다 — 장 카드가 12프레임 먼저 빈 채로 뜨고 그때 울린다(전체 길이·말 시각은 그대로).
//   · 음악: 말 밑 잔잔한 음(sample1017/pad.wav 자체 합성)을 말소리 파형으로 덕킹(말 0.07 ↔ 쉼 0.2, 붙기 6·풀기 12프레임) — OpenMontage 코드 복사 없음(AGPL), 우리가 새로 짬.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, staticFile, interpolate, useCurrentFrame} from 'remotion';
import {useAudioData} from '@remotion/media-utils';
import {T, CL} from './fm';

export const PAPER = 'human/paper_crumple.jpg';
export const PAPER_V = 'human/paper_crumple_v.jpg';
export const PaperBg: React.FC<{vertical?: boolean}> = ({vertical}) => (
  <AbsoluteFill style={{background: '#f3f1ec'}}><Img src={staticFile(vertical ? PAPER_V : PAPER)} style={{width: '100%', height: '100%'}} /></AbsoluteFill>
);

// 손 밑줄 — 살짝 휘고 끝이 올라가는 한 획(펜 굵기 6~9). p = 그려진 정도 0~1
export const HandUnderline: React.FC<{x: number; y: number; w: number; p: number; color?: string; seed?: number; stroke?: number}> = ({x, y, w, p, color = T.accent, seed = 1, stroke = 8}) => {
  const pts: string[] = [];
  for (let i = 0; i <= 24; i++) { const t = i / 24; const yy = y + Math.sin(t * 3.1 + seed) * 3 - t * t * 7 + (seed % 2 ? 2 : -1) * Math.sin(t * 9 + seed) * 1.2; pts.push(`${(x + t * w).toFixed(1)},${yy.toFixed(1)}`); }
  return <svg style={{position: 'absolute', left: 0, top: 0, width: 1, height: 1, overflow: 'visible', pointerEvents: 'none'}}>
    <polyline points={pts.join(' ')} fill="none" stroke={color} strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} /></svg>;
};
// 손 체크 표시(수페 A#35 초록 체크처럼) — 두 획
export const HandCheck: React.FC<{x: number; y: number; s: number; p: number; color?: string}> = ({x, y, s, p, color = T.accent}) => (
  <svg style={{position: 'absolute', left: 0, top: 0, width: 1, height: 1, overflow: 'visible', pointerEvents: 'none'}}>
    <polyline points={`${x},${y + s * 0.45} ${x + s * 0.36},${y + s * 0.82} ${x + s},${y - s * 0.1}`} fill="none" stroke={color} strokeWidth={s * 0.13} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} /></svg>
);
// 손으로 그은 세로 나눔 선(짝 비교 가운데)
export const HandDivider: React.FC<{x: number; y: number; h: number; p: number; color?: string}> = ({x, y, h, p, color = T.ink3}) => {
  const pts: string[] = []; for (let i = 0; i <= 16; i++) { const t = i / 16; pts.push(`${(x + Math.sin(t * 4.2) * 4).toFixed(1)},${(y + t * h).toFixed(1)}`); }
  return <svg style={{position: 'absolute', left: 0, top: 0, width: 1, height: 1, overflow: 'visible'}}><polyline points={pts.join(' ')} fill="none" stroke={color} strokeWidth={4} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} /></svg>;
};

// ───────── 소리 ─────────
export type SfxScene = {kind: string; data?: any; frames: number; lines: {audio: string | null; frames: number}[]};
export type Sfx = {at: number; src: string; vol: number};
export const SFX = {chime: 'human/chime.wav', pen: 'sample1017/pen.wav', ding: 'sample1017/ding.wav', whoosh: 'sample1017/whoosh.wav'};
export const CH_PRE = 12;   // 장 카드를 12프레임(0.4초) 먼저 띄우고 그때 띠링 — 앞 줄 꼬리 무음(실측 13프레임 안팎) 안
// 장 카드인가: 'ask' 장면 중 n이 '질문 ①'·'② …'처럼 장 번호를 가진 것(맨 앞 '오늘의 물음'·끝 사이트 안내는 장이 아님)
export const isChapter = (s: SfxScene) => s.kind === 'ask' && !!s.data && typeof s.data.n === 'string' && /[①-⑳]|^질문|^\d+장/.test(s.data.n);
// 기본값(10/19): 휙 없음 · 답 열기에 펜 소리만(작게) · 장 카드에 띠링. opts.whoosh=true면 옛 방식(판↔실사 바뀔 때 휙)
export const sfxPlan = (sc: SfxScene[], i: number, opts: {whoosh?: boolean; ding?: boolean; pen?: boolean; liveKinds?: Set<string>} = {}): Sfx[] => {
  const s = sc[i]; const o: Sfx[] = [];
  if (opts.whoosh && opts.liveKinds && i > 0 && opts.liveKinds.has(s.kind) !== opts.liveKinds.has(sc[i - 1].kind)) o.push({at: 0, src: SFX.whoosh, vol: 0.25});
  // 10/19 사장님 '동그라미 칠 때 땡 하는 소리도 너무 거슬려, 조사 안 하고 넣은 건 전부 하지 마' — 답 열기·동그라미 소리 기본 끔(opts.pen=true일 때만). 근거 조사 전엔 장 띠링만.
  if (s.data && s.data.rv != null) { if (opts.ding) o.push({at: s.data.rv, src: SFX.ding, vol: 0.3}); if (opts.pen) o.push({at: s.data.rv + 10, src: SFX.pen, vol: 0.3}); }
  return o;
};
export const SfxTrack: React.FC<{list: Sfx[]}> = ({list}) => <>{list.map((x, j) => <Sequence key={j} from={x.at} durationInFrames={45}><Audio src={staticFile(x.src)} volume={x.vol} /></Sequence>)}</>;
export const Chime: React.FC<{at: number; vol?: number}> = ({at, vol = 0.5}) => <Sequence from={Math.max(0, at)} durationInFrames={24}><Audio src={staticFile(SFX.chime)} volume={vol} /></Sequence>;

// 말소리 파형으로 덕킹하는 배경 음 — lines: 영상 전체 프레임 기준 {at, audio}. 파형에서 실제 말 구간(최대값 6% 넘는 첫·끝 표본)을 찾는다.
type VLine = {at: number; audio: string; frames?: number};
// 렌더 탭마다 한 번 잰 말 구간(파형) — 지금 프레임 근처 줄만 읽는다(한 편 160줄을 다 읽으면 첫 프레임이 33초 넘게 걸린다)
const SPAN = new Map<string, [number, number]>();
const spanOf = (d: any, at: number, fps: number): [number, number] => {
  const ch: Float32Array = d.channelWaveforms[0]; let mx = 0; for (let i = 0; i < ch.length; i += 4) mx = Math.max(mx, Math.abs(ch[i]));
  const th = mx * 0.06; let a = 0, b = ch.length - 1; while (a < ch.length && Math.abs(ch[a]) < th) a++; while (b > a && Math.abs(ch[b]) < th) b--;
  return [at + (a / d.sampleRate) * fps, at + (b / d.sampleRate) * fps];
};
const Probe: React.FC<{l: VLine; fps: number}> = ({l, fps}) => {
  const d = useAudioData(staticFile(l.audio)); const k = l.audio + '@' + l.at;
  if (d && !SPAN.has(k)) SPAN.set(k, spanOf(d, l.at, fps));
  return null;
};
export const DuckedMusic: React.FC<{src?: string; lines: VLine[]; fps?: number; low?: number; high?: number; attack?: number; release?: number}> = ({src = 'sample1017/pad.wav', lines, fps = 30, low = 0.07, high = 0.2, attack = 6, release = 12}) => {
  const f = useCurrentFrame();
  const len = (l: VLine) => l.frames ?? 300;
  const near = lines.filter((l) => f >= l.at - 40 && f <= l.at + len(l) + 40);
  const vol = (g: number) => {
    let d = 1e9;
    for (const l of lines) {
      if (g < l.at - 60 || g > l.at + len(l) + 60) continue;
      const sp = SPAN.get(l.audio + '@' + l.at) ?? [l.at + 5, l.at + len(l) - 12];
      if (g >= sp[0] - attack && g <= sp[1] + release) return low; d = Math.min(d, Math.abs(g - (sp[1] + release)), Math.abs(sp[0] - attack - g));
    }
    return low + (high - low) * interpolate(d, [0, 10], [0, 1], CL);
  };
  return <>{near.map((l) => <Probe key={l.audio + '@' + l.at} l={l} fps={fps} />)}<Audio src={staticFile(src)} loop volume={vol} /></>;
};
