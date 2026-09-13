// 위젯 카드 — 결과 화면 위쪽 히어로가 이미 파이어 나이를 말하므로, 여기는 D-day와 매일 바뀌는 지표를 맡는다.
// 위에 파이어 카운트다운(년·일·시:분:초), 3숫자: 환율 · 기준금리 · 물가. 그 아래 오늘 소식 한 줄.
// 앱 잠금화면 위젯은 파이어 나이·D-day를 쓰고, 이 카드가 그 배치의 웹 미리보기 역할을 한다.
// 저축을 접으면서 '연속 기록' 자리를 지표로 바꿨다. 지표는 참고용이고 파이어 나이 계산에는 쓰지 않는다.
import { useEffect, useState } from 'react';
import { Card, Stat, ListRow, Countdown } from '../../ui/index.js';
import { fetchIndicators, fxText, rateText, cpiText } from '../../utils/indicators.js';
import { loadNews } from '../../utils/firemapFeedbackApi.js';

const AUTO_RE = /^\s*\[자동\]\s*/;

export default function FireWidgetCard({ simulation, onMove }) {
  const [ind, setInd] = useState(null);
  const [news, setNews] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchIndicators().then((v) => { if (alive) setInd(v); });
    loadNews(1).then((rows) => {
      if (!alive || !Array.isArray(rows) || !rows.length) return;
      const t = String(rows[0].title || '').replace(AUTO_RE, '').trim();
      if (t) setNews(t);
    }).catch(() => { /* 소식이 없으면 조용히 숨긴다 */ });
    return () => { alive = false; };
  }, []);

  const fx = ind ? fxText(ind.fx) : null;
  const base = ind ? rateText(ind.baseRate) : null;
  const cpiNow = ind ? cpiText(ind.cpi) : null;

  return (
    <>
      <Card>
        <Countdown simulation={simulation} />
        <div className="ds-three ds-mt-2">
          <Stat label="환율" value={fx || '—'} size="md" />
          <Stat label="기준금리" value={base || '—'} size="md" />
          <Stat label="물가" value={cpiNow || '—'} size="md" />
        </div>
      </Card>

      <Card variant="soft" padding="md">
        <ListRow
          lead="📰"
          title={news || '오늘의 소식'}
          desc={news ? '지표 · 배당락' : '시장 지표 · 배당락'}
          onClick={() => onMove('news')}
          size="S"
        />
      </Card>
    </>
  );
}
