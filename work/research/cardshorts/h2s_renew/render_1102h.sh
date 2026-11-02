# h2s_renew 11/2 PD: c1clip(C1S live) · 디스크 22GB라 06:29 묶음에 이 편 파일(bg/h2 9컷·audio/h-2 9줄)만 채워 렌더(de1s_jepi 11/2와 같은 방법)
# 11/2 10시 PD: 칸 시각 고친 props(h2rclip.pre1102c) · 29826322·6787197을 libx264 -g 30으로 다시 싸서 public과 묶음에 복사(원본 public/bg/h2/_orig_*.mp4)
# 11/2 10시 2차: 466·0건 꼬리말 고친 props
# 2차 실패(5923592 No frame found 399프레임) → 쓰는 배경 7개 전부 libx264 -g 30로 다시 싸서 묶음에 복사
# 3차 실패(36216207 1145프레임, 클립마다 바뀜) → concurrency 1
set -u
# 11/2 4·5차: 29826322(1.6초)·6787197(1.4초) "No frame found" — 앞 렌더에선 같은 클립이 됐음(그때그때 나는 오류) → concurrency 2·캐시 1GB로
R=/c/Users/강영준/Documents/GitHub/retire-age-kr; D=$R/work/research/cardshorts/h2s_renew
cd $R/work/video && npx remotion render /c/Users/강영준/AppData/Local/Temp/remotion-webpack-bundle-4tnpX9 C1S out/h2s_renew_c1.mp4 --props=h2s_renew.json --pixel-format=yuv420p --concurrency=1 --timeout=120000 --offthreadvideo-cache-size-in-bytes=1073741824 > $D/render_1102h.log 2>&1 || { echo RENDER_FAIL; tail -20 $D/render_1102h.log; exit 1; }
PYTHONIOENCODING=utf-8 py -3.12 $R/work/video/deess.py out/h2s_renew_c1.mp4 out/h2s_renew_c1_ds.mp4 --chirp-short > $D/deess_1102h.log 2>&1; tail -3 $D/deess_1102h.log
echo "H2S_DONE $(date +%H:%M)"
