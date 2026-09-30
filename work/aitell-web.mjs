// 화면 문구 AI 티 검사 — src/의 글자(문자열·JSX 텍스트)에서 work/aitell_dict.json 표현을 찾는다(2026-10-01).
//   node work/aitell-web.mjs                    → 기준선(work/aitell-web-baseline.json)보다 새로 늘어난 것만 경고
//   node work/aitell-web.mjs --all              → 기준선 무시하고 전부
//   node work/aitell-web.mjs --update-baseline  → 지금 상태를 기준선으로 (editor-web이 전수 점검 끝낸 뒤)
//   AITELL_STRICT=1 이면 새로 늘어난 것이 있을 때 실패(종료코드 1). 지금은 경고만 — prebuild에 걸려 있다.
// 사장님 10/1 "사소한 것까지 모든 글을 다 검토해서 사람이 쓴 글로". 문구를 기계가 고치지 않는다 — 알려만 준다.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.join(HERE, '..')
const DICT = JSON.parse(fs.readFileSync(path.join(HERE, 'aitell_dict.json'), 'utf8'))
const BASE = path.join(HERE, 'aitell-web-baseline.json')
const TERMS = [...DICT.ko, ...DICT.ko_explain].map(t => ({ t, en: false })).concat(DICT.en.map(t => ({ t, en: true })))

export function textsOf(src) {
  // 주석을 빼고, 따옴표 문자열과 JSX 텍스트(>…<)만 모은다. 식별자·import 경로는 안 본다.
  const code = src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:'"`])\/\/.*$/gm, '$1')
  const out = []
  for (const m of code.matchAll(/'((?:[^'\\\n]|\\.)*)'|"((?:[^"\\\n]|\\.)*)"|`((?:[^`\\]|\\.)*)`/g)) out.push(m[1] ?? m[2] ?? m[3])
  for (const m of code.matchAll(/>([^<>{}]*[가-힣A-Za-z][^<>{}]*)</g)) out.push(m[1])
  return out.filter(s => /[가-힣]|[A-Za-z]{3,}\s+[A-Za-z]/.test(s))
}

export function hitsOf(texts) {
  const hits = {}
  for (const s of texts) {
    const low = s.toLowerCase()
    for (const { t, en } of TERMS) {
      const re = en ? new RegExp('(?<![a-z])' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![a-z])', 'g') : null
      const c = en ? (low.match(re) || []).length : s.split(t).length - 1
      if (c) hits[t] = (hits[t] || 0) + c
    }
  }
  return hits
}

function walk(dir, acc = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name)
    if (e.isDirectory()) walk(p, acc)
    else if (/\.(jsx?|tsx?)$/.test(e.name) && !/\.test\./.test(e.name)) acc.push(p)
  }
  return acc
}

function scan() {
  const res = {}
  for (const f of walk(path.join(ROOT, 'src'))) {
    const h = hitsOf(textsOf(fs.readFileSync(f, 'utf8')))
    for (const [t, c] of Object.entries(h)) res[path.relative(ROOT, f).replace(/\\/g, '/') + ' | ' + t] = c
  }
  return res
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const now = scan()
  if (process.argv.includes('--update-baseline')) {
    fs.writeFileSync(BASE, JSON.stringify(now, null, 1) + '\n')
    console.log(`aitell-web: 기준선 저장 ${Object.keys(now).length}곳`)
    process.exit(0)
  }
  const base = process.argv.includes('--all') || !fs.existsSync(BASE) ? {} : JSON.parse(fs.readFileSync(BASE, 'utf8'))
  const fresh = Object.entries(now).filter(([k, c]) => c > (base[k] || 0))
  const total = Object.values(now).reduce((a, b) => a + b, 0)
  if (!fresh.length) { console.log(`aitell-web: 새로 들어온 AI 티 문구 없음 (전체 ${total}건은 editor-web 점검 대상)`); process.exit(0) }
  console.warn(`aitell-web: 새로 들어온 AI 티 문구 ${fresh.length}곳 — 사람 말로 바꾼다 (work/research/editor/style-guide.md)`)
  for (const [k, c] of fresh) console.warn(`  ${k} ×${c}${base[k] ? ` (기준선 ${base[k]})` : ''}`)
  process.exit(process.env.AITELL_STRICT === '1' ? 1 : 0)
}
