// kakao-auth — 카카오 로그인 보안 엔드포인트
// 흐름(Authorization Code): 클라이언트가 Kakao.Auth.authorize로 받은 code를 보내면,
//   1) 서버에서 code→access_token 교환(REST API 키, 시크릿 env)
//   2) 카카오 API로 사용자 검증
//   3) firemap_accounts에 kakao_id로 upsert → 기존과 동일한 {id, handle, token} 발급
// 기존 커스텀 계정 시스템(fm_state/fm_claim)과 100% 호환 형식.
import { createClient } from 'jsr:@supabase/supabase-js@2';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, content-type, apikey, x-client-info',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, 'content-type': 'application/json' },
  });
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);

  try {
    const body = await req.json().catch(() => ({} as Record<string, string>));
    let accessToken: string | undefined = body.access_token;

    // 1) Authorization Code → access_token 교환 (서버에서만)
    if (!accessToken && body.code) {
      const restKey = Deno.env.get('KAKAO_REST_API_KEY');
      if (!restKey) return json({ error: 'missing_rest_key' }, 500);
      const form = new URLSearchParams();
      form.set('grant_type', 'authorization_code');
      form.set('client_id', restKey);
      form.set('redirect_uri', body.redirect_uri || '');
      form.set('code', body.code);
      const clientSecret = Deno.env.get('KAKAO_CLIENT_SECRET');
      if (clientSecret) form.set('client_secret', clientSecret);
      const tres = await fetch('https://kauth.kakao.com/oauth/token', {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded;charset=utf-8' },
        body: form.toString(),
      });
      const tjson = await tres.json().catch(() => null);
      if (!tres.ok || !tjson?.access_token) {
        return json({ error: 'token_exchange_failed', detail: tjson }, 401);
      }
      accessToken = tjson.access_token;
    }

    if (!accessToken) return json({ error: 'no_token' }, 400);

    // 2) 사용자 검증
    const kres = await fetch('https://kapi.kakao.com/v2/user/me', {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (!kres.ok) return json({ error: 'kakao_verify_failed' }, 401);
    const kuser = await kres.json();
    const kakaoId = kuser?.id != null ? String(kuser.id) : '';
    if (!kakaoId) return json({ error: 'no_kakao_id' }, 401);
    const rawNick = kuser?.properties?.nickname
      || kuser?.kakao_account?.profile?.nickname
      || '파이어러';
    const nickname = String(rawNick).trim().slice(0, 14) || '파이어러';

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
    );

    // 3) 기존 카카오 계정이면 그대로 반환
    const { data: existing } = await supabase
      .from('firemap_accounts')
      .select('id, handle, token')
      .eq('kakao_id', kakaoId)
      .maybeSingle();
    if (existing) return json(existing);

    // 4) 신규: 고유 handle 확보 후 생성 (token = 기존 형식 32 hex)
    const token = crypto.randomUUID().replace(/-/g, '');
    let handle = nickname;
    let lower = handle.toLowerCase();
    for (let i = 0; i < 6; i++) {
      const { data: clash } = await supabase
        .from('firemap_accounts')
        .select('id')
        .eq('handle_lower', lower)
        .maybeSingle();
      if (!clash) break;
      const suf = Math.floor(1000 + Math.random() * 9000);
      handle = `${nickname}${suf}`.slice(0, 16);
      lower = handle.toLowerCase();
    }

    const { data: created, error } = await supabase
      .from('firemap_accounts')
      .insert({ handle, handle_lower: lower, kakao_id: kakaoId, token })
      .select('id, handle, token')
      .single();
    if (error) return json({ error: 'create_failed', detail: error.message }, 500);

    return json(created);
  } catch (e) {
    return json({ error: 'server_error', detail: String(e) }, 500);
  }
});
