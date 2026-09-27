import json,glob,os,statistics,sys
sys.stdout.reconfigure(encoding='utf-8')
GU={'11110':'종로구','11140':'중구','11170':'용산구','11200':'성동구','11215':'광진구','11230':'동대문구','11260':'중랑구','11290':'성북구','11305':'강북구','11320':'도봉구','11350':'노원구','11380':'은평구','11410':'서대문구','11440':'마포구','11470':'양천구','11500':'강서구','11530':'구로구','11545':'금천구','11560':'영등포구','11590':'동작구','11620':'관악구','11650':'서초구','11680':'강남구','11710':'송파구','11740':'강동구'}
res=[];seen=set();tot=0
for c,n in GU.items():
    v=[]
    for m in ('202607','202608','202609'):
        f='../rt/%s_%s_trade.json'%(c,m)
        if not os.path.exists(f): continue
        for r in json.load(open(f,encoding='utf-8')):
            if r.get('cdealType'): continue   # 해제 신고 제외
            a=float(r['excluUseAr'])
            if not (57<=a<=60.5): continue
            k=(r['aptSeq'],r['dealYear'],r['dealMonth'],r['dealDay'],r['floor'],r['dealAmount'],r['excluUseAr'])
            if k in seen: continue
            seen.add(k)
            v.append(int(r['dealAmount'].replace(',','')))
    tot+=len(v)
    if len(v)>=10: res.append((n,statistics.median(v),len(v),min(v),max(v)))
res.sort(key=lambda x:-x[1])
print('전용 57~60.5㎡, 2026-07~09 계약, 해제 제외, 중복 제거. 총',tot,'건')
for r in res: print('%s 중앙값 %.0f만원 (%d건, 최저 %d 최고 %d)'%r)
print('파일 수정시각', max(os.path.getmtime(f) for f in glob.glob('../rt/*_202609_trade.json')))
