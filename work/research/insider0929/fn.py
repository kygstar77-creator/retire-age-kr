import urllib.request,re,sys,time
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'firemap research kygstar77@gmail.com'}
urls=sys.argv[1:]
for u in urls:
    t=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read().decode('utf-8','ignore')
    fns=re.findall(r'<footnote id="(F\d+)">(.*?)</footnote>',t,re.S)
    rem=re.findall(r'<remarks>(.*?)</remarks>',t,re.S)
    per=re.findall(r'<periodOfReport>(.*?)</periodOfReport>',t)
    print('==',u,per)
    for i,f in fns: print(' ',i,re.sub(r'\s+',' ',f)[:300])
    for r in rem: print('  REM',re.sub(r'\s+',' ',r)[:200])
    time.sleep(0.2)
