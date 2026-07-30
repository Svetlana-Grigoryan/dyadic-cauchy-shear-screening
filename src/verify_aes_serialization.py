#!/usr/bin/env python3
"""Verify the isolated AES linear map in one row-major coordinate system."""
import json
MOD=0x11B

def mul(a,b):
    r=0
    for _ in range(8):
        if b&1:r^=a
        b>>=1;a<<=1
        if a&0x100:a^=MOD
    return r&255

def pw(a,n):
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n>>=1
    return r

def inv(a): return pw(a,254)
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B):
    C=[[0]*len(B[0]) for _ in A]
    for i,row in enumerate(A):
        for k,a in enumerate(row):
            if a:
                for j,b in enumerate(B[k]):
                    if b:C[i][j]^=mul(a,b)
    return C

def mp(A,n):
    R=eye(len(A))
    while n:
        if n&1:R=mm(R,A)
        A=mm(A,A);n>>=1
    return R

def rank(A):
    A=[r[:] for r in A]; rr=0; n=len(A); m=len(A[0])
    for c in range(m):
        p=next((i for i in range(rr,n) if A[i][c]),None)
        if p is None: continue
        A[rr],A[p]=A[p],A[rr]
        z=inv(A[rr][c]);A[rr]=[mul(z,x) for x in A[rr]]
        for i in range(n):
            if i!=rr and A[i][c]:
                z=A[i][c];A[i]=[x^mul(z,y) for x,y in zip(A[i],A[rr])]
        rr+=1
    return rr

def addI(A):
    B=[r[:] for r in A]
    for i in range(len(B)):B[i][i]^=1
    return B

def mix_column(c):
    a0,a1,a2,a3=c
    return [mul(2,a0)^mul(3,a1)^a2^a3,
            a0^mul(2,a1)^mul(3,a2)^a3,
            a0^a1^mul(2,a2)^mul(3,a3),
            mul(3,a0)^a1^a2^mul(2,a3)]

def aes_linear_row_major(v):
    s=[[v[4*i+j] for j in range(4)] for i in range(4)]
    sr=[[s[i][(j+i)&3] for j in range(4)] for i in range(4)]
    out=[[0]*4 for _ in range(4)]
    for j in range(4):
        c=mix_column([sr[i][j] for i in range(4)])
        for i in range(4):out[i][j]=c[i]
    return [out[i][j] for i in range(4) for j in range(4)]

A=[[0]*16 for _ in range(16)]
for j in range(16):
    e=[0]*16;e[j]=1
    y=aes_linear_row_major(e)
    for i in range(16):A[i][j]=y[i]
assert mp(A,8)==eye(16)
assert all(mp(A,e)!=eye(16) for e in (1,2,4))
null_f256={e:16-rank(addI(mp(A,e))) for e in (1,2,4,8)}
assert null_f256=={1:2,2:4,4:8,8:16}
result={
  "coordinates":"row-major input and row-major output",
  "test_input":[f"{x:02X}" for x in range(16)],
  "test_output":[f"{x:02X}" for x in aes_linear_row_major(list(range(16)))],
  "order":8,
  "fixed_dimensions_F256":{str(k):v for k,v in null_f256.items()},
  "fixed_dimensions_F2":{str(k):8*v for k,v in null_f256.items()}
}
with open('aes_serialization_results.json','w') as f:json.dump(result,f,indent=2,sort_keys=True)
print(json.dumps(result,sort_keys=True))
