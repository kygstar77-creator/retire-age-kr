// DS-7 Stat · DS-8 StatTiles · DS-9 ProgressBar
const cx = (...a) => a.filter(Boolean).join(' ');

// value: 문자열/노드(숫자는 tabular) · unit: '세'|'원' · delta: {text, dir:'up'|'down'} · size: display|title|md|sm
export function Stat({ label, value, unit, delta, size = 'md', center = false, className = '' }) {
  return (
    <div className={cx('ds-stat', `ds-stat--${size}`, center && 'ds-stat--center', className)}>
      {label && <span className="ds-stat__label">{label}</span>}
      <span className="ds-stat__value">{value}{unit && <span className="ds-stat__unit">{unit}</span>}</span>
      {delta && <span className={cx('ds-stat__delta', delta.dir && `ds-stat__delta--${delta.dir}`)}>{delta.text}</span>}
    </div>
  );
}

// items: [{label, value, unit, onClick}] — 결과 화면 "타일 3"
export function StatTiles({ items = [], className = '' }) {
  return (
    <div className={cx('ds-tiles', className)} style={items.length !== 3 ? { gridTemplateColumns: `repeat(${Math.max(1, items.length)}, 1fr)` } : undefined}>
      {items.map((it, i) => {
        const inner = <Stat label={it.label} value={it.value} unit={it.unit} size="sm" center />;
        return it.onClick
          ? <button type="button" key={i} className="ds-tile ds-tile--btn" onClick={it.onClick}>{inner}</button>
          : <div key={i} className="ds-tile">{inner}</div>;
      })}
    </div>
  );
}

export function ProgressBar({ value = 0, max = 100, left, right, thin = false, tone, className = '' }) {
  const pct = Math.max(0, Math.min(100, (Number(value) / Math.max(1, Number(max))) * 100));
  return (
    <div className={cx('ds-progress', thin && 'ds-progress--thin', tone && `ds-progress--${tone}`, className)} role="progressbar" aria-valuenow={Math.round(pct)} aria-valuemin="0" aria-valuemax="100">
      {(left || right) && <div className="ds-progress__labels"><span>{left}</span><span>{right}</span></div>}
      <div className="ds-progress__track"><i className="ds-progress__fill" style={{ width: `${pct}%` }} /></div>
    </div>
  );
}
