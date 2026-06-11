import { useState } from 'react';
import { formatWon } from '../../firemap-v2/formatters.js';

const CHALLENGES = [
  { t: '오늘 배달·외식 0번 도전', s: 15000 },
  { t: '커피 집에서 내려 마시기', s: 5000 },
  { t: '충동구매 1건 참기', s: 30000 },
  { t: '안 쓰는 구독 서비스 1개 점검', s: 10000 },
  { t: '점심 도시락 싸기', s: 8000 },
  { t: '장보기 목록 정하고 그것만 사기', s: 12000 },
  { t: '택시 대신 대중교통 타기', s: 8000 },
  { t: '편의점 대신 마트 이용', s: 5000 },
  { t: '오늘 하루 무지출 도전', s: 25000 },
  { t: '카페 대신 텀블러 챙기기', s: 5000 },
  { t: '쿠폰·세일 1개 찾아 쓰기', s: 7000 },
  { t: '살 물건 중고로 알아보기', s: 20000 },
  { t: '통신·보험 고정비 1개 점검', s: 10000 },
  { t: '간식 대신 물 마시기', s: 3000 },
  { t: '오늘 지출 가계부에 기록', s: 0 },
  { t: '한 끼는 집밥으로', s: 8000 },
  { t: '가까운 거리 걸어가기', s: 3000 },
  { t: '배달앱 장바구니 비우기', s: 18000 },
  { t: '주말 약속 하나 홈카페로', s: 20000 },
  { t: '안 입는 옷 1벌 중고 판매', s: 10000 },
  { t: '자동결제 목록 한 번 훑기', s: 9000 },
  { t: '오늘 술·담배 0', s: 12000 },
  { t: '대용량으로 단가 낮추기', s: 6000 },
  { t: '외식 대신 밀키트', s: 9000 },
  { t: '하루 예산 정하고 지키기', s: 15000 },
  { t: '냉장고 털어 한 끼 해결', s: 8000 },
  { t: '필요 없는 알림·쇼핑앱 정리', s: 0 },
  { t: '커피값을 저축통장에 이체', s: 5000 },
  { t: '이번 달 가장 큰 지출 점검', s: 0 },
  { t: '내일 점심 미리 준비', s: 8000 }
];

const QUOTES = [
  '오늘 아낀 만원이 10년 뒤엔 자유의 하루가 된다.',
  '부는 많이 버는 것이 아니라 덜 쓰고 남기는 데서 시작된다.',
  '미래의 나에게 매달 월급을 먼저 보내자.',
  '소비를 줄이면 필요한 노후 자금도 함께 줄어든다.',
  '돈이 나 대신 일하게 만드는 것, 그게 파이어다.',
  '쓰지 않은 돈이 가장 확실한 수익률이다.',
  '자유는 잔고가 아니라 습관에서 나온다.',
  '남의 소비를 따라가면 남의 속도로 늙는다.',
  '복리는 시간을 먹고 자란다. 일찍 시작한 사람이 이긴다.',
  '작은 절약이 모여 퇴사 날짜를 앞당긴다.',
  '필요한 것과 갖고 싶은 것을 구분하는 순간 부자가 된다.',
  '버는 속도보다 모으는 속도가 자유를 결정한다.',
  '오늘의 한 끼 집밥이 내일의 하루치 자유다.',
  '조급해 말되 멈추지도 말자. 방향이 맞으면 도착한다.',
  '가장 비싼 지출은 남에게 보여주려는 지출이다.'
];

const today = () => new Date().toISOString().slice(0, 10);
const yesterday = () => new Date(Date.now() - 86400000).toISOString().slice(0, 10);
const load = () => { try { return JSON.parse(localStorage.getItem('fm_challenge') || 'null'); } catch { return null; } };

export default function DailyFire() {
  const ch = CHALLENGES[Math.floor(Date.now() / 86400000) % CHALLENGES.length];
  const quote = QUOTES[Math.floor(Date.now() / 86400000) % QUOTES.length];
  const [st, setSt] = useState(load);
  const doneToday = st && st.lastDate === today();
  const streak = st ? st.count : 0;
  const saved = st ? (st.saved || 0) : 0;
  const complete = () => {
    if (st && st.lastDate === today()) return;
    const consec = st && st.lastDate === yesterday() ? st.count + 1 : 1;
    const next = { count: consec, lastDate: today(), saved: (st ? st.saved || 0 : 0) + ch.s };
    try { localStorage.setItem('fm_challenge', JSON.stringify(next)); } catch { /* ignore */ }
    setSt(next);
  };
  return (
    <section className="fm-daily">
      <p className="fm-daily-wisdom">“{quote}”</p>
      <p className="fm-daily-kicker">오늘의 챌린지 🔥 {streak}일 연속</p>
      <p className="fm-daily-quote">{ch.t}{ch.s > 0 ? ` (예상 절약 ≈ ${formatWon(ch.s)})` : ''}</p>
      <button type="button" className={`fm-daily-btn full${doneToday ? ' done' : ''}`} onClick={complete} disabled={doneToday}>
        {doneToday ? '오늘 챌린지 완료 ✓' : '완료하기'}
      </button>
      {saved > 0 && <p className="fm-daily-saved">지금까지 챌린지로 아낀 돈 ≈ <b>{formatWon(saved)}</b> · 이 습관이 은퇴를 앞당겨요</p>}
      <p className="fm-daily-note">절약액은 대략 추정치예요. 매일 들어와 미션을 완료하면 연속일이 쌓여요.</p>
    </section>
  );
}
