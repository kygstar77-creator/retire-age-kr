// 장 카드(ChapterAsk) — 2026-11-27 motion. CC-1 장 카드 8장 '못함'(새 심사관 C, judge_c.json) 고침.
// 옛 Ask(KOSPI1 틀): 검은 빈 화면 + 주황 알약 'N장' + 제목 한 줄 → 클로드 티 목록 '알약 꼬리표·장 번호' 그대로, 그 장이 무엇을 재는지 단서 없음.
// 새 틀: 구겨진 종이 결 위에 바로 — ① 기준 한 줄(기간·조건, 대본 말) ② 장 질문 큰 글자 ③ 단서 칸 2~3개(무엇과 무엇을 재나, 값은 '?')
//        ④ 필요하면 식 한 줄. 경쟁 #12('걱정은 크게 세 가지' 번호 셋+손 동그라미)처럼 단서가 화면에 있다.
// 장 번호·알약·상자 없음. 강조는 손 동그라미 하나(mark) — 주황은 그것뿐. 칸 사이는 손 세로줄.
// 들어오기는 장마다 다르게(seed): 질문은 '써지듯'(왼→오) 또는 '찍기', 칸은 앞→뒤 차례로, 3칸은 세로로 쌓기(layout col).
// U5: 장면 내내 천천히 다가감(1.00→1.03, 가운데 기준). 글자는 전부 props(편 스크립트가 script.md 말과 대조).
// 띠링(isChapter)은 data.n('N장')으로 잡으니 n은 데이터에 두되 화면엔 그리지 않는다.
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing, random} from 'remotion';
import {T, F, CL, FONT_CSS, HandCircle} from '../parts/fm';
import {PaperBg, HandDivider, HandUnderline} from '../parts/human';

export type ChapterAskProps = {
  seed: string;
  q: string;                 // 장 질문(큰 글자)
  top?: string;              // 기준 한 줄 — 기간·조건
  cells?: string[];          // 단서 칸 2~3개
  mark?: number;             // 손 동그라미 칠 칸(없으면 -1)
  foot?: string;             // 식 한 줄(선택)
  layout?: 'row' | 'col';
  num?: boolean;             // 세로 칸 앞에 1·2·3(손 동그라미, 먹색) — 11/27 심사 C '함정은 번호 붙인 목록으로'
  end: number;               // 장면 길이(프레임)
};

const out = Easing.out(Easing.cubic);
const g = (f: number, a: number, d = 14, e = out) => interpolate(f, [a, a + d], [0, 1], {...CL, easing: e});
const units = (t: string) => [...t].reduce((a, c) => a + (/[ㄱ-힝]/.test(c) ? 1 : /\s/.test(c) ? 0.32 : 0.58), 0);
const fit = (t: string, room: number, max: number, min = 54) => Math.max(min, Math.min(max, Math.floor(room / Math.max(1, units(t)))));

export const ChapterAsk: React.FC<ChapterAskProps> = (p) => {
  const f = useCurrentFrame();
  const r = (k: string) => random(p.seed + k);
  const stamp = r('m') > 0.5;
  const cells = p.cells ?? []; const col = p.layout === 'col';
  const has = cells.length > 0 || !!p.foot;  // eslint-disable-line
  const qz = fit(p.q, 1500, has ? 118 : 136);
  const cz = col ? fit(cells.reduce((a, b) => units(a) > units(b) ? a : b, ''), 1300, 80, 58) : fit(cells.reduce((a, b) => units(a) > units(b) ? a : b, ''), 1500 / Math.max(1, cells.length) - 120, 92, 50);
  const rowH = cz * (col ? 1.95 : 1.55);
  const fz = cells.length ? 66 : 120;
  // 블록 전체 높이를 재서 자막 위 영역(90~880)의 가운데에 둔다 — 11/27 첫 미리보기: 위에 몰려 아래 절반이 빔
  const hTop = p.top ? 104 : 0, hQ = qz * 1.2, hC = cells.length ? 90 + (col ? cells.length * rowH : rowH) : 0, hF = p.foot ? (cells.length ? 30 : 90) + fz * 1.2 : 0;
  const y0 = Math.round(90 + (790 - (hTop + hQ + hC + hF)) / 2);
  const yTop = y0, yq = y0 + hTop, yC = yq + hQ + 90, yF = yq + hQ + hC + (cells.length ? 30 : 90);
  // 질문 들어오기
  const qa = 2, qp = g(f, qa, stamp ? 9 : 18, stamp ? Easing.out(Easing.back(1.5)) : Easing.inOut(Easing.cubic));
  const qStyle: React.CSSProperties = stamp
    ? {opacity: Math.min(1, qp * 1.6), transform: `scale(${1.12 - 0.12 * qp})`}
    : {clipPath: `inset(-20% ${(1 - qp) * 100}% -20% 0)`};
  const topO = g(f, 12, 12);
  const cA = (i: number) => 18 + i * 9;
  const z = interpolate(f, [0, Math.max(1, p.end)], [1, 1.03], CL);
  const mk = p.mark ?? -1;
  const cw = col ? 1200 : 1500 / Math.max(1, cells.length);
  const cx0 = 960 - (cw * cells.length) / 2;
  const colW = Math.max(0, ...cells.map((c) => units(c))) * cz; const colL = 960 - colW / 2 + (p.num ? 60 : 0);
  return (
    <AbsoluteFill>
      <style>{FONT_CSS}</style>
      <PaperBg />
      <div style={{position: 'absolute', inset: 0, transform: `scale(${z})`, transformOrigin: '50% 45%'}}>
        {p.top ? <div style={{position: 'absolute', left: 160, width: 1600, top: yTop, textAlign: 'center', ...F, fontWeight: 700, fontSize: 58, color: T.ink, opacity: topO, letterSpacing: -1}}>{p.top}</div> : null}
        <div style={{position: 'absolute', left: 160, width: 1600, top: yq, display: 'flex', justifyContent: 'center'}}>
          <div style={{...F, fontWeight: 800, fontSize: qz, color: T.ink, lineHeight: 1.18, letterSpacing: -2, textAlign: 'center', wordBreak: 'keep-all', ...qStyle}}>{p.q}</div>
        </div>
        {!has ? <HandUnderline x={960 - Math.min(1400, units(p.q) * qz) / 2} y={yq + qz * 1.2 + 14} w={Math.min(1400, units(p.q) * qz)} p={g(f, qa + 16, 16)} color={T.ink3} seed={3} stroke={6} /> : null}
        {cells.map((c, i) => {
          const o = g(f, cA(i), 12);
          const x = col ? colL : cx0 + cw * i; const y = col ? yC + i * rowH : yC;
          const w = units(c) * cz;
          return <React.Fragment key={i}>
            <div style={{position: 'absolute', left: x, width: col ? colW + 40 : cw, top: y, textAlign: col ? 'left' : 'center', ...F, fontWeight: 800, fontSize: cz, color: T.ink, opacity: o,
              transform: `translateX(${(1 - o) * (col ? -30 : 24)}px)`, whiteSpace: 'nowrap'}}>{c}</div>
            {i !== mk ? <HandUnderline x={col ? x - 20 : x + cw / 2 - Math.min(cw - 40, w + 60) / 2} y={y + cz * 1.28} w={Math.min(cw - 40, w + 60)} p={g(f, cA(i) + 6, 12)} color={T.ink2} seed={i + 2} stroke={7} /> : null}
            {col && p.num ? <><div style={{position: 'absolute', left: colL - 130, width: 80, top: y, textAlign: col ? 'left' : 'center', ...F, fontWeight: 800, fontSize: cz, color: T.ink2, opacity: o}}>{i + 1}</div>
              <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible'}}><HandCircle cx={colL - 90} cy={y + cz * 0.62} rx={cz * 0.62} ry={cz * 0.62} p={g(f, cA(i) + 4, 12)} color={T.ink3} /></svg></> : null}
            {!col && i > 0 ? <HandDivider x={x} y={y - 6} h={cz * 1.4} p={g(f, cA(i) - 4, 10)} color={T.ink2} /> : null}
            {i === mk ? <svg style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, overflow: 'visible'}}>
              <HandCircle cx={col ? x + w / 2 : x + cw / 2} cy={y + cz * 0.62} rx={w / 2 + (col ? 26 : 70)} ry={cz * (col ? 0.75 : 0.9)} p={g(f, cA(cells.length) + 8, 18)} /></svg> : null}
          </React.Fragment>;
        })}
        {p.foot ? <div style={{position: 'absolute', left: 160, width: 1600, top: yF,
          textAlign: 'center', ...F, fontWeight: 800, fontSize: fz, color: T.ink, opacity: g(f, cA(cells.length) + 2, 12)}}>{p.foot}</div> : null}
      </div>
    </AbsoluteFill>
  );
};
