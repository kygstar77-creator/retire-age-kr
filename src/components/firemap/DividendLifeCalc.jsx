import { useState } from 'react';
import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';

const won = (manwon) => manwon * 10000;

export default function DividendLifeCalc({ inputs, onChange, onMove, onBack }) {
  const [assetManwon, setAssetManwon] = useState(Math.round((inputs?.financialAsset || 300000000) / 10000));
  const [yieldX10, setYieldX10] = useState(40); // 4.0% (0.1% 단위)
  const [contribManwon, setContribManwon] = useState(50); // 월 적립 50만원
  const [growthPct, setGrowthPct] = useState(0); // 매년 적립액 증액률
  const [years, setYears] = useState(10); // 적립 기간(년)
  const yieldPct = yieldX10 / 10;
  const asset = won(assetManwon);
  const annual = asset * (yieldPct / 100);
  const monthlyPre = annual / 12;
  const afterTaxRate = 0.846; // 배당소득세 15.4% 원천징수
  const monthlyAfter = (annual * afterTaxRate) / 12;
  const withdraw4 = (asset * 0.04) / 12; // 월 4% 인출(세전 대략)
  const livingCost = inputs?.monthlyLivingCost || 0;
  const coverage = livingCost > 0 ? Math.round((monthlyAfter / livingCost) * 100) : null;
  const need = (targetMonthlyWon) => (yieldPct > 0 ? (targetMonthlyWon * 12) / ((yieldPct / 100) * afterTaxRate) : 0);
  const over2000 = annual > 20000000;
  const over1000 = annual > 10000000;

  // 적립 시뮬레이션: 매월 적립 + 매년 적립액 증액, 배당 재투자(연 yieldPct%) 가정
  const futureAsset = (() => {
    const r = (yieldPct / 100) / 12;
    const base = won(contribManwon);
    let a = asset;
    for (let y = 0; y < years; y += 1) {
      const m = base * Math.pow(1 + growthPct / 100, y);
      for (let k = 0; k < 12; k += 1) a = a * (1 + r) + m;
    }
    return a;
  })();
  const totalContrib = (() => {
    const base = won(contribManwon);
    let t = 0;
    for (let y = 0; y < years; y += 1) t += base * Math.pow(1 + growthPct / 100, y) * 12;
    return t;
  })();
  const futureAnnual = futureAsset * (yieldPct / 100);
  const futureMonthlyAfter = (futureAnnual * afterTaxRate) / 12;
  const futureCoverage = livingCost > 0 ? Math.round((futureMonthlyAfter / livingCost) * 100) : null;

  const appliedMonthly = Math.round(monthlyAfter);
  const isApplied = appliedMonthly > 0 && Math.round(Number(inputs?.partTimeIncomeAfterRetirement) || 0) === appliedMonthly;
  const apply = () => {
    if (onChange) onChange('partTimeIncomeAfterRetirement', appliedMonthly);
    if (onMove) onMove('result');
  };
  const unapply = () => { if (onChange) onChange('partTimeIncomeAfterRetirement', 0); };

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="파이어 후 현금흐름" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">파이어 후 현금흐름</p>
        <h2>배당으로 매달 얼마 받을 수 있을까?</h2>
        <p>보유 자산·배당률로 월 배당(세전·세후)을 계산하고, <b>배당만 받기 vs 자산 인출(매도)</b>도 비교해요. 금융소득 종합과세·건보료 경고까지.</p>
      </section>

      <section className="fm-card">
        <div className="fm-dl-field">
          <div className="fm-dl-head"><span>배당 투자 자산</span><b>{formatWon(asset)}</b></div>
          <input type="range" min="0" max="300000" step="1000" value={assetManwon} onChange={(e) => setAssetManwon(Number(e.target.value))} />
        </div>
        <div className="fm-dl-presets">
          {[{ l: 'S&P500', v: 13 }, { l: 'SCHD', v: 37 }, { l: '한국 고배당', v: 50 }, { l: 'JEPI', v: 84 }].map((pr) => (
            <button type="button" key={pr.l} className={yieldX10 === pr.v ? 'on' : ''} onClick={() => setYieldX10(pr.v)}>{pr.l} {(pr.v / 10).toFixed(1)}%</button>
          ))}
        </div>
        <p className="fm-dl-preset-note">SCHD=배당성장(상승 참여) · JEPI=고배당이지만 상승 제한. 높은 배당률이 늘 유리한 건 아니에요. (배당률 참고치)</p>
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
        <h2 className="fm-section-title">배당만 받기 vs 자산 인출(매도)</h2>
        <p className="fm-section-sub">같은 자산({formatWon(asset)})으로 비교 · 배당 논쟁의 다른 답</p>
        <div className="fm-dl-cmp">
          <div><small>배당만 (원금 유지)</small><b>월 {formatWon(monthlyAfter)}</b><em>평생</em></div>
          <div><small>4% 정률 인출(매도)</small><b>월 약 {formatWon(withdraw4)}</b><em>평생 유지</em></div>
          <div><small>4% 정액(물가연동)</small><b>월 {formatWon(withdraw4)}</b><em>약 30년</em></div>
        </div>
        <p className="fm-dl-note">정률 인출은 자산이 줄면 인출도 줄어 고갈 위험이 낮아요. 정액(물가연동)은 4% 룰 기준 약 30년 버팀. 절세는 연금계좌 비과세 원금부터 인출하는 게 유리해요. 매도 인출 세금은 계좌·상품별로 달라요(일반 정보).</p>
      </section>

      <section className="fm-card">
        <h2 className="fm-section-title">매달 적립하면 {years}년 뒤엔?</h2>
        <p className="fm-section-sub">매월 적립 + 매년 적립액 증액 · 배당 재투자(연 {yieldPct.toFixed(1)}%) 가정</p>
        <div className="fm-dl-field">
          <div className="fm-dl-head"><span>월 적립금</span><b>{formatWon(won(contribManwon))}</b></div>
          <input type="range" min="0" max="500" step="10" value={contribManwon} onChange={(e) => setContribManwon(Number(e.target.value))} />
        </div>
        <div className="fm-dl-field">
          <div className="fm-dl-head"><span>적립액 매년 증액률</span><b>{growthPct}%</b></div>
          <input type="range" min="0" max="15" step="1" value={growthPct} onChange={(e) => setGrowthPct(Number(e.target.value))} />
        </div>
        <div className="fm-dl-field">
          <div className="fm-dl-head"><span>적립 기간</span><b>{years}년</b></div>
          <input type="range" min="1" max="40" step="1" value={years} onChange={(e) => setYears(Number(e.target.value))} />
        </div>

        <div className="fm-dl-out">
          <div><small>{years}년 후 자산</small><b>{formatWon(futureAsset)}</b></div>
          <div className="hi"><small>{years}년 후 월 배당(세후)</small><b>{formatWon(futureMonthlyAfter)}</b></div>
        </div>
        <p className="fm-dl-cover">
          이 기간 내 돈으로 넣는 적립 원금은 총 {formatWon(totalContrib)}
          {futureCoverage != null ? <> · 그때 세후 배당이 지금 생활비의 <b>{futureCoverage}%</b></> : null}
        </p>
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

      {isApplied
        ? <button type="button" className="fm-city-cta on" onClick={unapply}>✓ 이 월배당이 결과에 반영됨 (파이어 후 소득) · 해제</button>
        : <button type="button" className="fm-city-cta" onClick={apply}>이 월배당을 파이어 후 소득으로 반영하기</button>}
      <p className="fm-dl-note">반영하면 세후 월배당이 <b>‘파이어 후 부업/기타 소득’</b>으로 들어가 결과의 인출 부담을 줄여요 (바꿔보기의 ‘파이어 후 부업 소득’과 같은 칸). 배당소득세 15.4%(지방세 포함) 원천징수 기준의 단순 계산이에요. 적립 시뮬레이션은 배당을 전액 재투자하고 수익률이 매년 일정하다는 가정의 추정치이며, 실제 수익률·세금·물가는 다를 수 있어요. 2,000만원 초과분은 종합과세로 실효세율이 더 높아질 수 있고, 특정 종목·상품 추천이 아닌 일반 정보입니다.</p>
    </main>
  );
}
