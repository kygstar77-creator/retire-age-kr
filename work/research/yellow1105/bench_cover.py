import re,subprocess,html,sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
UA="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
posts=[("adolfs","224429587454"),("gktnrndlsrks","224454151456"),("phillaslie","224461411489"),("sg-on","224452017136"),("kang4862","224462917238")]
ims=[]
for b,n in posts:
    h=subprocess.run(["curl","-s","-A",UA,f"https://m.blog.naver.com/PostView.naver?blogId={b}&logNo={n}"],capture_output=True).stdout.decode("utf-8","ignore")
    m=re.search(r'<meta property="og:image" content="([^"]*)"',h)
    if not m: print(b,'no og');continue
    u=html.unescape(m.group(1)); p=f"bench_raw/cover_{b}.jpg"
    subprocess.run(["curl","-s","-A",UA,"-e","https://m.blog.naver.com/","-o",p,u])
    try: im=Image.open(p).convert('RGB'); ims.append(im); print(b,im.size,u[:90])
    except Exception as e: print(b,'bad',e)
W=360; row=Image.new('RGB',(W*len(ims),W),'white')
for i,im in enumerate(ims):
    im.thumbnail((W,W)); row.paste(im,(i*W,(W-im.size[1])//2))
row.save('bench_raw/cover_cmp.png')
