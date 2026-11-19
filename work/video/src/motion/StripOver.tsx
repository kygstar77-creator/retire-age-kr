// 상시 장 띠·순위 범례를 편 컴포넌트 위에 얹는 겉싸개(2026-11-19 motion).
// 왜: KOSPI-1은 JT1.tsx 계열 틀을 쓸 예정인데 그 틀은 JT-1·H-5가 같이 쓴다(H-5 렌더 중) → 틀은 안 건드리고 겉에서 얹는다.
// 쓰는 법(Root.tsx): const K1Strip = (p) => <StripOver inner={JT1} p={p} strip={S.strip} legend={S.legend} />;
//   S = ep/KOSPI-1/kospi1_strip.json(strip·legend). 편 json에 strip·legend로 넣고 p.strip·p.legend를 넘겨도 된다.
// 장 시작: kind 'ask' 장면 중 data.n 이 'N장'인 것의 시작 프레임(여는 말·기초 카드에는 띠 없음).
// 장면 종류별 띠 모양(11/19 H-5 틀로 스틸 3장 눈 확인 뒤 정함):
//   ask(장 카드, 검은 바탕)·broll·live → 흰 글자+그림자 · pic(검은 테 안 종이 판, 판 윗변 y≈38) → 한 줄 작게(20px, 주제 줄 없음, top 2) 흰 글자
//   그 밖(종이 판 TallyFrame) → 진한 글자. 표 kinds 는 strip.style 로 바꿀 수 있다.
// 범례: legend.chapter 장 안에서만, legend.cues 글자로 시작하는 말 줄이 나올 때 그 번호로 점이 옮겨 간다.
//   legend.off_kinds(기본 table·grid·rows·pic·ask) 장면에서는 끈다 — pic 판은 오른쪽까지 그래프가 차 있어 겹친다(11/19 스틸 확인).
// 띠를 켤 때 TallyFrame chapter 칸은 props 쪽에서 비운다(같은 글자 두 번 금지) — 이 겉싸개는 장면 data를 바꾸지 않는다.
import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {ChapterStrip, StripChapter} from './ChapterStrip';
import {RankLegend, LegendItem} from './RankLegend';

type Line = {text: string; frames: number};
type Scene = {kind: string; frames: number; data: any; lines: Line[]};
type Look = 'light' | 'dark' | 'thin';
export type StripSpec = {topic?: string | null; side?: 'right' | 'left'; chapters: StripChapter[]; style?: Record<string, Look>};
export type LegendSpec = {chapter: number; title?: string | null; items: LegendItem[]; cues: {start: string; i: number}[]; off_kinds?: string[]};

const LOOK: Record<string, Look> = {ask: 'dark', broll: 'dark', live: 'dark', pic: 'thin'};
const chapNo = (s: Scene): number | null => {
  if (s.kind !== 'ask') return null;
  const m = /^(\d+)\s*장/.exec(String(s.data?.n ?? ''));
  return m ? Number(m[1]) : null;
};

export const stripPlan = (scenes: Scene[], strip?: StripSpec | null, legend?: LegendSpec | null) => {
  const look = {...LOOK, ...(strip?.style ?? {})};
  const starts: number[] = []; const runs: [number, number, Look][] = []; const leg: [number, number, boolean][] = [];
  const on: [number, number][] = [];
  let acc = 0; let ch = 0;
  const off = new Set(legend?.off_kinds ?? ['table', 'grid', 'rows', 'pic', 'ask']);
  const push = <T,>(arr: [number, number, T][], a: number, n: number, v: T) => {
    const last = arr[arr.length - 1];
    if (last && last[0] + last[1] === a && last[2] === v) last[1] += n; else arr.push([a, n, v]);
  };
  for (const s of scenes) {
    const n = chapNo(s);
    if (n) { ch = n; starts[n - 1] = acc; }
    const lk: Look = look[s.kind] ?? 'light';
    push(runs, acc, s.frames, lk);
    if (legend && ch === legend.chapter && n === null && !off.has(s.kind)) push(leg, acc, s.frames, lk !== 'light');
    if (legend && ch === legend.chapter) {
      let la = acc;
      for (const l of s.lines ?? []) {
        const c = legend.cues.find((q) => l.text.trim().startsWith(q.start));
        if (c) on.push([la, c.i]);
        la += l.frames;
      }
    }
    acc += s.frames;
  }
  return {starts, runs, leg, on};
};

export const StripOver: React.FC<{inner: React.FC<any>; p: any; strip?: StripSpec | null; legend?: LegendSpec | null}> = ({inner: Inner, p, strip, legend}) => {
  const plan = stripPlan(p.scenes as Scene[], strip, legend);
  const starts = (strip?.chapters ?? []).map((_, i) => plan.starts[i] ?? 1e9);
  return (
    <AbsoluteFill>
      <Inner {...p} />
      {/* Sequence 안 프레임은 0부터라 starts를 구간 시작만큼 당긴다 */}
      {strip ? plan.runs.map(([a, n, lk], i) => (
        <Sequence key={`st-${i}`} from={a} durationInFrames={n} layout="none">
          <ChapterStrip chapters={strip.chapters} starts={starts.map((x) => x - a)} total={strip.chapters.length} dark={lk !== 'light'}
            side={strip.side ?? 'right'} topic={lk === 'thin' ? null : strip.topic ?? null} top={lk === 'thin' ? 2 : 10} fs={lk === 'thin' ? 20 : 24} />
        </Sequence>
      )) : null}
      {legend ? plan.leg.map(([a, n, dk], i) => (
        <Sequence key={`lg-${i}`} from={a} durationInFrames={n} layout="none">
          <RankLegend items={legend.items} title={legend.title ?? null} on={plan.on.map(([f, k]) => [f - a, k] as [number, number])} dark={dk} />
        </Sequence>
      )) : null}
    </AbsoluteFill>
  );
};
