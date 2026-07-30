X=[0x2800,0x5A5A,0xEEEE,0x5004]
Y=[0xAAAA,0x7BDE,0xA004]
def bit(m,i,j): return (m>>(4*i+j))&1
def colwt(m,j): return sum(bit(m,i,j) for i in range(4))
for r in range(3):
 for i in range(4):
  for j in range(4): assert bit(X[r+1],i,j^i)==bit(Y[r],i,j)
 for j in range(4):
  a,b=colwt(X[r],j),colwt(Y[r],j)
  assert (a==0 and b==0) or (a>0 and b>0 and a+b>=5)
print('witness_weight',sum(m.bit_count() for m in X))
