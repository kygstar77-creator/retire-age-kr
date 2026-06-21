// Cloudflare Pages Function: /yt
// 파이어맵 유튜브 채널 최신 영상을 서버에서 RSS로 받아 JSON으로 변환(브라우저 CORS 회피).
// 썸네일은 videoId로 직접 구성. 실패하면 빈 목록 → 클라이언트는 채널 카드만 폴백.
const CHANNEL_ID = 'UCV3ZcSho5Z1i8k_FAiKPlVg';

function decodeEntities(s) {
  return String(s)
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'");
}
function json(obj, maxAge) {
  return new Response(JSON.stringify(obj), {
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': `public, max-age=${maxAge}, s-maxage=${maxAge * 6}` }
  });
}
export async function onRequest() {
  try {
    const res = await fetch(`https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`, {
      headers: { 'user-agent': 'Mozilla/5.0 (compatible; firemapbot/1.0; +https://firemap.kr)' }
    });
    if (!res.ok) return json({ videos: [] }, 600);
    const xml = await res.text();
    const entries = xml.split('<entry>').slice(1);
    const videos = [];
    for (const e of entries) {
      const id = (e.match(/<yt:videoId>([^<]+)<\/yt:videoId>/) || [])[1];
      if (!id) continue;
      const title = (e.match(/<title>([\s\S]*?)<\/title>/) || [])[1] || '';
      const published = (e.match(/<published>([^<]+)<\/published>/) || [])[1] || '';
      videos.push({ id, title: decodeEntities(title).trim(), published, thumb: `https://i.ytimg.com/vi/${id}/hqdefault.jpg`, url: `https://www.youtube.com/watch?v=${id}` });
      if (videos.length >= 3) break;
    }
    return json({ videos }, 3600);
  } catch (e) {
    return json({ videos: [] }, 300);
  }
}
