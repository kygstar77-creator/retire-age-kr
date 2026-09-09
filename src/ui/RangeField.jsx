// DS-11 RangeField — 라벨 · 값(탭하면 직접 입력 Sheet) · 슬라이더 · 빠른 칩. RangeControl(140행) 정리본.
// 돈은 슬라이더 상한을 넘겨 직접 입력 가능. '초기화' 칩은 제거(값 0 리셋이 F1 빈 입력의 원인).
import { useState } from 'react';
import { Sheet } from './Sheet.jsx';
import { Button } from './Button.jsx';
import { Chips, Chip } from './Chip.jsx';
const cx = (...a) => a.filter(Boolean).join(' ');

const clean = (v) => Number(String(v ?? '').replace(/[^\d.-]/g, '')) || 0;
function niceStep(span) {
  const raw = span / 200;
  if (!(raw > 0)) return 1;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  for (const m of [1, 2, 5]) { if (m * mag >= raw) return m * mag; }
  return 10 * mag;
}
const chipLabel = (n) => (n >= 100000000 ? `+${n / 100000000}억` : `+${n / 10000}만`);

// label · value · min · max · step · format(fn) · chips[] · onChange · money(상한 해제) · hint · required(0이면 경고)
export function RangeField({ label, value, min = 0, max = 100, step, format = (v) => String(v), chips = [], onChange, money = false, hint, required = false, className = '' }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');
  const numeric = clean(value);
  const upper = money ? Infinity : max;
  const sliderValue = Math.max(min, Math.min(max, numeric));
  const pct = max > min ? ((sliderValue - min) / (max - min)) * 100 : 0;
  const sliderStep = step || (money ? niceStep(max - min) : 1);
  const empty = required && numeric <= 0;
  const commit = () => { onChange(Math.max(min, Math.min(upper, clean(draft)))); setEditing(false); };
  return (
    <div className={cx('ds-range', empty && 'ds-range--empty', className)}>
      <div className="ds-range__head">
        <span className="ds-range__label">{label}</span>
        <button type="button" className="ds-range__value num" onClick={() => { setDraft(String(Math.round(numeric))); setEditing(true); }} aria-label={`${label} 직접 입력`}>
          {format(numeric)}<span className="ds-range__edit">✎</span>
        </button>
      </div>
      <input aria-label={label} type="range" min={min} max={max} step={sliderStep} value={sliderValue} onChange={(e) => onChange(clean(e.target.value))} style={{ '--value': `${pct}%` }} />
      <div className="ds-range__scale num"><span>{format(min)}</span><span>{numeric > max ? '직접 입력' : format(max)}</span></div>
      {chips.length > 0 && (
        <Chips className="ds-range__chips">
          {chips.map((n) => <Chip key={n} onClick={() => onChange(Math.max(min, Math.min(upper, numeric + n)))}>{chipLabel(n)}</Chip>)}
        </Chips>
      )}
      {empty ? <p className="ds-range__hint ds-range__hint--warn">아직 0이에요. 대략이라도 넣어야 계산이 맞아요.</p> : (hint && <p className="ds-range__hint">{hint}</p>)}
      <Sheet open={editing} title={label} onClose={() => setEditing(false)}>
        <p className="ds-body-sm" style={{ margin: '0 0 10px' }}>{money ? '슬라이더 최댓값보다 큰 금액도 넣을 수 있어요.' : '숫자만 입력해요.'}</p>
        <input className="ds-input num" autoFocus inputMode="numeric" pattern="[0-9]*" value={draft} onChange={(e) => setDraft(e.target.value.replace(/[^0-9]/g, ''))} onKeyDown={(e) => { if (e.key === 'Enter') commit(); }} />
        <p className="ds-caption" style={{ margin: '6px 0 0' }}>= {format(clean(draft))}</p>
        <div className="ds-bottomcta">
          <Button variant="secondary" size="md" onClick={() => setEditing(false)}>취소</Button>
          <Button variant="primary" size="md" onClick={commit}>확인</Button>
        </div>
      </Sheet>
    </div>
  );
}
