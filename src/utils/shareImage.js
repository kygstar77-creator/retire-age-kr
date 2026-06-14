import { statsRank } from '../firemap-v2/rank.js';
import { survivalPhrase } from '../firemap-v2/scenarios.js';

function roundRect(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + width, y, x + width, y + height, radius);
  ctx.arcTo(x + width, y + height, x, y + height, radius);
  ctx.arcTo(x, y + height, x, y, radius);
  ctx.arcTo(x, y, x + width, y, radius);
  ctx.closePath();
}

// 브랜드 로고(헤더와 동일한 두 겹 불꽃). viewBox 좌표를 캔버스에 맞춰 그림.
const LOGO_OUTER = 'M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z';
const LOGO_INNER = 'M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z';
function drawLogo(ctx, x, y, h, alpha = 1, twoTone = true) {
  ctx.save();
  ctx.globalAlpha = alpha;
  const s = h / 276;
  ctx.translate(x, y);
  ctx.scale(s, s);
  ctx.translate(-188, -84);
  ctx.fillStyle = '#ff5a00'; ctx.fill(new Path2D(LOGO_OUTER));
  if (twoTone) { ctx.fillStyle = '#fdba74'; ctx.fill(new Path2D(LOGO_INNER)); }
  ctx.restore();
}

// 결과 화면을 본뜬 공유용 이미지(1200x1200). 사용자 브라우저에서 개인 숫자로 렌더 → 카톡에 이미지 파일로 전송.
export async function makeShareImage(inputs, simulation) {
  const canvas = document.createElement('canvas');
  canvas.width = 1200; canvas.height = 1200;
  const ctx = canvas.getContext('2d');
  const rank = statsRank(simulation);
  const phrase = survivalPhrase(simulation);
  const earliest = simulation.earliestRetirementAge;
  const NAVY = '#1e2859', SOFT = '#b6c0ee', WHITE = '#ffffff', GREEN = '#86e0a0', ORANGE = '#ff5a00';
  const FONT = 'system-ui, -apple-system, "Apple SD Gothic Neo", sans-serif';
  const PAD = 120;

  const pill = (x, y, h, text, font, bg, fg) => {
    ctx.font = font;
    const m = ctx.measureText(text);
    const w = m.width + h * 0.8;
    ctx.fillStyle = bg; roundRect(ctx, x, y, w, h, h / 2); ctx.fill();
    ctx.fillStyle = fg;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    const asc = m.actualBoundingBoxAscent || h * 0.34;
    const desc = m.actualBoundingBoxDescent || h * 0.08;
    ctx.fillText(text, x + w / 2, y + h / 2 + (asc - desc) / 2);
    ctx.textAlign = 'left';
    return w;
  };

  ctx.fillStyle = NAVY; ctx.fillRect(0, 0, 1200, 1200);
  drawLogo(ctx, 720, 600, 560, 0.06, false);

  drawLogo(ctx, PAD, 104, 64, 1, true);
  ctx.fillStyle = WHITE; ctx.font = `800 46px ${FONT}`;
  ctx.fillText('파이어맵', PAD + 52, 158);

  ctx.fillStyle = SOFT; ctx.font = `600 36px ${FONT}`;
  ctx.fillText(`내 파이어 가능 나이 · ${rank.ageBandLabel} 또래 기준`, PAD, 308);

  const heroText = earliest ? `${earliest}세 파이어 가능` : '조금만 더!';
  ctx.fillStyle = WHITE; ctx.font = `800 100px ${FONT}`;
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  ctx.fillText(heroText, PAD, 452);

  if (rank && rank.percentile) {
    pill(PAD, 512, 96, `또래 자산 상위 ${rank.percentile}%`, `800 50px ${FONT}`, ORANGE, WHITE);
  }

  ctx.fillStyle = WHITE; ctx.font = `800 54px ${FONT}`;
  ctx.fillText(phrase.short, PAD, 720);
  ctx.fillStyle = SOFT; ctx.font = `600 34px ${FONT}`;
  ctx.fillText('지금 계획 기준 · 또래 중 내 등수도 확인', PAD, 786);
  ctx.fillStyle = GREEN; ctx.font = `600 30px ${FONT}`;
  ctx.fillText('전국 또래와 비교한 내 파이어 나이', PAD, 850);

  pill(PAD, 952, 100, '나도 내 파이어 나이 확인하기', `800 42px ${FONT}`, WHITE, NAVY);

  ctx.fillStyle = SOFT; ctx.font = `700 30px ${FONT}`;
  ctx.fillText('firemap.kr', PAD, 1108);

  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 0.95));
}
