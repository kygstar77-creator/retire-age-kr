// 파이어 시계 매일 발송 — 활성 구독에 '오늘 경제뉴스 N건 + 파이어 D-day' 묶음 푸시.
// 과발송 방지(같은 날 중복 skip), 옵트아웃(active=false만 제외), 무효 구독 자동 비활성(404/410), 발송 집계 로깅.
// 보안: 비밀키(VAPID_PRIVATE/CRON_SECRET)는 레포에 두지 않고 Supabase Function Secrets(환경변수)로 주입.
import webpush from 'npm:web-push@3.6.7';
import { createClient } from 'npm:@supabase/supabase-js@2';

const VAPID_PUBLIC = 'BJYJgOTmlTx9LcLWBex3RJZAicBp6D6Y8RJ3_cn4uKhDy6yFQp23uBagGUeZqcHHJTlXo8tJZp6t7HdI9eOTo44'; // 공개키(노출 정상)
const VAPID_PRIVATE = Deno.env.get('VAPID_PRIVATE')!;   // Supabase secret
const CRON_SECRET = Deno.env.get('CRON_SECRET')!;       // Supabase secret

webpush.setVapidDetails('mailto:retireage.kr@gmail.com', VAPID_PUBLIC, VAPID_PRIVATE);
const fmt = (n: number) => n.toLocaleString('en-US');

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);
  const token = req.headers.get('x-cron-secret') || url.searchParams.get('secret') || '';
  if (token !== CRON_SECRET) return new Response('forbidden', { status: 403 });

  const supa = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  const dry = url.searchParams.get('dry') === '1';

  // 오늘(최근 24h) 올라온 공식 경제뉴스 수
  let newsCount = 0;
  try {
    const since = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
    const { count } = await supa.from('firemap_feedback')
      .select('id', { count: 'exact', head: true })
      .eq('kind', 'community').eq('client_id', 'firemap-official').is('parent_id', null)
      .gte('created_at', since);
    newsCount = count || 0;
  } catch { /* ignore */ }
  const newsLine = newsCount > 0 ? `📰 오늘 경제뉴스 ${newsCount}건` : '';

  const { data: subs, error } = await supa.from('firemap_push_subs').select('*').eq('active', true);
  if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: { 'content-type': 'application/json' } });

  const now = Date.now();
  const todayKey = new Date().toISOString().slice(0, 10);
  let sent = 0, failed = 0, deactivated = 0, skipped = 0;

  for (const s of subs ?? []) {
    if (!dry && s.last_sent && String(s.last_sent).slice(0, 10) === todayKey) { skipped++; continue; } // 같은 날 중복 발송 방지
    let ddayLine = '';
    if (s.target_fire_date) {
      const t = new Date(String(s.target_fire_date) + 'T00:00:00Z').getTime();
      const days = Math.max(0, Math.round((t - now) / 86400000));
      ddayLine = days <= 0 ? '🎉 오늘 파이어 가능 나이 도달!' : `⏳ 파이어까지 D-${fmt(days)}`;
    }
    const parts = [newsLine, ddayLine].filter(Boolean);
    const body = (parts.length ? parts.join(' · ') : '오늘의 파이어 한 걸음을 확인해보세요') + ' — 확인하기';
    if (dry) { sent++; continue; }
    const payload = JSON.stringify({ title: '파이어맵 📰', body, url: 'https://firemap.kr/?from=push#news', tag: 'fire-daily' });
    const subscription = { endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } };
    try {
      await webpush.sendNotification(subscription as any, payload, { TTL: 86400 });
      sent++;
      await supa.from('firemap_push_subs').update({ last_sent: new Date().toISOString() }).eq('endpoint', s.endpoint);
    } catch (e) {
      failed++;
      const code = (e && ((e as any).statusCode || (e as any).status)) as number | undefined;
      if (code === 404 || code === 410) {
        deactivated++;
        await supa.from('firemap_push_subs').update({ active: false }).eq('endpoint', s.endpoint);
      }
    }
  }
  if (!dry) { try { await supa.from('firemap_events').insert({ client_id: 'system', event: 'push_daily_sent', props: { sent, failed, skipped, deactivated, news: newsCount, total: (subs ?? []).length } }); } catch { /* ignore */ } }
  return new Response(JSON.stringify({ sent, failed, skipped, deactivated, total: (subs ?? []).length, news: newsCount, dry }), { headers: { 'content-type': 'application/json' } });
});
