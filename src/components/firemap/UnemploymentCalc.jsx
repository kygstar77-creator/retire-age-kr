// 실업급여(구직급여) 계산기(/calc/unemployment-benefit) — 퇴직금 계산기와 같은 본진 밖 실험. 메뉴에 없고 검색으로만 들어온다.
// 입력 이름은 고용24 실업급여 모의계산(간편·상용)과 고용보험법 용어 그대로. 식·근거: src/utils/unemploymentBenefit.js, work/research/calc-unemployment/spec.md
import { useState } from 'react';
import { Card, SectionHead, RangeField, StatHero, Button, Fold, Tabs, Notice, Icon, toast } from '../../ui/index.js';
import CoupangPick from './CoupangPick.jsx';
import { unemploymentBenefit, UB_2026 } from '../../utils/unemploymentBenefit.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { inputsIsReal } from '../../utils/retirementSimulator.js';
import { logEvent } from '../../utils/live.js';
import useCalcEvents from './useCalcEvents.js';

const BASIS_DATE = '2026-09-30';
const won = (n) => formatWon(Math.round(n || 0));
const exact = (n) => `${Math.floor(n || 0).toLocaleString('ko-KR')}원`;
const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const months = (m) => `${Math.floor(m / 12)}년 ${m % 12}개월`;

export default function UnemploymentCalc({ inputs, onApply, onMove }) {
  // 기본 이직일 = 오늘. 2027년에 2026-12-31로 몰래 고정하면 틀린 해의 상·하한을 조용히 보여 준다(레드팀 9/30) — 2026 밖이면 '계산 안 함' 문구.
  const [lastWorkDay, setLastWorkDay] = useState(ymd(new Date()));
  const [over50, setOver50] = useState(false);
  const [insuredMonths, setInsuredMonths] = useState(36);
  const [monthly, setMonthly] = useState(3000000);
  const [hours, setHours] = useState(8);

  const r = unemploymentBenefit({ lastWorkDay, monthlyWage: monthly, insuredMonths, over50, dailyHours: hours });
  const ok = r.supported;
  useCalcEvents('unemployment', [lastWorkDay, over50, insuredMonths, monthly, hours], ok && r.total ? Math.min(20, Math.floor(r.total / 1000000)) : null);
  const limit = !ok ? '—' : r.capped ? `상한 ${exact(r.capDaily)}` : r.floored ? `하한 ${exact(r.floorDaily)}` : '평균임금의 60%';

  const toRetire = () => {
    if (!ok || !r.total) return;
    const base = Number(inputs?.financialAsset) || 0;
    onApply({ financialAsset: base + r.total });
    try { logEvent('unemployment_to_fire', { amount_bucket: Math.min(20, Math.floor(r.total / 1000000)) }); } catch { /* ignore */ }
    toast.good(`현재 자산에 실업급여 ${exact(r.total)}을 더했어요`);
    onMove(inputsIsReal(inputs) ? 'result' : 'question');
  };

  return (
    <>
      <StatHero
        tone="light" size="md" className="ds-hero--compact-tiles"
        label="예상 실업급여 총액 · 구직급여"
        value={ok ? exact(r.total) : '—'}
        sub={ok ? `고용보험법 제45조·제46조·제50조 · ${BASIS_DATE} 기준` : '2026년 1월 1일 ~ 12월 31일에 이직한 경우만 계산해요'}
        tiles={ok ? [
          { label: '1일 구직급여액', value: exact(r.daily) },
          { label: '소정급여일수', value: `${r.days}일` },
          { label: '상한 · 하한', value: limit }
        ] : undefined}
      />

      <Card>
        <SectionHead size="sm" kicker="실업급여 계산기" title="이직일 · 나이" desc="이직일 현재 나이로 소정급여일수가 정해져요" />
        <label className="ds-range__label" htmlFor="ub-last">이직일</label>
        <input id="ub-last" className="ds-input" type="date" value={lastWorkDay} min={UB_2026.from} max={UB_2026.to} onChange={(e) => setLastWorkDay(e.target.value)} />
        <Tabs className="ds-mt-2" label="이직일 현재 연령" value={over50 ? 'o' : 'u'} onChange={(k) => setOver50(k === 'o')}
          items={[{ key: 'u', label: '50세 미만' }, { key: 'o', label: '50세 이상 · 장애인' }]} />
      </Card>

      <Card>
        <SectionHead size="sm" kicker="고용보험" title="피보험기간" desc="고용보험에 가입한 기간" />
        <RangeField label="피보험기간" value={insuredMonths} min={0} max={240} step={1} format={months} onChange={setInsuredMonths}
          hint="이직한 회사에서 가입한 기간이에요. 그 전 회사를 그만두고 3년 안에 옮겼다면 합쳐요(그때 구직급여를 받았으면 빼요)" />
      </Card>

      <Card>
        <SectionHead size="sm" kicker="이직 전 3개월 임금" title="월평균 임금 · 세전" desc="기본급 + 기타수당" />
        <RangeField label="월평균 임금" value={monthly} min={0} max={10000000} step={100000} money format={won} chips={[100000, 500000, 1000000]} onChange={setMonthly} hint="이직 전 3개월 동안 매달 같게 받았다고 보고 계산해요" />
        <Fold title="1일 소정근로시간" hint="8시간보다 짧으면 하한액이 낮아져요">
          <RangeField label="1일 소정근로시간" value={hours} min={1} max={8} step={1} format={(h) => `${h}시간`} onChange={setHours} />
        </Fold>
      </Card>

      {ok && r.total > 0 && (
        <Card variant="dark">
          <SectionHead size="sm" title="재취업 뒤, 몇 살에 은퇴할 수 있을까?" desc={`실업급여는 재취업 활동 기간에 받는 돈이에요. ${exact(r.total)}을 현재 자산에 더해 파이어 나이를 계산해요`} />
          <Button variant="primary" size="lg" full onClick={toRetire}>은퇴 나이 계산</Button>
        </Card>
      )}

      <Card variant="flat">
        <SectionHead size="sm" kicker="계산 방법" title="1일 구직급여액 × 소정급여일수" />
        <p className="ds-caption ds-mb-0">1일 구직급여액 = 기초일액(이직 전 3개월 임금총액 ÷ 그 기간의 총일수) × 60%(고용보험법 제45조·제46조). 기초일액 상한은 113,500원이라 1일 최대 68,100원(시행령 제68조). 하한은 이직일 최저임금 10,320원 × 1일 소정근로시간 × 80%, 8시간이면 66,048원. 소정급여일수는 이직일 현재 연령과 피보험기간에 따라 120~270일(제50조 별표 1), 장애인은 50세 이상으로 봐요.</p>
        <p className="ds-caption ds-mt-2 ds-mb-0">받으려면 이직일 이전 18개월 동안 피보험 단위기간이 합산 180일 이상이어야 해요(제40조). 전직·자영업을 하려고 그만두는 등 자기 사정으로 이직하면 수급자격이 없을 수 있어요(제58조).</p>
        <Notice tone="neutral" icon={<Icon name="alert" />} className="ds-mt-2">
          {BASIS_DATE} 기준 · 2026년 이직자 기준이에요. 통상임금 비교와 일용근로자·자영업자·예술인·노무제공자는 반영하지 않았어요. 정확한 금액은 고용24 실업급여 모의계산에서 확인하세요.
        </Notice>
      </Card>

      <CoupangPick from="unemployment" />
    </>
  );
}
