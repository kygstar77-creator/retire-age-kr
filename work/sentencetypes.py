"""문장 유형 조사(2026-10-03)용 문장 나누기·뽑기.

경쟁 롱폼 받아쓰기(breakdown/*_transcript.txt)와 우리 대본(ep/<편>/voice.json의 say)을
문장으로 나누고, 고정 시드로 100문장씩 뽑는다. 결과는
work/research/cloud/sentence-types-1003/samples.tsv 와 blind.tsv(출처 숨긴 섞은 목록).

뽑는 법
- 경쟁: 영상마다 가중치 w = sqrt(조회수). 영상 v의 문장 하나가 뽑힐 몫 = w_v / n_v
  (n_v = 그 영상 문장 수) → 영상 전체 몫이 sqrt(조회수)에 비례한다.
  Efraimidis-Spirakis 방식(key = u ** (1/p))으로 비복원 가중 추출.
- 우리: 5편 문장 전체에서 균등 비복원 추출.
- 글자 수(공백·문장부호 제외) 5자 미만 문장은 양쪽 모두 뺀다("네." 같은 것).

실행: python3 work/sentencetypes.py
"""
from __future__ import annotations

import csv
import json
import math
import os
import random
import re
import sys

SEED = 1003
N_EACH = 100
MIN_CHARS = 5

HERE = os.path.dirname(os.path.abspath(__file__))
LF = os.path.join(HERE, "research", "longform")
OUT = os.path.join(HERE, "research", "cloud", "sentence-types-1003")
EPS = ["A-1", "E-1", "D-1", "E-2", "N-1"]

# 받아쓰기 영상 조회수(저장소 JSON에서 찾은 값, 출처는 보고서 표에 적음)
VIEWS = {
    "-Yh53SjCAiw": 117546, "5e8rHSGs5sw": 155574, "HuRs1geEFmo": 7326,
    "IOBgv9nZCTE": 70372, "QtciAE40DlU": 29015, "W42NW4wF5LU": 108741,
    "X3D8NVks04w": 113455, "cBFFyqiKFRs": 61560, "gJTto7SP8w0": 110273,
    "jSP16zTrEHY": 403904, "lSmbW1Par1M": 8802, "rmajvVmxGxM": 63717,
    "tVaz2qoAySM": 117264, "vJ6VxHMQsyA": 12710, "vr5qMqpwPZM": 526034,
    "wM09H0bKxXY": 4119, "zjie3J7lIRw": 71012,
}

TS_RE = re.compile(r"^\s*\**\s*\[(\d{1,2}:)?\d{1,2}:\d{2}\]\s*\**\s*")
NOISE_RE = re.compile(r"\((?:불명확|웃음|음악|박수|효과음|BGM)[^)]*\)|\[(?:음악|웃음|박수)[^\]]*\]")


def count_chars(s: str) -> int:
    return len(re.sub(r"[\s\W_]", "", s))


def split_sentences(text: str) -> list[str]:
    """한 덩어리 글을 문장 목록으로. 문장부호(. ? ! …) 뒤 공백에서 자른다."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.?!…])(?<!\d\.(?=\d))\s+", text)
    return [p.strip() for p in parts if p.strip()]


def transcript_lines(path: str) -> list[tuple[int, str]]:
    """받아쓰기 파일에서 [mm:ss]로 시작하는 줄만 (줄번호, 본문)으로."""
    out = []
    with open(path, encoding="utf-8") as f:
        for no, raw in enumerate(f, 1):
            if not TS_RE.match(raw):
                continue
            body = TS_RE.sub("", raw).strip()
            body = re.sub(r"^\**[가-힣A-Za-z0-9 ]{1,10}\**\s*:\s*", "", body)  # 화자 이름표
            body = NOISE_RE.sub("", body).strip()
            if body:
                out.append((no, body))
    return out


def sentences_from_lines(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """줄을 이어 붙여 문장으로 나누고, 문장이 시작한 줄 번호를 붙인다.
    줄 끝에 문장부호가 없으면 다음 줄과 이어진 한 문장으로 본다."""
    joined = " ".join(b for _, b in lines)
    if lines and len(re.findall(r"[.?!…](?:\s|$)", joined)) < len(lines) / 3:
        # 문장부호가 거의 없는 받아쓰기(gJTto7SP8w0 등): 시간표 한 줄을 한 문장으로 본다
        return [(no, re.sub(r"\s+", " ", b).strip()) for no, b in lines]
    text, starts = "", []  # starts: (글자 위치, 줄번호)
    for no, body in lines:
        if text:
            text += " "
        starts.append((len(text), no))
        text += re.sub(r"\s+", " ", body).strip()
    out, pos = [], 0
    for s in split_sentences(text):
        k = text.find(s, pos)
        pos = k + len(s)
        no = [n for off, n in starts if off <= k][-1]
        out.append((no, s))
    return out


def competitor_sentences() -> list[dict]:
    rows = []
    bd = os.path.join(LF, "breakdown")
    for vid in sorted(VIEWS):
        path = os.path.join(bd, f"{vid}_transcript.txt")
        if not os.path.exists(path):
            continue
        for no, s in sentences_from_lines(transcript_lines(path)):
            if count_chars(s) >= MIN_CHARS:
                rows.append({"side": "경쟁", "src": f"breakdown/{vid}_transcript.txt",
                             "line": no, "vid": vid, "text": s})
    return rows


def our_sentences() -> list[dict]:
    rows = []
    for ep in EPS:
        path = os.path.join(LF, "ep", ep, "voice.json")
        with open(path, encoding="utf-8") as f:
            raw_lines = f.read().split("\n")
        # say 줄 번호 찾기(파일 안 순서대로)
        say_lines = [i + 1 for i, l in enumerate(raw_lines) if re.match(r'\s*"say"\s*:', l)]
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        says = [ln["say"] for sec in d["sections"] for ln in sec.get("lines", []) if ln.get("say")]
        for k, say in enumerate(says):
            no = say_lines[k] if k < len(say_lines) else 0
            for s in split_sentences(say):
                if count_chars(s) >= MIN_CHARS:
                    rows.append({"side": "우리", "src": f"ep/{ep}/voice.json", "line": no,
                                 "vid": ep, "text": s})
    return rows


def weighted_sample(rows: list[dict], weights: list[float], k: int, rng: random.Random) -> list[dict]:
    keyed = []
    for r, w in zip(rows, weights):
        u = rng.random()
        keyed.append((u ** (1.0 / w) if w > 0 else 0.0, r))
    keyed.sort(key=lambda t: -t[0])
    return [r for _, r in keyed[:k]]


def sample(seed: int = SEED, n: int = N_EACH) -> list[dict]:
    rng = random.Random(seed)
    comp = competitor_sentences()
    ours = our_sentences()
    n_by_vid: dict[str, int] = {}
    for r in comp:
        n_by_vid[r["vid"]] = n_by_vid.get(r["vid"], 0) + 1
    w = [math.sqrt(VIEWS[r["vid"]]) / n_by_vid[r["vid"]] for r in comp]
    c = weighted_sample(comp, w, n, rng)
    o = rng.sample(ours, n)
    picked = c + o
    ids = list(range(1, len(picked) + 1))
    rng.shuffle(ids)  # 섞은 번호: 코딩할 때 출처를 숨긴다
    for r, i in zip(picked, ids):
        r["id"] = f"S{i:03d}"
    return picked


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    picked = sample()
    picked.sort(key=lambda r: r["id"])
    with open(os.path.join(OUT, "samples.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["id", "side", "src", "line", "views", "text"])
        for r in picked:
            w.writerow([r["id"], r["side"], r["src"], r["line"],
                        VIEWS.get(r["vid"], ""), r["text"]])
    with open(os.path.join(OUT, "blind.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["id", "text"])
        for r in picked:
            w.writerow([r["id"], r["text"]])
    comp = competitor_sentences()
    ours = our_sentences()
    print(f"seed={SEED} 경쟁 문장 {len(comp)} / 우리 문장 {len(ours)} → 각 {N_EACH} 뽑음", file=sys.stderr)


# ---------- 코딩 뒤 집계 ----------
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
DISCLAIM_RE = re.compile(  # 면책·한계 키워드(걸린 문장은 손으로 다시 확인할 것)
    r"말하지 않|짐작하지 않|뜻(은|이) 아닙|적혀 있지 않|나오지 않아|들어 있지 않|사람마다 다르|구간은 아니|"
    r"권유|추천(이|하는 게|하는 건) 아|확인하는 게 정확|투자 판단|책임|단정|보장(하지|할 수|은 없)|"
    r"참고(만|용)|개인(마다|차)|상황(마다|에 따라) 다")


def count_numbers(s: str) -> int:
    """숫자(아라비아 숫자 덩어리) 개수. 1,679 / 3.0 은 하나로 센다. 한글 수사(세 배)는 세지 않는다."""
    return len(NUM_RE.findall(s))


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """2x2 표 [[a,b],[c,d]] 피셔 정확 검정 양측 p."""
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2

    def pmf(x: int) -> float:
        return math.comb(r1, x) * math.comb(r2, c1 - x) / math.comb(n, c1)

    p0 = pmf(a)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    return min(1.0, sum(pmf(x) for x in range(lo, hi + 1) if pmf(x) <= p0 * (1 + 1e-9)))


def read_tsv(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def merge_codes() -> list[dict]:
    samples = {r["id"]: r for r in read_tsv(os.path.join(OUT, "samples.tsv"))}
    rows = []
    for c in read_tsv(os.path.join(OUT, "blind_codes.tsv")):
        s = samples[c["id"]]
        rows.append({"id": c["id"], "side": s["side"], "src": s["src"], "line": s["line"],
                     "views": s["views"], "text": s["text"], "note": c["note"], "type": c["type"],
                     "c1": int(c["c1_new_fact"]), "c2": int(c["c2_why"]), "c3": int(c["c3_check_do"]),
                     "nums": count_numbers(s["text"])})
    with open(os.path.join(OUT, "codes.tsv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["id", "side", "type", "note", "text", "src", "line", "views",
                    "c1_new_fact", "c2_why", "c3_check_do", "n_numbers"])
        for r in rows:
            w.writerow([r["id"], r["side"], r["type"], r["note"], r["text"], r["src"], r["line"],
                        r["views"], r["c1"], r["c2"], r["c3"], r["nums"]])
    return rows


def compare(rows: list[dict], pred) -> dict:
    comp = [r for r in rows if r["side"] == "경쟁"]
    ours = [r for r in rows if r["side"] == "우리"]
    a = sum(1 for r in comp if pred(r)); c = sum(1 for r in ours if pred(r))
    return {"comp": a, "n_comp": len(comp), "ours": c, "n_ours": len(ours),
            "ci_comp": wilson(a, len(comp)), "ci_ours": wilson(c, len(ours)),
            "p": fisher_two_sided(a, len(comp) - a, c, len(ours) - c)}


def full_corpus_rate(pattern: re.Pattern) -> dict:
    """뽑기 전 전체 문장에서 패턴이 든 문장 비율(편·영상별)."""
    out = {}
    for r in competitor_sentences() + our_sentences():
        k = (r["side"], r["vid"])
        t = out.setdefault(k, [0, 0])
        t[1] += 1
        if pattern.search(r["text"]):
            t[0] += 1
    return out


def analyze() -> None:
    rows = merge_codes()
    types = sorted({r["type"] for r in rows})
    print("type\t경쟁\t경쟁95%\t우리\t우리95%\tFisher p")
    for t in sorted(types, key=lambda t: -sum(r["type"] == t for r in rows)):
        x = compare(rows, lambda r, t=t: r["type"] == t)
        print(f"{t}\t{x['comp']}\t{x['ci_comp'][0]:.0%}-{x['ci_comp'][1]:.0%}\t{x['ours']}\t"
              f"{x['ci_ours'][0]:.0%}-{x['ci_ours'][1]:.0%}\t{x['p']:.4f}")
    checks = {
        "c1=c2=c3=0(얻는 것 없음)": lambda r: r["c1"] + r["c2"] + r["c3"] == 0,
        "숫자 2개 이상": lambda r: r["nums"] >= 2,
        "숫자 3개 이상": lambda r: r["nums"] >= 3,
        "숫자 1개 이상": lambda r: r["nums"] >= 1,
        "c1 새 사실": lambda r: r["c1"] == 1,
        "c2 왜 중요": lambda r: r["c2"] == 1,
        "c3 할 일": lambda r: r["c3"] == 1,
        "c1&c2&c3 모두": lambda r: r["c1"] and r["c2"] and r["c3"],
        "c1&c2": lambda r: r["c1"] and r["c2"],
    }
    print()
    for k, f in checks.items():
        x = compare(rows, f)
        print(f"{k}\t{x['comp']}/{x['n_comp']}\t{x['ci_comp'][0]:.0%}-{x['ci_comp'][1]:.0%}\t"
              f"{x['ours']}/{x['n_ours']}\t{x['ci_ours'][0]:.0%}-{x['ci_ours'][1]:.0%}\tp={x['p']:.4f}")
    print()
    for (side, vid), (k, n) in sorted(full_corpus_rate(DISCLAIM_RE).items()):
        print(f"면책·한계 키워드\t{side}\t{vid}\t{k}/{n}\t{k/n:.1%}")
    for r in competitor_sentences() + our_sentences():
        if DISCLAIM_RE.search(r["text"]):
            print(f"  걸린 문장\t{r['side']}\t{r['vid']}\t{r['text'][:80]}")


if __name__ == "__main__" and "--analyze" in sys.argv:
    analyze()
    sys.exit(0)


if __name__ == "__main__":
    main()
