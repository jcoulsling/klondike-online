import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
N=86
orig=Image.open('/home/claude/arena/dota.jpg').convert('RGB')
full=np.asarray(orig.resize((1290,1290),Image.BOX)).astype(float)/255   # 15 px per cell
lab=np.load('/home/claude/arena/lab12.npy')                             # 644x644 clusters
rv=np.load('/home/claude/arena/river.npy')                              # 1288 river mask
S900=1290/900.0
def cellmean(mask,res):
    k=res//N if res%N==0 else None
    m=np.asarray(Image.fromarray((mask*255).astype(np.uint8)).resize((N,N),Image.BOX)).astype(float)/255
    return m
rv_f=cellmean(np.pad(rv,((0,2),(0,2))),1290)
lab_big=np.kron(lab,np.ones((1,1),int))
def clusterfrac(ids):
    m=np.isin(lab,ids)
    return np.asarray(Image.fromarray((m*255).astype(np.uint8)).resize((N,N),Image.BOX)).astype(float)/255
tree_f=clusterfrac([3,5,10,7])
jung_f=clusterfrac([2,8])
# lava
a=full; r,g,b=a[...,0],a[...,1],a[...,2]
mx=a.max(2); mn=a.min(2); s=(mx-mn)/np.maximum(mx,1e-6)
lava=((r>g+0.12)&(r>b+0.12)&(s>0.45)&(mx>0.35))
lava_f=np.asarray(Image.fromarray((lava*255).astype(np.uint8)).resize((N,N),Image.BOX)).astype(float)/255
# playable polygon (900-view coordinates)
poly=[(42,28),(610,28),(612,58),(850,58),(878,110),(880,860),(290,858),(285,895),(30,895),(28,300),(45,260)]
pm=Image.new('L',(900,900),0); ImageDraw.Draw(pm).polygon(poly,fill=255)
inside=np.asarray(pm.resize((N,N),Image.BOX)).astype(float)/255
# dire side: above the river diagonal
def dire_side(cx,cy):   # cell centre in 900 coords
    if cx<185: return cy<262
    if cx>715: return cy<618
    y=275+(610-275)*(cx-185)/(715-185)
    return cy<y
CELL=900/N
cls=np.zeros((N,N),'<U1')
for y in range(N):
    for x in range(N):
        if inside[y,x]<0.5 or lava_f[y,x]>0.12: cls[y,x]='#'      # wall
        elif rv_f[y,x]>=0.5: cls[y,x]='~'                         # water
        elif tree_f[y,x]>=0.30: cls[y,x]='T'                      # tree
        elif jung_f[y,x]>=0.5: cls[y,x]='j'                       # jungle floor
        else: cls[y,x]='.'                                         # open ground
np.save('/home/claude/arena/cls_raw.npy',cls)
if __name__=='__main__':
    col={'#':(70,70,80),'~':(40,90,200),'T':(20,100,30),'j':(170,200,150),'.':(235,235,235)}
    img=Image.new('RGB',(N*10,N*10))
    px=img.load()
    for y in range(N):
        for x in range(N):
            c=col[cls[y,x]]
            for j in range(10):
                for i in range(10): px[x*10+i,y*10+j]=c
    side=Image.new('RGB',(N*10*2+10,N*10))
    side.paste(img,(0,0)); side.paste(orig.resize((N*10,N*10)),(N*10+10,0))
    side.save('/home/claude/arena/preview_raw.png')
    from collections import Counter
    print(Counter(cls.flatten()))
