# Independent row-oriented MILP formulation of the same four-layer relaxation.
from __future__ import annotations
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
R=4
# flattened arrays X[64], Y[48], A[12]
oX=0; oY=64; oA=112; N=124
def X(r,i,j): return oX+16*r+4*i+j
def Y(r,i,j): return oY+16*r+4*i+j
def A(r,j): return oA+4*r+j
I=[];J=[];V=[];lb=[];ub=[]
def row(entries,l=-np.inf,u=np.inf):
 q=len(lb); lb.append(l);ub.append(u)
 for k,v in entries: I.append(q);J.append(k);V.append(v)
row([(X(0,i,j),1) for i in range(4) for j in range(4)],1,np.inf)
for r in range(3):
 for j in range(4):
  a=A(r,j)
  for i in range(4):
   row([(X(r,i,j),1),(a,-1)],-np.inf,0)
   row([(Y(r,i,j),1),(a,-1)],-np.inf,0)
  row([(X(r,i,j),1) for i in range(4)]+[(a,-1)],0,np.inf)
  row([(Y(r,i,j),1) for i in range(4)]+[(a,-1)],0,np.inf)
  row([(X(r,i,j),1) for i in range(4)]+[(Y(r,i,j),1) for i in range(4)]+[(a,-5)],0,np.inf)
 for i in range(4):
  for j in range(4): row([(X(r+1,i,j^i),1),(Y(r,i,j),-1)],0,0)
M=coo_matrix((V,(I,J)),shape=(len(lb),N)).tocsr()
obj=np.zeros(N); obj[:64]=1
r=milp(obj,integrality=np.ones(N),bounds=Bounds(0,1),constraints=LinearConstraint(M,np.array(lb),np.array(ub)))
assert r.success
assert round(r.fun)==25
print('independent_optimum',round(r.fun))
