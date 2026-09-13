// DS-28 IndexRow — 지표 한 줄(라벨 · 값 · 변화). 소식·지표 카드에서 쓰는 촘촘한 목록형 Stat.
export function IndexRow({ label, value, unit, delta, deltaLabel, sub }) {
  const dir = delta == null ? null : (String(delta).startsWith('+') ? 'up' : (String(delta).startsWith('-') ? 'down' : 'flat'));
  return (
    <div className="ds-idx">
      <span className="ds-idx__label">{label}{sub ? <span className="ds-idx__sub">{sub}</span> : null}</span>
      <span className="ds-idx__value num">{value}{unit ? <span className="ds-idx__unit">{unit}</span> : null}</span>
      {delta != null && <span className={`ds-idx__delta num ds-idx__delta--${dir}`}>{delta}{deltaLabel ? <span className="ds-idx__dl">{deltaLabel}</span> : null}</span>}
    </div>
  );
}
