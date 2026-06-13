// 카카오톡 공유(피드 템플릿). 카드 이미지는 /og(개인 숫자) 그대로 사용 → 매 공유마다 그 사람 등수 반영.
const KAKAO_JS_KEY = 'ab42112f15f44fd86a631e6cee694c29'; // 도메인 제한된 공개 JS 키
let loadPromise;

function ensureKakao() {
  if (loadPromise) return loadPromise;
  loadPromise = new Promise((resolve, reject) => {
    if (window.Kakao) { resolve(window.Kakao); return; }
    const sc = document.createElement('script');
    sc.src = 'https://t1.kakaocdn.net/kakao_js_sdk/2.7.4/kakao.min.js';
    sc.async = true;
    sc.onload = () => resolve(window.Kakao);
    sc.onerror = () => reject(new Error('kakao sdk load fail'));
    document.head.appendChild(sc);
  }).then((K) => {
    try { if (K && !K.isInitialized()) K.init(KAKAO_JS_KEY); } catch (e) { /* ignore */ }
    return K;
  });
  return loadPromise;
}

export async function shareToKakao({ title, description, imageUrl, linkUrl }) {
  const K = await ensureKakao();
  if (!K || !K.Share || !K.isInitialized()) throw new Error('kakao unavailable');
  K.Share.sendDefault({
    objectType: 'feed',
    content: {
      title,
      description,
      imageUrl,
      link: { mobileWebUrl: linkUrl, webUrl: linkUrl }
    },
    buttons: [{ title: '내 등수 확인하기', link: { mobileWebUrl: linkUrl, webUrl: linkUrl } }]
  });
}
