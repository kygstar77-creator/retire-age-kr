// DS-19 StatHero — 화면의 '숫자 하나'. 결과·랭킹·역산·배당 상단이 전부 이 하나를 쓴다(fm-rank-hero 3벌 대체).
import { Stat, StatTiles } from './Stat.jsx';
const cx = (...a) => a.filter(Boolean).join(' ');

// label · value · unit · sub(한 줄) · delta{text,dir} · tiles[{label,value,unit,onClick}] · tone dark|light · children(하단)
export function StatHero({ label, value, unit, sub, delta, tiles, tone = 'dark', size = 'display', className = '', children }) {
  return (
    <section className={cx('ds-card', tone === 'dark' ? 'ds-card--dark' : 'ds-card--hero', 'ds-hero', className)}>
      <Stat label={label} value={value} unit={unit} delta={delta} size={size} />
      {sub && <p className="ds-hero__sub">{sub}</p>}
      {tiles && tiles.length > 0 && <StatTiles items={tiles} className="ds-hero__tiles" />}
      {children}
    </section>
  );
}
