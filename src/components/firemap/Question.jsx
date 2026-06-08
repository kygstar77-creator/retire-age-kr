import Header from './Header.jsx';
import PensionControls from './PensionControls.jsx';
import RangeControl from './RangeControl.jsx';
import { questions } from '../../firemap-v2/data.js';
import { cleanNumber } from '../../firemap-v2/formatters.js';

export default function Question({ step, inputs, onChange, onPrev, onNext }) {
  const question = questions[step];
  const value = cleanNumber(inputs[question.key]);
  const isAge = question.type === 'age';
  const isFinalQuestion = step === questions.length - 1;
  const progress = `${((step + 1) / questions.length) * 100}%`;

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
        <small>{isAge ? '손가락으로 움직여 1세 단위로 조절해요.' : `${question.unit} 단위로 조절해요.`}</small>
      </section>
      {isFinalQuestion && <PensionControls inputs={inputs} onChange={onChange} />}
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onPrev}>이전</button>
        <button type="button" onClick={onNext}>{isFinalQuestion ? '결과 보기' : '다음'}</button>
      </nav>
    </main>
  );
}
