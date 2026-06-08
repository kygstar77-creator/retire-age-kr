import { useState } from 'react';
import Header from './Header.jsx';
import { BASE_URL, CONTACT_EMAIL } from '../../firemap-v2/data.js';
import { buildShareUrl } from '../../utils/shareState.js';
import { runwayText } from '../../firemap-v2/scenarios.js';

function roundRect(ctx, x, y, width, height, radius) {
  ctx.beginPath(); ctx.moveTo(x + radius, y); ctx.arcTo(x + width, y, x + width, y + height, radius); ctx.arcTo(x + width, y + height, x, y + height, radius); ctx.arcTo(x, y + height, x, y, radius); ctx.arcTo(x, y, x + width, y, radius); ctx.closePath();
}

async function makeShareImage(inputs, simulation) {
  const canvas = document.createElement('canvas'); canvas.width = 1200; canvas.height = 630;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff7ed'; ctx.fillRect(0, 0, 1200, 630);
  ctx.fillStyle = '#ffffff'; roundRect(ctx, 70, 70, 1060, 490, 42); ctx.fill();
  ctx.strokeStyle = '#fed7aa'; ctx.lineWidth = 4; ctx.stroke();
  ctx.fillStyle = '#ea580c'; ctx.font = 'bold 44px sans-serif'; ctx.fillText('파이어맵 계산 결과', 120, 155);
  ctx.fillStyle = '#111827'; ctx.font = 'bold 74px sans-serif'; ctx.fillText(`${inputs.targetRetirementAge}세 퇴사`, 120, 280);
  ctx.fillStyle = '#ea580c'; ctx.font = 'bold 86px sans-serif'; ctx.fillText(`${runwayText(simulation)}까지`, 120, 385);
  ctx.fillStyle = '#4b5563'; ctx.font = 'bold 34px sans-serif'; ctx.fillText('내 돈이 얼마나 버티는지 계산해봤어요', 120, 465);
  ctx.fillStyle = '#9a3412'; ctx.font = 'bold 28px sans-serif'; ctx.fillText('retire-age-kr.pages.dev', 120, 520);
  ctx.strokeStyle = '#ea580c'; ctx.lineWidth = 16; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(720, 450); ctx.bezierCurveTo(810, 350, 875, 380, 965, 260); ctx.stroke();
  ctx.fillStyle = '#fff7ed'; ctx.strokeStyle = '#ea580c'; ctx.lineWidth = 8;
  [720, 965].forEach((x, i) => { ctx.beginPath(); ctx.arc(x, i ? 260 : 450, 16, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); });
  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 0.95));
}

export default function Share({ inputs, simulation, onBack }) {
  const [message, setMessage] = useState('');
  const shareUrl = buildShareUrl(inputs);
  const resultLine = `${inputs.targetRetirementAge}세 퇴사 → ${runwayText(simulation)}까지`;
  const shareText = `파이어맵 계산 결과\n${resultLine}\n내 돈이 얼마나 버티는지 계산해봤어요.`;
  const copyFallback = async (text, label) => { try { await navigator.clipboard.writeText(text); setMessage(label); setTimeout(() => setMessage(''), 1800); } catch { setMessage('복사가 막혀 있어요. 주소창에서 직접 복사해주세요.'); } };
  const shareLink = async (url, title) => {
    const payload = { title, url };
    if (navigator.share) { try { await navigator.share(payload); setMessage('공유창을 열었어요'); return; } catch (error) { if (error?.name === 'AbortError') return; } }
    await copyFallback(url, '링크를 복사했어요');
  };
  const shareImage = async () => {
    const blob = await makeShareImage(inputs, simulation); const file = new File([blob], 'firemap-result.png', { type: 'image/png' });
    if (navigator.canShare?.({ files: [file] })) { await navigator.share({ files: [file], title: '파이어맵 계산 결과' }); setMessage('이미지 공유창을 열었어요'); }
    else { const url = URL.createObjectURL(blob); window.open(url, '_blank'); setMessage('이미지를 새 창으로 열었어요. 길게 눌러 저장하세요.'); }
  };
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="공유" onBack={onBack} />
      <section className="fm-card fm-text-card"><p className="fm-kicker">공유</p><h2>결과를 공유해보세요</h2><div className="fm-share-preview"><strong>{resultLine}</strong><p>내 돈이 얼마나 버티는지 계산해봤어요.</p></div><button className="fm-primary" type="button" onClick={shareImage}>결과 이미지 공유하기</button><button className="fm-secondary" type="button" onClick={() => shareLink(BASE_URL, '파이어맵')}>앱 링크 공유하기</button><button className="fm-secondary" type="button" onClick={() => shareLink(shareUrl, '내 파이어맵 조건')}>내 조건 링크 공유하기</button><button className="fm-secondary" type="button" onClick={() => copyFallback(`${shareText}\n${BASE_URL}`, '결과 문구를 복사했어요')}>결과 문구 복사</button>{message && <div className="fm-toast">{message}</div>}</section>
      <section className="fm-card fm-info"><em>운영 안내</em><h2>개인정보·면책·문의</h2><p>입력값은 브라우저에서 계산됩니다. 조건 링크를 공유하면 일부 입력값이 링크에 포함될 수 있습니다.</p><small>문의: <b>{CONTACT_EMAIL}</b></small></section>
    </main>
  );
}
