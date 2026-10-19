#!/bin/bash
# 받는 대로 잰다: runall을 되풀이(다 재면 끝). 인자: 순서(fwd|rev|long)
cd "$(dirname "$0")"
for i in $(seq 1 200); do
  py -3.12 runall.py media 0 1 $1 >> media/run_$1.log 2>&1
  n=$(ls res/*.json 2>/dev/null | wc -l); [ "$n" -ge 43 ] && break
  sleep 30
done
