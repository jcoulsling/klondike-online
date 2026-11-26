import numpy as np, sys
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
N=86
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.60
orig=Image.open('/home/claude/arena/dota.jpg').convert('RGB')
tree=np.load('/home/claude/arena/tree_density.npy')
rv=np.load('/home/claude/arena/river.npy')
a=np.asarray(orig.resize((1290,1290),Image.BOX)).astype(float)/255
r,g,b=a[...,0],a[...,1],a[...,2]
mx=a.max(2); mn=a.min(2); s=(mx-mn)/np.maximum(mx,1e-6)
lava=((r>g+0.12)&(r>b+0.12)&(s>0.45)&(mx>0.35))
def cellmean(m):
    return np.asarray(Image.fromarray((np.clip(m,0,1)*255).astype(np.uint8)).resize((N,N),Image.BOX)).astype(float)/255
tree_c=cellmean(tree)
rv_c=cellmean(np.pad(rv,((0,2),(0,2))))
lava_c=cellmean(lava)
poly=[(42,28),(610,28),(612,58),(850,58),(878,110),(880,860),(290,858),(285,895),(30,895),(28,300),(45,260)]
pm=Image.new('L',(900,900),0); ImageDraw.Draw(pm).polygon(poly,fill=255)
inside=np.asarray(pm.resize((N,N),Image.BOX)).astype(float)/255
wall=(inside<0.5)|(lava_c>0.12)
water=(rv_c>=0.5)&~wall
land=~wall&~water
def dire_side(cx,cy):
    if cx<185: return cy<262
    if cx>715: return cy<618
    y=275+(610-275)*(cx-185)/(715-185)
    return cy<y
CELL=900/N
ds=np.zeros((N,N),bool)
for y in range(N):
    for x in range(N):
        ds[y,x]=dire_side((x+0.5)*CELL,(y+0.5)*CELL)
PD=float(sys.argv[2]) if len(sys.argv)>2 else 0.50
PR=float(sys.argv[3]) if len(sys.argv)>3 else 0.40
tr=np.zeros((N,N),bool)
for side,frac in ((ds,PD),(~ds,PR)):
    m=land&side
    thr=np.quantile(tree_c[m],1-frac)
    print('side thr',round(float(thr),3),'cells',int(m.sum()))
    tr|=(tree_c>thr)&m
np.save('/home/claude/arena/dire_side.npy',ds)
# clean: remove tiny tree specks and fill tiny gaps
lab,n=ndi.label(tr)
for i in range(1,n+1):
    if (lab==i).sum()<4: tr[lab==i]=False
op=land&~tr
lab,n=ndi.label(op)
for i in range(1,n+1):
    if (lab==i).sum()<3: tr[lab==i]=True
cls=np.full((N,N),'.','<U1')
cls[tr]='T'; cls[water]='~'; cls[wall]='#'
np.save('/home/claude/arena/cls2.npy',cls)
if __name__=='__main__':
    col={'#':(70,70,80),'~':(40,90,200),'T':(20,100,30),'.':(235,235,235)}
    img=Image.new('RGB',(N*10,N*10)); px=img.load()
    for y in range(N):
        for x in range(N):
            c=col[cls[y,x]]
            for j in range(10):
                for i in range(10): px[x*10+i,y*10+j]=c
    side=Image.new('RGB',(N*10*2+10,N*10))
    side.paste(img,(0,0)); side.paste(orig.resize((N*10,N*10)),(N*10+10,0))
    side.save('/home/claude/arena/preview2.png')
    from collections import Counter; print(T,Counter(cls.flatten()))
