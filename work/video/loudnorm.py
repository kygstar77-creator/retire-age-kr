# 음량 맞추기 + 관문 — 기준 리뉴얼 B-42(10/19, work/research/criteria/B-screen-1019.md)
#   통합 음량 −16~−18 LUFS, 참 피크 −1 dBTP 이하. 근거: 경쟁 쇼츠 25편 통합 중앙 −17.9(−21.3~−16.1)·롱폼 14편 −17.0(−18.0~−16.2) ②,
#   참 피크 −1은 EBU·애플 팟캐스트 ①. 유튜브 공식 −14 문서는 없다(2차 실측만). 우리 C-2 −19.8(작음).
#   py -3.12 work/video/loudnorm.py <mp4>            # 재기만(종료코드 0 = 기준 안, 1 = 밖)
#   py -3.12 work/video/loudnorm.py <mp4> --fix      # 두 번 재는 loudnorm(목표 −17 LUFS·참 피크 −1.5)으로 소리만 다시 만들어 같은 이름에 덮음(화면은 복사)
# 렌더(lfrender)·쉿소리 다듬기(deess) 다음, 올리기 전 마지막에 돌린다. 관문: ytlong gate(공개 2026-10-23 이후 편)·ytupload.upload(쇼츠, 2026-10-23부터).
import os, sys, re, json, subprocess, tempfile, shutil
sys.stdout.reconfigure(encoding='utf-8')
I_LO, I_HI, TP_MAX = -18.0, -16.0, -1.0
TARGET_I, TARGET_TP, TARGET_LRA = -17.0, -1.5, 11.0
LOUD_FROM = '2026-10-23'


def ff():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def measure(mp4):
    """{'I': 통합 LUFS, 'TP': 참 피크 dBTP} — ffmpeg ebur128(peak=true). 소리 없으면 None."""
    p = subprocess.run([ff(), '-hide_banner', '-nostats', '-i', mp4, '-map', '0:a:0?', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='ignore')
    t = p.stderr.split('Summary:')[-1]
    i = re.search(r'I:\s*(-?[\d.]+)\s*LUFS', t); tp = re.search(r'Peak:\s*(-?[\d.]+)\s*dBFS', t)
    if not i: return None
    return {'I': float(i.group(1)), 'TP': float(tp.group(1)) if tp else None}


def ok(m):
    return bool(m) and I_LO <= m['I'] <= I_HI and (m['TP'] is None or m['TP'] <= TP_MAX)


def gate(mp4):
    """(통과, 한 줄)."""
    m = measure(mp4)
    if not m: return False, f'음량 못 잼(소리 없음?) {os.path.basename(mp4)}'
    msg = f"음량 통합 {m['I']:.1f} LUFS(기준 {I_LO:g}~{I_HI:g})·참 피크 {m['TP']} dBTP(기준 ≤{TP_MAX:g}) — B-42"
    return ok(m), msg + ('' if ok(m) else f' → py -3.12 work/video/loudnorm.py {mp4} --fix')


def fix(mp4):
    """두 번 재는 loudnorm: 첫 번째로 잰 값을 넣어 선형으로 맞춘다. 화면은 그대로 복사, 소리만 AAC 192k로 다시."""
    f = f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}'
    p = subprocess.run([ff(), '-hide_banner', '-nostats', '-i', mp4, '-map', '0:a:0', '-af', f + ':print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='ignore')
    j = json.loads(p.stderr[p.stderr.rindex('{'):p.stderr.rindex('}') + 1])
    f2 = (f + f":measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}"
          f":offset={j['target_offset']}:linear=true")
    tmp = os.path.join(os.path.dirname(os.path.abspath(mp4)), '.ln_' + os.path.basename(mp4))
    r = subprocess.run([ff(), '-hide_banner', '-y', '-i', mp4, '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'copy', '-af', f2, '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', tmp],
                       capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if r.returncode or not os.path.exists(tmp): sys.exit('loudnorm 실패: ' + r.stderr[-300:])
    shutil.move(tmp, mp4)
    return measure(mp4)


if __name__ == '__main__':
    path = sys.argv[1]
    if '--fix' in sys.argv:
        print('전', measure(path)); print('뒤', fix(path))
    g, msg = gate(path); print(('통과 · ' if g else '밖 · ') + msg); sys.exit(0 if g else 1)
