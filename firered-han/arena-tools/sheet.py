import struct, re
from PIL import Image, ImageDraw
FR='/home/claude/pokefirered/data/tilesets/'
def pal(path):
    L=open(path).read().split()
    n=int(L[2]); cols=[]
    for i in range(n):
        r,g,b=int(L[3+3*i]),int(L[4+3*i]),int(L[5+3*i]); cols.append((r,g,b))
    return cols
def load(folder):
    t=Image.open(FR+folder+'/tiles.png'); 
    mt=open(FR+folder+'/metatiles.bin','rb').read()
    pals=[pal(FR+folder+'/palettes/%02d.pal'%i) for i in range(16)]
    return t,mt,pals
P=load('primary/hoenn_general_snow'); S=load('secondary/hoenn_dewford')
def tile_img(sheet,idx,palette,hf,vf):
    t=sheet
    x=(idx%16)*8; y=(idx//16)*8
    c=t.crop((x,y,x+8,y+8))
    px=c.load(); out=Image.new('RGBA',(8,8))
    o=out.load()
    for j in range(8):
        for i in range(8):
            v=px[i,j]
            o[i,j]=(0,0,0,0) if v==0 else palette[v]+(255,)
    if hf: out=out.transpose(Image.FLIP_LEFT_RIGHT)
    if vf: out=out.transpose(Image.FLIP_TOP_BOTTOM)
    return out
def metatile(mid):
    if mid<512: t,mt,pals=P; k=mid
    else: t2,mt,pals2=S; k=mid-512
    ents=struct.unpack_from('<8H',(P[1] if mid<512 else S[1]),k*16)
    img=Image.new('RGBA',(16,16),(0,0,0,255))
    for layer in range(2):
        for q in range(4):
            e=ents[layer*4+q]
            ti=e&0x3FF; hf=(e>>10)&1; vf=(e>>11)&1; pn=e>>12
            if ti<512: sheet=P[0]; ptile=ti; 
            else: sheet=S[0]; ptile=ti-512
            palette=P[2][pn] if pn<6 else S[2][pn]
            tim=tile_img(sheet,ptile,palette,hf,vf)
            img.alpha_composite(tim,((q%2)*8,(q//2)*8))
    return img
if __name__=='__main__':
    import sys
    lo,hi,name=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
    per=16; sc=3; cw=16*sc+8; ch=16*sc+14
    rows=(hi-lo+per-1)//per
    sheet=Image.new('RGB',(per*cw,rows*ch),(40,40,40))
    d=ImageDraw.Draw(sheet)
    for n,mid in enumerate(range(lo,hi)):
        im=metatile(mid).resize((16*sc,16*sc),Image.NEAREST)
        x=(n%per)*cw+4; y=(n//per)*ch+2
        sheet.paste(im,(x,y)); d.text((x,y+16*sc),'%03x'%mid,fill=(255,255,0))
    sheet.save(name)
