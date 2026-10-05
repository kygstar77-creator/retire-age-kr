"""네이버 AI 브리핑 고정 질문 측정 (growth, 2026-10-05).
모바일 UA curl로 통합검색 1페이지를 받아 ex_csa 블록(= AI 브리핑)의 '정보출처' 목록을 뽑는다.
사용: py -3.12 work/aibrief.py  → work/research/growth/ai_briefing_raw/<날짜>.json 저장 + 요약 출력
질문 세트는 QUESTIONS를 바꾸지 않는다(주 1회 같은 세트 재측정이 목적)."""
import re, sys, json, time, subprocess, urllib.parse, datetime, pathlib
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
QUESTIONS = ['연봉 5000 실수령액', '퇴직금 계산 방법', '국민연금 수령 나이', '건강보험료 재산 점수 계산', '농지연금 수령액',
             '월세 세액공제 조건', '장기요양등급 본인부담금', '국민연금 임의가입 보험료', '은퇴 자금 얼마나 필요할까', '금 투자 세금']

def kind(u):
    if 'firemap' in u: return '우리'
    if re.search(r'\.go\.kr|\.or\.kr|krx\.co\.kr', u): return '공공'
    if 'blog.naver' in u: return '네이버블로그'
    if 'cafe.naver' in u: return '네이버카페'
    if 'kin.naver' in u: return '지식iN'
    if 'news.naver' in u or 'news' in u: return '언론'
    if 'in.naver.com' in u: return '인플루언서'
    return '개인·기업 웹'

def measure(q):
    u = 'https://m.search.naver.com/search.naver?query=' + urllib.parse.quote(q)
    s = subprocess.run(['curl', '-s', '-A', UA, '-H', 'Accept-Language: ko-KR', u], capture_output=True).stdout.decode('utf-8', 'replace')
    if len(s) < 50000: return dict(q=q, ok=False, size=len(s))           # 막힘(29바이트 등) = 못 잼
    i = s.find('data-meta-ssuid="ex_csa"')
    if i < 0: return dict(q=q, ok=True, aib=False, ours_page='firemap' in s)
    blk = s[i:s.find('data-fender-root="true"', i + 100)]
    a = blk.find('정보출처'); b = blk.find('AI브리핑에서', a)
    refs = {}
    for line in blk[a:b].split(chr(92) + 'n'):
        m = re.match(r'\[(\d+)\] (.*), (https?://\S+)$', line.strip())
        if m: refs.setdefault(int(m[1]), (m[2], m[3]))
    refs = [dict(n=k, name=n, url=u, kind=kind(u)) for k, (n, u) in sorted(refs.items())]
    return dict(q=q, ok=True, aib=True, refs=refs, ours=any(r['kind'] == '우리' for r in refs), ours_page='firemap' in s)

if __name__ == '__main__':
    now = datetime.datetime.now()
    out = []
    for q in QUESTIONS:
        r = measure(q); out.append(r); time.sleep(3)
        print(q, '| 못 잼' if not r['ok'] else ('| 브리핑 있음 | 우리 인용 ' + ('O' if r['ours'] else 'X') + ' | ' + ', '.join(x['kind'] for x in r['refs'])) if r.get('aib') else '| 브리핑 없음')
    d = pathlib.Path(__file__).parent / 'research/growth/ai_briefing_raw'; d.mkdir(parents=True, exist_ok=True)
    (d / f'{now:%Y-%m-%d}.json').write_text(json.dumps(dict(at=f'{now:%Y-%m-%d %H:%M}', results=out), ensure_ascii=False, indent=1), encoding='utf-8')
