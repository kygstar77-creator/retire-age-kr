// DS-21 LeverRow — "이걸 하면 −N년" 한 줄. 누르면 그 값이 들어간 채 바꿔보기가 열린다.
// 예전엔 줄마다 '적용' 버튼이 따로 있었는데, 바꿔보기가 탭으로 나오면서 같은 일을 두 곳에서 하게 돼 줄 자체를 버튼으로 합쳤다.
const cx = (...a) => a.filter(Boolean).join(' ');

// items: [{key, tag, label, gain('−4년'|'+2년'), off, onApply}]
export function LeverList({ items = [], className = '' }) {
  return (
    <ul className={cx('ds-levers', className)}>
      {items.map((it) => {
        const body = (
          <>
            <span className="ds-lever__tag">{it.tag}</span>
            <span className="ds-lever__body">
              <span className="ds-lever__label">{it.label}</span>
              {it.gain && <span className={cx('ds-lever__gain', 'num', it.gainTone && `ds-lever__gain--${it.gainTone}`)}>{it.gain}</span>}
            </span>
            {!it.off && it.onApply && <span className="ds-lever__chev" aria-hidden="true">›</span>}
          </>
        );
        return (
          <li key={it.key || it.tag} className={cx('ds-lever', it.off && 'ds-lever--off')}>
            {!it.off && it.onApply
              ? <button type="button" className="ds-lever__btn" onClick={it.onApply}>{body}</button>
              : body}
          </li>
        );
      })}
    </ul>
  );
}
