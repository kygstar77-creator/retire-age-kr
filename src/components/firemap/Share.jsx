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
  const NAVY = '#1e2859', ORANGE = '#ff5a00', GRAY = '#8b9098', INK = '#1a1c22';
  const FONT = 'system-ui, -apple-system, "Apple SD Gothic Neo", sans-serif';

  ctx.fillStyle = NAVY; ctx.fillRect(0, 0, 1200, 1200);
  ctx.fillStyle = '#ffffff'; roundRect(ctx, 64, 64, 1072, 1072, 60); ctx.fill();

  // 장식용 불꽃 워터마크 (우하단, 은은하게)
  drawFlame(ctx, 720, 560, 4.6, ORANGE, 0.05);

  // 브랜드
  drawFlame(ctx, 132, 116, 0.62, ORANGE, 1);
  ctx.fillStyle = NAVY; ctx.font = `800 46px ${FONT}`;
  ctx.fillText('파이어맵', 202, 168);

  // 라벨
  ctx.fillStyle = GRAY; ctx.font = `600 34px ${FONT}`;
  ctx.fillText(`내 FIRE 자생력 · ${rank.ageBandLabel} 또래 기준`, 132, 288);

  // 히어로 백분위
  ctx.fillStyle = NAVY; ctx.font = `900 122px ${FONT}`;
  ctx.fillText(`또래 상위 ${rank.percentile}%`, 132, 422);

  // 등급 배지 (오렌지)
  ctx.fillStyle = ORANGE; roundRect(ctx, 132, 470, 228, 86, 43); ctx.fill();
  ctx.fillStyle = '#ffffff'; ctx.font = `800 46px ${FONT}`;
  ctx.fillText(`${rank.grade}등급`, 170, 528);

  // 구분선
  ctx.strokeStyle = '#eef0f4'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(132, 642); ctx.lineTo(1068, 642); ctx.stroke();

  // 결과 문구
  ctx.fillStyle = INK; ctx.font = `800 52px ${FONT}`;
  ctx.fillText(phrase.short, 132, 728);
  ctx.fillStyle = GRAY; ctx.font = `600 32px ${FONT}`;
  ctx.fillText(`자산수명 점수 ${simulation.survivalScore}/100`, 132, 788);

  // CTA
  ctx.fillStyle = ORANGE; roundRect(ctx, 132, 952, 580, 100, 50); ctx.fill();
  ctx.fillStyle = '#ffffff'; ctx.font = `800 42px ${FONT}`;
  ctx.fillText('나도 내 사표 날짜 계산하기', 178, 1014);

  // URL
  ctx.fillStyle = GRAY; ctx.font = `700 30px ${FONT}`;
  ctx.fillText('retire-age-kr.pages.dev', 132, 1100);

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

  const shareCondition = async () => {
    const url = buildScenarioShareUrl(inputs);
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
