import re,requests,sys,html
S=requests.Session()
r=S.get('https://www.fbo.or.kr/pesn/my/IqireForm.do?menuId=04101020',timeout=30)
t=r.text
tok=re.search(r'name="csrfToken" value="([^"]+)"',t).group(1)
print('baseYear',re.findall(r'baseYear1\s*=\s*([^;]+);',t),re.findall(r'pensionRate\s*=\s*([^;]+);',t))
def q(birth,amount,succ='N',b2='',method='P',serp='5'):
    d={'csrfToken':tok,'birthday1':birth,'birthday2':b2,'successionYn':succ,'flndEvlMth':method,'amount':str(amount),'menuId':'04101020','serp':serp}
    r=S.post('https://www.fbo.or.kr/pesn/my/Iqire.do',data=d,timeout=30)
    return r.text
if __name__=='__main__':
    x=q(sys.argv[1],sys.argv[2])
    x=re.sub(r'<script.*?</script>|<style.*?</style>','',x,flags=re.S)
    print(re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x)))[:2500])
