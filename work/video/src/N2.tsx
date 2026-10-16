// N-2 '직장인 100명을 월급 순서로 세우면, 내 월급은 몇 등?' 화면 — 재료 work/video/n2.json(ep/N-2/n2props.py가 voice.json·n2nums 값으로 만든다) · 2026-10-16 N-2 PD
// 틀은 TallyFrame(제목·형광 부제·흰 보드·정확한 값 칩·말 자막·출처) + 10/16 총괄 기준 실사 배경(bg). TallyFrame은 고치지 않고 bg만 넘긴다.
// 배경은 장 안에서도 조각(segs, 6.5초 이하)마다 다른 Pexels 클립·구간으로 바뀐다. 제목·자막 시계는 장 시작부터 이어지게 조각마다 Sequence(from=-조각 시작)로 감싼다
// (그래서 조각 영상 파일은 앞에 조각 시작만큼 첫 화면을 채워 둔다 — n2props.py --cut).
// 그림 종류: 100명 줄(사람 점 100개·주황 표시 이동·방향 화살표) · 원문 표 캡처(2024년 줄 노란 띠) · 통장→세전 카드 · 큰 숫자 카드 · 평균/한가운데 막대 · 0원 바닥/몇 배 꼭대기 · 요약 표.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL} from './parts/fm';
import {TallyFrame, TallyLine, TallyBg, tallyStarts, tallyIdx} from './motion/TallyFrame';

type NLine = TallyLine & {audio?: string | null};
type Seg = {from: number; frames: number; bg: TallyBg};
export type NScene = {key: string; kind: string; title: string; sub?: string | null; source?: string | null; board: boolean; data: any; lines: NLine[]; frames: number; segs: Seg[]};
export type N2Props = {fps: number; scenes: NScene[]; missing: number};
export const n2Frames = (p: N2Props) => p.scenes.reduce((a, s) => a + s.frames, 0);

const fade = (f: number, at: number, d = 10) => interpolate(f, [at, at + d], [0, 1], CL);
const ease = (f: number, a: number, d: number) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: Easing.inOut(Easing.cubic)});
const SHW = '0 20px 60px rgba(0,0,0,0.45)';
const useBeat = (s: NScene) => {
  const f = useCurrentFrame(); const st = tallyStarts(s.lines);
  const k = Math.max(0, tallyIdx(s.lines, f));
  const at = (i: number) => st[Math.max(0, Math.min(s.lines.length - 1, i))] ?? 0;
  return {f, k, at};
};

// ───────── 큰 숫자 카드(보드 없이 사진 위) ─────────
const BigCard: React.FC<{big: string; small?: string; at: number; f: number; x?: number; y?: number}> = ({big, small, at, f, x = 120, y = 330}) => {
  const o = fade(f, at, 9);
  return (
    <div style={{position: 'absolute', left: x, top: y + (1 - o) * 14, opacity: o, background: '#fff', borderRadius: 28, padding: '28px 48px 32px', boxShadow: SHW}}>
      <div style={{...F, fontWeight: 700, fontSize: 176, lineHeight: 1, color: T.accent, letterSpacing: -4, whiteSpace: 'nowrap'}}>{big}</div>
      {small ? <div style={{...F, fontWeight: 700, fontSize: 42, color: T.ink2, marginTop: 16, whiteSpace: 'nowrap'}}>{small}</div> : null}
    </div>
  );
};

// ───────── 100명 줄 ─────────
// 왼쪽 끝 = 1등(가장 많이), 오른쪽 끝 = 100등(가장 적게). 사람 점 100개, 표시한 등수에 주황 사람.
const QX0 = 190, QX1 = 1730, QY = 560;
const qx = (rank: number) => QX0 + (QX1 - QX0) * (rank - 1) / 99;
const Person: React.FC<{x: number; y: number; c: string; s?: number}> = ({x, y, c, s = 1}) => (
  <div style={{position: 'absolute', left: x - 6 * s, top: y - 34 * s}}>
    <div style={{width: 12 * s, height: 12 * s, borderRadius: 99, background: c, margin: '0 auto'}} />
    <div style={{width: 12 * s, height: 26 * s, borderRadius: `${6 * s}px ${6 * s}px 2px 2px`, background: c, marginTop: 3 * s}} />
  </div>
);
const Queue: React.FC<{rank: number | null; f: number; showEnds?: number; arrowAt?: number; label?: string | null; money?: string | null; labelAt?: number; mid?: number | null; between?: number[] | null; betweenAt?: number}> =
  ({rank, f, showEnds = 0, arrowAt = 1e9, label, money, labelAt = 0, mid = null, between = null, betweenAt = 1e9}) => {
  const people = Array.from({length: 100}, (_, i) => i + 1);
  const r = rank == null ? null : Math.round(rank);
  const eo = fade(f, showEnds, 10), ao = fade(f, arrowAt, 10), lo = fade(f, labelAt, 10), bo = fade(f, betweenAt, 10);
  return (
    <>
      {people.map((p) => <Person key={p} x={qx(p)} y={QY} c={r != null && p === r ? T.accent : (r != null && p < r ? T.ink : '#c9ced6')} s={p === r ? 1.9 : 1} />)}
      <div style={{position: 'absolute', left: QX0 - 70, top: QY + 26, width: 220, opacity: eo, ...F, fontWeight: 700, fontSize: 30, color: T.ink, textAlign: 'left'}}>1등 · 가장 많이</div>
      <div style={{position: 'absolute', left: QX1 - 190, top: QY + 26, width: 260, opacity: eo, ...F, fontWeight: 700, fontSize: 30, color: T.ink3, textAlign: 'right'}}>100등 · 가장 적게</div>
      <div style={{position: 'absolute', left: 720, top: QY + 90, width: 480, opacity: ao, display: 'flex', alignItems: 'center', gap: 14, justifyContent: 'center'}}>
        <div style={{...F, fontWeight: 700, fontSize: 44, color: T.accent}}>←</div>
        <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink2}}>앞으로 갈수록 월급이 많다</div>
      </div>
      {mid != null ? <div style={{position: 'absolute', left: qx(mid) - 2, top: QY - 120, width: 4, height: 150, background: T.ink3, opacity: 0.6}} /> : null}
      {mid != null ? <div style={{position: 'absolute', left: qx(mid) - 90, top: QY + 30, width: 180, textAlign: 'center', ...F, fontWeight: 700, fontSize: 26, color: T.ink3}}>50등 · 한가운데</div> : null}
      {between ? <div style={{position: 'absolute', left: qx(between[1]), top: QY + 12, width: qx(between[0]) - qx(between[1]), height: 10, borderRadius: 5, background: T.accent, opacity: bo * 0.5}} /> : null}
      {between ? <div style={{position: 'absolute', left: (qx(between[0]) + qx(between[1])) / 2 - 220, top: QY + 90, width: 440, textAlign: 'center', opacity: bo, ...F, fontWeight: 700, fontSize: 30, color: T.ink2}}>그 사이 월급 = 그 사이 등수</div> : null}
      {r != null && label ? (
        <div style={{position: 'absolute', left: Math.min(1360, Math.max(140, qx(r) - 150)), top: 300 + (1 - lo) * 10, width: 300, opacity: lo, textAlign: 'center'}}>
          <div style={{...F, fontWeight: 700, fontSize: 88, color: T.accent, lineHeight: 1}}>{label}</div>
          {money ? <div style={{...F, fontWeight: 700, fontSize: 32, color: T.ink, marginTop: 6, whiteSpace: 'nowrap'}}>{money}</div> : null}
        </div>
      ) : null}
    </>
  );
};

const Queue0: React.FC<{s: NScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data;
  const qo = fade(f, at(1), 10);
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, opacity: 1 - qo}}>
        <div style={{position: 'absolute', left: 560, top: 330, width: 800, textAlign: 'center'}}>
          <div style={{...F, fontWeight: 700, fontSize: 200, lineHeight: 1, color: T.accent, letterSpacing: -4}}>{d.big}</div>
          <div style={{...F, fontWeight: 700, fontSize: 40, color: T.ink2, marginTop: 20}}>{d.bigSub}</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, opacity: qo}}>
        <Queue rank={null} f={f} showEnds={at(1)} arrowAt={at(2)} />
      </div>
    </>
  );
};

const QueueScene: React.FC<{s: NScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data;
  const m = ease(f, 4, 26);
  const rank = d.from + (d.to - d.from) * m;
  return <Queue rank={rank} f={f} showEnds={0} label={`${d.to}등`} money={d.money} labelAt={14} mid={d.mid ?? null} between={d.between ?? null} betweenAt={d.betweenAt != null ? at(d.betweenAt) : 1e9} />;
};

// ───────── 원문 표 + 통장→세전 ─────────
const Doc: React.FC<{s: NScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data;
  const co = fade(f, at(d.convAt), 10);
  const W = 1500, H = 375, X = 210, Y = 330;
  return (
    <>
      <div style={{position: 'absolute', left: X, top: Y, width: W, height: H, opacity: 1 - co}}>
        <Img src={staticFile(d.img)} style={{width: W, height: H}} />
        <div style={{position: 'absolute', left: 0, top: H * d.row[0], width: W * fade(f, 20, 24), height: H * (d.row[1] - d.row[0]), background: 'rgba(255,212,59,0.35)'}} />
      </div>
      <div style={{position: 'absolute', left: X, top: Y + H + 20, display: 'flex', gap: 18, opacity: (1 - co)}}>
        {d.tags.map((t: string, i: number) => (
          <div key={i} style={{opacity: fade(f, at(2) + i * 45, 8), background: T.ink, color: '#fff', borderRadius: 12, padding: '8px 20px', ...F, fontWeight: 700, fontSize: 30, whiteSpace: 'nowrap'}}>{t}</div>
        ))}
      </div>
      <div style={{position: 'absolute', left: 160, top: 330, width: 1600, opacity: co, display: 'flex', flexDirection: 'column', gap: 34}}>
        {d.conv.map((c: string[], i: number) => {
          const o = fade(f, at(d.convAt + 1 + i), 10);
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 30, opacity: o, transform: `translateY(${(1 - o) * 10}px)`}}>
              <div style={{width: 520, background: '#eef0f3', borderRadius: 18, padding: '22px 30px', ...F, fontWeight: 700, fontSize: 48, color: T.ink, whiteSpace: 'nowrap'}}>{c[0]}</div>
              <div style={{...F, fontWeight: 700, fontSize: 60, color: T.accent}}>→</div>
              <div style={{width: 560, background: T.ink, borderRadius: 18, padding: '22px 30px', ...F, fontWeight: 700, fontSize: 48, color: '#fff', whiteSpace: 'nowrap'}}>{c[1]}</div>
              <div style={{...F, fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{c[2]}</div>
            </div>
          );
        })}
      </div>
    </>
  );
};

const BigScene: React.FC<{s: NScene}> = ({s}) => {
  const {f, k, at} = useBeat(s);
  const items = s.data.items as {at: number; big: string; small?: string}[];
  const cur = [...items].reverse().find((it) => k >= it.at) ?? items[0];
  return <BigCard key={cur.at} big={cur.big} small={cur.small} at={at(cur.at)} f={f} />;
};

// ───────── 평균이 높은 까닭 ─────────
const Avg: React.FC<{s: NScene}> = ({s}) => {
  const {f, k, at} = useBeat(s); const d = s.data;
  if (k < d.barsAt) return <BigCard big={d.big} small={d.bigSub} at={0} f={f} />;
  const o = fade(f, at(d.barsAt), 10); const g = ease(f, at(d.barsAt) + 4, 24);
  const max = 420, BW = 1100, X = 520;
  const bar = (label: string, v: number, c: string, y: number, sub: string) => (
    <div style={{position: 'absolute', left: 160, top: y, width: 1600}}>
      <div style={{position: 'absolute', left: 0, top: 18, width: 340, ...F, fontWeight: 700, fontSize: 38, color: T.ink, whiteSpace: 'nowrap'}}>{label}</div>
      <div style={{position: 'absolute', left: X - 160, top: 0, width: BW * v / max * g, height: 86, background: c, borderRadius: 12}} />
      <div style={{position: 'absolute', left: X - 160 + BW * v / max * g + 20, top: 14, ...F, fontWeight: 700, fontSize: 48, color: c === T.accent ? T.accent : T.ink, whiteSpace: 'nowrap', opacity: g}}>{v}만원</div>
      <div style={{position: 'absolute', left: 0, top: 62, width: 340, ...F, fontWeight: 500, fontSize: 24, color: T.ink3, whiteSpace: 'nowrap'}}>{sub}</div>
    </div>
  );
  const fo = fade(f, at(d.floorAt), 10), to = fade(f, at(d.topAt), 10);
  return (
    <div style={{position: 'absolute', left: 100, top: 300, width: 1720, height: 552, background: 'rgba(255,255,255,0.96)', borderRadius: 24, boxShadow: SHW, opacity: o}}>
      <div style={{position: 'absolute', left: -100, top: -300}}>
        {bar('평균', d.avg, T.accent, 360, '모두 더해서 사람 수로 나눔')}
        {bar('한가운데 50등', d.mid, T.ink, 500, '100명 중 딱 가운데 사람')}
        <div style={{position: 'absolute', left: 260, top: 650, opacity: fo, display: 'flex', gap: 22, alignItems: 'center'}}>
          <div style={{background: '#eef0f3', borderRadius: 14, padding: '12px 24px', ...F, fontWeight: 700, fontSize: 34, color: T.ink, whiteSpace: 'nowrap'}}>적게 받는 쪽: 0원 밑으로는 못 내려감</div>
          <div style={{opacity: to, background: T.ink, borderRadius: 14, padding: '12px 24px', ...F, fontWeight: 700, fontSize: 34, color: '#fff', whiteSpace: 'nowrap'}}>많이 받는 쪽: 한가운데의 몇 배까지</div>
        </div>
      </div>
    </div>
  );
};

// ───────── 요약 표 ─────────
const Summary: React.FC<{s: NScene}> = ({s}) => {
  const {f, at} = useBeat(s); const d = s.data;
  const rows = d.rows as string[][]; const rh = 72, X = 300, Y = 300, Wd = 1320;
  const no = fade(f, at(d.noteAt), 10);
  return (
    <>
      {rows.map((r, i) => {
        const o = fade(f, 6 + i * 8, 8); const hi = i === d.hi;
        return (
          <div key={i} style={{position: 'absolute', left: X, top: Y + i * (rh + 8), width: Wd, height: rh, opacity: o, borderRadius: 14, background: hi ? T.accent : (i % 2 ? '#f2f3f5' : '#fff'),
            border: hi ? 'none' : `2px solid ${T.line}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 32px', boxSizing: 'border-box'}}>
            <div style={{...F, fontWeight: 700, fontSize: 36, color: hi ? '#fff' : T.ink, whiteSpace: 'nowrap'}}>{r[0]}</div>
            <div style={{...F, fontWeight: 700, fontSize: 40, color: hi ? '#fff' : T.accent, whiteSpace: 'nowrap'}}>{r[1]}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', left: X, top: Y + rows.length * (rh + 8) + 6, opacity: no, ...F, fontWeight: 700, fontSize: 30, color: T.ink2, whiteSpace: 'nowrap'}}>{d.note}</div>
    </>
  );
};

const Body: React.FC<{s: NScene}> = ({s}) => {
  switch (s.kind) {
    case 'queue0': return <Queue0 s={s} />;
    case 'queue': return <QueueScene s={s} />;
    case 'doc': return <Doc s={s} />;
    case 'big': return <BigScene s={s} />;
    case 'avg': return <Avg s={s} />;
    case 'summary': return <Summary s={s} />;
    default: return null;
  }
};

const SceneView: React.FC<{s: NScene}> = ({s}) => {
  const st = tallyStarts(s.lines);
  return (
    <AbsoluteFill>
      {s.segs.map((g, i) => (
        <Sequence key={i} from={g.from} durationInFrames={g.frames}>
          <Sequence from={-g.from}>
            <TallyFrame title={s.title} sub={s.sub} source={s.source} lines={s.lines} board={s.board} bg={g.bg}>
              <Body s={s} />
            </TallyFrame>
          </Sequence>
        </Sequence>
      ))}
      {s.lines.map((l, i) => l.audio ? <Sequence key={'a' + i} from={st[i]} durationInFrames={l.frames}><Audio src={staticFile(l.audio)} /></Sequence> : null)}
    </AbsoluteFill>
  );
};

export const N2: React.FC<N2Props> = (p) => {
  let from = 0;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {p.scenes.map((s, i) => { const el = <Sequence key={i} from={from} durationInFrames={s.frames}><SceneView s={s} /></Sequence>; from += s.frames; return el; })}
    </AbsoluteFill>
  );
};
