import math
def _rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0]*len(x); i = 0
    while i < len(x):
        j = i
        while j+1 < len(x) and x[o[j+1]] == x[o[i]]: j += 1
        for k in range(i, j+1): r[o[k]] = (i+j)/2 + 1
        i = j+1
    return r
def spearman(a, b):
    ra, rb = _rank(a), _rank(b); n = len(a); ma, mb = sum(ra)/n, sum(rb)/n
    num = sum((x-ma)*(y-mb) for x, y in zip(ra, rb)); den = math.sqrt(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))
    return num/den if den else float('nan')
def fisher(t):
    (a, b), (c, d) = t; n = a+b+c+d; r1 = a+b; c1 = a+c
    def p(x): return math.comb(r1, x)*math.comb(n-r1, c1-x)/math.comb(n, c1)
    p0 = p(a); lo = max(0, c1-(n-r1)); hi = min(r1, c1)
    return min(1.0, sum(p(x) for x in range(lo, hi+1) if p(x) <= p0*(1+1e-9)))
