// 커뮤니티 유입 — 카페와 오픈채팅으로 보내는 카드. 결과·랭킹 아래에 둔다(가장 이야기하고 싶어지는 지점).
// 오픈채팅 주소가 비어 있으면 그 줄은 아예 그리지 않는다.
import { Card, SectionHead, ListGroup, ListRow } from '../../ui/index.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL, OPENCHAT_URL } from '../../firemap-v2/links.js';

export default function CommunityCta({ where = 'result', title = '혼자 하면 오래 못 가요', desc = '같은 구간 사람들이 숫자와 후기를 올려요' }) {
  const hit = (k) => { try { track(k, { where }); } catch { /* ignore */ } };
  return (
    <Card padding="md">
      <SectionHead size="sm" kicker="같이 하기" title={title} desc={desc} />
      <ListGroup>
        <ListRow
          lead="🟢"
          title="파이어맵 네이버 카페"
          desc="인증 · 봐주세요 · 파이어 후 하루"
          href={CAFE_URL}
          external
          onClick={() => hit('cafe_click')}
        />
        {OPENCHAT_URL && (
          <ListRow
            lead="💬"
            title="카카오톡 오픈채팅"
            desc="질문 하나 던지고 가도 돼요"
            href={OPENCHAT_URL}
            external
            onClick={() => hit('openchat_click')}
          />
        )}
      </ListGroup>
    </Card>
  );
}
