from __future__ import annotations
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

R=4
# x[r,i,j], r=0..3; y[r,i,j], r=0..2; z[r,j], r=0..2
idx={}; n=0
for r in range(R):
  for i in range(4):
    for j in range(4): idx[('x',r,i,j)]=n; n+=1
for r in range(R-1):
  for i in range(4):
    for j in range(4): idx[('y',r,i,j)]=n; n+=1
for r in range(R-1):
  for j in range(4): idx[('z',r,j)]=n; n+=1
rows=[]; lo=[]; hi=[]
def add(coefs,l=-np.inf,u=np.inf): rows.append(coefs); lo.append(l); hi.append(u)
# x0 nonzero
add({idx[('x',0,i,j)]:1 for i in range(4) for j in range(4)},1,np.inf)
for r in range(R-1):
  for j in range(4):
    z=idx[('z',r,j)]
    # x and y bits imply z; z implies nonzero x and y
    for i in range(4):
      add({idx[('x',r,i,j)]:1,z:-1},-np.inf,0)
      add({idx[('y',r,i,j)]:1,z:-1},-np.inf,0)
    add({**{idx[('x',r,i,j)]:1 for i in range(4)},z:-1},0,np.inf)
    add({**{idx[('y',r,i,j)]:1 for i in range(4)},z:-1},0,np.inf)
    c={z:-5}
    for i in range(4): c[idx[('x',r,i,j)]]=1; c[idx[('y',r,i,j)]]=1
    add(c,0,np.inf)
  # shear: destination (i, j xor i)
  for i in range(4):
    for j in range(4):
      add({idx[('x',r+1,i,j^i)]:1,idx[('y',r,i,j)]:-1},0,0)
A=lil_matrix((len(rows),n),dtype=float)
for rr,c in enumerate(rows):
  for k,v in c.items(): A[rr,k]=v
c=np.zeros(n)
for r in range(R):
  for i in range(4):
    for j in range(4): c[idx[('x',r,i,j)]]=1
res=milp(c, integrality=np.ones(n), bounds=Bounds(np.zeros(n),np.ones(n)), constraints=LinearConstraint(A.tocsr(),np.array(lo),np.array(hi)), options={'disp':True})
assert res.success, res.message
print('optimum',round(res.fun))
for r in range(R):
  mask=0
  for i in range(4):
    for j in range(4):
      if res.x[idx[('x',r,i,j)]]>.5: mask |= 1<<(4*i+j)
  print(f'x{r}=0x{mask:04X} wt={mask.bit_count()}')
