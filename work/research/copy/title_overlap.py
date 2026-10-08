import json,glob,os,re
B='C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research'
comp={}
def walk(o,src):
    if isinstance(o,dict):
        t=o.get('title')
        if isinstance(t,str) and len(t)>=12 and (o.get('views') or o.get('viewCount') or o.get('view_count') or o.get('channel') or o.get('channelTitle') or o.get('channel_title')):
            v=o.get('views') or o.get('viewCount') or o.get('view_count') or ''
            ch=o.get('channel') or o.get('channelTitle') or o.get('channel_title') or ''
            comp.setdefault(t,(src,v,ch))
        for x in o.values(): walk(x,src)
    elif isinstance(o,list):
        for x in o: walk(x,src)
files=glob.glob(B+'/longform/**/*.json',recursive=True)+glob.glob(B+'/cardshorts/**/yt*.json',recursive=True)+glob.glob(B+'/longform/breakdown/*.json')
ours={}
for f in files:
    if os.path.basename(f)=='meta.json':
        if os.path.basename(os.path.dirname(os.path.dirname(f)))!='ep': continue
        d=json.load(open(f,encoding='utf-8')); ours[f.split(os.sep)[-2]]=d.get('title');continue
    if f.endswith('meta.json'): continue
    try: walk(json.load(open(f,encoding='utf-8')),os.path.relpath(f,B))
    except Exception: pass
def norm(s): return re.sub(r'[\s\W_]+','',s.lower())
def tri(s):
    s=norm(s); return {s[i:i+3] for i in range(len(s)-2)}
def skel(s): # 틀: 숫자→N
    return re.sub(r'\d[\d,.]*\s*(억|만원|만 원|원|%|년|배|천만원)?','N',s)
print('competitor titles:',len(comp),'from',len(files),'files')
for ep,t in sorted(ours.items()):
    if not t: continue
    a=tri(t); sk=tri(skel(t))
    res=[]
    for c,(src,v,ch) in comp.items():
        if norm(c)==norm(t): continue
        b=tri(c)
        ov=len(a&b)/max(1,min(len(a),len(b)))
        so=len(sk&tri(skel(c)))/max(1,min(len(sk),len(tri(skel(c)))))
        res.append((max(ov,so),ov,so,c,src,v,ch))
    res.sort(reverse=True)
    print('\n##',ep,t)
    for r in res[:3]: print('  %.2f (글 %.2f 틀 %.2f) %s | %s %s %s'%r[:3]+'' if False else '  %.2f (글 %.2f 틀 %.2f) %s | %s | %s | %s'%(r[0],r[1],r[2],r[3][:70],r[6],r[5],r[4]))
