// 연봉 실수령 계산기(/calc/salary) — 퇴직금·실업급여와 같은 본진 밖 실험. 메뉴에 없고 검색으로만 들어온다.
// 입력 이름은 국세청 간이세액표 용어(월급여액·비과세·공제대상가족·8세 이상 20세 이하 자녀) 그대로. 식·근거: src/utils/salaryNet.js, work/research/calc-salary/spec.md
// 간이세액표(41KB)는 이 화면에서만 쓰니 FireMapMVP가 React.lazy로 따로 불러온다.
import { useState } from 'react';
import { Card, SectionHead, RangeField, StatHero, Button, Tabs, Notice, Icon, ListGroup, ListRow, toast } from '../../ui/index.js';
import CoupangPick from './CoupangPick.jsx';
import { salaryNet, SALARY_RULES } from '../../utils/salaryNet.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { inputsIsReal } from '../../utils/retirementSimulator.js';
import { logEvent } from '../../utils/live.js';

const won = (n) => formatWon(Math.round(n || 0));
const exact = (n) => `${Math.floor(n || 0).toLocaleString('ko-KR')}원`;

export default function SalaryCalc({ inputs, onApply, onMove }) {
  const [annual, setAnnual] = useState(40000000);
  const [nontax, setNontax] = useState(SALARY_RULES.mealNontaxMax);
  const [family, setFamily] = useState(1);
  const [kids, setKids] = useState(0);
  const [ratio, setRatio] = useState(100);

  const r = salaryNet({ annual, nontaxMonthly: nontax, family, kids: Math.min(kids, family - 1), ratio });
  const insurance = r.pension + r.health + r.ltc + r.employment;
  // 생활비 기본값: 본인이 넣은 값이 있으면 그것, 없으면 질문 화면 예시(Question.jsx EXAMPLE 250만원).
  // 앱 기본 300만원을 그대로 쓰면 연봉 4,000만원 실수령(약 293만원)에서 저축 0원이 돼 은퇴 연결이 막혔다(레드팀 10/1).
  const [living, setLiving] = useState(inputsIsReal(inputs) ? (Number(inputs?.monthlyLivingCost) || 2500000) : 2500000);
  const saving = Math.max(0, r.net - living);

  const toRetire = () => {
    onApply({ monthlyInvestment: saving, monthlyLivingCost: living });
    try { logEvent('salary_to_fire', { net_bucket: Math.min(20, Math.floor(r.net / 500000)) }); } catch { /* ignore */ }
    toast.good(`월 저축 ${exact(saving)}을 넣었어요`);
    onMove(inputsIsReal(inputs) ? 'result' : 'question');
  };
  const toNext = () => {
    try { logEvent('next_calc_click', { from: 'salary', to: 'severance' }); } catch { /* ignore */ }
    onMove('severance');
  };

  return (
    <>
      {/* F3 A안(design/salary-result, 10/1): 다크 결과 카드 숫자 하나 → 80/100/120% 칩(경쟁 5곳에 없음) → 주황 버튼 하나. 타일 값은 375px에서 붙지 않게 body-sm */}
      <StatHero
        className="ds-hero--compact-tiles"
        label="월 실수령액"
        value={exact(r.net)}
        sub={`연봉 ${won(annual)} · 비과세 월 ${won(nontax)} · 가족 ${family}명 · 자녀 ${Math.min(kids, family - 1)}명`}
        tiles={[
          { label: '연 실수령', value: won(r.netAnnual) },
          { label: '월 공제', value: exact(r.deductions) },
          { label: '세액표', value: `${ratio}%` }
        ]}
      >
        <Tabs className="ds-mt-4" label="원천징수 비율" value={String(ratio)} onChange={(k) => { setRatio(Number(k)); try { logEvent('salary_ratio', { ratio: Number(k) }); } catch { /* ignore */ } }}
          items={[{ key: '80', label: '80%' }, { key: '100', label: '100%' }, { key: '120', label: '120%' }]} />
        <p className="ds-hero__sub ds-mb-0">원천징수 비율 · 기본은 100%예요 · 회사에 신청하면 80% · 120%도 돼요</p>
      </StatHero>

      <div>
        <Button variant="primary" size="lg" full onClick={toRetire}>이 돈이면 몇 살에 은퇴?</Button>
        <p className="ds-caption ds-mb-0 ds-mt-2">{saving > 0
          ? `실수령 ${exact(r.net)}에서 생활비 ${exact(living)}을 빼고 남는 ${exact(saving)}을 월 저축으로 넣어 계산해요`
          : `실수령 ${exact(r.net)}이 생활비 ${exact(living)}보다 적어 월 저축 0원으로 계산해요`} · 생활비는 아래에서 바꿔요</p>
      </div>

      <Card>
        <SectionHead size="sm" kicker="연봉 실수령 계산기" title="연봉 · 비과세액" desc="연봉은 비과세액을 포함한 세전 금액이에요" />
        <RangeField label="연봉" value={annual} min={0} max={200000000} step={1000000} money format={won} chips={[1000000, 5000000, 10000000]} onChange={setAnnual} hint="퇴직금은 빼고 넣어요 · 12개월로 나눠 월급을 계산해요" />
        <RangeField label="비과세액 · 월" value={nontax} min={0} max={1000000} step={10000} money format={won} chips={[10000, 100000]} onChange={setNontax} hint="식대는 월 20만원 이하가 비과세예요" />
      </Card>

      <Card>
        <SectionHead size="sm" kicker="소득세" title="공제대상가족" desc="본인과 배우자도 각각 1명으로 세요" />
        <RangeField label="공제대상가족 수 · 본인 포함" value={family} min={1} max={11} step={1} format={(v) => `${Math.round(v)}명`} onChange={(v) => setFamily(Math.round(v))} />
        <RangeField label="8세 이상 20세 이하 자녀 수" value={Math.min(kids, family - 1)} min={0} max={Math.max(1, family - 1)} step={1} format={(v) => `${Math.round(v)}명`} onChange={(v) => setKids(Math.round(v))} hint="공제대상가족 수에 포함된 자녀예요" />
      </Card>

      <ListGroup label="한 달 공제 6가지">
        <ListRow title="국민연금 · 4.75%" trail={exact(r.pension)} chevron={false} size="S" />
        <ListRow title="건강보험 · 3.595%" trail={exact(r.health)} chevron={false} size="S" />
        <ListRow title="장기요양보험 · 건강보험료의 13.14%" trail={exact(r.ltc)} chevron={false} size="S" />
        <ListRow title="고용보험 · 0.9%" trail={exact(r.employment)} chevron={false} size="S" />
        <ListRow title={`소득세 · 간이세액표${ratio !== 100 ? ` ${ratio}%` : ''}`} trail={exact(r.incomeTax)} chevron={false} size="S" />
        <ListRow title="지방소득세 · 소득세의 10%" trail={exact(r.localTax)} chevron={false} size="S" />
        <ListRow title={<b>공제 합계</b>} trail={<b>{exact(r.deductions)}</b>} chevron={false} size="S" />
      </ListGroup>

      <Card>
        <SectionHead size="sm" kicker="은퇴 계산" title="한 달 생활비" />
        <RangeField label="한 달 생활비" value={living} min={500000} max={10000000} step={100000} money format={won} chips={[100000, 500000]} onChange={setLiving} />
      </Card>


      <ListGroup label="다음 계산">
        <ListRow lead={<Icon name="calc" />} title="퇴직금 계산기" desc="입사일·퇴직일·월급으로 예상 퇴직금" size="S" onClick={toNext} />
      </ListGroup>

      <CoupangPick from="salary" />

      <Card variant="flat">
        <SectionHead size="sm" kicker="계산 방법" title="월급 − 4대보험 − 소득세 − 지방소득세" />
        <p className="ds-caption ds-mb-0">소득세는 근로소득 간이세액표(소득세법 시행령 별표 2, 2026. 2. 27. 개정)의 월급여액(비과세 제외)·공제대상가족 수 해당란 세액이에요. 8세 이상 20세 이하 자녀는 1명 20,830원, 2명 45,830원, 3명부터 1명당 33,330원을 더 빼요. 국민연금은 기준소득월액(41만원~659만원)의 4.75%, 건강보험은 3.595%, 장기요양보험은 건강보험료의 13.14%, 고용보험은 0.9%예요. 10원 미만은 버려요.</p>
        <Notice tone="neutral" icon={<Icon name="alert" />} className="ds-mt-2">
          {SALARY_RULES.basisDate} 기준 · 참고용, 실제와 다를 수 있어요. 매달 떼는 세금은 연말정산으로 다시 맞춰요 · <a className="ds-link ds-link--muted" href="/disclaimer">면책 안내</a>
        </Notice>
      </Card>
    </>
  );
}
