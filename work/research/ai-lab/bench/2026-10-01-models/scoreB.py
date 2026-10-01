import re,sys,subprocess,collections
src=open('src2.md',encoding='utf-8').read()
src=re.sub(r'\(화면:[^)]*\)','',src)
num=lambda t: collections.Counter(re.findall(r'\d[\d,\.]*',t))
S=num(src)
for m in ['haiku','sonnet','opus']:
    try: t=open(f'outB_{m}.txt',encoding='utf-8').read()
    except: print(m,'missing'); continue
    T=num(t)
    miss=[k for k in S if k not in T]; extra=[k for k in T if k not in S]
    ko=len(re.findall(r'[가-힣]',t))
    r=subprocess.run(['py','-3.12','C:/Users/강영준/Documents/GitHub/retire-age-kr/work/aitell.py',f'outB_{m}.txt'],capture_output=True,text=True,encoding='utf-8')
    print(f'== {m} 한글{ko}자 빠진숫자{miss} 새숫자{extra}'); print(r.stdout.strip()[:600])
