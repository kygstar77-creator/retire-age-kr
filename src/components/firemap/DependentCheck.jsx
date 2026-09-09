// 파이어 후 건보료 — 결론(피부양자 유지/박탈 + 월 건보료) StatHero 위, 조건 입력 아래. TopBar는 FireMapMVP 도구 래퍼가 그려요.
import { useState } from 'react';
import { Card, SectionHead, RangeField, StatHero, Tabs, Chips, Chip, Notice, Button, toast } from '../../ui/index.js';
import { assessDependentEligibility, estimateLocalPremium, estimateBaristaPremium } from '../../firemap-v2/healthInsurance.js';
import { formatWon } from '../../firemap-v2/formatters.js';

const eok = (n) => formatWon(Math.round(n || 0));
const toMan = (won) => Math.round((Number(won) || 0) / 10000);

export default function DependentCheck({ inputs, onApply }) {
  const [other, setOther] = useState(0);          // 금융 외 소득(연, 원)
  const [fin, setFin] = useState(0);              // 금융소득(연, 원)
  const [prop, setProp] = useState(3);            // 재산세 과세표준(억)
  const [biz, setBiz] = useState(false);
  const [rental, setRental] = useState(false);
  const [mode, setMode] = useState('local');      // local 지역가입자 | barista 직장가입자 유지
  const [wage, setWage] = useState(1000000);      // 월 급여(원)

  const r = assessDependentEligibility({ otherIncomeManwon: toMan(other), financialIncomeManwon: toMan(fin), propertyTaxBaseEok: prop, hasBusinessIncome: biz, hasRentalIncome: rental });
  const est = estimateLocalPremium({ chargeableIncomeManwon: r.combinedIncome, propertyTaxBaseEok: prop });
  const bar = estimateBaristaPremium({ wageMonthlyManwon: toMan(wage), otherIncomeManwon: toMan(other), financialIncomeManwon: toMan(fin) });
  const saving = est.monthly - bar.monthly;
  const applyMonthly = mode === 'barista' ? bar.monthly : est.monthly;
  const applied = Number(inputs?.healthInsuranceEnabled) > 0;
  const appliedMonthly = Number(inputs?.monthlyHealthInsurance) || 0;
  const finMan = toMan(fin);

  // 판정 근거 — 해요체 한 줄씩
  const why = [];
  if (biz) why.push('사업자 소득이 있으면 바로 박탈돼요');
  if (rental) why.push('주택임대소득이 있으면 바로 박탈돼요');
  if (prop > 9) why.push('재산세 과표 9억을 넘으면 소득과 상관없이 박탈돼요');
  else if (prop > 5.4 && r.combinedIncome > 1000) why.push('재산 5.4억~9억 구간은 합산소득 1,000만원까지만 유지돼요');
  else if (r.combinedIncome > 2000) why.push('합산소득 2,000만원을 넘으면 박탈돼요');
  if (finMan > 1000) why.push('금융소득이 1,000만원을 넘어 전액 합산돼요');

  const hero = mode === 'local'
    ? {
      label: r.eligible ? '피부양자 유지 가능 · 지역가입자가 되면 월' : '피부양자 박탈 · 지역가입자로 바뀌면 월',
      value: eok(est.monthly),
      sub: r.eligible ? '지금은 0원이에요 · 소득·재산이 기준을 넘으면 이 금액을 내요' : '회사 없이 혼자 내는 건강보험이에요 · 재산도 같이 잡혀요',
      tiles: [
        { label: '소득 보험료', value: eok(est.incomeMonthly) },
        { label: '재산 보험료', value: eok(est.propMonthly) },
        { label: '합산소득 · 연', value: eok(r.combinedIncome * 10000) }
      ]
    }
    : {
      label: '바리스타 파이어면 월 건보료',
      value: eok(bar.monthly),
      sub: saving > 0 ? <>완전 은퇴보다 월 <b className="num">{eok(saving)}</b> 덜 내요 · 재산은 안 잡혀요</> : '이 조건에선 지역가입자가 더 유리할 수 있어요',
      tiles: [
        { label: '급여 보험료', value: eok(bar.wagePremium) },
        { label: '소득월액 보험료', value: bar.overThreshold ? eok(bar.incomePremium) : '0원' },
        { label: '완전 은퇴면', value: eok(est.monthly) }
      ]
    };

  return (
    <>
      <StatHero tone="dark" label={hero.label} value={hero.value} sub={hero.sub} tiles={hero.tiles} />

      <Tabs items={[{ key: 'local', label: '완전 은퇴' }, { key: 'barista', label: '☕ 바리스타 파이어' }]} value={mode} onChange={setMode} label="가입 형태" />

      <Card>
        <SectionHead size="sm" kicker="파이어 후 조건" title={mode === 'local' ? '소득과 재산을 넣어요' : '급여와 소득을 넣어요'} desc={mode === 'local' ? '1년 기준 · 금융소득은 1,000만원을 넘어야 합산돼요' : '파트타임으로 직장가입자를 유지하는 경우예요'} />
        {mode === 'barista' && <RangeField label="월 급여" value={wage} min={0} max={5000000} step={100000} money format={eok} chips={[100000, 500000, 1000000]} onChange={setWage} />}
        <RangeField label="금융 외 소득 · 연" value={other} min={0} max={50000000} step={1000000} money format={eok} chips={[1000000, 5000000, 10000000]} onChange={setOther} hint="임대·연금·사업 소득을 합쳐요" />
        <RangeField label="금융소득 · 연" value={fin} min={0} max={50000000} step={1000000} money format={eok} chips={[1000000, 5000000, 10000000]} onChange={setFin} hint="이자와 배당을 합쳐요" />
        {mode === 'local' && <RangeField label="재산세 과세표준" value={prop} min={0} max={20} step={0.5} format={(v) => `${Number(v) || 0}억`} onChange={setProp} hint="집·땅의 재산세 과세표준이에요 · 시세보다 낮아요" />}
        {mode === 'local' && (
          <Chips className="ds-mt-2">
            <Chip on={biz} onClick={() => setBiz(!biz)}>사업자 소득 있어요</Chip>
            <Chip on={rental} onClick={() => setRental(!rental)}>주택임대소득 있어요</Chip>
          </Chips>
        )}
      </Card>

      {mode === 'local' && (
        <Notice tone={r.eligible ? 'good' : 'warn'} icon={r.eligible ? '✅' : '⚠️'} title={r.eligible ? '피부양자 유지 가능' : '피부양자 박탈 가능'}>
          {why.length > 0 ? why.map((t) => <p key={t} className="ds-caption ds-mb-0">{t}</p>) : <p className="ds-caption ds-mb-0">지금 조건이면 기준 안이에요</p>}
        </Notice>
      )}
      {mode === 'barista' && (
        <Notice tone="accent" icon="☕">
          직장가입자라 재산은 건보료에 안 잡혀요 · 금융소득 외 소득이 <b className="num">2,000만원</b>을 넘는 부분부터 추가돼요
        </Notice>
      )}

      {applied
        ? <Button variant="secondary" size="md" full onClick={() => { onApply({ healthInsuranceEnabled: 0, monthlyHealthInsurance: 0 }); toast('건보료 반영을 해제했어요'); }}>✓ 반영 중 · 월 {eok(appliedMonthly)} · 해제</Button>
        : <Button variant="primary" size="md" full onClick={() => { onApply({ healthInsuranceEnabled: 1, monthlyHealthInsurance: applyMonthly }); toast.good('건보료를 반영했어요. 결과 숫자가 바뀌어요'); }}>월 {eok(applyMonthly)} 내 파이어 계산에 반영</Button>}

      <p className="ds-caption ds-textcenter">2026 요율 기준 추정이에요 · 정확한 금액은 건강보험공단에서 확인해요</p>
      <p className="ds-caption ds-textcenter">참고용 계산이에요 · 투자 자문이 아니에요</p>
    </>
  );
}
