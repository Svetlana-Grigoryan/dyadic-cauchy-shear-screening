#!/usr/bin/env python3
"""Exact verifier for the representative gamma=04 instance."""
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

def inv(a):
    if not a: raise ZeroDivisionError
    return pw(a,254)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
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
def maddI(A):
    B=[r[:] for r in A]
    for i in range(len(B)):B[i][i]^=1
    return B
def rank(A):
    A=[r[:] for r in A]; n=len(A); m=len(A[0]); rr=0
    for c in range(m):
        p=next((i for i in range(rr,n) if A[i][c]),None)
        if p is None:continue
        A[rr],A[p]=A[p],A[rr]
        z=inv(A[rr][c]); A[rr]=[mul(z,x) for x in A[rr]]
        for i in range(n):
            if i!=rr and A[i][c]:
                z=A[i][c]; A[i]=[x^mul(z,y) for x,y in zip(A[i],A[rr])]
        rr+=1
    return rr
def scalar(A):
    s=A[0][0]
    return s if all(A[i][j]==(s if i==j else 0) for i in range(len(A)) for j in range(len(A))) else None

def det(A):
    A=[r[:] for r in A]; d=1
    for c in range(len(A)):
        p=next((i for i in range(c,len(A)) if A[i][c]),None)
        if p is None:return 0
        A[c],A[p]=A[p],A[c]
        d=mul(d,A[c][c]); z=inv(A[c][c]); A[c]=[mul(z,x) for x in A[c]]
        for i in range(c+1,len(A)):
            if A[i][c]:
                z=A[i][c];A[i]=[x^mul(z,y) for x,y in zip(A[i],A[c])]
    return d

def aes_sbox(x):
    y=0 if x==0 else inv(x)
    def rot(v,n): return ((v<<n)|(v>>(8-n)))&255
    return y ^ rot(y,1)^rot(y,2)^rot(y,3)^rot(y,4)^0x63

def parity(x):return x.bit_count()&1
h=[inv(4^a) for a in range(4)]
assert h==[0xCB,0x52,0x7B,0xD1]
M=[[h[i^j] for j in range(4)] for i in range(4)]
M2=mm(M,M); assert scalar(M2)==0x72 and mul(0x72,0x97)==1
# 69 nonzero square minors
from itertools import combinations
minor_count=0
for k in range(1,5):
    for rs in combinations(range(4),k):
        for cs in combinations(range(4),k):
            assert det([[M[i][j] for j in cs] for i in rs])!=0;minor_count+=1
assert minor_count==69
L=[[0]*16 for _ in range(16)]
for i in range(4):
    for j in range(4):
        out=4*i+(j^i)
        for k in range(4):L[out][4*k+j]=M[i][k]
assert scalar(mp(L,4))==0xD8
assert all(scalar(mp(L,e)) is None for e in (1,2,3))
c=0
for x in h:c^=x
assert c==0x33 and pw(c,4)==0xD8
U=[[mul(inv(c),x) for x in row] for row in L]
N=maddI(U)
nullities=[];P=eye(16)
for k in range(1,5):
    P=mm(P,N);nullities.append(16-rank(P))
assert nullities==[4,8,12,16]
fixed={}
for e in (51,102,204): fixed[str(e)]=8*(16-rank(maddI(mp(L,e))))
assert fixed=={"51":32,"102":64,"204":128}
S=[aes_sbox(x) for x in range(256)]
ddt_diag=[];lat_diag=[];ddt_values={};lat_abs={}
for a in range(1,256):
    d=sum(1 for x in range(256) if (S[x]^S[x^a])==a)
    if d:ddt_diag.append(a);ddt_values[a]=d
    w=sum(1 if parity(a&x)==parity(a&S[x]) else -1 for x in range(256))
    if w:lat_diag.append(a);lat_abs[a]=abs(w)
assert len(ddt_diag)==116 and set(ddt_values.values())=={2,4}
assert len(lat_diag)==234 and set(lat_abs.values())==set(range(4,33,4))
H=[];x=1
for _ in range(51):H.append(x);x=mul(x,0xD8)
reps=[];unused=set(range(1,256))
while unused:
    r=min(unused);C={mul(r,h0) for h0 in H};reps.append(r);unused-=C
assert len(reps)==5
dints=[sum(x in ddt_diag for x in {mul(r,h0) for h0 in H}) for r in reps]
assert sorted(dints)==sorted([20,25,22,22,27])

# Standard AES LAT masks use the binary dot product in the polynomial basis.
# If C_alpha is multiplication by alpha, the backward mask map is C_alpha^{-T}.
def mat2_inv(A):
    n=len(A); aug=[A[i][:]+[int(i==j) for j in range(n)] for i in range(n)]
    for c0 in range(n):
        p=next(i for i in range(c0,n) if aug[i][c0])
        aug[c0],aug[p]=aug[p],aug[c0]
        for i in range(n):
            if i!=c0 and aug[i][c0]:
                aug[i]=[u^v for u,v in zip(aug[i],aug[c0])]
    return [row[n:] for row in aug]
def transpose(A): return [list(row) for row in zip(*A)]
def apply2(A,x):
    y=0
    for i,row in enumerate(A):
        bit=0
        for j,aij in enumerate(row): bit ^= aij & ((x>>j)&1)
        y |= bit<<i
    return y
def mult_matrix(alpha):
    return [[(mul(alpha,1<<j)>>i)&1 for j in range(8)] for i in range(8)]
C_D8=mult_matrix(0xD8)
A_adj=transpose(mat2_inv(C_D8))
assert A_adj != mult_matrix(inv(0xD8))
adj_orbits=[];unused=set(range(1,256))
while unused:
    r=min(unused); orb=[]; z=r
    while z not in orb:
        orb.append(z); z=apply2(A_adj,z)
    assert z==r and len(orb)==51
    adj_orbits.append(orb); unused-=set(orb)
assert len(adj_orbits)==5
lat_adj_intersections=[sum(x in lat_diag for x in orb) for orb in adj_orbits]
assert lat_adj_intersections==[46,47,49,45,47]
assert sorted(lat_adj_intersections)==[45,46,47,47,49]
adjoint_record={
    "basis":"AES polynomial basis, LSB-first coefficients",
    "dot_product":"standard binary dot product",
    "scalar":"D8",
    "backward_four_step_matrix":["".join(str(b) for b in row) for row in A_adj],
    "orbit_representatives":[f"{orb[0]:02X}" for orb in adj_orbits],
    "orbit_lengths":[len(orb) for orb in adj_orbits],
    "lat_diagonal_intersections":lat_adj_intersections,
    "orbits":[[f"{x:02X}" for x in orb] for orb in adj_orbits]
}
with open("lat_adjoint_orbits.json","w") as f:json.dump(adjoint_record,f,indent=2,sort_keys=True)
result={"kernel":[f"{x:02X}" for x in h],"minor_count":69,"M_square_scalar":"72",
        "inverse_scalar":"97","L4_scalar":"D8","projective_order":4,
        "normalized_nullities":nullities,"binary_fixed_dimensions":fixed,
        "ddt_diagonal_support":116,"lat_diagonal_support":234,
        "ddt_coset_intersections":dints,
        "lat_adjoint_orbit_representatives":adjoint_record["orbit_representatives"],
        "lat_adjoint_orbit_intersections":lat_adj_intersections}
with open("full_certificate_results.json","w") as f:json.dump(result,f,indent=2,sort_keys=True)
print(json.dumps(result,sort_keys=True))
