import { useState } from 'react';
import Header from './Header.jsx';
import { BASE_URL, CONTACT_EMAIL } from '../../firemap-v2/data.js';
import { runwayText } from '../../firemap-v2/scenarios.js';

function roundRect(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + width, y, x + width, y + height, radius);
  ctx.arcTo(x + width, y + height, x, y + height, radius);
  ctx.arcTo(x, y + height, x, y, radius);
  ctx.arcTo(x, y, x + width, y, radius);
  ctx.closePath();
}

async function makeShareImage(inputs, simulation) {
  const canvas = document.createElement('canvas');
  canvas.width = 1200;
  canvas.height = 1200;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fffdf9';
  ctx.fillRect(0, 0, 1200, 1200);
  ctx.fillStyle = '#ffffff';
  roundRect(ctx, 48, 48, 1104, 1104, 56);
  ctx.fill();
  ctx.strokeStyle = '#fed7aa';
  ctx.lineWidth = 4;
  ctx.stroke();
  ctx.fillStyle = '#111827';
  ctx.font = 'bold 58px sans-serif';
  ctx.fillText('파이어맵', 110, 170);
  ctx.fillStyle = '#ea580c';
  ctx.font = 'bold 42px sans-serif';
  ctx.fillText('파이어맵 계산 결과', 110, 340);
  ctx.fillStyle = '#111827';
  ctx.font = 'bold 88px sans-serif';
  ctx.fillText(`${inputs.targetRetirementAge}세에 퇴사하면`, 110, 485);
  ctx.fillStyle = '#ff5a00';
  ctx.font = 'bold 118px sans-serif';
  ctx.fillText(`${runwayText(simulation)}까지`, 110, 640);
  ctx.fillStyle = '#111827';
  ctx.font = 'bold 86px sans-serif';
  ctx.fillText('버틸 수 있어요', 110, 760);
  ctx.fillStyle = '#6b7280';
  ctx.font = 'bold 40px sans-serif';
  ctx.fillText('자산 · 생활비 · 수익률 · 국민연금 기준', 110, 900);
  ctx.fillStyle = '#ff5a00';
  roundRect(ctx, 110, 985, 330, 70, 35);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 30px sans-serif';
  ctx.fillText('무료 계산하기', 170, 1031);
  ctx.fillStyle = '#9a3412';
  ctx.font = 'bold 28px sans-serif';
  ctx.fillText('retire-age-kr.pages.dev', 110, 1105);
  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 0.95));
}

export default function Share({ inputs, simulation, onBack }) {
  const [message, setMessage] = useState('');
  const resultLine = `${inputs.targetRetirementAge}세 퇴사 → ${runwayText(simulation)}까지`;
  const copyFallback = async (text, label) => {
    try {
      await navigator.clipboard.writeText(text);
      setMessage(label);
      setTimeout(() => setMessage(''), 1800);
    } catch {
      setMessage('복사가 막혀 있어요. 주소창에서 직접 복사해주세요.');
    }
  };
  const shareLink = async () => {
    const payload = { title: '파이어맵', url: BASE_URL };
    if (navigator.share) {
      try {
        await navigator.share(payload);
        setMessage('공유창을 열었어요');
        return;
      } catch (error) {
        if (error?.name === 'AbortError') return;
      }
    }
    await copyFallback(BASE_URL, '링크를 복사했어요');
  };
  const shareImage = async () => {
    const blob = await makeShareImage(inputs, simulation);
    const file = new File([blob], 'firemap-result.png', { type: 'image/png' });
    if (navigator.canShare?.({ files: [file] })) {
      await navigator.share({ files: [file], title: '파이어맵 계산 결과' });
      setMessage('이미지 공유창을 열었어요');
    } else {
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      setMessage('이미지를 새 창으로 열었어요. 길게 눌러 저장하세요.');
    }
  };
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="공유" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">공유</p>
        <h2>공유는 두 가지만 남겼어요</h2>
        <div className="fm-share-preview"><strong>{resultLine}</strong><p>이미지는 내 계산 결과, 링크는 앱 첫 화면을 공유해요.</p></div>
        <button className="fm-primary" type="button" onClick={shareImage}>결과 이미지 공유하기</button>
        <button className="fm-secondary" type="button" onClick={shareLink}>앱 링크 공유하기</button>
        {message && <div className="fm-toast">{message}</div>}
      </section>
      <section className="fm-card fm-info"><em>운영 안내</em><h2>개인정보·면책·문의</h2><p>입력값은 브라우저에서 계산됩니다. 결과 이미지는 사용자가 직접 공유할 때만 생성됩니다.</p><small>문의: <b>{CONTACT_EMAIL}</b></small></section>
    </main>
  );
}
