// 카페·오픈채팅으로 보내는 카드. 결과·랭킹·랜딩 아래에 둔다.
// 설명 문구는 넣지 않는다 — 링크 이름이 곧 설명이다. 오픈채팅 주소가 비어 있으면 그 줄과 제목에서 뺀다.
import { Card, SectionHead, ListGroup, ListRow, Icon } from '../../ui/index.js';
import { track } from '../../firemap-v2/dailyData.js';
import { CAFE_URL, OPENCHAT_URL } from '../../firemap-v2/links.js';

export default function CommunityCta({ where = 'result' }) {
  const hit = (k) => { try { track(k, { where }); } catch { /* ignore */ } };
  return (
    <Card padding="md">
      <SectionHead size="sm" title={OPENCHAT_URL ? '카페 · 오픈채팅' : '카페'} />
      <ListGroup>
        <ListRow lead={<Icon name="leaf" />} title="파이어맵 네이버 카페" href={CAFE_URL} external onClick={() => hit('cafe_click')} />
        {OPENCHAT_URL && (
          <ListRow lead={<Icon name="chat" />} title="카카오톡 오픈채팅" href={OPENCHAT_URL} external onClick={() => hit('openchat_click')} />
        )}
      </ListGroup>
    </Card>
  );
}
