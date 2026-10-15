import sys, re
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
sys.stdout.reconfigure(encoding='utf-8')
import toprank
s = open('src/nv_은행주 배당.html', encoding='utf-8', errors='replace').read()
seen = []
for m in re.finditer(r'blog\.naver\.com/([A-Za-z0-9_\-]+)/(\d{9,})', s):
    if m.groups() not in seen: seen.append(m.groups())
out = []
for i, (bid, no) in enumerate(seen[:6], 1):
    r = toprank.post(bid, no)
    if not r: print(i, 'fail', bid); continue
    open(f'comp_{bid}_{no}.txt', 'w', encoding='utf-8').write(r['title'] + '\n' + '\n'.join(r['paras']))
    t = '\n'.join(r['paras'])
    print(i, bid, no, r['title'][:60], r['chars'], r['imgs'], '| 배당수익률', t.count('배당수익률'), '1천만', t.count('1천만') + t.count('1,000만'), '세후', t.count('세후'), '분기', t.count('분기'), '코스피', t.count('코스피'), '날짜', re.findall(r'2026[.\-년 ]+\d+', t)[:2])
    out.append(f'{i} | {r["title"]} | {r["chars"]}자·{r["imgs"]}장 | https://blog.naver.com/{bid}/{no}')
open('comp_titles.txt', 'w', encoding='utf-8').write('\n'.join(out))
