// node --test work/video/tests/yt_quality_proto.test.mjs  (node 22.18+는 그대로, 22.6~22.17은 --experimental-strip-types)
import test from 'node:test';
import assert from 'node:assert/strict';
import {spokenWeight, wordTimings, paginate, activeWord, pageOf} from '../src/motion-proto/captionTiming.ts';
import {speakWon, wonExact, speakPct, numbersInSentence} from '../src/motion-proto/numberSpeech.ts';

test('spokenWeight: 숫자는 자리당 1.5음절, %는 3음절', () => {
  assert.equal(spokenWeight('연봉은'), 3);
  assert.equal(spokenWeight('41.4%'), 3 * 1.5 + 3 + 1);
  assert.equal(spokenWeight('—'), 1);
});

test('wordTimings: 순서대로 이어지고 말 구간 안에서 끝난다', () => {
  const tm = wordTimings('상위 10%가 낸 세금은 얼마일까요', 100);
  assert.equal(tm.length, 5);
  for (let i = 1; i < tm.length; i++) assert.equal(tm[i].from, tm[i - 1].to);
  assert.equal(tm[0].from, 0);
  assert.equal(tm.at(-1).to, 92);
  tm.forEach((t) => assert.ok(t.to > t.from));
  assert.ok(tm[1].to - tm[1].from > tm[0].to - tm[0].from, '숫자 어절이 더 길게 걸린다');
  assert.deepEqual(wordTimings('', 50), []);
  assert.deepEqual(wordTimings('a b', 0), []);
});

test('activeWord: 말 전 -1, 구간마다 해당 단어, 끝나면 마지막 단어', () => {
  const tm = wordTimings('하나 둘 셋', 60, 1);
  assert.equal(activeWord(tm, -1), -1);
  assert.equal(activeWord(tm, 0), 0);
  assert.equal(activeWord(tm, tm[1].from), 1);
  assert.equal(activeWord(tm, 59), 2);
  assert.equal(activeWord(tm, 500), 2);
  assert.equal(activeWord([], 3), -1);
});

test('paginate: 쪽마다 글자 수 한도, 단어를 빠뜨리지 않는다', () => {
  const words = '국민연금 수령 나이는 1969년생부터 만 65세로 늦춰집니다 그래서 지금 계획을 다시 봐야 합니다'.split(' ');
  const pages = paginate(words, 14);
  assert.equal(pages[0].first, 0);
  assert.equal(pages.at(-1).last, words.length - 1);
  for (let i = 1; i < pages.length; i++) assert.equal(pages[i].first, pages[i - 1].last + 1);
  pages.forEach((p) => { const n = words.slice(p.first, p.last + 1).join('').length; assert.ok(n <= 14 || p.first === p.last); });
  assert.equal(paginate(['아주아주아주긴한단어하나입니다요'], 5).length, 1);
  assert.equal(pageOf(pages, words.length - 1), pages.length - 1);
  assert.equal(pageOf(pages, 999), 0);
});

test('speakWon: 유효숫자 2자리 한국어 단위, 정확값은 show에 그대로', () => {
  assert.deepEqual(speakWon(324567000), {say: '약 3억 2천만 원', show: '3억 2,456만 7,000원', rounded: true});
  assert.equal(speakWon(1234000).say, '약 120만 원');
  assert.equal(speakWon(45600).say, '약 4만 6천 원');
  assert.equal(speakWon(25000000).say, '2천5백만 원');
  assert.equal(speakWon(100000000).say, '1억 원');
  assert.equal(speakWon(100000000).rounded, false);
  assert.equal(speakWon(1520000000000).say, '약 1조 5천억 원');
  assert.equal(speakWon(1500000000000).say, '1조 5천억 원');
  assert.equal(speakWon(-4560).say, '약 −4천6백 원');
  assert.equal(wonExact(0), '0원');
});

test('speakPct: 10 이상 정수, 10 아래 소수 한 자리', () => {
  assert.deepEqual(speakPct(41.4), {say: '약 41%', show: '41.4%', rounded: true});
  assert.equal(speakPct(7.65, 2).say, '약 7.7%');
  assert.equal(speakPct(7.65, 2).show, '7.65%');
  assert.equal(speakPct(-54.7).say, '약 −55%');
  assert.equal(speakPct(5).say, '5%');
  assert.equal(speakPct(5).rounded, false);
});

test('numbersInSentence: 콤마·소수점 숫자는 한 덩어리', () => {
  assert.equal(numbersInSentence('3억 2,456만 원이고 41.4%입니다'), 3);
  assert.equal(numbersInSentence('숫자가 없어요'), 0);
});
