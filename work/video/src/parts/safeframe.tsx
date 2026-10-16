// 쇼츠 안전 영역 틀(10/16 쇼츠 담당) — 사장님 휴대폰에서 위 띠 질문·아래 답 칸·오른쪽 숫자가 유튜브 버튼·제목 밑에 깔리고 왼쪽 끝이 잘림.
// 기준(work/safezone.py와 같은 값): Google Ads 세로 동영상 안전 영역 1080×1920 — 위 288 · 아래 672 · 왼쪽 48 · 오른쪽 192 px. 글자는 전부 x 48~888 · y 288~1248 안.
// 근거·출처: work/research/cardshorts/safe-zone-1016.md. 바탕(검은 띠·흰 판·그림)은 가장자리까지 깔아도 되고, 글자만 안에 둔다.
import React from 'react';
import {Flame, F, T} from './fm';

export const SZ = {x0: 48, y0: 288, x1: 888, y1: 1248};
export const PAD = 14;                                   // 안전 영역 안쪽 여백
export const CX = (SZ.x0 + SZ.x1) / 2;                   // 글자 가운데 맞춤 기준(화면 가운데가 아니라 안전 영역 가운데 — 오른쪽 버튼 줄을 피한다)
export const IW = SZ.x1 - SZ.x0 - PAD * 2;               // 글자 줄 최대 너비 812

// 글자 너비 어림(Pretendard 굵게): 한글 0.96em · 숫자 0.6em · 영문 0.6em · 공백 0.28em · 기호 0.4em
export const units = (t: string) => {
  let u = 0;
  for (const ch of t) u += /[가-힣ㄱ-ㅎ㎡]/.test(ch) ? 0.96 : /\d/.test(ch) ? 0.6 : /[A-Za-z]/.test(ch) ? 0.62 : ch === ' ' ? 0.28 : /[−~→%+]/.test(ch) ? 0.62 : 0.4;
  return u;
};
export const fit = (t: string, w: number, max: number, min = 16) => Math.max(min, Math.min(max, Math.floor(w / Math.max(1, units(t)))));

// 위 띠: 0~band 검은 바탕(가장자리까지), 글자는 y0부터 — 브랜드 줄 + 질문 2줄
export const BRAND_TOP = SZ.y0 + 6, Q_TOP = SZ.y0 + 40, Q_LH = 1.1;
export const qSize = (q: string[]) => Math.min(...q.map((l) => fit(l, IW, 54)));
export const bandEnd = (q: string[]) => Math.round(Q_TOP + q.length * qSize(q) * Q_LH + 12);

export const TopBand: React.FC<{question: string[]; hot: string; base: string; hotColor?: string}> = ({question, hot, base, hotColor = '#FFD000'}) => {
  const qs = qSize(question); const be = bandEnd(question);
  const bs = fit(base, IW - 140, 20, 14);
  return (
    <>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: be, background: T.dbg}} />
      <div style={{position: 'absolute', left: SZ.x0 + PAD, top: BRAND_TOP, width: IW, display: 'flex', alignItems: 'center', gap: 8, whiteSpace: 'nowrap', overflow: 'hidden'}}>
        <Flame size={20} /><span style={{...F, fontWeight: 700, fontSize: 22, color: T.dink3}}>파이어맵</span>
        <span style={{...F, fontWeight: 500, fontSize: bs, color: T.dink3, marginLeft: 8}}>{base}</span>
      </div>
      <div style={{position: 'absolute', left: SZ.x0 + PAD, top: Q_TOP, width: IW, textAlign: 'center'}}>
        {question.map((line, i) => {
          const k = line.indexOf(hot);
          return <div key={i} style={{...F, fontWeight: 700, fontSize: qs, lineHeight: Q_LH, color: '#fff', letterSpacing: -1.5, whiteSpace: 'nowrap'}}>
            {k < 0 || !hot ? line : <>{line.slice(0, k)}<span style={{color: hotColor}}>{hot}</span>{line.slice(k + hot.length)}</>}</div>;
        })}
      </div>
    </>
  );
};

// 아래 답 칸(y1에 붙임): 이름표 · 답 숫자 한 줄 · 덧붙임 한 줄
export const ANS_H = 118;
export type Answer = {label: string; items: string[]; arrow?: boolean; note?: string} | null | undefined;
export const AnswerCard: React.FC<{answer: Answer}> = ({answer}) => {
  if (!answer) return null;
  const sep = answer.arrow ? ' → ' : ' · '; const all = answer.items.join(sep);
  const is = fit(all, IW - 36, 46, 24);
  return (
    <div style={{position: 'absolute', left: SZ.x0 + 6, top: SZ.y1 - ANS_H - 4, width: SZ.x1 - SZ.x0 - 12, height: ANS_H, boxSizing: 'border-box', background: T.soft, borderRadius: 20, padding: '8px 18px', overflow: 'hidden'}}>
      <div style={{...F, fontWeight: 700, fontSize: fit(answer.label, IW - 36, 21, 14), color: T.ink2, whiteSpace: 'nowrap', lineHeight: 1.25}}>{answer.label}</div>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 10, whiteSpace: 'nowrap', lineHeight: 1.2}}>
        {answer.items.map((x, i) => <React.Fragment key={i}>
          {i ? <span style={{...F, fontWeight: 700, fontSize: is * 0.8, color: T.ink3}}>{answer.arrow ? '→' : '·'}</span> : null}
          <span style={{...F, fontWeight: 700, fontSize: is, color: i === answer.items.length - 1 || !answer.arrow ? T.accent : T.ink, letterSpacing: -1}}>{x}</span>
        </React.Fragment>)}
      </div>
      {answer.note ? <div style={{...F, fontWeight: 700, fontSize: fit(answer.note, IW - 36, 20, 14), color: T.ink2, whiteSpace: 'nowrap', lineHeight: 1.25}}>{answer.note}</div> : null}
    </div>
  );
};

// 자막 상자: 답 칸 바로 위 한 줄
export const CAP_H = 78;
export const capTop = (answer: Answer) => (answer ? SZ.y1 - ANS_H - 4 : SZ.y1) - 8 - CAP_H;
export const capSize = (t: string) => fit(t, IW - 40, 50, 28);

// 가운데 판: band 끝 ~ 자막 위. 판(원래 bw×bh 좌표)을 높이·너비 둘 다 맞게 줄여 안전 영역 가운데에 둔다.
export const boardBox = (question: string[], answer: Answer, bw: number, bh: number) => {
  const top = bandEnd(question) + 8; const bottom = capTop(answer) - 8;
  const s = Math.min((bottom - top) / bh, (SZ.x1 - SZ.x0 - 8) / bw);
  const w = bw * s, h = bh * s;
  return {top, bottom, s, left: CX - w / 2, w, h, y: top + (bottom - top - h) / 2};
};

// 아래 가려지는 곳(y1~1920): 글자 없이 검은 바탕 + 진행 막대(유튜브 제목·채널 이름이 흰 글자라 어두운 바탕에서 읽힌다)
export const BottomShade: React.FC<{progress: number}> = ({progress}) => (
  <>
    <div style={{position: 'absolute', left: 0, top: SZ.y1, width: 1080, height: 1920 - SZ.y1, background: T.dbg}} />
    <div style={{position: 'absolute', left: SZ.x0, top: SZ.y1 + 14, width: SZ.x1 - SZ.x0, height: 8, background: '#2a2c33', borderRadius: 4}}>
      <div style={{width: `${Math.max(0, Math.min(1, progress)) * 100}%`, height: 8, background: T.accent, borderRadius: 4}} />
    </div>
  </>
);
