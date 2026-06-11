import { useState } from 'react';

const QUOTES = [
  '오늘 아낀 만 원이 미래의 자유로운 하루가 된다.',
  '퇴사는 용기가 아니라 준비의 결과다.',
  '지출을 줄이면 필요한 자산도 함께 줄어든다.',
  '작은 저축이 모여 결국 사표가 된다.',
  '남과 비교하지 말고, 어제의 나와 비교하라.',
  '자유는 잔고가 아니라 선택지에서 온다.',
  '오늘의 절제가 내일의 선택권이다.',
  '쓰지 않은 돈은 가장 확실한 수익이다.',
  '은퇴는 끝이 아니라 내 시간의 시작이다.',
  '복리는 시간을 먹고 자란다. 일찍 시작하라.',
  '버는 것보다 지키는 것이 더 어렵다.',
  '목표가 분명하면 절약은 희생이 아니라 투자가 된다.',
  '조급함은 통장을 망치고, 꾸준함은 통장을 키운다.',
  '내가 원하는 삶의 가격표를 먼저 계산하라.',
  '돈을 위해 일할지, 돈이 나를 위해 일하게 할지 정하라.',
  '파이어는 부자가 되는 게 아니라 자유로워지는 것이다.',
  '오늘 한 걸음이 은퇴를 하루 앞당긴다.',
  '불안은 계획으로 이긴다.',
  '절약은 가난이 아니라 우선순위다.',
  '시간이 가장 큰 자산이다. 오늘부터 모아라.'
];

const today = () => new Date().toISOString().slice(0, 10);
const yesterday = () => new Date(Date.now() - 86400000).toISOString().slice(0, 10);
const loadStreak = () => { try { return JSON.parse(localStorage.getItem('fm_streak') || 'null'); } catch { return null; } };

export default function DailyFire() {
  const quote = QUOTES[Math.floor(Date.now() / 86400000) % QUOTES.length];
  const [streak, setStreak] = useState(loadStreak);
  const doneToday = streak && streak.lastDate === today();
  const check = () => {
    let next;
    if (!streak) next = { count: 1, lastDate: today() };
    else if (streak.lastDate === today()) return;
    else if (streak.lastDate === yesterday()) next = { count: streak.count + 1, lastDate: today() };
    else next = { count: 1, lastDate: today() };
    try { localStorage.setItem('fm_streak', JSON.stringify(next)); } catch { /* ignore */ }
    setStreak(next);
  };
  return (
    <section className="fm-daily">
      <p className="fm-daily-kicker">오늘의 파이어</p>
      <p className="fm-daily-quote">“{quote}”</p>
      <div className="fm-daily-streak">
        <span className="fm-daily-count">🔥 {streak ? streak.count : 0}일 연속 실천</span>
        <button type="button" className={`fm-daily-btn${doneToday ? ' done' : ''}`} onClick={check} disabled={doneToday}>
          {doneToday ? '오늘 완료 ✓' : '오늘 절약·저축 실천 체크'}
        </button>
      </div>
    </section>
  );
}
