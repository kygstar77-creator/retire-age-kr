# irp70_1020 그림 3장 — 표지(두 줄 비교) · 01 두 계좌 위험자산 비중 막대 · 02 계좌별 한도와 넘었을 때
import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F
BG=(250,247,240); INK=(24,32,56); SUB=(110,116,130); ACC=(214,72,32); LINE=(222,218,208); SAFE=(120,150,190); RISK=(214,72,32)

# 00 표지 v2 — 심사(bench_shots/judge.md): 제목 1.3~1.5배, 카드 글자 줄이기, 100px 읽힘
im=Image.new('RGB',(1080,1080),BG); d=ImageDraw.Draw(im)
d.text((80,70),'IRP · DC 퇴직연금',font=F(40,True),fill=SUB)
d.text((80,135),'위험자산 70%',font=F(128,True),fill=INK)
d.text((80,290),'넘었다는 문자',font=F(128,True),fill=INK)
d.text((80,445),'팔아야 할까?',font=F(128,True),fill=ACC)
d.rounded_rectangle((80,660,1000,860),radius=28,fill=(255,255,255),outline=LINE,width=3)
d.text((120,690),'작년 말 70% 담은 코스피200 ETF 계좌',font=F(38,True),fill=SUB)
d.text((120,760),'지금 77.5%',font=F(72,True),fill=ACC)
d.text((80,905),'강제로 팔리지는 않아요',font=F(72,True),fill=INK)
d.text((80,1030),'자료: 미래에셋·KB자산운용 연금 안내 · 야후·네이버 증권(10/19 종가)',font=F(22),fill=SUB)
im.save('pkg/img/00.png'); im.resize((100,100),Image.LANCZOS).save('pkg/cover_100.png')

# 01 두 계좌 막대
im=Image.new('RGB',(1080,760),BG); d=ImageDraw.Draw(im)
d.text((60,50),'작년 말 1억을 70 : 30으로 나눴다면',font=F(46,True),fill=INK)
d.text((60,115),'10월 19일 종가로 다시 잰 위험자산 비중',font=F(32),fill=SUB)
X0,X1=60,1020
def bar(y,name,share,amt):
    d.text((X0,y),name,font=F(36,True),fill=INK)
    w=(X1-X0); r=int(w*share/100)
    d.rectangle((X0,y+60,X0+r,y+150),fill=RISK); d.rectangle((X0+r,y+60,X1,y+150),fill=SAFE)
    d.text((X0+20,y+82),f'위험자산 {share}%',font=F(40,True),fill=(255,255,255))
    d.text((X0,y+165),amt,font=F(30),fill=SUB)
bar(190,'KODEX 200 (코스피200)',77.5,'70% 선과의 차이 약 1,000만원')
bar(440,'TIGER 미국S&P500',70.6,'70% 선과의 차이 약 64만원')
for y in (250,500):
    x=X0+int((X1-X0)*0.7); d.line((x,y-10,x,y+160),fill=INK,width=5)
d.text((X0+int((X1-X0)*0.7)+14,150),'70% 선',font=F(30,True),fill=INK)
d.text((60,725),'파란 칸 = 예금(안전자산) · ETF 가격만, 예금 이자 뺌 · 자료: 야후·네이버 증권 · 10/20 조회',font=F(22),fill=SUB)
im.save('pkg/img/01.png')

# 02 계좌별 한도와 넘었을 때
im=Image.new('RGB',(1080,820),BG); d=ImageDraw.Draw(im)
d.text((60,50),'계좌마다 다른 위험자산 한도',font=F(50,True),fill=INK)
def card(y,name,lim,col):
    d.rounded_rectangle((60,y,1020,y+120),radius=22,fill=(255,255,255),outline=LINE,width=3)
    d.text((100,y+35),name,font=F(44,True),fill=INK)
    tw=d.textlength(lim,font=F(48,True)); d.text((980-tw,y+33),lim,font=F(48,True),fill=col)
card(140,'연금저축','한도 없음',(40,80,140))
card(280,'IRP (개인형 퇴직연금)','70%까지',ACC)
card(420,'DC (확정기여형)','70%까지',ACC)
d.text((60,580),'가격이 올라 70%를 넘으면',font=F(40,True),fill=INK)
d.text((60,640),'· 강제로 팔리지 않음, 금융회사가 알려 줌',font=F(36),fill=INK)
d.text((60,695),'· 주식형을 새로 더 살 수 없음',font=F(36),fill=INK)
d.text((60,775),'자료: 근로자퇴직급여 보장법 시행규칙 제10조 · 미래에셋·KB자산운용 안내',font=F(22),fill=SUB)
im.save('pkg/img/02.png')
json.dump({"made_at":"2026-10-20","by":"irp70_1020/mkimg.py","out":"img/00.png","type":"chart","source":"네이버 증권 fchart 수정주가 KODEX 200·TIGER 미국S&P500 2025-12-30·2026-10-19 종가로 계산(../calc.py), 퇴직연금감독규정 제13조② — 두 줄 비교표"},open('pkg/cover_meta.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
