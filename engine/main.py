import sys
import time
B=range
E=print
H=chr
I=ord
J=True
K=copy
L=False
M=min
N=max
O=abs
P=int
class Q:
 def __init__(self):
  self.reset()
 def reset(self):
  self.b=[[ch for ch in row]for row in['rnbqkbnr',8*'p']+4*[8*'.']+[8*'P','RNBQKBNR']];self.t='w'
  self.c={'K':J,'Q':J,'k':J,'q':J};self.e=None;self.h=0;self.f=1
 def S(self,x,y):return self.b[y][x]
 def U(self,m):
  x1,y1=I(m[0])-97,8-P(m[1]);x2,y2=I(m[2])-97,8-P(m[3])
  p=self.b[y1][x1];F=J
  if p.lower()=='k'and O(x1-x2)==2:
   if x2>x1:self.b[y1][5],self.b[y1][7]=self.b[y1][7],'.'
   else:self.b[y1][3],self.b[y1][0]=self.b[y1][0],'.'
  if p.lower()=='p'and x1!=x2 and self.b[y2][x2]=='.':self.b[y1][x2]='.'
  if len(m)==5:p=m[4].upper()if self.t=='w'else m[4].lower()
  self.b[y2][x2]=p;self.b[y1][x1]='.'
  if p=='K' or p=='k':F=L
  elif p.lower()=='r':
   if p=='R'and y1==7:
    if x1==0:F=self.c['Q']=L
    elif x1==7:F=self.c['K']=L
   elif p=='r'and y1==0:
    if x1==0:F=self.c['q']=L
    elif x1==7:F=self.c['k']=L
  self.e=None
  if p.lower()=='p'and O(y1-y2)==2:self.e=(x1,(y1+y2)//2)
  if p.lower()=='p'or self.b[y2][x2]!='.':self.h=0
  else:self.h+=1
  if self.t=='b':self.f+=1
  self.t='b'if self.t=='w'else'w'
 def generate_moves(self):
  m=[]
  for y in B(8):
   for x in B(8):
    p=self.b[y][x]
    if p=='.'or(p.isupper()and self.t=='b')or(p.islower()and self.t=='w'):continue
    d=-1 if p.isupper()else 1
    if p.lower()=='p':
     s=P(d<0)
     if y+d in B(8)and self.b[y+d][x]=='.':
      m+=[f"{H(x+97)}{8-y}{H(x+97)}{8-(y+d)}"]
      if y==(6if s else 1)and self.b[y+2*d][x]=='.':m+=[f"{H(x+97)}{8-y}{H(x+97)}{8-(y+2*d)}"]
     for dx in(-1,1):
      if x+dx in B(8):
       if self.b[y+d][x+dx]!='.'and((self.b[y+d][x+dx].isupper()and self.t=='b')or(self.b[y+d][x+dx].islower()and self.t=='w')):m+=[f"{H(x+97)}{8-y}{H(x+dx+97)}{8-(y+d)}"]
       if self.e and(x+dx,y+d)==self.e:m+=[f"{H(x+97)}{8-y}{H(x+dx+97)}{8-(y+d)}"]
    elif p.lower()=='n':
     for dx,dy in((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
      nx,ny=x+dx,y+dy
      if 0<=nx<8 and 0<=ny<8 and(self.b[ny][nx]=='.'or(self.b[ny][nx].isupper()and self.t=='b')or(self.b[ny][nx].islower()and self.t=='w')):m+=[f"{H(x+97)}{8-y}{H(nx+97)}{8-ny}"]
    elif p.lower() in'bq':
     for dx,dy in((1,1),(1,-1),(-1,1),(-1,-1)):
      for e in B(1,8):
       nx,ny=x+dx*e,y+dy*e
       if not(0<=nx<8 and 0<=ny<8):break
       if self.b[ny][nx]=='.':m+=[f"{H(x+97)}{8-y}{H(nx+97)}{8-ny}"]
       else:
        if(self.b[ny][nx].isupper()and self.t=='b')or(self.b[ny][nx].islower()and self.t=='w'):m+=[f"{H(x+97)}{8-y}{H(nx+97)}{8-ny}"]
        break
    elif p.lower() in'rq':
     for dx,dy in((1,0),(0,1),(-1,0),(0,-1)):
      for e in B(1,8):
       nx,ny=x+dx*e,y+dy*e
       if not(0<=nx<8 and 0<=ny<8):break
       if self.b[ny][nx]=='.':m+=[f"{H(x+97)}{8-y}{H(nx+97)}{8-ny}"]
       else:
        if(self.b[ny][nx].isupper()and self.t=='b')or(self.b[ny][nx].islower()and self.t=='w'):m+=[f"{H(x+97)}{8-y}{H(nx+97)}{8-ny}"]
        break
    elif p.lower()=='k':
     for dx,dy in((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)):
      nx,ny=x+dx,y+dy
      if 0<=nx<8 and 0<=ny<8 and(self.b[ny][nx]=='.'or(self.b[ny][nx].isupper()and self.t=='b')or(self.b[ny][nx].islower()and self.t=='w')):m+=[f"{H(x+97)}{8-y}{H(nx+97)}{8-ny}"]
     if self.t=='w'and p=='K':
      if self.c['K']and self.b[7][5]==self.b[7][6]=='.':m+=["e1g1"]
      if self.c['Q']and self.b[7][3]==self.b[7][2]==self.b[7][1]=='.':m+=["e1c1"]
     elif self.t=='b'and p=='k':
      if self.c['k']and self.b[0][5]==self.b[0][6]=='.':m+=["e8g8"]
      if self.c['q']and self.b[0][3]==self.b[0][2]==self.b[0][1]=='.':m+=["e8c8"]
  return m
 def evaluate(self):
  s=p=0
  for y in B(8):
   for x in B(8):
    if(self.b[y][x])=='.':continue
    p=self.b[y][x];v=(10+(p.lower()=='n')+(p.lower()=='b')*2+(p.lower()=='r')*4+(p.lower()=='q')*8+(p.lower()=='k')*199)*10
    v+=(2,1,1,0,1,1,0)[x]*(1+(y==1or y==6))*5+(0,5,5,0,5,5,0)[x]*(1+(y>1and y<6))
    s+=v*(1-2*(p.islower()))
  return s*(1-2*(self.t=='b'))
T=lambda b,d,a,B,E:
 if d==0:return b.evaluate()
 m=b.generate_moves()
 if not m:return-20000if E else 20000
 m.sort(key=lambda x:(0 if b.S(I(x[2])-97,8-P(x[3]))!='.'else 1,-O(100*(1+2*(b.S(I(x[0])-97,8-P(x[1])).lower()=='n')+3*(_.lower()=='b')+5*(_.lower()=='r')+9*(_.lower()=='q')+200*(_.lower()=='k')))))
 if E:
  V=-1e9
  for u in m:
   c=Q();c.b=[r[:]for r in b.b];c.t=b.t;c.c=b.c.copy();c.e=b.e;c.h=b.h;c.f=b.f;c.U(u)
   e=T(c,d-1,a,B,L);V=M(V,e);a=M(a,e)
   if B<=a:break
  return V
 else:
  V=1e9
  for u in m:
   c=Q();c.b=[r[:]for r in b.b];c.t=b.t;c.c=b.c.copy();c.e=b.e;c.h=b.h;c.f=b.f;c.U(u)
   e=T(c,d-1,a,B,J);V=M(V,e);B=M(B,e)
   if B<=a:break
  return V
def main():
 b=Q()
 while J:
  l=sys.stdin.readline().strip()
  if not l:continue
  if l=='uci':E("id name TinyChess");E("id author Hermes");E("uciok")
  elif l=='isready':E("readyok")
  elif l.startswith('position'):
   p=l.split()
   if p[1]=='startpos':
    b.reset()
    if len(p)>2 and p[2]=='moves':
     for u in p[3:]:b.U(u)
  elif l.startswith('go'):
   p=l.split();d=3
   if'depth'in p:d=P(p[p.index('depth')+1])
   _=None;W=-1e9
   for u in b.generate_moves():
    c=Q();c.b=[r[:]for r in b.b];c.t=b.t;c.c=b.c.copy();c.e=b.e;c.h=b.h;c.f=b.f;c.U(u)
    s=-T(c,d-1,-1e9,1e9,b.t=='b')
    if s>W:W=s;_=u
   E(f"bestmove {_}")
  elif l=='quit':break
if __name__=='__main__':main()