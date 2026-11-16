import os,sys,subprocess,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
FF=imageio_ffmpeg.get_ffmpeg_exe(); S='stock_try/stock'
ids=sys.argv[1:]; W,H=320,180
im=Image.new('RGB',(W*4,(H+24)*len(ids)),'white'); d=ImageDraw.Draw(im)
F=ImageFont.truetype('../../../fonts/pd700.ttf',18)
for r,i in enumerate(ids):
    dur=float(subprocess.run([sys.executable,'-c',f"import imageio_ffmpeg as f;print(f.count_frames_and_secs(r'{S}/{i}.mp4')[1])"],capture_output=True,text=True).stdout.strip() or 8)
    d.text((4,r*(H+24)+2),i,font=F,fill='black')
    for k,t in enumerate([0.1,0.35,0.6,0.85]):
        p=f'{os.environ["TEMP"]}/jt1s_{i}_{k}.jpg'
        subprocess.run([FF,'-y','-loglevel','error','-ss',str(dur*t),'-i',f'{S}/{i}.mp4','-frames:v','1','-vf',f'scale={W}:{H}',p])
        if os.path.exists(p): im.paste(Image.open(p),(k*W,r*(H+24)+24))
im.save(sys.argv[0].replace('sheet.py','')+'sheet_'+ids[0]+'.jpg',quality=80)
