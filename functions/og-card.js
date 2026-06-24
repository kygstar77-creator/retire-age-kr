// 공유 카드(남색 카카오 스타일) 공통 SVG 빌더.
// /og 동적 생성(functions/og.js)과 정적 og-image(work/fix-branding-og.mjs)가 함께 써서
// 카카오·다른 앱·웹 링크 어디서 공유하든 같은 남색 카드가 나오게 한다.
const COMMA = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
const FLAME = '<svg x="497" y="92" width="30" height="60" viewBox="188 84 136 276"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>';

// opts: { mode: 'rank'|'generic'|'save'|'firetype', ea, pos, tot, runway, tname, nick, cities, font }
export function buildCardSvg(opts = {}) {
  const font = opts.font || 'Noto Sans CJK KR';
  const mode = opts.mode || 'rank';
  const header = `<rect width="1200" height="600" fill="#18224d"/>
${FLAME}
<text x="537" y="138" font-family="${font}" font-weight="700" font-size="40" fill="#ffffff">파이어맵</text>`;

  let body;
  if (mode === 'save') {
    body = `<text x="600" y="216" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">절약으로 파이어 앞당기기</text>
<text x="600" y="322" font-family="${font}" font-weight="700" font-size="78" fill="#ffffff" text-anchor="middle">하루 아낀 돈이</text>
<text x="600" y="416" font-family="${font}" font-weight="700" font-size="78" fill="#ffffff" text-anchor="middle"><tspan fill="#ff5a00">파이어</tspan>를 당겨요</text>`;
  } else if (mode === 'generic') {
    body = `<text x="600" y="216" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">또래 중 내 파이어 등수도 1분 만에</text>
<text x="600" y="322" font-family="${font}" font-weight="700" font-size="80" fill="#ffffff" text-anchor="middle">나는 몇 살에</text>
<text x="600" y="416" font-family="${font}" font-weight="700" font-size="80" fill="#ffffff" text-anchor="middle"><tspan fill="#ff5a00">파이어</tspan>할 수 있을까?</text>`;
  } else if (mode === 'firetype') {
    const tname = (opts.tname || '').trim() || '파이어족';
    const nick = (opts.nick || '').trim();
    const cities = (opts.cities || '').trim();
    body = `<text x="600" y="206" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">나의 파이어 유형은</text>
<text x="600" y="312" font-family="${font}" font-weight="700" font-size="84" fill="#ffffff" text-anchor="middle">${tname}</text>
${nick ? `<text x="600" y="372" font-family="${font}" font-weight="700" font-size="40" fill="#ff8a4c" text-anchor="middle">“${nick}”</text>` : ''}
${cities ? `<text x="600" y="448" font-family="${font}" font-weight="600" font-size="34" fill="#9aa4d4" text-anchor="middle">추천 도시 · ${cities}</text>` : ''}`;
  } else {
    // rank — 사용자별 또래 상위 %·등수·파이어 나이
    const ea = Number(opts.ea) || 0;
    const pos = Number(opts.pos) || 0;
    const tot = Math.max(1, Number(opts.tot) || 1);
    const runway = (opts.runway && opts.runway !== '—') ? String(opts.runway) : '';
    const p = Math.max(1, Math.min(99, Math.round((pos / tot) * 100)));
    const parts = [];
    if (ea > 0) parts.push(ea + '세 파이어 가능');
    if (runway) parts.push(runway.indexOf('이상') >= 0 ? runway + ' 버팀' : runway + '까지 버팀');
    const mid = parts.join(' · ');
    body = `<text x="600" y="208" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">파이어 랭킹 · 또래 상위</text>
<text x="600" y="358" font-family="${font}" font-weight="700" font-size="150" fill="#ff5a00" text-anchor="middle">${p}%</text>
<text x="600" y="418" font-family="${font}" font-weight="700" font-size="40" fill="#ffffff" text-anchor="middle">전체 <tspan fill="#ff8a4c">${COMMA(tot)}명</tspan> 중 <tspan fill="#ff8a4c">${COMMA(pos)}등</tspan></text>
<text x="600" y="470" font-family="${font}" font-weight="600" font-size="30" fill="#9aa4d4" text-anchor="middle">${mid}</text>`;
  }

  const cta = `<text x="600" y="540" font-family="${font}" font-weight="700" font-size="30" fill="#ffffff" text-anchor="middle">나도 1분 만에 확인  →  <tspan fill="#ff8a4c">firemap.kr</tspan></text>`;
  return `<svg width="1200" height="600" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">
${header}
${body}
${cta}
</svg>`;
}
