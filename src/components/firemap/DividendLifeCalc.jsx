import { useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';

const won = (manwon) => manwon * 10000;

export default function DividendLifeCalc({ inputs, onChange, onMove, onBack }) {
  const [assetManwon, setAssetManwon] = useState(Math.round((inputs?.financialAsset || 300000000) / 10000));
  const [yieldX10, setYieldX10] = useState(40); // 4.0% (0.1% 단위)
  const yieldPct = yieldX10 / 10;
  const asset = won(assetManwon);
  const annual = asset * (yieldPct / 100);
  const monthlyPre = annual / 12;
  const afterTaxRate = 0.846; // 배당소득세 15.4% 원천징수
  const monthlyAfter = (annual * afterTaxRate) / 12;
  const livingCost = inputs?.monthlyLivingCost || 0;
  const coverage = livingCost > 0 ? Math.round((monthlyAfter / livingCost) * 100) : null;
  const need = (targetMonthlyWon) => (yieldPct > 0 ? (targetMonthlyWon * 12) / ((yieldPct / 100) * afterTaxRate) : 0);
  const over2000 = annual > 20000000;
  const over1000 = annual > 10000000;
  const apply = () => {
    if (onChange) onChange('partTimeIncomeAfterRetirement', Math.round(monthlyAfter));
    if (onMove) onMove('result');
  };

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="배당 생활" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">배당 파이어</p>
        <h2>배당으로 매달 얼마 받을 수 있을까?</h2>
        <p>보유 자산과 배당수익률로 월 배당(세전·세후)과, 목표 월배당에 필요한 원금을 계산해요.</p>
      </section>

      <section className="fm-card">
        <div className="fm-dl-field">
          <div className="fm-dl-head"><span>배당 투자 자산</span><b>{formatWon(asset)}</b></div>
          <input type="range" min="0" max="300000" step="1000" value={assetManwon} onChange={(e) => setAssetManwon(Number(e.target.value))} />
        </div>
        <div className="fm-dl-field">
          <div className="fm-dl-head"><span>배당수익률(세전)</span><b>{yieldPct.toFixed(1)}%</b></div>
          <input type="range" min="5" max="100" step="1" value={yieldX10} onChange={(e) => setYieldX10(Number(e.target.value))} />
        </div>

        <div className="fm-dl-out">
          <div><small>월 배당 (세전)</small><b>{formatWon(monthlyPre)}</b></div>
          <div className="hi"><small>월 배당 (세후 15.4%)</small><b>{formatWon(monthlyAfter)}</b></div>
        </div>
        {coverage != null && (
          <p className="fm-dl-cover">세후 배당이 지금 생활비({formatWon(livingCost)})의 <b>{coverage}%</b>를 충당해요{coverage >= 100 ? ' — 배당만으로 생활 가능!' : ''}</p>
        )}

        <div className={`fm-dl-warn ${over2000 ? 'no' : over1000 ? 'caution' : 'ok'}`}>
          {over2000
            ? <span>연 배당 {formatWon(annual)} · 금융소득 2,000만원 초과 → 종합과세 대상(누진 가산 가능) + 건보료 부담</span>
            : over1000
              ? <span>연 배당 {formatWon(annual)} · 1,000만원 초과 → 지역가입 시 건보료 부과소득 합산, 피부양자 자격 영향</span>
              : <span>연 배당 {formatWon(annual)} · 종합과세·건보료 경고선 아래예요</span>}
        </div>
      </section>

      <section className="fm-card">
        <h2 className="fm-section-title">월 OOO만원 받으려면 얼마 필요할까?</h2>
        <p className="fm-section-sub">세후 기준 · 배당수익률 {yieldPct.toFixed(1)}%로 계산</p>
        <div className="fm-dl-need">
          {[2000000, 3000000, 5000000].map((t) => (
            <div key={t}><small>월 {formatWon(t)}</small><b>{formatWon(need(t))}</b></div>
          ))}
        </div>
      </section>

      <button type="button" className="fm-city-cta" onClick={apply}>이 월배당을 퇴사 후 소득으로 반영하기</button>
      <p className="fm-dl-note">배당소득세 15.4%(지방세 포함) 원천징수 기준의 단순 계산이에요. 2,000만원 초과분은 종합과세로 실효세율이 더 높아질 수 있어요. 특정 종목·상품 추천이 아닌 일반 정보입니다.</p>
    </main>
  );
}
