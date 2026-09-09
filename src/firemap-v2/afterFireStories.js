// 파이어 후 하루 — 소식 화면 hero 카드용 짧은 이야기 8편. 날짜(dayIdx)로 돌아가며 하나씩 보여줘요.
// 카피 규칙: 해요체 · 2~3문장 · 한 문장 25자 안팎. 실제 인증·후기는 카페 '파이어 후 하루' 게시판에서.
export const AFTER_FIRE_STORIES = [
  {
    key: 'morning',
    title: '알람 없이 눈을 떴어요',
    body: '평일 아침 9시, 출근 대신 동네 카페로 걸어가요. 커피 한 잔에 책 30쪽, 그게 오늘 첫 일정이에요.'
  },
  {
    key: 'jeju',
    title: '제주에서 한 달째예요',
    body: '월세 60만에 바다가 보이는 작은 집을 빌렸어요. 오전엔 오름, 오후엔 배당 내역 확인이 전부예요.'
  },
  {
    key: 'market',
    title: '장 보는 날이 즐거워졌어요',
    body: '사람 없는 평일 오전 마트를 천천히 돌아요. 생활비 월 180만 안에서 오늘도 여유 있게 끝났어요.'
  },
  {
    key: 'parttime',
    title: '주 2일만 일해요',
    body: '좋아하던 목공을 동네 공방에서 가르쳐요. 돈보다 사람이 좋아서 하는 일이라 퇴근이 가벼워요.'
  },
  {
    key: 'parents',
    title: '부모님과 평일 점심을 먹어요',
    body: '회사 다닐 땐 명절에만 보던 얼굴이에요. 이제 매주 수요일은 부모님 댁에서 국수 먹는 날이에요.'
  },
  {
    key: 'dividend',
    title: '배당이 들어온 날이에요',
    body: '분기마다 통장에 찍히는 숫자가 이번 달 생활비예요. 일 안 해도 굴러간다는 게 아직도 신기해요.'
  },
  {
    key: 'rain',
    title: '비 오는 날엔 그냥 쉬어요',
    body: '예전엔 우산 들고 지하철에 끼였을 시간이에요. 오늘은 창가에서 빗소리 들으며 낮잠을 잤어요.'
  },
  {
    key: 'study',
    title: '다시 학생이 됐어요',
    body: '평생교육원에서 사진 수업을 들어요. 과제도 시험도 없이 배우기만 하니까 마흔이 스무 살 같아요.'
  }
];

export function storyOfDay(idx) {
  const n = AFTER_FIRE_STORIES.length;
  const i = ((Number(idx) || 0) % n + n) % n;
  return AFTER_FIRE_STORIES[i];
}
