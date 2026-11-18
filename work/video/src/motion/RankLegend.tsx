// 순위·사다리 범례 — 오른쪽에 칸 목록을 세로로 두고, 지금 말하는 칸에 불을 켠다(2026-11-18 motion).
// 근거: registry B-57(전력분석소 iJ4haRGxOpw 1~31칸 오른쪽 '0.1%·1%·상위 10%…·최저' 사다리 범례, 말하는 칸 켬).
// 금지 목록 지킴: 칸 상자·알약 없음. 글자 줄 + 왼쪽 손 점 하나 + 켜진 줄에만 주황 손 밑줄. 지나간 줄은 진하게, 아직 안 온 줄은 옅게.
// 쓰는 법: <RankLegend items={[{label:'2001-09-12', value:'−12.02%'}, …]} on={[[프레임, 칸 번호], …]} dark={실사 위?} />
//   on: 오름차순 [시작 프레임, 켤 칸] 목록. 첫 켬 전에는 범례가 옅게만 깔리고, 켜진 칸이 바뀌면 10프레임에 걸쳐 옮겨 간다.
// 자리: 오른쪽 x 1500~1800(SAFE.brX 1440 바깥), 판 본문(제목 아래 y 250~820)과 겹치지 않게 판 오른쪽 여백에만. 넓은 표 판에선 끈다.
import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {T, F, CL, FONT_CSS} from '../parts/fm';
import {HandUnderline} from '../parts/human';

export type LegendItem = {label: string; value?: string | null};
const SH = '0 2px 6px rgba(0,0,0,0.75)';
export const RankLegend: React.FC<{items: LegendItem[]; on: [number, number][]; title?: string | null; dark?: boolean; x?: number; top?: number; rowH?: number}> =
  ({items, on, title = null, dark = false, x = 1500, top = 260, rowH = 54}) => {
  const f = useCurrentFrame();
  let cur = -1; let since = 0; let prev = -1;
  for (const [a, i] of on) if (f >= a) { prev = cur; cur = i; since = a; }
  const mv = interpolate(f, [since, since + 10], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const fadeIn = interpolate(f, [0, 12], [0, 1], CL);
  const seen = new Set(on.filter(([a]) => f >= a).map(([, i]) => i));
  const dotY = (cur < 0 ? 0 : (prev < 0 ? cur : prev + (cur - prev) * mv)) * rowH + rowH / 2;
  const ink = dark ? '#ffffff' : T.ink; const ink3 = dark ? 'rgba(255,255,255,0.55)' : T.ink3;
  const acc = dark ? T.daccent : T.accent;
  return (
    <div style={{position: 'absolute', left: x, top, width: 1820 - x, opacity: fadeIn}}>
      <style>{FONT_CSS}</style>
      {title ? <div style={{...F, fontWeight: 700, fontSize: 20, color: dark ? '#e8eaee' : T.ink2, textShadow: dark ? SH : undefined, marginBottom: 10, whiteSpace: 'nowrap'}}>{title}</div> : null}
      <div style={{position: 'relative'}}>
        {/* 왼쪽 세로 손 선 — 사다리의 기둥 */}
        <div style={{position: 'absolute', left: 9, top: rowH / 2, width: 2, height: (items.length - 1) * rowH, background: ink3, opacity: 0.6}} />
        {cur >= 0 ? <div style={{position: 'absolute', left: 1, top: dotY - 9, width: 18, height: 18, borderRadius: 9, background: acc}} /> : null}
        {items.map((it, i) => {
          const isOn = i === cur; const done = seen.has(i);
          const c = isOn ? acc : done ? ink : ink3;
          return (
            <div key={i} style={{position: 'relative', height: rowH, display: 'flex', alignItems: 'center', gap: 14, paddingLeft: 32, whiteSpace: 'nowrap', textShadow: dark ? SH : undefined}}>
              <span style={{...F, fontWeight: isOn ? 700 : 500, fontSize: isOn ? 26 : 22, color: c}}>{it.label}</span>
              {it.value ? <span style={{...F, fontWeight: 700, fontSize: isOn ? 28 : 22, color: c}}>{it.value}</span> : null}
              {isOn ? <HandUnderline x={32} y={rowH - 8} w={260} p={mv} stroke={4} seed={i + 2} color={acc} /> : null}
            </div>
          );
        })}
      </div>
    </div>
  );
};
