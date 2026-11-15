import sys
def isin(code):
    body = 'KR7' + code + '00'
    digits = ''.join(str(int(c, 36)) for c in body)
    s = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2 == 0: n *= 2
        s += n // 10 + n % 10
    return body + str((10 - s % 10) % 10)
if __name__ == '__main__':
    for c in sys.argv[1:]: print(c, isin(c))
