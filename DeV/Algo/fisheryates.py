
import random

def shuffle(ary):
  a=len(ary)
  b=a-1
  for d in range(b,0,-1):
    e=random.randint(0,d)
    if e == d:
        continue
    ary[d],ary[e]=ary[e],ary[d]
  return ary

a = [10,20,30,40,50]
shuffle(a)
print(a)
shuffle(a)
print(a)
shuffle(a)
print(a)
shuffle(a)
print(a)
shuffle(a)
print(a)