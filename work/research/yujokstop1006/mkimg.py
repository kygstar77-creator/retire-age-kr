# yujokstop1006 본문 표 2장 — firemap-write 2026-10-05 22:3x (goldway1005/mkimg.py 틀)
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['1953~1956년','56세'],['1957~1960년','57세'],['1961~1964년','58세'],['1965~1968년','59세'],['1969년 이후','60세']]
B.table('pkg/img/01.png','유족연금 멈췄다 다시 받는 나이',['배우자 출생연도','다시 받는 나이'],rows,hl_col=1,
        note='법 조문은 55세, 부칙이 출생연도마다 1~5세를 더한다',src='국민연금법 제76조제1항 · 부칙(법률 제8541호) 제8조')
rows2=[['57세 이후','3년 받는 사이 60세 넘음','0년'],['52세','55세~60세','5년'],['50세','53세~60세','7년'],['45세','48세~60세','12년']]
B.table('pkg/img/02.png','1969년 이후 출생 배우자, 멈출 수 있는 기간',['배우자를 잃은 나이','멈출 수 있는 때','기간'],rows2,hl_col=2,
        note='예외(장애·25세 미만 자녀 부양·기준 넘는 소득 없음)에 하나라도 해당하면 멈추지 않는다',src='국민연금법 제76조제1항 · 부칙(법률 제8541호) 제8조')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
