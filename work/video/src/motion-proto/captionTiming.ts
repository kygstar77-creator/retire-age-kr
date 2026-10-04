// 단어 강조 자막의 시간 계산(2026-10-03 cloud yt-quality 시제품 — React·remotion 없이 순수 함수라 node --test로 바로 시험한다).
// 근거: 리모션 공식 createTikTokStyleCaptions(쪽 나누기 + 지금 말하는 단어 강조). 우리는 단어 시각(위스퍼)이 아직 없어서
// 문장 오디오 길이(VLine.frames)를 어절의 '읽는 음절 수'로 나눠 단어 시각을 어림한다. 실제 음성과의 오차는 확인 안 함 — 단어 시각이 생기면 timings를 바로 넣는다.
// 다른 파일을 import하지 않는다(node 타입 지우기로 그대로 읽히게).

export type WordTiming = {word: string; from: number; to: number};
export type CaptionPage = {first: number; last: number; text: string};

const HANGUL = /[가-힣]/g;

// 숫자 한 자리를 한국어로 읽으면 평균 1.5음절쯤(1,234 → 천이백삼십사 = 6음절/4자리). %는 '퍼센트' 3음절, 소수점은 '점' 1음절.
export const spokenWeight = (word: string): number => {
  const hangul = (word.match(HANGUL) || []).length;
  const digits = (word.match(/\d/g) || []).length;
  const pct = (word.match(/%/g) || []).length;
  const dot = (word.match(/\d\.\d/g) || []).length;
  const latin = (word.match(/[A-Za-z]/g) || []).length;
  return Math.max(1, hangul + digits * 1.5 + pct * 3 + dot + latin * 0.8);
};

// frames = 그 문장 오디오 길이(프레임). speechFrac = 문장 끝 쉼을 뺀 말 구간 비율(기본 0.92 — 가정, 실측 아님).
export const wordTimings = (text: string, frames: number, speechFrac = 0.92): WordTiming[] => {
  const words = text.split(/\s+/).filter(Boolean);
  if (!words.length || frames <= 0) return [];
  const ws = words.map(spokenWeight);
  const total = ws.reduce((a, b) => a + b, 0);
  const span = frames * Math.min(1, Math.max(0.1, speechFrac));
  let acc = 0;
  return words.map((word, i) => {
    const from = Math.round((acc / total) * span); acc += ws[i];
    const to = i === words.length - 1 ? Math.round(span) : Math.round((acc / total) * span);
    return {word, from, to: Math.max(to, from + 1)};
  });
};

// 한 쪽에 공백 뺀 글자 maxChars 이하(롱폼 기본 28 ≈ 자막 카드 한 줄, 쇼츠는 14~16 권장). 한 단어가 길면 그 단어 혼자 한 쪽.
export const paginate = (words: string[], maxChars = 28): CaptionPage[] => {
  const pages: CaptionPage[] = []; let first = 0; let len = 0;
  words.forEach((w, i) => {
    const l = w.length;
    if (i > first && len + l > maxChars) { pages.push({first, last: i - 1, text: words.slice(first, i).join(' ')}); first = i; len = 0; }
    len += l;
  });
  if (words.length) pages.push({first, last: words.length - 1, text: words.slice(first).join(' ')});
  return pages;
};

// f = 문장 시작부터 센 프레임. 말 시작 전 -1, 마지막 단어 뒤에는 마지막 단어를 계속 강조.
export const activeWord = (timings: WordTiming[], f: number): number => {
  if (!timings.length || f < timings[0].from) return -1;
  for (let i = 0; i < timings.length; i++) if (f < timings[i].to) return i;
  return timings.length - 1;
};

export const pageOf = (pages: CaptionPage[], wordIdx: number): number => {
  const i = pages.findIndex((p) => wordIdx >= p.first && wordIdx <= p.last);
  return i < 0 ? 0 : i;
};
