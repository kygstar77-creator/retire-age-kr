import re,html,json
import fbo_calc as F
def parse(x):
    x=re.sub(r'<script.*?</script>|<style.*?</style>','',x,flags=re.S)
    s=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x)))
    age=re.search(r'기준나이 : (\d+)세',s).group(1)
    m=re.search(r'종신정액형 ([\d,]+) \(저소득층: ([\d,]+) \) \(장기영농인: ([\d,]+) \)',s)
    j=re.search(r'전후후박형 ([\d,]+)\(전\) ([\d,]+)\(후\)',s)
    return dict(age=age,fixed=m.group(1),low=m.group(2),long=m.group(3),jeon=j.group(1),hu=j.group(2))
out={}
for age in (60,65,70,75,80):
    for amt in (100,200,300,400,500,600,800):
        x=F.q(f'{2026-age}-03-01',amt*1000000)
        try: out[f'{age}_{amt}']=parse(x)
        except Exception as e: out[f'{age}_{amt}']=str(e)
        print(age,amt,out[f'{age}_{amt}'])
# spouse succession: owner 65, spouse 58 / 55 vs non-succession
for b2,lab in (('1968-03-01','spouse58'),('1971-03-01','spouse55')):
    x=F.q('1961-03-01',300000000,succ='Y',b2=b2); 
    try: out['succ_'+lab]=parse(x)
    except Exception as e: out['succ_'+lab]=str(e)
    print(lab,out['succ_'+lab])
json.dump(out,open('grid.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
