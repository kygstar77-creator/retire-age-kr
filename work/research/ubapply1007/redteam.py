import sys, os, json, urllib.request, time, base64
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
body=''.join(open(os.path.join(H,'pkg',f),encoding='utf-8').read()+'\n' for f in ['c00.txt','c01.txt','c03.txt','c04.txt','c05.txt'])
img=base64.b64encode(open(os.path.join(H,'pkg','img','00.png'),'rb').read()).decode()
ROLES={'레드팀':'당신은 냉정한 레드팀입니다. 제목 약점·과장·사실 오류 가능성을 공격하세요.',
       '독자':'당신은 퇴직을 앞둔 55세 직장인으로 네이버 카페 목록에서 제목과 썸네일만 보고 누를지 정합니다.'}
for role,persona in ROLES.items():
    P=(f'{persona}\n제목: 실업급여 270일 받는 분이 신청을 4개월 미루면 얼마를 못 받을까\n첨부 이미지는 그 글의 대표 썸네일(1초 시험).\n[본문]\n{body}\n'
       '1) 제목 점수(0~10, 6=경쟁 평균, 7=통과) 2) 썸네일 1초 시험 점수(0~10) 3) 본문 사실·산수에서 틀리거나 오해될 수 있는 문장(있으면 인용, 없으면 없음) 4) 고칠 점 한 줄. 첫 줄은 "제목:점수 썸네일:점수" 형식.')
    r=None
    for m in ('gemini-3.1-flash-lite','gemini-3-flash-preview'):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={KEY}',
              data=json.dumps({'contents':[{'parts':[{'text':P},{'inline_data':{'mime_type':'image/png','data':img}}]}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            t=m+'\n'+r['candidates'][0]['content']['parts'][0]['text']; break
        except Exception as e: t='실패 '+str(e)[:100]
    print('=====',role); print(t)
