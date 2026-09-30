// IndexNow 제출 — 배포 뒤 바뀐 주소를 검색엔진(네이버·빙 등 IndexNow 참여사)에 바로 알린다. 구글은 참여하지 않는다.
// 회의 2026-09-30 배정(product-dev ①): "배포 때 /calc/severance를 알린다, 성공 기준 응답 200/202 기록".
// 키는 비밀이 아니다 — 규약상 https://firemap.kr/<키>.txt 로 공개해야 한다(public/ 에 둔 파일이 빌드 때 그대로 나간다).
//
// 실행(운영 반영 뒤에만 — 키 파일이 운영에 없으면 제출하지 않고 멈춘다):
//   node work/indexnow.mjs                      # 기본: 생활 돈 계산기 주소 + 퇴직금 가이드
//   node work/indexnow.mjs https://firemap.kr/tax https://firemap.kr/pension
// 결과는 work/research/indexnow-log.jsonl 에 한 줄씩 쌓인다.
import { appendFile } from 'node:fs/promises';
import { TOOL_PAGES } from '../src/firemap-v2/toolPages.js';

const HOST = 'firemap.kr';
const KEY = '6216379c64e2e01d7d1a9e1b1bcf4a16';
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;
const ENDPOINT = 'https://api.indexnow.org/indexnow';
const LOG = 'work/research/indexnow-log.jsonl';

const defaults = [
  ...TOOL_PAGES.filter((t) => t.path.startsWith('/calc/')).map((t) => `https://${HOST}${t.path}`),
  `https://${HOST}/guide/severance-irp-tax.html`
];
const urlList = process.argv.slice(2).length ? process.argv.slice(2) : defaults;

const log = async (row) => appendFile(LOG, `${JSON.stringify({ at: new Date().toISOString(), ...row })}\n`, 'utf8');

const keyRes = await fetch(KEY_LOCATION, { redirect: 'follow' }).catch((e) => ({ ok: false, status: String(e) }));
const keyText = keyRes.ok ? (await keyRes.text()).trim() : '';
if (keyText !== KEY) {
  const msg = `키 파일이 운영에 아직 없음(${KEY_LOCATION} → ${keyRes.status}) — 운영 반영 뒤 다시 실행`;
  await log({ ok: false, step: 'key', status: keyRes.status, urls: urlList.length });
  console.error(msg);
  process.exitCode = 2;
} else {
  await submit();
}

async function submit() {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ host: HOST, key: KEY, keyLocation: KEY_LOCATION, urlList })
  });
  const body = (await res.text()).slice(0, 300);
  const ok = res.status === 200 || res.status === 202;
  await log({ ok, step: 'submit', status: res.status, urls: urlList, body });
  console.log(`${res.status} ${ok ? '접수' : '실패'} · ${urlList.length}개 주소`);
  if (!ok) { console.error(body); process.exitCode = 1; }
}
