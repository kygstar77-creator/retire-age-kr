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
  const ctx = canvas.getContext('2d'); ctx.fillStyle = '#fff7ed'; ctx.fillRect(0, 0, 1200, 630);
  const gradient = ctx.createLinearGradient(0, 0, 1200, 630); gradient.addColorStop(0, '#1f2937'); gradient.addColorStop(0.55, '#ea580c'); gradient.addColorStop(1, '#fb923c');
  ctx.fillStyle = gradient; roundRect(ctx, 70, 70, 1060, 490, 42); ctx.fill();
  ctx.fillStyle = '#fed7aa'; ctx.font = 'bold 42px sans-serif'; ctx.fillText('파이어맵 계산 결과', 120, 155);
  ctx.fillStyle = '#ffffff'; ctx.font = 'bold 78px sans-serif'; ctx.fillText(`${inputs.targetRetirementAge}세 퇴사`, 120, 275); ctx.fillText(`${runwayText(simulation)}까지`, 120, 370);
  ctx.fillStyle = '#fff7ed'; ctx.font = 'bold 34px sans-serif'; ctx.fillText('생활비 줄이기 · 퇴사 후 월 100만 원 · 1년 더 근무 효과 비교', 120, 450);
  ctx.fillStyle = '#fed7aa'; ctx.font = 'bold 30px sans-serif'; ctx.fillText('retire-age-kr.pages.dev', 120, 510);
  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 0.95));
}

export default function Share({ inputs, simulation, onBack }) {
  const [message, setMessage] = useState('');
  const shareUrl = buildShareUrl(inputs);
  const shareText = `파이어맵 계산 결과\n${inputs.targetRetirementAge}세 퇴사 → ${runwayText(simulation)}까지\n퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.\n\n${BASE_URL}`;
  const copy = async (text, label) => { try { await navigator.clipboard.writeText(text); setMessage(label); setTimeout(() => setMessage(''), 1800); } catch { setMessage('복사 권한이 막혀 있어요. 직접 복사해주세요.'); } };
  const shareImage = async () => {
    const blob = await makeShareImage(inputs, simulation); const file = new File([blob], 'firemap-result.png', { type: 'image/png' });
    if (navigator.canShare?.({ files: [file] })) { await navigator.share({ files: [file], title: '파이어맵 계산 결과', text: '내 FIRE 결과 카드' }); setMessage('이미지 카드 공유창을 열었어요'); }
    else { const url = URL.createObjectURL(blob); window.open(url, '_blank'); setMessage('이미지 카드를 새 창으로 열었어요. 길게 눌러 저장하세요.'); }
  };
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="공유" onBack={onBack} />
      <section className="fm-card fm-text-card"><p className="fm-kicker">공유</p><h2>내 FIRE 결과 공유하기</h2><p>이미지로 저장하거나 링크로 공유할 수 있어요.</p><div className="fm-share-preview"><strong>{inputs.targetRetirementAge}세 퇴사 → {runwayText(simulation)}까지</strong><p>퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.</p></div><button className="fm-primary" type="button" onClick={shareImage}>결과 이미지 공유하기</button><button className="fm-secondary" type="button" onClick={() => copy(shareText, '결과 문구 복사됨')}>결과 문구 복사</button><button className="fm-secondary" type="button" onClick={() => copy(BASE_URL, '앱 기본 링크 복사됨')}>앱 기본 링크 복사</button><button className="fm-secondary" type="button" onClick={() => copy(shareUrl, '내 조건 링크 복사됨')}>내 조건 링크 복사</button>{message && <div className="fm-toast">{message}</div>}</section>
      <section className="fm-card fm-info"><em>운영 안내</em><h2>개인정보·면책·문의</h2><p>입력값은 서버로 전송하지 않고 이 브라우저에 저장됩니다. 본 서비스는 투자·세무·법률 자문이 아닌 참고용 계산입니다.</p><small>피드백·협업 문의: <b>{CONTACT_EMAIL}</b></small></section>
    </main>
  );
}
