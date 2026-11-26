import struct
from PIL import Image, ImageDraw
from sheet import pal, tile_img
FR='/home/claude/pokefirered/data/tilesets/'
def load(folder):
    return (Image.open(FR+folder+'/tiles.png'), open(FR+folder+'/metatiles.bin','rb').read(),
            [pal(FR+folder+'/palettes/%02d.pal'%i) for i in range(16)])
P=load('primary/general'); S=load('secondary/tanoby_ruins')
def metatile(k):      # k = index inside the secondary tileset
    ents=struct.unpack_from('<8H',S[1],k*16)
    img=Image.new('RGBA',(16,16),(0,0,0,255))
    for layer in range(2):
        for q in range(4):
            e=ents[layer*4+q]; ti=e&0x3FF; hf=(e>>10)&1; vf=(e>>11)&1; pn=e>>12
            sheet,pt=(P[0],ti) if ti<640 else (S[0],ti-640)
            palette=P[2][pn] if pn<7 else S[2][pn]
            img.alpha_composite(tile_img(sheet,pt,palette,hf,vf),((q%2)*8,(q//2)*8))
    return img
if __name__=='__main__':
    n=len(S[1])//16; sc=4; per=14
    sheet=Image.new('RGB',(per*(16*sc+6),((n+per-1)//per)*(16*sc+16)),(40,40,40)); d=ImageDraw.Draw(sheet)
    for k in range(n):
        x=(k%per)*(16*sc+6); y=(k//per)*(16*sc+16)
        sheet.paste(metatile(k).resize((16*sc,16*sc),Image.NEAREST),(x,y)); d.text((x,y+16*sc+2),'%02x'%k,fill=(255,255,0))
    sheet.save('tanoby.png'); print(n)
