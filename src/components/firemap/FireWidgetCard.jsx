// 위젯 카드 — 결과 화면 위쪽 히어로가 이미 파이어 나이를 말하므로, 여기는 D-day와 매일 바뀌는 지표를 맡는다.
// 위에 파이어 카운트다운(년·일 + 시:분:초), 그 아래 지표 한 줄(코스피·S&P500·환율·금리·물가·서울 아파트 매매·전세·월세)이
// 몇 초마다 다음 지표로 넘어간다. 그 아래 카드는 최근 소식 제목이 같은 방식으로 넘어간다. 둘 다 누르면 소식 화면.
// 앱 잠금화면 위젯은 파이어 나이·D-day를 쓰고, 이 카드가 그 배치의 웹 미리보기 역할을 한다.
// 지표는 참고용이고 파이어 나이 계산에는 쓰지 않는다.
import { useEffect, useState } from 'react';
import { Card, Countdown, Ticker, Icon } from '../../ui/index.js';
import { fetchIndicators, buildIndicatorRows } from '../../utils/indicators.js';
import { loadNews } from '../../utils/firemapFeedbackApi.js';

const AUTO_RE = /^\s*\[자동\]\s*/;
const EMOJI_RE = /[\p{Extended_Pictographic}\u{FE0F}\u{200D}]/gu;

export default function FireWidgetCard({ simulation, onMove }) {
  const [rows, setRows] = useState([]);
  const [news, setNews] = useState([]);

  useEffect(() => {
    let alive = true;
    fetchIndicators().then((v) => { if (alive) setRows(buildIndicatorRows(v)); });
    loadNews(5).then((list) => {
      if (!alive || !Array.isArray(list)) return;
      setNews(list.map((r) => ({ key: r.id, text: String(r.title || '').replace(AUTO_RE, '').replace(EMOJI_RE, '').replace(/\s{2,}/g, ' ').trim() })).filter((r) => r.text));
    }).catch(() => { /* 소식이 없으면 조용히 숨긴다 */ });
    return () => { alive = false; };
  }, []);

  return (
    <>
      <Card>
        <Countdown simulation={simulation} />
        {rows.length > 0 && <Ticker className="ds-mt-2" items={rows} onClick={() => onMove('news')} ariaLabel="오늘의 참고 지표" />}
      </Card>

      {news.length > 0 && (
        <Card variant="soft" padding="md">
          <div className="sc-widget-news">
            <span className="ds-row-item__lead"><Icon name="newspaper" /></span>
            <Ticker items={news} onClick={() => onMove('news')} ariaLabel="최근 소식" />
          </div>
        </Card>
      )}
    </>
  );
}
