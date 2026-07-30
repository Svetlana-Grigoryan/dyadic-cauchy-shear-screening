#!/usr/bin/env python3
"""Exact scan of all dyadic Cauchy parameters over the AES field."""
from collections import Counter
import csv, json
MOD = 0x11B
V = range(4)

def gf_mul(a,b):
    r=0
    for _ in range(8):
        if b&1: r ^= a
        b >>= 1; a <<= 1
        if a & 0x100: a ^= MOD
    return r & 0xFF

def gf_pow(a,n):
    r=1
    while n:
        if n&1: r=gf_mul(r,a)
        a=gf_mul(a,a); n >>= 1
    return r

def gf_inv(a):
    if not a: raise ZeroDivisionError
    return gf_pow(a,254)

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def matmul(A,B):
    C=[[0]*len(B[0]) for _ in A]
    for i,row in enumerate(A):
        for k,a in enumerate(row):
            if a:
                for j,b in enumerate(B[k]):
                    if b: C[i][j] ^= gf_mul(a,b)
    return C

def scalar_of(A):
    s=A[0][0]
    return s if all(A[i][j] == (s if i==j else 0) for i in range(len(A)) for j in range(len(A))) else None

def operator(gamma):
    h=[gf_inv(gamma ^ a) for a in V]
    M=[[h[i^k] for k in V] for i in V]
    L=[[0]*16 for _ in range(16)]
    for i in V:
        for j in V:
            out=4*i+(j^i)
            for k in V: L[out][4*k+j]=M[i][k]
    return h,L

def scalar_order(a):
    for d in (1,3,5,15,17,51,85,255):
        if gf_pow(a,d)==1: return d
    raise AssertionError

def projective_order(L):
    P=eye(16)
    for e in range(1,5):
        P=matmul(P,L)
        s=scalar_of(P)
        if s is not None: return e,s
    raise AssertionError

rows=[]
for gamma in range(4,256):
    h,L=operator(gamma)
    s=0
    for x in h: s ^= x
    e,beta=projective_order(L)
    assert e==4 and beta==gf_pow(s,4)
    rows.append({"gamma":f"{gamma:02X}","coset_representative":f"{gamma & 0xFC:02X}",
                 "kernel_sum":f"{s:02X}","scalar":f"{beta:02X}",
                 "scalar_order":scalar_order(beta),"projective_order":e})
# One representative per coset gamma+V.
cosets = [r for r in rows if int(r["gamma"], 16) % 4 == 0]

dist_cosets = Counter(r["scalar_order"] for r in cosets)
dist_parameters = Counter(r["scalar_order"] for r in rows)

expected_cosets = {
    5: 2,
    15: 1,
    17: 3,
    51: 12,
    85: 12,
    255: 33,
}

expected_parameters = {
    5: 8,
    15: 4,
    17: 12,
    51: 48,
    85: 48,
    255: 132,
}

assert dict(sorted(dist_cosets.items())) == expected_cosets
assert dict(sorted(dist_parameters.items())) == expected_parameters

with open("gamma_family.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

summary = {
    "admissible_parameters": 252,
    "distinct_cosets": 63,
    "projective_order": 4,
    "scalar_order_distribution_cosets": {
        str(k): v for k, v in sorted(dist_cosets.items())
    },
    "scalar_order_distribution_parameters": {
        str(k): v for k, v in sorted(dist_parameters.items())
    },
}
with open("family_summary.json","w") as f: json.dump(summary,f,indent=2,sort_keys=True)
print(json.dumps(summary,sort_keys=True))
