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

function drawFlame(ctx, x, y, scale = 1) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);
  const flame = ctx.createLinearGradient(0, 0, 0, 76);
  flame.addColorStop(0, '#ff8a00');
  flame.addColorStop(1, '#ff4d00');
  ctx.fillStyle = flame;
  ctx.beginPath();
  ctx.moveTo(44, 4);
  ctx.bezierCurveTo(88, 42, 86, 92, 44, 104);
  ctx.bezierCurveTo(7, 94, 2, 51, 28, 24);
  ctx.bezierCurveTo(26, 47, 47, 50, 44, 4);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = '#ffd166';
  ctx.beginPath();
  ctx.moveTo(47, 43);
  ctx.bezierCurveTo(64, 61, 62, 90, 43, 96);
  ctx.bezierCurveTo(27, 88, 27, 66, 41, 53);
  ctx.bezierCurveTo(39, 65, 52, 67, 47, 43);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

async function makeShareImage(inputs, simulation) {
  const canvas = document.createElement('canvas');
  canvas.width = 1200;
  canvas.height = 1200;
  const ctx = canvas.getContext('2d');
  const runway = runwayText(simulation);

  ctx.fillStyle = '#fff7ed';
  ctx.fillRect(0, 0, 1200, 1200);

  ctx.fillStyle = '#ffffff';
  roundRect(ctx, 58, 58, 1084, 1084, 52);
  ctx.fill();
  ctx.strokeStyle = '#fed7aa';
  ctx.lineWidth = 4;
  ctx.stroke();

  drawFlame(ctx, 106, 112, 0.72);
  ctx.fillStyle = '#111827';
  ctx.font = '700 46px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText('파이어맵', 184, 170);

  ctx.fillStyle = '#ea580c';
  ctx.font = '800 42px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText('파이어맵 계산 결과', 110, 330);

  ctx.fillStyle = '#111827';
  ctx.font = '800 82px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText(`${inputs.targetRetirementAge}세에 퇴사하면`, 110, 474);

  ctx.fillStyle = '#ff5a00';
  ctx.font = '900 118px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText(`${runway}까지`, 110, 628);

  ctx.fillStyle = '#111827';
  ctx.font = '800 82px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText('버틸 수 있어요', 110, 752);

  ctx.fillStyle = '#6b7280';
  ctx.font = '700 36px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText('자산 · 생활비 · 수익률 · 국민연금 기준', 110, 902);

  ctx.fillStyle = '#ff5a00';
  roundRect(ctx, 110, 980, 326, 72, 36);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.font = '800 30px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText('무료 계산하기', 176, 1027);

  ctx.fillStyle = '#9a3412';
  ctx.font = '700 28px system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  ctx.fillText('retire-age-kr.pages.dev', 110, 1110);

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
      setMessage('복사가 막혀 있어요. 주소창에서 직접 복사해 주세요.');
    }
  };

  const shareLink = async () => {
    const payload = { title: '파이어맵', text: '내 돈은 몇 살까지 버틸 수 있을까?', url: BASE_URL };
    if (navigator.share) {
      try {
        await navigator.share(payload);
        setMessage('공유창을 열었어요');
        return;
      } catch (error) {
        if (error?.name === 'AbortError') return;
      }
    }
    await copyFallback(BASE_URL, '앱 링크를 복사했어요');
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
      setMessage('이미지를 새 창으로 열었어요. 길게 눌러 저장해 주세요.');
    }
  };

  return (
    <main className="fm-screen fm-scroll">
      <Header onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">공유</p>
        <h2>결과만 간단하게 공유해요</h2>
        <div className="fm-share-preview">
          <strong>{resultLine}</strong>
          <p>결과 이미지는 계산 결과만, 앱 링크는 첫 화면만 공유해요.</p>
        </div>
        <button className="fm-primary" type="button" onClick={shareImage}>결과 이미지 공유하기</button>
        <button className="fm-secondary" type="button" onClick={shareLink}>앱 링크 공유하기</button>
        {message && <div className="fm-toast">{message}</div>}
      </section>
      <section className="fm-card fm-info">
        <em>운영 안내</em>
        <h2>개인정보 · 면책 · 문의</h2>
        <p>입력값은 브라우저에서 계산돼요. 결과 이미지는 사용자가 직접 공유할 때만 생성돼요.</p>
        <small>문의: <b>{CONTACT_EMAIL}</b></small>
      </section>
    </main>
  );
}
