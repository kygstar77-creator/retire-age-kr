// 소식 — 지표 5개 · 파이어 후 하루 · 배당락 이번 주 · 소식 목록(자동 봇 글은 '자동' 배지). 개편 최종본 §3 소식.
// 지표는 참고만. 내 파이어 나이 계산엔 쓰지 않아요.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, Card, SectionHead, ListGroup, ListRow, Tabs, Badge, Button, Skeleton, EmptyState } from '../../ui/index.js';
import { sbRpc } from '../../utils/supabaseClient.js';
import { loadNews } from '../../utils/firemapFeedbackApi.js';
import { storyOfDay } from '../../firemap-v2/afterFireStories.js';
import { dayIdx } from '../../utils/dates.js';
import { CAFE_URL } from '../../firemap-v2/links.js';
import '../../ui/screens/news.css';

const CATS = [
  { key: 'all', label: '전체', emoji: '📰' },
  { key: 'news', label: '경제', emoji: '📈' },
  { key: 'ranking', label: '랭킹', emoji: '🏆' },
  { key: 'goal', label: '인증', emoji: '🔥' },
  { key: 'realestate', label: '부동산', emoji: '🏠' },
  { key: 'invest', label: '투자', emoji: '🌎' },
  { key: 'sidejob', label: '부업', emoji: '💼' },
  { key: 'pension', label: '연금·세금', emoji: '🏦' },
  { key: 'save', label: '저축', emoji: '💰' },
  { key: 'life', label: '파이어 후', emoji: '🏝️' }
];
const NEWS_CATS = new Set(CATS.map((c) => c.key).filter((k) => k !== 'all'));
const catMeta = (k) => CATS.find((c) => c.key === k) || CATS[0];
const AUTO_RE = /^\s*\[자동\]\s*/;
const isAuto = (r) => r.kind === 'auto' || AUTO_RE.test(String(r.title || ''));
const cleanTitle = (r) => String(r.title || '').replace(AUTO_RE, '').trim();

// 배당락 데이터는 있을 때만(파일이 없으면 조용히 숨김) — import.meta.glob은 파일이 없어도 빌드가 깨지지 않아요.
const dividendModules = import.meta.glob('../../firemap-v2/dividendWatch.js');
async function loadDividendWeek() {
  const loader = Object.values(dividendModules)[0];
  if (!loader) return [];
  try {
    const m = await loader();
    if (typeof m.expectedExDates !== 'function') return [];
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const end = new Date(today.getTime() + 7 * 86400000);
    // 이번 주가 달을 넘기면 다음 달 규칙표도 같이 봐요
    const months = [[today.getFullYear(), today.getMonth() + 1]];
    if (end.getMonth() !== today.getMonth()) months.push([end.getFullYear(), end.getMonth() + 1]);
    const out = [];
    for (const [y, mo] of months) {
      for (const d of m.expectedExDates(y, mo) || []) {
        const date = new Date(y, mo - 1, d.day);
        if (date >= today && date < end) out.push({ key: `${d.symbol}-${y}-${mo}`, name: d.name, date, expected: d.expected !== false, note: d.market === 'KR' ? '국내 · 분배금' : (d.freq === 'monthly' ? '미국 · 매달' : '미국 · 분기') });
      }
    }
    return out.sort((a, b) => a.date - b.date).slice(0, 6);
  } catch { return []; }
}

function relativeTime(value) {
  const diff = Math.max(1, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (diff < 60) return `${diff}분 전`;
  const h = Math.round(diff / 60);
  if (h < 24) return `${h}시간 전`;
  return `${Math.round(h / 24)}일 전`;
}
const mdOf = (iso) => { const d = new Date(iso); return Number.isNaN(d.getTime()) ? '' : `${d.getMonth() + 1}월 ${d.getDate()}일`; };
const pct1 = (v) => (v == null || Number.isNaN(Number(v)) ? null : `${Number(v) > 0 ? '+' : ''}${Number(v).toFixed(1)}%`);
const num0 = (v) => Math.round(Number(v)).toLocaleString('ko-KR');
const periodOf = (p) => { const s = String(p || ''); return s.length === 6 ? `${s.slice(0, 4)}년 ${Number(s.slice(4))}월` : s; };

// 지표 한 줄 — 라벨 · 값 · 변화. 소식 화면 전용(DS Stat보다 촘촘한 목록형).
function IndexRow({ label, value, unit, delta, deltaLabel, sub }) {
  const dir = delta == null ? null : (String(delta).startsWith('+') ? 'up' : (String(delta).startsWith('-') ? 'down' : 'flat'));
  return (
    <div className="sc-news-idx">
      <span className="sc-news-idx__label">{label}{sub ? <span className="sc-news-idx__sub">{sub}</span> : null}</span>
      <span className="sc-news-idx__value num">{value}{unit ? <span className="sc-news-idx__unit">{unit}</span> : null}</span>
      {delta != null && <span className={`sc-news-idx__delta num sc-news-idx__delta--${dir}`}>{delta}{deltaLabel ? <span className="sc-news-idx__dl">{deltaLabel}</span> : null}</span>}
    </div>
  );
}

function useIndicators() {
  const [data, setData] = useState({ loading: true, rows: [] });
  useEffect(() => {
    let alive = true;
    (async () => {
      const [m, macro] = await Promise.all([sbRpc('fm_market_latest'), sbRpc('fm_macro_latest')]);
      if (!alive) return;
      const mk = Array.isArray(m) ? m : [];
      const find = (sym) => mk.find((x) => x.symbol === sym);
      const rows = [];
      const kospi = find('^kospi'); const spx = find('^spx'); const fx = find('usdkrw');
      const idx = (label, r) => {
        if (!r || r.level == null) return;
        const d1 = pct1(r.ret_1d); const d7 = pct1(r.ret_7d);
        rows.push({ key: label, label, value: num0(r.level), delta: d1 || d7, deltaLabel: d1 ? '어제보다' : (d7 ? '이번 주' : null) });
      };
      idx('코스피', kospi); idx('S&P500', spx);
      if (fx && fx.level != null) rows.push({ key: 'fx', label: '환율', sub: '1달러', value: num0(fx.level), unit: '원', delta: pct1(fx.ret_1d) || pct1(fx.ret_7d), deltaLabel: fx.ret_1d != null ? '어제보다' : (fx.ret_7d != null ? '이번 주' : null) });
      const rates = (macro && Array.isArray(macro.rates)) ? macro.rates : [];
      const base = rates.find((r) => r.key === 'base_rate');
      if (base && base.value != null) rows.push({ key: 'base', label: '기준금리', value: Number(base.value).toFixed(2).replace(/0$/, ''), unit: '%', sub: base.as_of ? periodOf(base.as_of) : null });
      const cpi = macro && macro.cpi;
      if (cpi && cpi.yoy != null) rows.push({ key: 'cpi', label: '물가', sub: cpi.period ? periodOf(cpi.period) : '1년 전보다', value: Number(cpi.yoy).toFixed(1), unit: '%' });
      setData({ loading: false, rows });
    })();
    return () => { alive = false; };
  }, []);
  return data;
}

export default function News({ onBack }) {
  const [rows, setRows] = useState(null);
  const [cat, setCat] = useState('all');
  const [openId, setOpenId] = useState(null);
  const [shown, setShown] = useState(20);
  const [dividends, setDividends] = useState([]);
  const ind = useIndicators();
  const story = useMemo(() => storyOfDay(dayIdx()), []);

  useEffect(() => {
    let alive = true;
    loadNews(80).then((r) => { if (alive) setRows(Array.isArray(r) ? r : []); });
    loadDividendWeek().then((d) => { if (alive) setDividends(d); });
    return () => { alive = false; };
  }, []);

  const list = (rows || []).filter((r) => {
    const c = r.category || 'news';
    if (!NEWS_CATS.has(c)) return false;
    return cat === 'all' || c === cat;
  });

  return (
    <main className="fm-screen fm-scroll ds-screen-gap">
      <TopBar title="소식" onBack={onBack} />

      {/* 1. 지표 */}
      <Card>
        <SectionHead kicker="📊 지표" title="오늘의 참고 지표" size="sm" />
        {ind.loading && <Skeleton lines={4} />}
        {!ind.loading && ind.rows.length === 0 && <p className="ds-p">지표를 아직 못 불러왔어요 · 잠시 뒤 다시 열어보세요</p>}
        {!ind.loading && ind.rows.length > 0 && (
          <div className="sc-news-idx-list">
            {ind.rows.map((r) => { const { key, ...rest } = r; return <IndexRow key={key} {...rest} />; })}
          </div>
        )}
        <p className="ds-caption ds-mt-2 sc-news-cap">지표는 참고만 · 내 파이어 나이엔 영향 없어요</p>
      </Card>

      {/* 2. 파이어 후 하루 */}
      <Card variant="hero">
        <SectionHead kicker="🏝️ 파이어 후 하루" title={story.title} size="sm" />
        <p className="ds-p sc-news-story">{story.body}</p>
        <a className="ds-link sc-news-more" href={CAFE_URL} target="_blank" rel="noopener noreferrer">카페에서 진짜 이야기 더 보기 →</a>
      </Card>

      {/* 3. 배당락 이번 주 — 데이터 있을 때만 */}
      {dividends.length > 0 && (
        <Card>
          <SectionHead kicker="💸 배당락 이번 주" title="이 날 전에 사야 배당을 받아요" size="sm" />
          <ListGroup>
            {dividends.map((d) => (
              <ListRow key={d.key} lead="📅" title={d.name} desc={d.note || undefined} trail={<span className="num">{d.date ? mdOf(d.date) : ''}{d.expected ? <Badge tone="neutral" className="sc-news-exp">예상</Badge> : null}</span>} chevron={false} size="S" />
            ))}
          </ListGroup>
          <p className="ds-caption ds-mt-2 sc-news-cap">과거 배당 기준 예상이에요 · 실제 날짜는 운용사 공지로 확인해요</p>
        </Card>
      )}

      {/* 4. 소식 목록 */}
      <Tabs items={CATS.map((c) => ({ key: c.key, label: c.key === 'all' ? c.label : `${c.emoji} ${c.label}` }))} value={cat} onChange={(k) => { setCat(k); setOpenId(null); }} variant="pill" label="소식 분류" className="sc-news-cats" />

      {rows === null && <Card><Skeleton lines={4} /></Card>}
      {rows !== null && list.length === 0 && <EmptyState icon="📰" title="아직 이 분야 소식이 없어요" desc="매일 아침 지표, 금요일 랭킹 소식이 올라와요" />}
      {rows !== null && list.length > 0 && (
        <ListGroup>
          {list.slice(0, shown).map((r) => {
            const m = catMeta(r.category || 'news');
            const auto = isAuto(r);
            const open = openId === r.id;
            const body = String(r.body || '').trim();
            const expandable = !!body || !!r.url;
            return (
              <div key={r.id} className={`sc-news-item${open ? ' sc-news-item--open' : ''}`}>
                <ListRow
                  lead={m.emoji}
                  title={<span className="sc-news-title">{auto && <Badge tone="neutral" className="sc-news-auto">자동</Badge>}{cleanTitle(r)}</span>}
                  desc={`${m.label} · ${relativeTime(r.created_at)}${r.source ? ` · ${r.source}` : ''}`}
                  chevron={expandable}
                  onClick={expandable ? () => setOpenId(open ? null : r.id) : undefined}
                  size="M"
                  aria-expanded={expandable ? open : undefined}
                />
                {open && (
                  <div className="sc-news-body">
                    {body && <p className="ds-p sc-news-body__text">{body}</p>}
                    {r.url && <a className="ds-link" href={r.url} target="_blank" rel="noopener noreferrer">출처 보기 →</a>}
                  </div>
                )}
              </div>
            );
          })}
        </ListGroup>
      )}
      {rows !== null && list.length > shown && (
        <Button variant="secondary" size="md" full onClick={() => setShown((n) => n + 20)}>더 보기 · {list.length - shown}개</Button>
      )}
      <p className="ds-caption ds-textcenter sc-news-cap">참고용 정보예요 · 투자 자문이 아니에요</p>
    </main>
  );
}
