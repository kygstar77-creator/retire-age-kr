// 조회수 배지 주입기 — outputs/deploy 의 가이드/정적 콘텐츠 페이지에 '조회수' 배지+스크립트를 삽입.
// 빌드 후처리(gen-* 다음)로 실행. 소스(public/)는 건드리지 않고 배포본에만 주입한다(추가전용).
// ★ 조회수 집계(+1)는 모든 방문자에게 적용되지만, 배지 '표시'는 관리자(나)에게만 보인다.
//   관리자 전환: 아무 가이드 URL 뒤에 ?vc=on 을 붙여 한 번 방문 → 그 브라우저에 표시 플래그 저장.
//   해제: ?vc=off
import { readdirSync, statSync, readFileSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';

const ROOT = 'outputs/deploy';
const SUPABASE_URL = 'https://cvhskxdwqubmshdgkzhj.supabase.co';
const SUPABASE_KEY = 'sb_publishable_uhbAVqCA8JrJNXqaAcft9g_yYtwgct9';
const MARK = 'fm-vc-script';

function snippet(ctype, cid) {
  return `<style>.fm-vc{display:inline-flex;align-items:center;gap:5px;font-size:13px;color:#8e8e93;margin:8px 0 4px;font-weight:600}</style>` +
    `<script id="${MARK}">(function(){` +
    `var U=${JSON.stringify(SUPABASE_URL)},K=${JSON.stringify(SUPABASE_KEY)},T=${JSON.stringify(ctype)},I=${JSON.stringify(cid)};` +
    `var admin=false;try{var p=new URLSearchParams(location.search||'');var v=p.get('vc');if(v==='on'){localStorage.setItem('fm_vc_admin','1');}else if(v==='off'){localStorage.removeItem('fm_vc_admin');}admin=localStorage.getItem('fm_vc_admin')==='1';}catch(e){}` +
    `function fmt(n){try{return Number(n).toLocaleString('ko-KR');}catch(e){return n;}}` +
    `function badge(){var b=document.getElementById('fm-vc');if(b)return b;` +
    `b=document.createElement('span');b.id='fm-vc';b.className='fm-vc';b.textContent='\\uD83D\\uDC41 \\u2026';` +
    `var h=document.querySelector('main h1')||document.querySelector('h1');` +
    `if(h&&h.parentNode){h.parentNode.insertBefore(b,h.nextSibling);}else{document.body.insertBefore(b,document.body.firstChild);}return b;}` +
    `function show(n){if(!admin)return;var b=badge();if(typeof n==='number'&&!isNaN(n)){b.textContent='\\uD83D\\uDC41 '+fmt(n)+'\\uD68C \\uC870\\uD68C (\\uB098\\uB9CC \\uBCF4\\uC784)';}}` +
    `try{fetch(U+'/rest/v1/rpc/fm_view_hit',{method:'POST',headers:{apikey:K,authorization:'Bearer '+K,'content-type':'application/json'},body:JSON.stringify({p_type:T,p_id:I})})` +
    `.then(function(r){return r.json();}).then(show).catch(function(){});}catch(e){}` +
    `})();</script>`;
}

function idFor(relPath) {
  const p = relPath.split('\\').join('/');
  if (p === 'fire-jok.html') return { ctype: 'page', cid: 'fire-jok' };
  if (p.startsWith('guide/')) {
    const slug = p.slice('guide/'.length).replace(/\.html$/, '').replace(/\/index$/, '') || 'index';
    return { ctype: 'guide', cid: slug };
  }
  return null;
}

let count = 0;
function walk(dir) {
  for (const e of readdirSync(dir)) {
    const fp = join(dir, e);
    const st = statSync(fp);
    if (st.isDirectory()) { if (e === 'assets') continue; walk(fp); continue; }
    if (!e.endsWith('.html')) continue;
    const rel = relative(ROOT, fp);
    const target = idFor(rel);
    if (!target) continue;
    let html = readFileSync(fp, 'utf8');
    if (html.includes(MARK)) continue;
    const idx = html.lastIndexOf('</body>');
    const snip = snippet(target.ctype, target.cid);
    if (idx >= 0) html = html.slice(0, idx) + snip + html.slice(idx);
    else html += snip;
    writeFileSync(fp, html);
    count += 1;
  }
}
walk(ROOT);
console.log(`[fix-view-counter] injected view counter into ${count} pages (admin-only display)`);
