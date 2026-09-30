// aitell-web.mjs 시험 — 문자열·JSX 텍스트만 보고, 주석·식별자는 안 보는지(2026-10-01)
import assert from 'node:assert/strict'
import { textsOf, hitsOf } from './aitell-web.mjs'

const src = `// 결론적으로 주석은 안 본다
const leverage = 1 /* delve */
const a = '결론적으로 은퇴 나이는 늦어져요'
export default () => <p>쉽게 말해 이렇습니다</p>
const b = "Let's delve into your robust plan"`
const t = textsOf(src)
const h = hitsOf(t)
assert.equal(h['결론적으로'], 1, '문자열 속 한국어 표현은 센다, 주석은 안 센다')
assert.equal(h['쉽게 말해'], 1, 'JSX 텍스트도 센다')
assert.equal(h['delve'], 1, '영어는 문자열에서만')
assert.equal(h['robust'], 1)
assert.equal(h['leverage'], undefined, '변수 이름은 안 센다')
assert.deepEqual(hitsOf(['은퇴까지 12년 남았어요']), {}, '평범한 문장은 0')
console.log('test-aitell: ok')
