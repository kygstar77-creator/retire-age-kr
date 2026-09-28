import json,re,collections,statistics,subprocess,sys
sys.stdout.reconfigure(encoding='utf-8')
sgg=json.load(open('research/seoul_sgg.json',encoding='utf-8'))
num=lambda s:int(re.sub(r'[^\d]','',s or '0') or 0)
key=lambda r:(r['aptSeq'],r['excluUseAr'],r['dealAmount'],r['dealDay'],r['floor'])
T=[];new=[];PUB=[]
for l,n in sgg.items():
  cur=json.load(open(f'research/rt/{l}_202609_trade.json',encoding='utf-8'))
  old=json.loads(subprocess.run(['git','show',f'HEAD:work/research/rt/{l}_202609_trade.json'],capture_output=True).stdout.decode('utf-8'))
  ok={key(r) for r in old}
  for r in cur:
    r['gu']=n
    if r['cdealType']: continue
    if r.get('buyerGbn')=='공공기관': PUB.append(r); continue
    T.append(r)
    if key(r) not in ok: new.append(r)
print('9월 매매(해제 제외)',len(T),'9/23 수집 뒤 새로 올라온',len(new))
print('9/23 수집분',sum(1 for l in sgg for r in json.loads(subprocess.run(['git','show',f'HEAD:work/research/rt/{l}_202609_trade.json'],capture_output=True).stdout.decode('utf-8')) if not r['cdealType']))
print('중앙(만원)',statistics.median(num(r['dealAmount']) for r in T))
g=collections.Counter(r['gu'] for r in T); print('구 상위',g.most_common(5)); print('구 하위',g.most_common()[-3:])
c=collections.Counter((r['gu'],r['umdNm'],r['aptNm']) for r in T); print('단지 상위',c.most_common(6))
for r in sorted(T,key=lambda r:-num(r['dealAmount']))[:6]: print('비싼',r['gu'],r['umdNm'],r['aptNm'],r['excluUseAr'],r['dealAmount'],'9/'+r['dealDay'],r['floor'],r['buildYear'],r.get('dealingGbn'))
print('새로 올라온 것 구',collections.Counter(r['gu'] for r in new).most_common(5))
for r in sorted(new,key=lambda r:-num(r['dealAmount']))[:5]: print('새 비싼',r['gu'],r['umdNm'],r['aptNm'],r['excluUseAr'],r['dealAmount'],'9/'+r['dealDay'],r['floor'])
print('공공기관 매입',len(PUB),collections.Counter((r['gu'],r['aptNm']) for r in PUB).most_common(4))
t8=[r for l in sgg for r in json.load(open(f'research/rt/{l}_202608_trade.json',encoding='utf-8')) if not r['cdealType'] and r.get('buyerGbn')!='공공기관']
print('8월 전체',len(t8),'8월 중앙',statistics.median(num(r['dealAmount']) for r in t8))
