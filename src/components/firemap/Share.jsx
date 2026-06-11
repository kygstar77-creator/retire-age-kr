import { useState } from 'react';
import Header from './Header.jsx';
import { BASE_URL, CONTACT_EMAIL } from '../../firemap-v2/data.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { buildScenarioShareUrl, buildShareText } from '../../utils/shareState.js';
import { survivalPhrase } from '../../firemap-v2/scenarios.js';

function roundRect(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + width, y, x + width, y + height, radius);
  ctx.arcTo(x + width, y + height, x, y + height, radius);
  ctx.arcTo(x, y + height, x, y, radius);
  ctx.arcTo(x, y, x + width, y, radius);
  ctx.closePath();
}

function drawFlame(ctx, x, y, scale, color, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.translate(x, y);
  ctx.scale(scale, scale);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(44, 4);
  ctx.bezierCurveTo(88, 42, 86, 92, 44, 104);
  ctx.bezierCurveTo(7, 94, 2, 51, 28, 24);
  ctx.bezierCurveTo(26, 47, 47, 50, 44, 4);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

async function makeShareImage(inputs, simulation) {
  const canvas = document.createElement('canvas');
  canvas.width = 1200; canvas.height = 1200;
  const ctx = canvas.getContext('2d');
  const rank = statsRank(simulation);
  const phrase = survivalPhrase(simulation);
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

  // 네이비 배경 (결과 RankHero와 동일 톤)
  ctx.fillStyle = NAVY; ctx.fillRect(0, 0, 1200, 1200);
  drawFlame(ctx, 880, 720, 4.4, ORANGE, 0.08);

  // 브랜드
  drawFlame(ctx, PAD, 108, 0.6, ORANGE, 1);
  ctx.fillStyle = WHITE; ctx.font = `800 46px ${FONT}`;
  ctx.fillText('파이어맵', PAD + 76, 158);

  // 라벨
  ctx.fillStyle = SOFT; ctx.font = `600 36px ${FONT}`;
  ctx.fillText(`내 FIRE 자생력 · ${rank.ageBandLabel} 또래 기준`, PAD, 308);

  // 히어로 백분위 + 등급 배지 (RankHero처럼 한 줄, 세로 중앙)
  const heroText = `상위 ${rank.percentile}%`;
  ctx.fillStyle = WHITE; ctx.font = `800 130px ${FONT}`;
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  ctx.fillText(heroText, PAD, 462);
  const heroW = ctx.measureText(heroText).width;
  const badgeH = 80;
  const badgeCenter = 462 - 130 * 0.35;
  pill(PAD + heroW + 40, badgeCenter - badgeH / 2, badgeH, `${rank.grade}등급`, `800 42px ${FONT}`, WHITE, NAVY);

  // 결과 문구 + 점수
  ctx.fillStyle = WHITE; ctx.font = `800 54px ${FONT}`;
  ctx.fillText(phrase.short, PAD, 730);
  ctx.fillStyle = SOFT; ctx.font = `600 34px ${FONT}`;
  ctx.fillText(`자산수명 점수 ${simulation.survivalScore}/100`, PAD, 794);
  ctx.fillStyle = GREEN; ctx.font = `600 30px ${FONT}`;
  ctx.fillText('전국 또래와 비교한 내 FIRE 등수', PAD, 856);

  // CTA (긍정 문구 · 중앙정렬)
  pill(PAD, 952, 100, '나도 내 FIRE 등수 확인하기', `800 42px ${FONT}`, WHITE, NAVY);

  // URL
  ctx.fillStyle = SOFT; ctx.font = `700 30px ${FONT}`;
  ctx.fillText('retire-age-kr.pages.dev', PAD, 1108);

  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 0.95));
}

export default function Share({ inputs, simulation, onBack }) {
  const [message, setMessage] = useState('');
  const rank = statsRank(simulation);
  const phrase = survivalPhrase(simulation);
  const resultLine = `또래 상위 ${rank.percentile}% · ${rank.grade}등급 · ${phrase.short}`;

  const flash = (text) => { setMessage(text); setTimeout(() => setMessage(''), 2000); };
  const copyFallback = async (text, label) => {
    try { await navigator.clipboard.writeText(text); flash(label); }
    catch { flash('복사가 막혀 있어요. 주소창에서 직접 복사해 주세요.'); }
  };

  const shareImage = async () => {
    const blob = await makeShareImage(inputs, simulation);
    const file = new File([blob], 'firemap-grade.png', { type: 'image/png' });
    if (navigator.canShare?.({ files: [file] })) {
      await navigator.share({ files: [file], title: '내 FIRE 등급', text: resultLine });
      flash('등급 카드 공유창을 열었어요');
    } else {
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      flash('이미지를 새 창으로 열었어요. 길게 눌러 저장해 주세요.');
    }
  };

  const buildPreviewUrl = () => {
    const u = new URL(buildScenarioShareUrl(inputs));
    u.pathname = '/s';
    u.searchParams.set('p', String(rank.percentile));
    u.searchParams.set('g', rank.grade);
    u.searchParams.set('rw', phrase.short);
    return u.toString();
  };
  const shareCondition = async () => {
    const url = buildPreviewUrl();
    const text = `${resultLine}\n내 조건 그대로 열어보기`;
    if (navigator.share) {
      try { await navigator.share({ title: '파이어맵 — 내 조건', text, url }); flash('조건 링크 공유창을 열었어요'); return; }
      catch (e) { if (e?.name === 'AbortError') return; }
    }
    await copyFallback(url, '내 조건 링크를 복사했어요 (계산값 포함)');
  };

  const shareApp = async () => {
    if (navigator.share) {
      try { await navigator.share({ title: '파이어맵', text: '내 돈은 몇 살까지 버틸 수 있을까?', url: BASE_URL }); return; }
      catch (e) { if (e?.name === 'AbortError') return; }
    }
    await copyFallback(BASE_URL, '앱 링크를 복사했어요');
  };

  return (
    <main className="fm-screen fm-scroll">
      <Header onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">공유</p>
        <h2>내 FIRE 등급 자랑하기</h2>
        <section className="fm-rank-hero fm-share-hero">
          <p className="fm-rank-label">내 FIRE 자생력 · {rank.ageBandLabel} 또래 기준</p>
          <div className="fm-rank-top">
            <span className="fm-rank-pct">또래 상위 {rank.percentile}%</span>
            <span className="fm-rank-badge">{rank.grade}등급</span>
          </div>
          <p className="fm-rank-line">{phrase.short}</p>
        </section>
        <div className="fm-share-actions">
          <button className="fm-share-btn fm-share-primary" type="button" onClick={shareImage}>
            <b>등급 카드 이미지</b><span>또래 상위 %·등급만 — 금액은 안 담겨요</span>
          </button>
          <button className="fm-share-btn" type="button" onClick={shareCondition}>
            <b>내 조건 그대로 공유</b><span>계산값 링크 — 받은 사람 화면에 자동 입력</span>
          </button>
          <button className="fm-share-btn" type="button" onClick={shareApp}>
            <b>앱 링크만 공유</b><span>첫 화면 링크</span>
          </button>
        </div>
        {message && <div className="fm-toast">{message}</div>}
      </section>
      <section className="fm-card fm-info">
        <em>운영 안내</em>
        <h2>개인정보 · 면책 · 문의</h2>
        <p>입력값은 브라우저에서 계산돼요. 등급 카드엔 금액이 들어가지 않고, 조건 링크는 본인이 공유할 때만 만들어져요.</p>
        <small>문의: <b>{CONTACT_EMAIL}</b></small>
      </section>
    </main>
  );
}
