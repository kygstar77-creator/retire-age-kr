// 퇴직금 계산기(/calc/severance) — 본진 밖 실험. 메뉴에 없고 검색으로만 들어온다(product-principles.md 2).
// 입력 항목 이름은 고용노동부 퇴직금 계산(moel.go.kr/retirementpayCal.do) 그대로. 식·근거: src/utils/severancePay.js
import { useMemo, useState } from 'react';
import { Card, SectionHead, RangeField, StatHero, Button, Fold, Tabs, Notice, Icon, ListGroup, ListRow, toast } from '../../ui/index.js';
import CoupangPick from './CoupangPick.jsx';
import { severancePay } from '../../utils/severancePay.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildSimulation, inputsIsReal } from '../../utils/retirementSimulator.js';
import { logEvent } from '../../utils/live.js';
import useCalcEvents from './useCalcEvents.js';

const BASIS_DATE = '2026-09-30';
const won = (n) => formatWon(Math.round(n || 0));
const exact = (n) => `${Math.floor(n || 0).toLocaleString('ko-KR')}원`;
const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const today = () => ymd(new Date());
const yearsAgo = (n) => { const d = new Date(); d.setFullYear(d.getFullYear() - n); return ymd(d); };
const validDate = (s) => /^\d{4}-\d{2}-\d{2}$/.test(s || '');

export default function SeveranceCalc({ inputs, onApply, onMove }) {
  const [hireDate, setHireDate] = useState(yearsAgo(3));
  const [retireDate, setRetireDate] = useState(today());
  const [monthly, setMonthly] = useState(3000000);
  const [bonus, setBonus] = useState(0);
  const [leave, setLeave] = useState(0);
  const [under15, setUnder15] = useState(false);

  const ok = validDate(hireDate) && validDate(retireDate) && retireDate > hireDate;
  const r = ok ? severancePay({ hireDate, retireDate, wages3m: monthly * 3, weeklyHours: under15 ? 14 : 40, annualBonus: bonus, annualLeavePay: leave }) : null;
  const years = r ? Math.floor(r.serviceDays / 365) : 0;
  const amount = r && r.eligible ? r.amount : 0;
  useCalcEvents('severance', [hireDate, retireDate, monthly, bonus, leave, under15], amount ? Math.min(10, Math.floor(amount / 10000000)) : null);

  // calc-3 숫자 줄(design/calc-3/spec.md 3): 저장된 내 입력이 있고 1년 이상 앞당겨질 때만. 기본값으로 낸 숫자는 남의 숫자라 그리지 않는다.
  const gainYears = useMemo(() => {
    if (!amount || !inputsIsReal(inputs)) return 0;
    try {
      const before = buildSimulation(inputs).earliestRetirementAge;
      const after = buildSimulation({ ...inputs, financialAsset: (Number(inputs?.financialAsset) || 0) + amount }).earliestRetirementAge;
      return before && after ? Math.max(0, before - after) : 0;
    } catch { return 0; }
  }, [inputs, amount]);

  const toRetire = () => {
    if (!r || !r.amount) return;
    const base = Number(inputs?.financialAsset) || 0;
    onApply({ financialAsset: base + r.amount });
    try { logEvent('severance_to_fire', { amount_bucket: Math.min(10, Math.floor(r.amount / 10000000)), gain_shown: gainYears >= 1 }); } catch { /* ignore */ }
    toast.good(`현재 자산에 퇴직금 ${exact(r.amount)}을 더했어요`);
    onMove(inputsIsReal(inputs) ? 'result' : 'question');
  };

  // 퇴사자 동선: 퇴직금 다음에 찾는 계산(회의 2026-09-30 배정). 제목은 그 화면 제목 그대로.
  const toNext = () => {
    try { logEvent('next_calc_click', { from: 'severance', to: 'unemployment' }); } catch { /* ignore */ }
    onMove('unemployment');
  };

  return (
    <>
      <StatHero
        tone="light" size="md" className="ds-hero--compact-tiles"
        label="예상 퇴직금 · 세전"
        value={r ? exact(r.amount) : '—'}
        sub={!ok ? '퇴직일자가 입사일자보다 뒤여야 해요'
          : !r.eligible ? (under15 ? '1주 소정근로시간 15시간 미만이면 퇴직금 대상이 아니에요' : '계속근로기간 1년 미만이면 퇴직금 대상이 아니에요')
          : <>재직 <b className="num">{r.serviceDays.toLocaleString()}</b>일{years > 0 ? ` · 약 ${years}년` : ''}</>}
        tiles={r ? [
          { label: '재직일수', value: `${r.serviceDays.toLocaleString()}일` },
          { label: '1일 평균임금', value: exact(r.dailyWage) },
          { label: '3개월 총일수', value: `${r.periodDays}일` }
        ] : undefined}
      >
        {gainYears >= 1 && (
          <p className="fm-gain">
            <span className="fm-gain__lead">퇴직금을 더하면</span>
            <span className="fm-gain__line">파이어 나이가 <span className="num">{gainYears}년</span> 앞당겨져요</span>
          </p>
        )}
      </StatHero>

      {r && r.amount > 0 && (
        <div>
          <Button variant="primary" size="lg" full onClick={toRetire}>이 돈이면 몇 살에 은퇴?</Button>
          <p className="ds-caption ds-mb-0 ds-mt-2">현재 자산 + 퇴직금 {exact(r.amount)}</p>
        </div>
      )}

      <Card>
        <SectionHead size="sm" kicker="퇴직금 계산기" title="입사일자 · 퇴직일자" desc="퇴직일자는 마지막으로 근무한 날의 다음 날이에요" />
        <label className="ds-range__label" htmlFor="sev-hire">입사일자</label>
        <input id="sev-hire" className="ds-input ds-mb-2" type="date" value={hireDate} max={retireDate} onChange={(e) => setHireDate(e.target.value)} />
        <label className="ds-range__label" htmlFor="sev-retire">퇴직일자</label>
        <input id="sev-retire" className="ds-input" type="date" value={retireDate} min={hireDate} onChange={(e) => setRetireDate(e.target.value)} />
        <Tabs className="ds-mt-2" label="1주 소정근로시간" value={under15 ? 'u' : 'o'} onChange={(k) => setUnder15(k === 'u')}
          items={[{ key: 'o', label: '1주 15시간 이상' }, { key: 'u', label: '1주 15시간 미만' }]} />
      </Card>

      <Card>
        <SectionHead size="sm" kicker="퇴직 전 3개월 임금" title="한 달 임금 · 세전" desc="기본급 + 기타수당" />
        <RangeField label="월 기본급 + 기타수당" value={monthly} min={0} max={10000000} step={100000} money format={won} chips={[100000, 500000, 1000000]} onChange={setMonthly} hint="퇴직 전 3개월 동안 매달 같게 받았다고 보고 계산해요" />
        <Fold title="상여금 · 연차수당" hint="있으면 3개월치(3/12)를 더해요">
          <RangeField label="연간상여금 총액" value={bonus} min={0} max={30000000} step={500000} money format={won} chips={[1000000, 5000000]} onChange={setBonus} />
          <RangeField label="연차수당" value={leave} min={0} max={5000000} step={50000} money format={won} chips={[100000, 500000]} onChange={setLeave} />
        </Fold>
      </Card>

      {r && r.amount > 0 && (
        <ListGroup label="다음 계산">
          <ListRow lead={<Icon name="calc" />} title="실업급여 계산기" desc="나이·피보험기간·월급으로 1일 구직급여액·총액" size="S" onClick={toNext} />
        </ListGroup>
      )}

      <Card variant="flat">
        <SectionHead size="sm" kicker="계산 방법" title="1일 평균임금 × 30일 × (재직일수 ÷ 365)" />
        <p className="ds-caption ds-mb-0">1일 평균임금 = 퇴직일 이전 3개월 임금총액 ÷ 그 기간의 총일수(근로기준법 제2조). 계속근로기간 1년에 대하여 30일분 이상의 평균임금(근로자퇴직급여 보장법 제8조). 계속근로기간 1년 미만이거나 1주 소정근로시간 15시간 미만이면 대상이 아니에요(같은 법 제4조).</p>
        <Notice tone="neutral" icon={<Icon name="alert" />} className="ds-mt-2">
          {BASIS_DATE} 기준 · 퇴직소득세를 빼기 전 금액이에요. 육아휴직 등 미산입기간과 통상임금 비교는 반영하지 않았어요. 정확한 금액은 고용노동부 퇴직금 계산에서 확인하세요.
        </Notice>
      </Card>

      <CoupangPick from="severance" />
    </>
  );
}
