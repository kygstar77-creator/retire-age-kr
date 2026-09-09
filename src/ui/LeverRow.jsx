// DS-21 LeverRow — "이걸 하면 −N년" 한 줄 + 적용 버튼. ChooseFI 레버 3 문법. fm-goal-item 대체.
import { Button } from './Button.jsx';
const cx = (...a) => a.filter(Boolean).join(' ');

// items: [{key, tag, label, gain('−4년'|'+2년'), off, onApply}]
export function LeverList({ items = [], className = '' }) {
  return (
    <ul className={cx('ds-levers', className)}>
      {items.map((it) => (
        <li key={it.key || it.tag} className={cx('ds-lever', it.off && 'ds-lever--off')}>
          <span className="ds-lever__tag">{it.tag}</span>
          <span className="ds-lever__body">
            <span className="ds-lever__label">{it.label}</span>
            {it.gain && <span className={cx('ds-lever__gain', 'num', it.gainTone && `ds-lever__gain--${it.gainTone}`)}>{it.gain}</span>}
          </span>
          {!it.off && it.onApply && <Button variant="tint" size="sm" onClick={it.onApply}>적용</Button>}
        </li>
      ))}
    </ul>
  );
}
