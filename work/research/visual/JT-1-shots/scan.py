"""경쟁 장면 &t=초가 진행자 얼굴에 떨어진 번호의 앞뒤 초를 훑어 실제 장면 시각 찾기(visual 11/16). 영상 안 받음, 스트림 프레임만."""
import os,sys,subprocess,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
FF=imageio_ffmpeg.get_ffmpeg_exe(); F=ImageFont.truetype('../../../fonts/pd700.ttf',20)
jobs=[('5','TX4W8Tpftfg',602),('9','8A9Dm0Gm2cQ',326),('13','vRBgIpV-nPo',316),('14','vRBgIpV-nPo',503)]
off=[-40,-25,-10,5,20,35,50,70]; W,H=320,180
urls={}
im=Image.new('RGB',(W*len(off),(H+26)*len(jobs)),'white'); d=ImageDraw.Draw(im)
for r,(n,vid,t) in enumerate(jobs):
    if vid not in urls:
        urls[vid]=subprocess.run([sys.executable,'-m','yt_dlp','-q','--js-runtimes','node','-f','best[height<=480]/bv*[height<=480]','-g',f'https://www.youtube.com/watch?v={vid}'],capture_output=True,text=True).stdout.strip().splitlines()[0]
    for k,o in enumerate(off):
        s=max(0,t+o); p=os.path.join(os.environ['TEMP'],f'scan_{n}_{s}.jpg')
        subprocess.run([FF,'-y','-loglevel','error','-ss',str(s),'-i',urls[vid],'-frames:v','1','-vf',f'scale={W}:{H}',p])
        d.text((k*W+4,r*(H+26)+2),f'#{n} {s}s',font=F,fill='black')
        if os.path.exists(p): im.paste(Image.open(p),(k*W,r*(H+26)+26))
im.save('scan_sheet.jpg',quality=80)
