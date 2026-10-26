// 꽉 찬 실사 장면(TallyBroll) — 10/17 롱폼 화면 기준(work/research/longform/visual-gap-1017.md 4·7절, 관문 work/bgcheck.py)
// 왜: 수페TV는 관점·사람 이야기·비유·여는 말에서 화면을 꽉 채운 실사 영상을 쓴다(그 말일 때 실사 21~34%, 사실일 때 11%).
//      우리는 무엇을 말하든 같은 흰 판(85% 이상)이었다. 실사는 판 뒤 배경이 아니라 판과 번갈아 나오는 '숨 고르기' 장면이다.
// 언제: 대본 꼬리표 [실사] 문단(관점·사례·비유·장 머리·여는 말). 한 편에 실사 장면 합계 10% 이상(관문). 장 머리 2.5~4초는 StockShot을 써도 된다.
// 재료: 상업 이용 허락된 무료 스톡만(Pexels — work/pexelsvid.py가 ep/<편>/stock/credits.json에 출처 기록, 설명란 끝에 붙임).
//   license 칸 필수(예 'Pexels 26753905 무료'). 뉴스 사진·남의 영상 캡처 금지(블러해도). 실존 인물 얼굴·상표·간판·번호판은 blur 칸으로 가린다.
// 정직성: 실사는 분위기일 뿐 — 숫자는 넣지 않는다(숫자는 판에서). 실존 인물·기관처럼 읽히는 글자(이름표·'○○공단')를 얹지 않는다.
// 관문 판정과 맞추기: 글자 쪽만 살짝 어둡게(화면 절반 넘게 덮지 않는다). 너무 덮으면 bgcheck가 '판'으로 본다(평평한 점 45% 이상).
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS, Flame} from '../parts/fm';
import {TallyCaption, TallyLine, SAFE} from './TallyFrame';

export type BrollBlur = {x: number; y: number; w: number; h: number};
export type TallyBrollProps = {
  src: string;            // public 아래 경로('stock/26753905.mp4' 또는 사진 'stock/x.jpg')
  license: string;        // 출처·라이선스 한 줄 — 비우면 렌더를 멈춘다
  lines: TallyLine[];     // 이 장면 동안의 말(자막). frames 합 = 장면 길이
  from?: number;          // 영상 앞에서 잘라 낼 프레임(30fps)
  say?: string | null;    // 화면에 크게 얹을 한 줄(관점·비유 한마디, 18자 안). 숫자 금지
  chapter?: string | null;
  blur?: BrollBlur[];
  side?: 'left' | 'right';
  x?: number;             // objectPosition 가로 %(기본 50)
  dim?: number;           // 10/27 visual: 큰 글 쪽 그라데이션 진하기(기본 0.55) — 밝은 실사 위 흰 글 대비
  flip?: boolean;         // 10/27 visual: 좌우 뒤집기(동전 탑이 오른쪽으로 높아지게 등)
};

const out = Easing.out(Easing.cubic);

export const TallyBroll: React.FC<TallyBrollProps> = (p) => {
  if (!p.license || !p.license.trim()) throw new Error('TallyBroll: license(출처·라이선스) 칸이 비었다 — credits.json 줄을 적는다');
  if (p.say && /\d/.test(p.say)) throw new Error('TallyBroll: say에 숫자 금지 — 숫자는 판에서');
  const f = useCurrentFrame();
  const dur = p.lines.reduce((a, l) => a + l.frames, 0) || 90;
  const s = interpolate(f, [0, dur], [1.04, 1.12], CL);          // 끝까지 멈추지 않는 밀어 들어가기
  const enter = interpolate(f, [0, 8], [0, 1], {...CL, easing: out});
  const gT = interpolate(f, [6, 24], [0, 1], {...CL, easing: out});
  const left = (p.side ?? 'left') === 'left';
  const vid = /\.(mp4|webm|mov)$/i.test(p.src);
  const st: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${p.x ?? 50}% 50%`, transform: p.flip ? 'scaleX(-1)' : undefined};
  return (
    <AbsoluteFill style={{background: T.dbg, overflow: 'hidden'}}>
      <style>{FONT_CSS}</style>
      <AbsoluteFill style={{transform: `scale(${s})`, filter: `saturate(0.9) brightness(${0.6 + 0.4 * enter})`}}>
        {vid ? <OffthreadVideo src={staticFile(p.src)} trimBefore={p.from ?? 0} muted style={st} /> : <Img src={staticFile(p.src)} style={st} />}
        {(p.blur ?? []).map((b, i) => (
          <div key={i} style={{position: 'absolute', left: b.x, top: b.y, width: b.w, height: b.h, borderRadius: 24, backdropFilter: 'blur(28px)', WebkitBackdropFilter: 'blur(28px)'}} />
        ))}
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(10,11,14,0.62) 0%, rgba(10,11,14,0) 34%)'}} />
      {p.say ? <AbsoluteFill style={{background: `linear-gradient(${left ? 90 : 270}deg, rgba(10,11,14,${p.dim ?? 0.55}) 0%, rgba(10,11,14,0) ${p.dim ? 60 : 45}%)`}} /> : null}
      <div style={{position: 'absolute', left: SAFE.left, top: 18, display: 'flex', alignItems: 'center', gap: 10}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', textShadow: '0 1px 8px rgba(0,0,0,0.6)'}}>파이어맵</span>
        {p.chapter ? <div style={{...F, fontWeight: 700, fontSize: 22, color: '#fff', marginLeft: 10, textShadow: '0 1px 8px rgba(0,0,0,0.6)'}}>{p.chapter}</div> : null}
      </div>
      {p.say ? (
        <div style={{position: 'absolute', top: 330, [left ? 'left' : 'right']: 140, width: 1100, textAlign: left ? 'left' : 'right', opacity: gT,
          transform: `translateY(${(1 - gT) * 24}px)`}}>
          <div style={{...F, color: '#fff', fontWeight: 700, fontSize: 100, lineHeight: 1.15, letterSpacing: -2, wordBreak: 'keep-all', textShadow: '0 2px 28px rgba(0,0,0,0.55)'}}>{p.say}</div>
        </div>
      ) : null}
      <TallyCaption lines={p.lines} />
    </AbsoluteFill>
  );
};
