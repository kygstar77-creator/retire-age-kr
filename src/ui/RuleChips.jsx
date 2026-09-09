// DS-22 RuleChips — 오늘 한 걸음 규칙 6개(Qapital 규칙 문법). 3열 grid, 각 칩 = 이모지·라벨·금액·(파이어 당김).
const cx = (...a) => a.filter(Boolean).join(' ');

// rules: [{key, emoji, label, amount, gain?}] · onPick(rule) · onCustom()
export function RuleChips({ rules = [], onPick, onCustom, className = '' }) {
  return (
    <div className={cx('ds-rules', className)}>
      {rules.map((r) => (
        <button type="button" key={r.key || r.label} className="ds-rule" onClick={() => onPick && onPick(r)}>
          <span className="ds-rule__emoji" aria-hidden="true">{r.emoji}</span>
          <span className="ds-rule__label">{r.label}</span>
          <span className="ds-rule__amount num">+{Math.round(r.amount / 10000)}만</span>
          {r.gain && <span className="ds-rule__gain num">⏱ {r.gain}</span>}
        </button>
      ))}
      {onCustom && (
        <button type="button" className="ds-rule ds-rule--custom" onClick={onCustom}>
          <span className="ds-rule__emoji" aria-hidden="true">✏️</span>
          <span className="ds-rule__label">직접 입력</span>
          <span className="ds-rule__amount">금액</span>
        </button>
      )}
    </div>
  );
}
