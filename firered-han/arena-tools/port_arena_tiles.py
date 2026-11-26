"""port_arena_tiles.py: a small secondary tileset for the Dash Arena, with the ruins tiles of the Sevii Islands (FireRed's sevii_islands_67):
metatile 0x200 = plain ruins cobblestone, 0x201 = the white stone pillar.
It is written in the Hoenn way (tile numbers from 512, palettes 6 to 12) into pokefirered/data/tilesets/secondary/hoenn_arena."""
import os, struct
from PIL import Image
import sheet_fr
from sheet import pal

FR = '/home/claude/pokefirered/data/tilesets/'
OUT = FR + 'secondary/hoenn_arena'
sheet_fr.S = sheet_fr.load('secondary/sevii_islands_67')
P, S = sheet_fr.P, sheet_fr.S
PICK = [('cobble', 0x0DA), ('pillar', 0x0AE)]

def tile_pixels(ti):
    sheet, k = (P[0], ti) if ti < 640 else (S[0], ti - 640)
    x, y = (k % 16) * 8, (k // 16) * 8
    c = sheet.crop((x, y, x + 8, y + 8))
    return tuple(c.getdata())     # 64 palette indices

def flip(px, hf, vf):
    rows = [px[r * 8:(r + 1) * 8] for r in range(8)]
    if vf: rows = rows[::-1]
    if hf: rows = [r[::-1] for r in rows]
    return tuple(v for r in rows for v in r)

tiles = []            # unique tiles (64 indices each), flips already applied
tile_index = {}
slots = {}            # source palette (kind, number) -> new slot 6..12
palettes = {}
metatiles = []
for name, k in PICK:
    ents = struct.unpack_from('<8H', S[1], k * 16)
    new = []
    for e in ents:
        ti, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
        key = ('p', pn) if pn < 7 else ('s', pn)
        if key not in slots:
            slots[key] = 6 + len(slots)
            palettes[slots[key]] = (P[2][pn] if pn < 7 else S[2][pn])
        px = flip(tile_pixels(ti), 0, 0)
        # flips are kept in the entry (cheaper than new tiles)
        if px not in tile_index:
            tile_index[px] = len(tiles); tiles.append(px)
        new.append(((512 + tile_index[px]) & 0x3FF) | (hf << 10) | (vf << 11) | (slots[key] << 12))
    metatiles.append(new)
# custom tree tiles, made of tiles the primary set already has: the tip of a tree lives in the bottom row of the tree above it (the
# 0x20cc / 0x20cd pieces on the top layer), so a tree with open ground above has no tip. 0x202/0x203: the tip over snow; 0x204/0x205:
# the trunk row of a tree with nothing below it (without the tip of a tree that is not there).
PH = open(FR + 'primary/hoenn_general_snow/metatiles.bin', 'rb').read()
PA = struct.unpack('<512I', open(FR + 'primary/hoenn_general_snow/metatile_attributes.bin', 'rb').read())
ent = lambda m: list(struct.unpack_from('<8H', PH, m * 16))
snow = ent(0x001)
tip_l = snow[:4] + [0, 0, 0, 0x20CC]
tip_r = snow[:4] + [0, 0, 0x20CD, 0]
trunk_l = ent(0x1DC)[:4] + [0, 0, 0, 0]
trunk_r = ent(0x1DD)[:4] + [0, 0, 0, 0]
assert ent(0x1DC)[7] == 0x20CC and ent(0x1DD)[6] == 0x20CD
metatiles += [tip_l, tip_r, trunk_l, trunk_r]
assert len(slots) <= 7, slots
print('metatiles', len(metatiles), 'tiles', len(tiles), 'palette slots', slots)

os.makedirs(OUT + '/palettes', exist_ok=True)
# the picture: 16 tiles a row, 4-bit indices
rows = (max(len(tiles), 16) + 15) // 16
img = Image.new('P', (128, rows * 8), 0)
img.putpalette([v for i in range(16) for v in (i * 17, i * 17, i * 17)])
for n, px in enumerate(tiles):
    img.paste(Image.frombytes('P', (8, 8), bytes(px)), ((n % 16) * 8, (n // 16) * 8))
img.save(OUT + '/tiles.png')
open(OUT + '/metatiles.bin', 'wb').write(b''.join(struct.pack('<8H', *m) for m in metatiles))
open(OUT + '/metatile_attributes.bin', 'wb').write(struct.pack('<%dI' % len(metatiles), *([0, 0, PA[0x1DC], PA[0x1DC], PA[0x1DC], PA[0x1DC]])))
for i in range(16):
    cols = palettes.get(i, [(0, 0, 0)] * 16)
    open(OUT + '/palettes/%02d.pal' % i, 'w').write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))
print('written', OUT)
