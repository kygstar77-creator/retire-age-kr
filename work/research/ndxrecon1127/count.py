# 나스닥 공식 발표문(raw/pr20xx.html)에서 12월 정기 교체 넣은·뺀 회사 수와 티커를 다시 센다 — 11/26 write-b
import re, html, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')
def tx(f):
    t=open(f,encoding='utf-8',errors='ignore').read()
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
W={'three':3,'five':5,'six':6,'seven':7}
tot_a=tot_r=0; seen={}
for y,f in [(2019,'raw/pr2019.html'),(2020,'raw/pr2020.html'),(2021,'raw/pr2021.html'),(2022,'raw/pr2022.html'),(2023,'raw/pr2023.html'),(2024,'raw/pr2024.html'),(2025,'raw/pr2025.html'),('2026-06','raw/jun_finviz.html')]:
    s=tx(f)
    ann=re.search(r'NEW YORK ?, ?([A-Z][a-z]+\.? ?\d+, \d{4})',s).group(1)
    eff=re.search(r'effective prior to market open on (Monday, [A-Z][a-z]+ \d+, \d{4})',s).group(1)
    a_part=s[s.find('will be added'):s.find('will be added')+700]
    a_part=a_part[:a_part.find('. The')] if '. The' in a_part else a_part
    r_i=s.find('will be removed'); r_part=s[r_i:r_i+700]; r_part=r_part.split(' Information')[0].split(' For additional')[0]
    na=W[re.search(r'following (\w+) companies will be added',s).group(1)]
    nr=W[re.search(r'following (\w+) companies will be removed',s).group(1)]
    ta=re.findall(r'Nasdaq: ([A-Z]{2,5})',a_part); tr=re.findall(r'(?:Nasdaq: )?\(?([A-Z]{2,5})(?:/ ?[A-Z]+ ?)?\)',r_part)
    tr=[t for t in tr if t not in ('NDAQ',)]
    if y!='2026-06': tot_a+=na; tot_r+=nr
    for t in ta: seen.setdefault(t,[]).append(f'{y} 들어옴')
    for t in tr: seen.setdefault(t,[]).append(f'{y} 빠짐')
    print(f'{y} | 발표 {ann} | 적용 {eff} | 넣음 {na} {ta} | 뺌 {nr} {tr}')
print(f'\n12월 정기 교체 2019~2025 7번: 넣음 합 {tot_a} · 뺌 합 {tot_r} · 평균 넣음 {tot_a/7:.1f}')
print('\n두 번 넘게 나온 회사:')
for t,v in seen.items():
    if len(v)>=2: print(' ',t,' · '.join(v))
# 2026년 12월 셋째 금요일
d=datetime.date(2026,12,1); fr=[d+datetime.timedelta(i) for i in range(31) if (d+datetime.timedelta(i)).weekday()==4]
print('\n2026-12 금요일:',fr[:3],'→ 둘째',fr[1],'셋째',fr[2],'다음 월요일',fr[2]+datetime.timedelta(3))
