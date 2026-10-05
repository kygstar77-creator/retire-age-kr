// 대출이자 계산기(/calc/loan v1, dev만) — 시안 work/research/design/loan/spec.md(디자인 통과 7.0) · 기획 work/research/plans/loan.md.
// 숫자1 = 다 갚는 나이(지금 나이 + ⌊상환 개월 ÷ 12⌋), 행동1 = 이 돈이면 몇 살에 은퇴?. 식은 src/utils/loanRepay.js(부동산계산기.com 상환표 360회 일치).
// 화면 글자는 시안 가안 그대로 — copywriter 문구 시안(10/20)·editor-web 통과 전에는 검색 경로(TOOL_PAGES)에 올리지 않는다(#loan으로만 열림).
import { useEffect, useRef, useState } from 'react';
import { Card, RangeField, StatHero, Button, Tabs, Notice, Icon, ListGroup, ListRow, Fold, Sheet, Chip, toast } from '../../ui/index.js';
import { loanSchedule, compareMethods, extraEffect } from '../../utils/loanRepay.js';
import { inputsIsReal } from '../../utils/retirementSimulator.js';
import { logEvent } from '../../utils/live.js';
import useCalcEvents from './useCalcEvents.js';

const exact = (n) => `${Math.round(n || 0).toLocaleString('ko-KR')}원`;
// 큰 금액은 '억·만원' 내림(3,408만원 = 34,086,621원 내림, 시안 ② 끝)
const man = (v) => {
  const n = Math.max(0, Math.floor(v || 0));
  const e = Math.floor(n / 1e8);
  const m = Math.floor((n % 1e8) / 1e4);
  if (!e && !m) return exact(n);
  return `${e ? `${e}억${m ? ' ' : ''}` : ''}${m ? `${m.toLocaleString('ko-KR')}만` : ''}원`;
};
const manShort = (v) => (v >= 1e4 ? `${(v / 1e4).toLocaleString('ko-KR')}만원` : exact(v));
const METHODS = { equal: '원리금균등', principal: '원금균등', bullet: '만기일시' };
const EXAMPLE = { age: 35, principal: 300000000, rate: 4.5, years: 30, method: 'equal' }; // 기획서 예시와 같은 값
const extraBucket = (e) => [0, 100000, 300000, 500000, 1000000].filter((b) => e >= b).pop();

export default function LoanCalc({ inputs, onMove }) {
  const real = inputsIsReal(inputs);
  const [age, setAge] = useState(real ? Number(inputs?.currentAge) || EXAMPLE.age : EXAMPLE.age);
  const [principal, setPrincipal] = useState(EXAMPLE.principal);
  const [rate, setRate] = useState(EXAMPLE.rate);
  const [years, setYears] = useState(EXAMPLE.years);
  const [method, setMethod] = useState(EXAMPLE.method);
  const [extra, setExtra] = useState(100000);
  const [edit, setEdit] = useState(null); // 'age' | 'loan'
  const touched = useRef(false);

  const loan = { principal, annualRate: rate, months: years * 12, method };
  const base = loanSchedule(loan);
  const fx = extraEffect(loan, extra);
  const ageAt = (months) => age + Math.floor(months / 12);
  const endAge = ageAt(base.months);
  const goal = Number(inputs?.targetRetirementAge) || 0;
  const isExample = !real && age === EXAMPLE.age && principal === EXAMPLE.principal && rate === EXAMPLE.rate && years === EXAMPLE.years && method === EXAMPLE.method;
  useCalcEvents('loan', [age, principal, rate, years, method], Math.min(20, Math.floor(base.firstPayment / 500000)));

  // 슬라이더는 놓고 1.5초 멈췄을 때 한 번(값은 구간만)
  useEffect(() => {
    if (!touched.current) return undefined;
    const t = setTimeout(() => { try { logEvent('loan_extra', { bucket: extraBucket(extra) }); } catch { /* ignore */ } }, 1500);
    return () => clearTimeout(t);
  }, [extra]);

  const closeEdit = () => { try { logEvent('loan_edit', { row: edit }); } catch { /* ignore */ } setEdit(null); };
  const toRetire = () => {
    try { logEvent('loan_retire_click', { age_bucket: Math.floor(endAge / 5) * 5 }); } catch { /* ignore */ }
    onMove(real ? 'result' : 'question');
  };
  const share = async () => {
    const url = 'https://firemap.kr/calc/loan';
    const text = `다 갚는 나이 ${endAge}세${extra > 0 ? ` · 매달 ${manShort(extra)} 더 → ${ageAt(fx.withExtra.months)}세` : ''}`;
    try { logEvent('loan_share', {}); } catch { /* ignore */ }
    try {
      if (navigator.share) await navigator.share({ title: '대출이자 계산기', text, url });
      else { await navigator.clipboard.writeText(`${text}\n${url}`); toast.good('주소를 복사했어요'); }
    } catch { /* 닫음 */ }
  };

  const goalLine = real && goal > 0
    ? (endAge > goal ? `은퇴 목표 ${goal}세 뒤에도 ${endAge - goal}년 더 갚아요` : `은퇴 목표 ${goal}세 전에 끝나요`)
    : null;
  const label = <>다 갚는 나이{isExample && <Chip className="ds-loan__ex">예시</Chip>}</>;

  return (
    <div className="ds-col-560 ds-salary-v5 ds-loan">
      <StatHero label={label} value={`${endAge}세`}
        sub={<><span className="ds-nw">매달 {exact(base.firstPayment)}</span> · <span className="ds-nw">총이자 {man(base.totalInterest)}</span></>}>
        {goalLine && <p className="ds-hero__sub ds-loan__goal">{goalLine}</p>}
      </StatHero>

      <ListGroup className="ds-cond">
        <ListRow title="지금 나이" trail={`${age}세`} size="M" onClick={() => setEdit('age')} />
        <ListRow title="대출 조건" trail={`${man(principal)} · ${rate}% · ${years}년`} size="M" onClick={() => setEdit('loan')} />
      </ListGroup>

      <Card className="ds-loan__extra">
        <RangeField label="매달 더 갚기" value={extra} min={0} max={1000000} step={10000} format={(v) => (v ? manShort(v) : '0원')}
          onChange={(v) => { touched.current = true; setExtra(Math.round(v / 10000) * 10000); }} />
        <p className="ds-loan__out">{extra > 0 && fx.monthsSaved >= 0
          ? <><span className="ds-nw"><b>{ageAt(fx.withExtra.months)}세</b>에 끝나요</span> · <span className="ds-nw">{fx.monthsSaved}개월 일찍</span> · <span className="ds-nw">이자 {man(fx.interestSaved)} 덜</span></>
          : '움직이면 다 갚는 나이가 바뀌어요'}</p>
      </Card>

      <Button variant="primary" size="lg" full onClick={toRetire}>이 돈이면 몇 살에 은퇴?</Button>

      <Fold title="상환 방식별 총이자">
        <ListGroup>
          {compareMethods(loan).map((m) => <ListRow key={m.method} title={METHODS[m.method]} trail={man(m.totalInterest)} chevron={false} size="S" />)}
        </ListGroup>
      </Fold>
      <Fold title="매달 상환표" hint={`${fx.withExtra.months}회`}>
        <ListGroup>
          {fx.withExtra.rows.slice(0, 12).map((r) => <ListRow key={r.month} title={`${r.month}회 · 이자 ${exact(r.interest)}`} trail={exact(r.payment)} chevron={false} size="S" />)}
          {fx.withExtra.months > 12 && <ListRow title={`… ${fx.withExtra.months}회 · 남은 원금 0원`} trail={exact(fx.withExtra.lastPayment)} chevron={false} size="S" />}
        </ListGroup>
      </Fold>
      <Fold title="계산 방법">
        {/* [카피 몫] 문구 최종은 copywriter·editor-web */}
        <p className="ds-caption">월 이자 = 남은 원금 × 연 금리 ÷ 12. 총이자는 상환표 매달 이자의 합이에요. 중도상환수수료는 빼고 계산해요.</p>
        <Notice tone="neutral" icon={<Icon name="alert" />} className="ds-mt-2">
          참고용{isExample ? ' · 예시 값' : ''} · 실제 대출 조건은 은행마다 달라요 · <a className="ds-link ds-link--muted" href="/disclaimer">면책 안내</a>
        </Notice>
      </Fold>

      <button type="button" className="ds-link ds-link--muted ds-loan__share" onClick={share}>결과 공유</button>

      <Sheet open={edit === 'age'} title="지금 나이" onClose={closeEdit}>
        <RangeField label="지금 나이" value={age} min={19} max={80} step={1} format={(v) => `${Math.round(v)}세`} onChange={(v) => setAge(Math.round(v))} />
      </Sheet>
      <Sheet open={edit === 'loan'} title="대출 조건" onClose={closeEdit}>
        <RangeField label="대출 금액" value={principal} min={0} max={1000000000} step={10000000} money format={man} chips={[10000000, 100000000]} onChange={setPrincipal} />
        <RangeField label="연 금리" value={rate} min={0} max={15} step={0.01} format={(v) => `${Math.round(v * 100) / 100}%`} onChange={(v) => setRate(Math.round(v * 100) / 100)} />
        <RangeField label="기간" value={years} min={1} max={50} step={1} format={(v) => `${Math.round(v)}년`} onChange={(v) => setYears(Math.max(1, Math.round(v)))} />
        <Tabs className="ds-mt-4" label="상환 방식" value={method} onChange={setMethod}
          items={Object.entries(METHODS).map(([key, l]) => ({ key, label: l }))} />
      </Sheet>
    </div>
  );
}
