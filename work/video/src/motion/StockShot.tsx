// 실사 장 머리(StockShot) — 장이 바뀔 때 2.5~4초 '주제를 보여 주는 실사 장면' + 장 물음(2026-10-12 motion, 사장님 10/11 "다른 애들도 다 장면 넣고 있구만").
// 재료: 상업 이용 허락된 무료 스톡만(Pexels, work/pexelsvid.py가 ep/<편>/stock/credits.json에 출처 기록 → 설명란). 뉴스 사진·남의 영상 캡처 금지(블러해도).
// 정직성: 숫자는 props(chip)로만, facts.txt 원문 그대로. 실사는 '분위기'일 뿐 — 실제 인물·기관처럼 읽히는 글자(이름표·'○○공단')는 얹지 않는다.
//   얼굴·상표·간판·번호판이 보이면 blur 칸으로 가린다. 알아볼 수 있는 사람을 나쁘게 그리지 않는다(Pexels 라이선스).
// 반복 방지: seed로 어두운 쪽(왼/오), 밀려 들어오는 방향, 글자 등장 방향, 색 입힘(잉크/남색)이 편마다 바뀐다.
import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, random, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS} from '../parts/fm';

export type Blur = {x: number; y: number; w: number; h: number};
export type StockShotProps = {
  seed: string;
  src: string;          // public 아래 경로(예 'stock/26753905.mp4')
  from?: number;        // 원본에서 잘라 낼 앞 프레임(30fps 기준, trimBefore)
  chapter: string;      // '4장'
  title: string;        // 대본 장 제목 그대로
  chip?: string;        // facts 원문 짧은 줄(없으면 안 보임)
  chipAt?: number;      // chip 나오는 프레임
  dur: number;          // 이 장면 길이(프레임) — 끝 10프레임은 어두워지며 다음 판으로
  blur?: Blur[];        // 화면 1920x1080 좌표(원본이 1366이어도 cover로 늘린 뒤 기준, 밀어 들어가기와 같이 움직임)
  side?: 'left' | 'right'; // 글자 쪽. 한 편 안에서는 번갈아(레드팀 10/12 '4장 중 3장 왼쪽') — 없으면 seed
};

const out = Easing.out(Easing.cubic);

export const StockShot: React.FC<StockShotProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + p.src + k);
  const left = p.side ? p.side === 'left' : r('side') < 0.5;                 // 글자·어둠이 놓이는 쪽
  const navy = r('tint') < 0.5;                 // 색 입힘
  const dx = (r('dx') - 0.5) * 60, dy = (r('dy') - 0.5) * 30;
  const fromBelow = r('enter') < 0.5;

  // 카메라: 끝까지 멈추지 않는 밀어 들어가기(선형 — 끝에서 서지 않게)
  const s = interpolate(f, [0, p.dur], [1.06, 1.16], CL);
  const tx = interpolate(f, [0, p.dur], [0, dx], CL), ty = interpolate(f, [0, p.dur], [0, dy], CL);
  const enter = interpolate(f, [0, 8], [0, 1], {...CL, easing: out});            // 앞 판에서 밝아짐
  const leave = interpolate(f, [p.dur - 10, p.dur], [0, 1], CL);                 // 다음 판 앞 어두워짐
  const gT = interpolate(f, [6, 26], [0, 1], {...CL, easing: out});
  const gC = interpolate(f, [p.chipAt ?? 40, (p.chipAt ?? 40) + 16], [0, 1], {...CL, easing: out});
  const gBar = interpolate(f, [2, 22], [0, 1], {...CL, easing: out});
  const ink = navy ? '16,24,48' : '16,17,20';

  return (
    <AbsoluteFill style={{background: T.dbg, overflow: 'hidden'}}>
      <style>{FONT_CSS}</style>
      <AbsoluteFill style={{transform: `translate(${tx}px,${ty}px) scale(${s})`, filter: `saturate(0.82) contrast(1.04) brightness(${0.55 + 0.45 * enter})`}}>
        <OffthreadVideo src={staticFile(p.src)} trimBefore={p.from ?? 0} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        {(p.blur ?? []).map((b, i) => (
          <div key={i} style={{position: 'absolute', left: b.x, top: b.y, width: b.w, height: b.h, borderRadius: 24, backdropFilter: 'blur(28px)', WebkitBackdropFilter: 'blur(28px)'}} />
        ))}
      </AbsoluteFill>
      {/* 글자 쪽만 어둡게(사진의 절반은 살린다) */}
      <AbsoluteFill style={{background: `linear-gradient(${left ? 90 : 270}deg, rgba(${ink},0.86) 0%, rgba(${ink},0.62) 34%, rgba(${ink},0) 66%)`}} />
      <AbsoluteFill style={{background: `linear-gradient(0deg, rgba(${ink},0.55) 0%, rgba(${ink},0) 30%)`}} />

      <div style={{position: 'absolute', top: 0, bottom: 0, [left ? 'left' : 'right']: 120, width: 1000, display: 'flex', flexDirection: 'column', justifyContent: 'center',
        alignItems: left ? 'flex-start' : 'flex-end', textAlign: left ? 'left' : 'right', ...F}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 16, flexDirection: left ? 'row' : 'row-reverse', opacity: gT}}>
          <div style={{width: 64 * gBar, height: 6, background: T.daccent, borderRadius: 3}} />
          <div style={{color: T.daccent, fontWeight: 700, fontSize: 38, letterSpacing: 1}}>{p.chapter}</div>
        </div>
        <div style={{overflow: 'hidden', marginTop: 18}}>
          <div style={{color: T.dink, fontWeight: 700, fontSize: 92, lineHeight: 1.18, wordBreak: 'keep-all',
            transform: `translate${fromBelow ? 'Y' : 'X'}(${(1 - gT) * (fromBelow ? 110 : left ? -80 : 80)}px)`, opacity: gT, textShadow: '0 2px 24px rgba(0,0,0,0.35)'}}>
            {p.title}
          </div>
        </div>
        {p.chip ? (
          <div style={{marginTop: 34, padding: '14px 24px', borderRadius: 14, background: 'rgba(255,255,255,0.12)', border: '1.5px solid rgba(255,255,255,0.28)',
            color: T.dink, fontWeight: 500, fontSize: 44, whiteSpace: 'nowrap', opacity: gC, transform: `translateY(${(1 - gC) * 18}px)`}}>{p.chip}</div>
        ) : null}
      </div>
      <AbsoluteFill style={{background: T.dbg, opacity: leave}} />
    </AbsoluteFill>
  );
};
