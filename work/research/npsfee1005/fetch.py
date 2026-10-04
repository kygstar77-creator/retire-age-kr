import urllib.request, urllib.parse, re, sys
sys.stdout.reconfigure(encoding='utf-8')
for name,out in [('국민연금법','law.xml'),('국민연금법 시행령','rule.xml')]:
    u='http://www.law.go.kr/DRF/lawService.do?OC=test&target=law&type=XML&LM='+urllib.parse.quote(name)
    x=urllib.request.urlopen(u,timeout=60).read().decode('utf-8')
    open(out,'w',encoding='utf-8').write(x)
    m=re.search(r'<시행일자>(\d+)</시행일자>',x); print(name,len(x),m.group(1) if m else None)
