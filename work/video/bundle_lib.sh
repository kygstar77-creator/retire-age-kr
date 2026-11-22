# 렌더 스크립트용 bundle 함수(11/22 — bundle마다 public 전체 약 11GB를 복사해 C 드라이브가 2주에 두 번 찼다).
# 쓰는 법(렌더 스크립트 맨 위, R·D 정한 뒤):
#   . $R/work/video/bundle_lib.sh
#   B=$(fm_bundle $D src/c1s_index.ts) || { echo BUNDLE_FAIL; exit 1; }
#   ... npx remotion render $B ...
#   (CONCAT OK 뒤) fm_bundle_done $B
# - bundle은 늘 그 편 폴더 안 $D/bundle에만 만든다(다른 편 bundle을 빌려 쓰지 않는다 — 지워졌으면 렌더가 깨진다).
# - 렌더가 끝나면 fm_bundle_done이 바로 지운다. 중간에 실패해 남은 것은 work/bundleclean.py가 2시간 뒤 지운다.
fm_bundle() {
  local D="$1" ENTRY="${2:-src/c1s_index.ts}" B="$1/bundle"
  if [ ! -f "$B/index.html" ]; then
    (cd "$R/work/video" && npx remotion bundle "$ENTRY" --out-dir="$B" > "$D/bundle.log" 2>&1) || return 1
  fi
  echo "$B"
}
fm_bundle_done() {
  case "$1" in */bundle|*/bundle2|*/bundle_*) rm -rf "$1" && echo "BUNDLE_RM $1";; *) echo "BUNDLE_KEEP(이름이 bundle 아님) $1";; esac
}
