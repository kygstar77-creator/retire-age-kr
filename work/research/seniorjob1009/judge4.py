import sys, os, json, base64, urllib.request, re, time
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[-1].strip() for l in open(r'C:\Users\강영준\Documents\gemini_key.txt',encoding='utf-8-sig') if l.strip()][0]
M='gemini-3.1-flash-lite'
def ask(parts):
    err=''
    for t in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={KEY}',data=json.dumps({'contents':[{'parts':parts}]}).encode(),headers={'Content-Type':'application/json'}),timeout=240))
            return r['candidates'][0]['content']['parts'][0]['text']
        except Exception as e: err=str(e); time.sleep(5)
    return '(실패 '+err+')'
lead=open(H+'/pkg/c00.txt',encoding='utf-8').read()
T={'T5':'노인일자리 생계급여 받으면 어떤 유형만 신청할 수 있을까','T7':'노인일자리 생계급여·직장가입자도 신청할 수 있을까','T8':'노인일자리 생계급여 받으면 어떤 유형만 신청할 수 있을까'}
comp='노인일자리 신청방법｜60세·65세 기준부터 온라인·방문 신청까지 / 70세 이상 노인일자리, 지금도 신청할 수 있을까? 자격·급여·모집 확인 방법 / 노인일자리 신청방법 총정리, 115만개 중 내 유형 찾기 / 월 최대 70만 원 지원! 2026 노인 일자리 및 공공근로 지원 정책 신청 방법 총정리'
P=f'네이버 카페 글 제목 심사. 검색어 노인일자리(월 15,590). [경쟁 상위 제목] {comp}\n[본문 첫머리] {lead}\n[사실] 선발 제외: 생계급여 수급자·건보 직장가입자·장기요양 1~5등급·일자리 2개 이상 참여(취업지원 유형은 앞 셋 예외, 의료·주거·교육급여는 가능)\n[후보]\n'+'\n'.join(f'{k}. {v}' for k,v in T.items())+'\n기준: ①1초에 주제 ②궁금증 장치 ③낚시·과장 아님 ④경쟁 틀 반복 아님 ⑤검색어 앞. 6=경쟁 평균,7=통과,8=목표. 답: 후보마다 한 줄 "T1: 점수 N — 이유", 마지막 "1위: 기호".'
cp=f'네이버 카페 글 대표사진 심사(휴대폰 목록 110px로 줄어 보임). 글 제목: "{"노인일자리 생계급여 받으면 어떤 유형만 신청할 수 있을까"}". 사실: 생계급여 수급자·직장가입자는 선발 제외(취업지원 유형은 예외). 점수: N(1~10, 6=경쟁평균, 7=통과) 형식 첫 줄, 이어서 읽히는 글자·약점·오독 위험.'

raw=[]
for i in ():
    t=ask([{'text':P}]); raw.append('[title %d]\n'%i+t); print(t[:700]); print('--')
for n in ('N7','N9'):
    for i in (1,2):
        t=ask([{'text':cp},{'inline_data':{'mime_type':'image/png','data':base64.b64encode(open(H+'/covers_try/00_%s.png'%n,'rb').read()).decode()}}]); raw.append('[cover %s %d]\n'%(n,i)+t)
        m=re.search(r'점수[^0-9]{0,20}(\d+(?:\.\d+)?)',t); print(n,i,m.group(1) if m else t[:80])
open(H+'/judge_raw4.md','w',encoding='utf-8').write('\n---\n'.join(raw))
