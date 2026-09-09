// 인증 카드 시트 — 배당 투자자 모임 제목 공식(출생연도+가족+숫자+회차) · Reddit 댓글 6종(숫자·기간·가정) 포함.
// 카톡(og 이미지) · 링크 복사 · 카페 인증 게시판(제목 복사 + 카페 열기; 게시 API는 사장님 앱 등록 후 활성) · 방명록.
import { useState } from 'react';
import { Sheet, Button, Chips, Chip, toast } from '../../ui/index.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { shareToKakao } from '../../utils/kakaoShare.js';
import { sendCommunity } from '../../utils/firemapFeedbackApi.js';
import { survivalPhrase } from '../../firemap-v2/scenarios.js';
import { fetchUserRank } from '../../utils/firemapScoresApi.js';
import { track } from '../../firemap-v2/dailyData.js';
import { prefs } from '../../utils/prefs.js';
import { CAFE_URL } from '../../firemap-v2/links.js';

const FAMILY = ['1인', '2인', '3인', '4인+'];
const roundNo = () => { try { const f = Number(localStorage.getItem('fm_first_seen') || 0); if (!f) return 1; return Math.max(1, Math.floor((Date.now() - f) / (30.44 * 86400000)) + 1); } catch { return 1; } };

export function buildResultShare(simulation, extra = {}) {
  const ph = survivalPhrase(simulation);
  const earliest = simulation.earliestRetirementAge;
  const inp = simulation.inputs;
  const img = new URL('https://firemap.kr/og');
  if (earliest) img.searchParams.set('ea', String(earliest));
  img.searchParams.set('target', String(inp.targetRetirementAge));
  img.searchParams.set('rw', ph.runway);
  img.searchParams.set('ret', String(inp.annualReturnRate));
  img.searchParams.set('inf', String(inp.inflationRate));
  if (extra.pos && extra.tot) { img.searchParams.set('pos', String(extra.pos)); img.searchParams.set('tot', String(extra.tot)); }
  img.searchParams.set('v', 'c3');
  const l = new URL('https://firemap.kr/s');
  if (earliest) l.searchParams.set('ea', String(earliest));
  l.searchParams.set('target', String(inp.targetRetirementAge));
  l.searchParams.set('rwy', ph.runway);
  l.searchParams.set('ret', String(inp.annualReturnRate));
  l.searchParams.set('inf', String(inp.inflationRate));
  if (extra.pos && extra.tot) { l.searchParams.set('pos', String(extra.pos)); l.searchParams.set('tot', String(extra.tot)); }
  return { imageUrl: img.toString(), url: l.toString(), phrase: ph };
}

export default function ShareSheet({ open, onClose, simulation, onMove }) {
  const inp = simulation.inputs;
  const earliest = simulation.earliestRetirementAge;
  const year = new Date().getFullYear() - (Number(inp.currentAge) || 35);
  const [family, setFamily] = useState('1인');
  const [hideAmt, setHideAmt] = useState(false);
  const [busy, setBusy] = useState(false);
  const need = Math.round(simulation.requiredFireAssetByFourPercent || 0);
  const asset = Number(inp.financialAsset) || 0;
  const title = `${year}년생 ${family} · ${earliest ? `${earliest}세 파이어 가능` : '파이어 준비 중'} · ${hideAmt ? '자산 비공개' : `자산 ${formatWon(asset)}`} · ${roundNo()}회차`;
  const body = [
    `🔥 파이어 나이 ${earliest ? `${earliest}세` : '아직'} (목표 ${inp.targetRetirementAge}세)`,
    `필요 자산 ${formatWon(need)} · 현재 ${hideAmt ? '비공개' : formatWon(asset)}`,
    `월 저축 ${hideAmt ? '비공개' : formatWon(inp.monthlyInvestment)} · 파이어 후 생활비 ${formatWon(inp.monthlyLivingCost)}`,
    `가정: 수익률 ${inp.annualReturnRate}% · 물가 ${inp.inflationRate}% · 국민연금 ${inp.expectedPensionAge}세~`,
    '계산: firemap.kr'
  ].join('\n');

  const kakao = async () => {
    setBusy(true); track('share', { type: 'cert_kakao' });
    let pos, tot; try { const rr = await fetchUserRank(earliest); if (rr && rr.total) { pos = rr.position; tot = rr.total; } } catch { /* ignore */ }
    const s = buildResultShare(simulation, { pos, tot });
    try { await shareToKakao({ title: earliest ? `나는 ${earliest}세에 파이어 가능 🔥 — 파이어맵` : '내 파이어 나이 — 파이어맵', description: '물가·국민연금까지 따진 현실적인 파이어 계산 · 1분', imageUrl: s.imageUrl, linkUrl: s.url }); prefs.bumpCert(); }
    catch {
      if (navigator.share) { try { await navigator.share({ text: `${title}\n${body}`, url: s.url }); prefs.bumpCert(); } catch { /* ignore */ } }
      else { try { await navigator.clipboard.writeText(`${title}\n${body}\n${s.url}`); toast.good('카드 내용을 복사했어요'); } catch { /* ignore */ } }
    }
    setBusy(false);
  };
  const copyForCafe = async () => {
    track('share', { type: 'cert_cafe' });
    try { await navigator.clipboard.writeText(`${title}\n\n${body}`); toast.good('제목·본문을 복사했어요. 카페 인증 게시판에 붙여넣기!', { ms: 3200 }); } catch { toast.bad('복사가 안 됐어요'); }
    prefs.bumpCert();
    try { window.open(CAFE_URL, '_blank', 'noopener'); } catch { /* ignore */ }
  };
  const copyLink = async () => {
    const s = buildResultShare(simulation);
    try { await navigator.clipboard.writeText(s.url); toast.good('내 결과 링크를 복사했어요'); track('share', { type: 'cert_link' }); } catch { /* ignore */ }
  };
  const toWall = async () => {
    setBusy(true);
    const created = await sendCommunity(`🔥 ${title}`, null, 'goal', null);
    setBusy(false);
    if (created) { toast.good('방명록에 올렸어요'); prefs.bumpCert(); onClose(); if (onMove) onMove('wall'); }
    else toast.bad('잠시 후 다시 시도해 주세요');
  };

  return (
    <Sheet open={open} title="🪪 인증 카드" onClose={onClose}>
      <div className="ds-card ds-card--dark ds-p-3-5">
        <p className="ds-caption ds-mb-1-5">{title}</p>
        <p className="sc-cert-body">{body}</p>
      </div>
      <p className="ds-caption ds-mt-3 ds-mb-1-5">가족 형태</p>
      <Chips>{FAMILY.map((f) => <Chip key={f} on={family === f} onClick={() => setFamily(f)}>{f}</Chip>)}<Chip on={hideAmt} onClick={() => setHideAmt((v) => !v)}>🙈 금액 숨김</Chip></Chips>
      <p className="ds-caption ds-mt-2">카페 제목 공식(출생연도·가족·숫자·회차)이라 다른 인증 글과 나란히 비교돼요.</p>
      <div className="ds-stack ds-mt-3">
        <Button variant="primary" size="lg" full loading={busy} onClick={copyForCafe}>🟢 카페 인증 게시판에 올리기</Button>
        <div className="ds-bottomcta ds-mt-0">
          <Button variant="secondary" size="md" onClick={kakao}>💬 카톡</Button>
          <Button variant="secondary" size="md" onClick={copyLink}>🔗 링크</Button>
          <Button variant="secondary" size="md" onClick={toWall}>📝 방명록</Button>
        </div>
      </div>
    </Sheet>
  );
}
