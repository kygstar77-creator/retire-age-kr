# 토막 렌더 중 디스크 감시(회의 11/2 21:43 3GB 선): 3GB 아래면 J-1 렌더 프로세스만 멈춤, 최저 남은 양 기록
EP=C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/longform/ep/J-1
start=$(df -BM /c | tail -1 | awk '{print $4}' | tr -d M); low=$start
for i in $(seq 1 720); do
  [ -f $EP/check/parts_done_1103 ] && break
  f=$(df -BM /c | tail -1 | awk '{print $4}' | tr -d M); [ $f -lt $low ] && low=$f
  if [ $f -lt 3000 ]; then echo "$(date '+%F %H:%M') 남은 ${f}MB < 3GB — 멈춤" | tee -a $EP/renderguard.log
    powershell -NoProfile -Command "Get-CimInstance Win32_Process | ? { \$_.CommandLine -match 'render_parts_1103|lfrender.py render .*J-1|props=j1.json' } | % { Stop-Process -Id \$_.ProcessId -Force }"; break; fi
  sleep 20
done
echo "$(date '+%F %H:%M') 토막 렌더 감시 끝 · 시작 ${start}MB 최저 ${low}MB 최대 사용 $((start-low))MB 멈춤선 3GB" >> $EP/renderguard.log
