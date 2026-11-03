# law.go.kr 웹(lsSideInfoP)에서 조문 본문 텍스트를 받아 저장한다. 법령 API(OC=test)가 "사용자 검증 실패"일 때 쓴다(2026-11-03 firemap-write).
# 실행: PYTHONIOENCODING=utf-8 py -3.12 work/lawweb.py 주택임대차보호법 제3조의3 <pkg>/raw<날짜>/파일.txt  (Windows에서 한글 인자는 Git Bash로)
import sys, re, urllib.request, urllib.parse, html
law, jo, out = sys.argv[1], sys.argv[2], sys.argv[3]
u = "https://www.law.go.kr/" + urllib.parse.quote(f"법령/{law}/{jo}")
r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"}), timeout=20).read().decode("utf-8","replace")
src = html.unescape(re.search(r'src="(/LSW/[^"]*lsSideInfoP[^"]*)"', r).group(1))
b = urllib.request.urlopen(urllib.request.Request("https://www.law.go.kr"+src, headers={"User-Agent":"Mozilla/5.0","Referer":u}), timeout=20).read().decode("utf-8","replace")
t = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
t = html.unescape(re.sub(r"<[^>]+>", "\n", t)); t = "\n".join(l.strip() for l in t.splitlines() if l.strip())
open(out, "w", encoding="utf-8").write(f"# {u}\n# {'https://www.law.go.kr'+src}\n# 받은 날 2026-11-03\n\n{t}\n")
print(len(t))
