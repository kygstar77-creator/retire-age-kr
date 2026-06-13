import { useState } from 'react';
import Header from './Header.jsx';
import { BASE_URL, CONTACT_EMAIL } from '../../firemap-v2/data.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { buildScenarioShareUrl, buildShareText } from '../../utils/shareState.js';
import { survivalPhrase } from '../../firemap-v2/scenarios.js';
import { makeShareImage } from '../../utils/shareImage.js';

// 공유 이미지 생성은 utils/shareImage.js로 분리(결과 화면에서도 재사용)

export default function Share({ inputs, simulation, onBack }) {
  const [message, setMessage] = useState('');
  const rank = statsRank(simulation);
  const phrase = survivalPhrase(simulation);
  const earliest = simulation.earliestRetirementAge;
  const resultLine = earliest ? `나는 ${earliest}세에 퇴사 가능 · ${phrase.short}` : phrase.short;

  const flash = (text) => { setMessage(text); setTimeout(() => setMessage(''), 2000); };
  const copyFallback = async (text, label) => {
    try { await navigator.clipboard.writeText(text); flash(label); }
    catch { flash('복사가 막혀 있어요. 주소창에서 직접 복사해 주세요.'); }
  };

  const shareImage = async () => {
    const blob = await makeShareImage(inputs, simulation);
    const file = new File([blob], 'firemap-result.png', { type: 'image/png' });
    if (navigator.canShare?.({ files: [file] })) {
      await navigator.share({ files: [file], title: '내 퇴사 나이', text: resultLine });
      flash('결과 카드 공유창을 열었어요');
    } else {
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      flash('이미지를 새 창으로 열었어요. 길게 눌러 저장해 주세요.');
    }
  };

  const buildPreviewUrl = () => {
    const u = new URL(buildScenarioShareUrl(inputs));
    u.pathname = '/s';
    if (earliest) u.searchParams.set('ea', String(earliest));
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
        <h2>내 결과 공유하기</h2>
        <section className="fm-rank-hero fm-share-hero">
          <p className="fm-rank-label">내 퇴사 가능 나이 · {rank.ageBandLabel} 또래 기준</p>
          <div className="fm-rank-top">
            <span className="fm-rank-pct">{earliest ? `${earliest}세 퇴사 가능` : '조금만 더!'}</span>
          </div>
          <p className="fm-rank-line">{phrase.short}</p>
        </section>
        <div className="fm-share-actions">
          <button className="fm-share-btn fm-share-primary" type="button" onClick={shareImage}>
            <b>결과 카드 이미지</b><span>퇴사 나이·또래 비교만 — 금액은 안 담겨요</span>
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
        <p>입력값은 브라우저에서 계산돼요. 결과 카드엔 금액이 들어가지 않고, 조건 링크는 본인이 공유할 때만 만들어져요.</p>
        <small>문의: <b>{CONTACT_EMAIL}</b></small>
      </section>
    </main>
  );
}
