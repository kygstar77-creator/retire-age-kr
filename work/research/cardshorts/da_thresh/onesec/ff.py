# da_thresh 첫 프레임 1초 시험 — npsday1007/onesec 방식(경쟁5 비교판 168px + gemini-3.1-flash-lite 고정) 축약판. firemap-shorts 10/10
import sys, os, json, base64, urllib.request, re, subprocess, time
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(os.path.join(H,'..','..'))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
COMP=['-YuYOLaMYcM','HXqB-GiDwtY','KfQASIS4G0A','UINdvu1cqkc','yF8xbi4CwbU']
W,HH=168,299
def small(im):
    im=im.convert('RGB'); w,h=im.size; t=round(h*9/16)
    if t<w: im=im.crop(((w-t)//2,0,(w-t)//2+t,h))
    return im.resize((W,HH),Image.LANCZOS)
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
mp4=os.path.join(R,'da_thresh.mp4'); ff=os.path.join(H,'first_f05.png')
subprocess.run([FF,'-v','error','-y','-ss','0.5','-i',mp4,'-frames:v','1',ff],check=True)
tiles=[('우리',small(Image.open(ff)))]
for i,v in enumerate(COMP):
    p=os.path.join(H,v+'.jpg')
    if not os.path.exists(p):
        for q in ('oardefault','hqdefault'):
            try: open(p,'wb').write(urllib.request.urlopen(f'https://i.ytimg.com/vi/{v}/{q}.jpg',timeout=30).read()); break
            except Exception as e: print(v,q,e)
    tiles.append(('경쟁%d'%(i+1),small(Image.open(p))))
F=ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf',13)
b=Image.new('RGB',(len(tiles)*(W+8)+8,HH+30),'white'); d=ImageDraw.Draw(b)
for n,(lab,im) in enumerate(tiles): b.paste(im,(8+n*(W+8),26)); d.text((8+n*(W+8),5),lab,fill='black',font=F)
bp=os.path.join(H,os.environ.get('B','ff_board168.png')); b.save(bp)
def ask(t,p):
    parts=[{'text':t},{'inline_data':{'mime_type':'image/png','data':base64.b64encode(open(p,'rb').read()).decode()}}]
    for k in range(3):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':parts}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return '(실패 '+err+')'
def sc(t):
    m=re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)',t); return float(m.group(1)) if m else None
PS=('유튜브 쇼츠 첫 프레임(휴대폰 목록 크기, 세로형 가로 168px) 심사. 이미지는 비교판이다. 맨 왼쪽 "우리"가 발행 전 시안, "경쟁1~5"는 같은 주제(건강보험 피부양자 소득) 최근 30일 쇼츠 상위 영상의 실제 표지.\n'
 '영상 제목: "피부양자 소득 2천만원, 1,999만원 vs 2,001만원 뭐가 달라질까? #shorts"\n영상 내용: 법령 원문 기준 카드 — 합산소득 연 2천만원 이하면 소득요건 통과(1,999만원), 2,001만원은 초과. 사업소득·재산요건도 같이 맞아야 한다는 단서 포함.\n'
 '제약: 인물 금지, 과장·낚시 금지, 숫자는 원문 그대로.\n'
 '답 형식: 첫 줄 "점수: N"(1~10, 이 목록에서 경쟁 썸네일 옆에 있을 때 먼저 누르고 싶은가 + 168px에서 글자가 읽히는가. 6=경쟁 평균, 7=통과, 8=목표) · 읽히는 글자 · 1초 주제 한 문장 · 약점 · 8점이 되려면 바꿀 것 한 가지. 그 아래 "카피 점수: N"(제목·첫 3초 문구: 1초 주제, 궁금증 장치, 낚시 아님, 경쟁 제목 틀 반복 아님, 검색어 앞 — 5기준).')
raw=[];v=[]
for r in range(2):
    t=ask(PS,bp); v.append(sc(t)); raw.append(f'### 회{r+1} 점수 {v[-1]}\n{t}\n')
print(v)
open(os.path.join(H,os.environ.get('O','')+'ff_raw.md'),'w',encoding='utf-8').write('\n'.join(raw))
