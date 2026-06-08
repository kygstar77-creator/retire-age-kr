import { useState } from 'react';
import Header from './Header.jsx';
import PensionControls from './PensionControls.jsx';
import { questions } from '../../firemap-v2/data.js';
import { cleanNumber, formatValue, formatWon } from '../../firemap-v2/formatters.js';

export default function Question({ step, inputs, onChange, onPrev, onNext }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');
  const question = questions[step];
  const value = cleanNumber(inputs[question.key]);
  const isAge = question.type === 'age';
  const isFinalQuestion = step === questions.length - 1;
  const progress = `${((step + 1) / questions.length) * 100}%`;
  const changeBy = (amount) => onChange(question.key, Math.max(0, value + amount));
  const openDirectEdit = () => {
    setDraft(String(value));
    setEditing(true);
  };
  const confirmDirectEdit = () => {
    onChange(question.key, draft);
    setEditing(false);
  };

  return (
    <main className="fm-screen fm-question-screen">
      <Header tag={`질문 ${step + 1}/${questions.length}`} />
      <div className="fm-progress"><i style={{ width: progress }} /></div>
      <section className="fm-card fm-question">
        <em>{question.label}</em>
        <h2>{question.title}</h2>
        <p>{question.helper}</p>
        <div className="fm-stepper fm-stepper-display">
          <button type="button" onClick={() => changeBy(-question.step)}>-</button>
          <button type="button" className="fm-value-box" onClick={openDirectEdit}>{formatValue(value, question.type, question.key)}</button>
          <button type="button" onClick={() => changeBy(question.step)}>+</button>
        </div>
        {isAge ? <small>나이는 빠른 선택 버튼 없이 1세 단위로만 조절해요. 가운데 값을 누르면 직접 입력할 수 있어요.</small> : (
          <>
            <small>{question.unit}로 조절돼요. 가운데 금액을 누르면 직접 입력할 수 있어요.</small>
            <div className="fm-chips fm-preset-rail">
              {question.presets.map((preset) => <button type="button" key={preset} onClick={() => onChange(question.key, preset)}>{formatWon(preset)}</button>)}
            </div>
          </>
        )}
      </section>
      {isFinalQuestion && <PensionControls inputs={inputs} onChange={onChange} />}
      {editing && (
        <div className="fm-input-overlay" role="dialog" aria-modal="true" aria-label={`${question.label} 직접 입력`}>
          <div className="fm-input-sheet">
            <em>{question.label}</em>
            <h2>{question.title}</h2>
            <p>숫자만 입력해주세요. {isAge ? '나이는 세 단위예요.' : '금액은 원 단위로 저장돼요.'}</p>
            <input
              autoFocus
              inputMode="numeric"
              pattern="[0-9]*"
              value={draft}
              onChange={(event) => setDraft(event.target.value.replace(/[^0-9]/g, ''))}
              onKeyDown={(event) => { if (event.key === 'Enter') confirmDirectEdit(); if (event.key === 'Escape') setEditing(false); }}
            />
            <div className="fm-input-actions">
              <button type="button" onClick={() => setEditing(false)}>취소</button>
              <button type="button" onClick={confirmDirectEdit}>확인</button>
            </div>
          </div>
        </div>
      )}
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onPrev}>이전</button>
        <button type="button" onClick={onNext}>{step === questions.length - 1 ? '결과 보기' : '다음'}</button>
      </nav>
    </main>
  );
}
