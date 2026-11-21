R=range(8)
import sys
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000,'p':-100,'n':-320,'b':-330,'r':-500,'q':-900,'k':-20000,'.':0}
D={'P':[(-1,-1),(-1,1)],'p':[(1,-1),(1,1)],'N':[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],'B':[(-1,-1),(-1,1),(1,-1),(1,1)],'R':[(-1,0),(1,0),(0,-1),(0,1)],'Q':[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)],'K':[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]}
D['n'],D['b'],D['r'],D['q'],D['k']=D['N'],D['B'],D['R'],D['Q'],D['K']
def init():return [list(r)for r in['rnbqkbnr','pppppppp']+['.'*8]*4+['PPPPPPPP','RNBQKBNR']],1
def atk(b,r,c,w):
 for dr,dc in[(1,-1),(1,1)] if w else [(-1,-1),(-1,1)]:
 nr,nc=r+dr,c+dc
 if 8>nr>=0<=nc<8 and b[nr][nc]=='pP'[w]:return 1
 for dr,dc in D['N']:
 nr,nc=r+dr,c+dc
 if 8>nr>=0<=nc<8 and b[nr][nc]=='nN'[w]:return 1
 for dr,dc in D['K']:
 nr,nc=r+dr,c+dc
 if 8>nr>=0<=nc<8 and b[nr][nc]=='kK'[w]:return 1
 for dr,dc in D['B']:
 nr,nc=r+dr,c+dc
 while 8>nr>=0<=nc<8:
 p=b[nr][nc]
 if p!=".":
 if p in('bq','BQ')[w]:return 1
 break
 nr+=dr;nc+=dc
 for dr,dc in D['R']:
 nr,nc=r+dr,c+dc
 while 8>nr>=0<=nc<8:
 p=b[nr][nc]
 if p!=".":
 if p in('rq','RQ')[w]:return 1
 break
 nr+=dr;nc+=dc
 return 0
def gen(b,w):
 ms=[]
 for r in R:
 for c in R:
 p=b[r][c]
 if p=='.' or p.isupper()!=(w>0):continue
 if p in 'Pp':
 d=-1 if w else 1;st=6 if w else 1;pr=0 if w else 7
 if 8>r+d>=0 and b[r+d][c]=='.':
 for q in ('qrbn','QRBN')[w] if r+d==pr else ['.']:ms+=[(r,c,r+d,c,q)]
 if r==st and b[r+2*d][c]=='.':ms+=[(r,c,r+2*d,c,'.')]
 for dc in (-1,1):
 if 8>r+d>=0 and 0<=c+dc<8 and b[r+d][c+dc]!='.' and b[r+d][c+dc].isupper()!=(w>0):
 for q in ('qrbn','QRBN')[w] if r+d==pr else ['.']:ms+=[(r,c,r+d,c+dc,q)]
 else:
 sl=p in 'BRQbrq'
 for dr,dc in D[p]:
 nr,nc=r+dr,c+dc
 while 8>nr>=0<=nc<8:
 t=b[nr][nc]
 if t=='.':ms+=[(r,c,nr,nc,'.')]
 else:
 if t.isupper()!=(w>0):ms+=[(r,c,nr,nc,'.')]
 break
 if not sl:break
 nr+=dr;nc+=dc
 return ms
def mk(b,m):
 nb=[r[:] for r in b];r1,c1,r2,c2,q=m;p=nb[r1][c1];nb[r1][c1]='.';nb[r2][c2]=p if q=='.' else q
 if p=='K' and r1==7 and c1==4 and c2==6:nb[7][5],nb[7][7]='R','.'
 if p=='K' and r1==7 and c1==4 and c2==2:nb[7][3],nb[7][0]='R','.'
 if p=='k' and r1==0 and c1==4 and c2==6:nb[0][5],nb[0][7]='r','.'
 if p=='k' and r1==0 and c1==4 and c2==2:nb[0][3],nb[0][0]='r','.'
 return nb
def ik(b,w):
 k='kK'[w]
 for r in R:
 for c in R:
 if b[r][c]==k:return atk(b,r,c,1-w)
 return 1
def ev(b):
 s=0
 for r in R:
 for c in R:
 p=b[r][c]
 if p!=".":s+=V[p]+(4-abs(3.5-c))*(5 if p.isupper() else -5)
 return int(s)
def ab(b,d,a,bt,w):
 if d==0:return ev(b)*(w*2-1),None
 ms=gen(b,w);ms.sort(key=lambda m:b[m[2]][m[3]]!='.',reverse=1);bm=None;leg=0
 for m in ms:
 nb=mk(b,m)
 if ik(nb,w):continue
 leg+=1;sc=-ab(nb,d-1,-bt,-a,1-w)[0]
 if sc>a:
 a=sc;bm=m
 if a>=bt:break
 if not leg:return (-19000-d if ik(b,w) else 0),None
 return a,bm
def um(m):return f'{chr(97+m[1])}{8-m[0]}{chr(97+m[3])}{8-m[2]}{m[4].lower() if m[4]!="." else ""}'
def pf(f):
 ps=f.split();b=[]
 for r in ps[0].split('/'):
 row=[]
 for ch in r:row+=['.']*int(ch) if ch.isdigit() else [ch]
 b+=[row]
 return b,+(ps[1]=='w')
b,w=init()
for ln in sys.stdin:
 ln=ln.strip()
 if ln=='uci':print('id name TC4K\nid author nh\nuciok',flush=1)
 elif'i'==ln[0]:print('readyok',flush=1)
 elif'u'==ln[0]:b,w=init()
 elif'p'==ln[0]:
 ps=ln.split();b,w=init()if ps[1]=='startpos'else pf(' '.join(ps[2:8] ));idx=2+6*(ps[1]!='startpos')
 if len(ps)>idx and ps[idx]=='moves':
 for mv in ps[idx+1:]:b=mk(b,(8-int(mv[1]),ord(mv[0])-97,8-int(mv[3]),ord(mv[2])-97,(mv[4].lower(),mv[4].upper())[w] if len(mv)>4 else '.'));w=1-w
 elif'g'==ln[0]:
 _,bm=ab(b,3 if 'movetime' in ln else 2,-99999,99999,w)
 if not bm:
 for m in gen(b,w):
 if not ik(mk(b,m),w):bm=m;break
 print('bestmove '+(um(bm) if bm else '0000'),flush=1)
 elif'q'==ln[0]:break
