# W-3 끝맺음 표본: 경쟁 영상 마지막 50초를 제미나이 구간 보기로 받아 적는다(2026-10-20 youtube-loop, 자막 API IpBlocked 대체)
import json, sys, urllib.request
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
vid, dur, title = sys.argv[1], int(sys.argv[2]), sys.argv[3]
s=max(0,dur-50)
prompt="이 구간(영상 마지막 50초)에서 화자가 한 말을 [mm:ss] 시각과 함께 한국어로 그대로 받아 적고, 끝에 화면에 무엇이 보였는지 두세 문장. 지어내지 말고 들리지 않으면 '안 들림'."
for model in ['gemini-3-flash-preview','gemini-2.5-flash']:
    body={'contents':[{'parts':[{'file_data':{'file_uri':f'https://www.youtube.com/watch?v={vid}'},'video_metadata':{'start_offset':f'{s}s','end_offset':f'{dur}s'}},{'text':prompt}]}],'generationConfig':{'maxOutputTokens':2000}}
    req=urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    try:
        r=json.load(urllib.request.urlopen(req,timeout=240)); txt=r['candidates'][0]['content']['parts'][0]['text']; break
    except Exception as e:
        txt=None; err=str(e)[:200]
if not txt: print('ERR',err); sys.exit(1)
out=f"# {vid} 끝 50초 ({title} · 구간 {s}~{dur}s · {model} · 2026-10-20)\nhttps://www.youtube.com/watch?v={vid}&t={s}s\n\n{txt}\n"
open(sys.argv[4],'w',encoding='utf-8').write(out); print(out[:1500])
