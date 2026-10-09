import sys,re; sys.path.insert(0,'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
for t in sys.stdin.read().strip().splitlines():
    nums=len(re.findall(r'\d+(?:,\d+)*',t)); 
    bad=[]
    if re.search(r'왜|는데',t): bad.append('반전')
    core=re.sub(r"[\s\)\]\.!·~…\"']+$","",t)
    if (t.endswith('?') or re.search(r'(까|나요|가요|죠|요|니다)$',core)) and not re.search(r'얼마|몇',t): bad.append('물음B틀')
    if ',' in t: bad.append('쉼표')
    print(len(t),'자 숫자',nums,bad,t)
