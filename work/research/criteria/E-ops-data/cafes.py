import json,urllib.request,time,sys,datetime,collections,statistics as st
sys.stdout.reconfigure(encoding='utf-8')
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'
C={'31789001':'파이어맵(우리)','31050378':'배당 투자자 모임','22290117':'월급쟁이 재테크 연구','23676262':'은퇴 후 50년','26251287':'거북이투자법','28497937':'미국 주식이 미래다','12730407':'부동산 스터디','15112066':'평생주식카페'}
out={}
for cid,nm in C.items():
    arts=[]
    for p in range(1,41):
        u=f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.queryType=lastArticle&search.page={p}&search.perPage=50'
        try:
            r=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=20).read())
        except Exception as e: print(nm,'err',e); break
        res=r['message']['result']; al=res.get('articleList',[])
        arts+= [dict(id=a['articleId'],ts=a['writeDateTimestamp'],nick=a['writerNickname'],mk=a.get('memberKey'),lv=a.get('memberLevel'),menu=a.get('menuName'),read=a.get('readCount'),cmt=a.get('commentCount'),subj=a.get('subject','')[:40]) for a in al]
        if not res.get('hasNext') or not al: break
        if (arts[0]['ts']-arts[-1]['ts'])/864e5>14: break
        time.sleep(0.4)
    out[cid]=dict(name=nm,arts=arts); print(nm,len(arts),flush=True)
json.dump(out,open('cafes.json','w',encoding='utf-8'),ensure_ascii=False)
