def isin(code):
    b='KR7'+code+'00'
    s=''.join(str(int(c,36)) for c in b)
    tot=0
    for i,ch in enumerate(reversed(s)):
        d=int(ch)
        if i%2==0:
            d*=2
            if d>9: d-=9
        tot+=d
    return b+str((10-tot%10)%10)
if __name__=='__main__':
    import sys; print(isin(sys.argv[1]))
