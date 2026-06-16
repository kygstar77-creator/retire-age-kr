import { useState } from 'react';
import Header from './Header.jsx';
import RangeControl from './RangeControl.jsx';
import { questions } from '../../firemap-v2/data.js';
import { cleanNumber } from '../../firemap-v2/formatters.js';

export default function Question({ step, inputs, onChange, onPrev, onNext }) {
  const question = questions[step];
  const value = cleanNumber(inputs[question.key]);
  const isAge = question.type === 'age';
  const isFinalQuestion = step === questions.length - 1;
  const progress = `${((step + 1) / questions.length) * 100}%`;
  const isAsset = question.key === 'financialAsset';
  const [showMore, setShowMore] = useState(false);
  const reVal = cleanNumber(inputs.realEstateValue);
  const debtVal = cleanNumber(inputs.debt);
  const hasExtra = reVal > 0 || debtVal > 0;

  return (
    <main className="fm-screen fm-question-screen">
      <Header tag={`질문 ${step + 1}/${questions.length}`} />
      <div className="fm-progress"><i style={{ width: progress }} /></div>
      <section className="fm-card fm-question">
        <em>{question.label}</em>
        <h2>{question.title}</h2>
        <p>{question.helper}</p>
        <RangeControl
          label={question.label}
          value={value}
          inputKey={question.key}
          type={question.type}
          step={question.step}
          onChange={(nextValue) => onChange(question.key, nextValue)}
        />
        <small>{isAge ? '손가락으로 움직여 1세 단위로 조절해요.' : `${question.unit}로 조절해요.`}</small>

        {isAsset && (
          <div className="fm-asset-extra" style={{ marginTop: '14px', paddingTop: '14px', borderTop: '1px solid rgba(0,0,0,0.08)' }}>
            {(showMore || hasExtra) ? (
              <>
                <p className="fm-asset-extra-note" style={{ fontSize: '12px', color: 'var(--fm-muted, #6b6f76)', lineHeight: 1.6, margin: '0 0 12px' }}>부동산·부채는 <b>순자산·또래 비교</b>에만 반영돼요. 살고 있는 집은 매달 생활비를 만들지 못해서 <b>파이어 가능 나이 계산엔 넣지 않아요</b>. (안 적으면 0)</p>
                <RangeControl
                  label="부동산 (선택)"
                  value={reVal}
                  inputKey="realEstateValue"
                  type="money"
                  step={1000000}
                  onChange={(v) => onChange('realEstateValue', v)}
                />
                <RangeControl
                  label="부채 (선택)"
                  value={debtVal}
                  inputKey="debt"
                  type="money"
                  step={1000000}
                  onChange={(v) => onChange('debt', v)}
                />
              </>
            ) : (
              <button type="button" className="fm-asset-extra-toggle" onClick={() => setShowMore(true)} style={{ display: 'block', width: '100%', padding: '11px 14px', borderRadius: '10px', border: '1px dashed rgba(0,0,0,0.18)', background: 'transparent', color: 'var(--fm-accent, #ff5a00)', fontSize: '13px', fontWeight: 600, cursor: 'pointer' }}>+ 부동산·부채 추가 입력 (선택)</button>
            )}
          </div>
        )}
      </section>
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onPrev}>이전</button>
        <button type="button" onClick={onNext}>{isFinalQuestion ? '결과 보기' : '다음'}</button>
      </nav>
    </main>
  );
}
