"""build_arena.py: the Dota map as a FireRed map (86 x 86), from cls2.npy made by classify2.py.
Writes arena/out/map.bin, border.bin, arena.txt (one character per tile) and arena.json (where things are), and a preview picture
drawn with the real tiles. Run it after classify2.py."""
import numpy as np, json, os, struct, re, collections
from PIL import Image
from scipy import ndimage as ndi
import sheet as SH
SH.S = SH.load('secondary/hoenn_arena')

N = 86
cls = np.load('/home/claude/arena/cls2.npy').copy()
dire = np.load('/home/claude/arena/dire_side.npy')
OUT = '/home/claude/arena/out'
os.makedirs(OUT, exist_ok=True)

# ---- metatile numbers (raw map words: metatile | collision << 10 | elevation << 12) ----
SNOW = 0x3001
SNOW2 = [0x3001, 0x3001, 0x3001, 0x3001]
TREE_R = [[0x1D4, 0x1D5], [0x1DC, 0x1DD]]          # a frosty tree, 2 x 2 tiles (Radiant side)
TREE_D = TREE_R                                   # the Dire side has the same trees (the dark pine set is not a whole tree)
ROCK = 0x00AA
TIP = [0x3202, 0x3203]                           # the tip of a tree, over snow (own tileset)
TRUNK = [0x0604, 0x0605]                         # the trunk row of a tree with nothing below it (own tileset)
COBBLE = 0x3200                                  # ruins cobblestone (own tileset)
PILLAR = 0x0601                                  # the white stone pillar, solid
CAVE = [[0x078, 0x064, 0x07A], [0x088, 0x0A7, 0x08A]]   # the cave in the river: rock face on top, the doorway below
WATER = 0x1170
def wall(mid): return mid | (1 << 10)

# ---- helpers on the class grid ----
def regrow():
    return (cls == '.')

# 00. trees come in whole 2 x 2 blocks (one tree is 2 x 2 tiles): a block of land is a tree when most of it is, else open
for by in range(0, N, 2):
    for bx in range(0, N, 2):
        blk = cls[by:by + 2, bx:bx + 2]
        if all(c in '.T' for c in blk.flatten()):
            blk[:, :] = 'T' if (blk == 'T').sum() >= 2 else '.'
        else:
            if (blk == '#').sum() >= 2: blk[:, :] = '#'
            else: blk[blk == 'T'] = '.'

# 0. lone rocks (from lava specks) inside the arena are trees; only the outer wall and the big lava walls stay rock
rock = (cls == '#')
rl, rn = ndi.label(rock)
for i in range(1, rn + 1):
    comp = (rl == i)
    ys, xs = np.nonzero(comp)
    touches = ys.min() == 0 or xs.min() == 0 or ys.max() == N - 1 or xs.max() == N - 1
    if not touches and comp.sum() < 5:
        cls[comp] = 'T'

# 1. pockets of open ground that nothing connects to: small ones are filled with trees, big ones get a cut through the trees
openm = regrow()
lab, n = ndi.label(openm)
sizes = ndi.sum(openm, lab, range(1, n + 1))
main = int(np.argmax(sizes)) + 1
cuts = 0; filled = 0
for i in range(1, n + 1):
    if i == main: continue
    sz = int(sizes[i - 1])
    comp = (lab == i)
    if sz <= 30:
        cls[comp] = 'T'; filled += 1; continue
    # shortest way through trees to the main area: breadth first from the pocket
    q = collections.deque([(y, x) for y, x in zip(*np.nonzero(comp))])
    prev = {p: None for p in q}
    found = None
    while q and found is None:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < N and 0 <= nx < N) or (ny, nx) in prev: continue
            if cls[ny, nx] == 'T':
                prev[(ny, nx)] = (y, x); q.append((ny, nx))
            elif lab[ny, nx] == main:
                prev[(ny, nx)] = (y, x); found = (ny, nx); break
    if found:
        p = prev[found]
        while p is not None and not comp[p]:
            cls[p] = '.'
            if p[1] + 1 < N and cls[p[0], p[1] + 1] == 'T': cls[p[0], p[1] + 1] = '.'   # two wide
            p = prev[p]
        cuts += 1
print('pockets filled', filled, 'cut through', cuts)

# 2. the bridges: the places the picture has them (cell coordinates), each carried across the water by the shortest straight run
BR = []   # no bridges: the river is water all the way
deck = np.zeros((N, N), bool)
bridges = []
for bx, by in BR:
    cx, cy = int(bx * N / 1288), int(by * N / 1288)
    best = None
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        # from the nearest water cell on this side, march across to land
        for start in range(0, 6):
            x, y = cx + dx * start, cy + dy * start
            if 0 <= x < N and 0 <= y < N and cls[y, x] == '~':
                run = 0
                while 0 <= x < N and 0 <= y < N and cls[y, x] == '~':
                    run += 1; x += dx; y += dy
                if 0 <= x < N and 0 <= y < N and cls[y, x] != '#' and run <= 18:
                    if best is None or run < best[0]:
                        best = (run, cx + dx * start, cy + dy * start, dx, dy)
                break
    if best is None:
        print('no bridge for', bx, by); continue
    run, x0, y0, dx, dy = best
    # two wide: this line and the one beside it that has more water
    px, py = (dy, dx)   # perpendicular
    def water_side(s):
        c = 0
        for k in range(run):
            x, y = x0 + dx * k + px * s, y0 + dy * k + py * s
            if 0 <= x < N and 0 <= y < N and cls[y, x] == '~': c += 1
        return c
    s = 1 if water_side(1) >= water_side(-1) else -1
    cells = []
    for k in range(-1, run + 1):
        for w in (0, s):
            x, y = x0 + dx * k + px * w, y0 + dy * k + py * w
            if 0 <= x < N and 0 <= y < N and cls[y, x] in '~.T':
                cells.append((x, y))
    for x, y in cells:
        deck[y, x] = True
    bridges.append({'from': [cx, cy], 'dir': [dx, dy], 'length': run})
print('bridges', bridges)
for y, x in zip(*np.nonzero(deck)):
    cls[y, x] = 'B'

# 3. the middle drop-off and the two spawn pads: 3 x 3 of ruins cobblestone inside a ring of cobblestone, a stone pillar at each corner of the ring
def pad(cx, cy, mark):
    for y in range(cy - 2, cy + 3):
        for x in range(cx - 2, cx + 3):
            if not (0 <= x < N and 0 <= y < N): continue
            if cls[y, x] == '#': continue
            corner = abs(x - cx) == 2 and abs(y - cy) == 2
            inner = abs(x - cx) <= 1 and abs(y - cy) <= 1
            cls[y, x] = 'Q' if corner else (mark if inner else 'R')
def ford(cx, cy):         # the middle: shallow water to wade through, from one bank of the river to the other
    for y in range(cy - 2, cy + 3):
        for x in range(cx - 2, cx + 3):
            if 0 <= x < N and 0 <= y < N and cls[y, x] != '#': cls[y, x] = 'F'
ford(43, 43)
def ancient(cx, cy):        # an ancient: a 3 x 3 patch of ruins cobblestone with a stone pillar in the middle
    for y in range(cy - 2, cy + 3):
        for x in range(cx - 2, cx + 3):
            if 0 <= x < N and 0 <= y < N and cls[y, x] == 'T': cls[y, x] = '.'
    for y in range(cy - 1, cy + 2):
        for x in range(cx - 1, cx + 2):
            if cls[y, x] != '#': cls[y, x] = 'R'
    cls[cy, cx] = 'Q'
ancient(11, 73)           # radiant ancient (bottom left)
ancient(72, 17)           # dire ancient (top right)
for lane, k, x, y in json.load(open('/home/claude/arena/bases.json')):
    if cls[y, x] == 'T': cls[y, x] = '.'
    cls[y, x] = 'R' if k.startswith('bar') else 'Q'     # a barracks is a ruins cobblestone, a tower a stone pillar
FLAG_R = (11, 73); FLAG_D = (72, 17)

# the cave in the river: where the rock island was (rows 29-30, columns 26-28)
for j in range(2):
    for i in range(3):
        cls[29 + j, 26 + i] = 'K'

# 4. make sure the three places are in the same open area as each other
openm = np.isin(cls, list('.PCRB'))
lab, n = ndi.label(openm)
ids = {lab[43, 43], lab[73, 11], lab[17, 72]}
print('drop-off, radiant and dire spawn in', len(ids), 'area(s)')

# ---- last: a tree is only ever a whole 2 x 2 block; leftovers of the steps above are opened up ----
partial = 0
for by in range(0, N, 2):
    for bx in range(0, N, 2):
        blk = cls[by:by + 2, bx:bx + 2]
        t = int((blk == 'T').sum())
        if 0 < t < 4:
            blk[blk == 'T'] = '.'; partial += t
print('partial tree tiles opened', partial)

# ---- tile for each cell ----
land_after = np.isin(cls, list('.TPCRQBK#'))      # for the shore: what counts as land
# the catalogue of water tiles with a shore, found from the pictures of the tiles
inc = open('/home/claude/pokefirered/include/constants/metatile_behaviors.h').read()
mb = {k: int(v, 16) for k, v in re.findall(r'#define (MB_\w+) (0x[0-9A-Fa-f]+)', inc)}
src = open('/home/claude/pokefirered/src/metatile_behavior.c').read()
tab = src[src.index('sBehaviorSurfable'):]; tab = tab[:tab.index('};')]
surf = {mb[m.group(1)] for m in re.finditer(r'\[(MB_\w+)\]\s*=\s*([^,\n]+)', tab) if 'TRUE' in m.group(2)}
pa = struct.unpack('<512I', open('/home/claude/pokefirered/data/tilesets/primary/hoenn_general_snow/metatile_attributes.bin', 'rb').read())
def sig(mid):
    im = np.asarray(SH.metatile(mid).convert('RGB')).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    water = (b - r > 70) & (r < 160)
    brown = (r > g + 12) & (g > b - 10) & (r > 90)
    gray = (abs(r - g) < 14) & (abs(g - b) < 18) & (r > 110) & (r < 200)
    if brown.mean() > 0.03 or gray.mean() > 0.03: return None
    f = water.mean()
    if f < 0.04 or f > 0.985: return None
    s = np.zeros((3, 3))
    edges = [0, 5, 11, 16]
    for j in range(3):
        for i in range(3):
            s[j, i] = water[edges[j]:edges[j + 1], edges[i]:edges[i + 1]].mean()
    return s
catalog = {}
for mid in range(0x100, 0x1c0):
    if (pa[mid] & 0x1FF) in surf:
        s = sig(mid)
        if s is not None: catalog[mid] = s
print('shore tiles', len(catalog))
def shore(x, y):
    def L(dx, dy):
        xx, yy = x + dx, y + dy
        if not (0 <= xx < N and 0 <= yy < N): return False
        return bool(land_after[yy, xx])
    n_, e_, s_, w_ = L(0, -1), L(1, 0), L(0, 1), L(-1, 0)
    want = np.ones((3, 3))
    want[0, 1] = 0 if n_ else 1; want[1, 2] = 0 if e_ else 1; want[2, 1] = 0 if s_ else 1; want[1, 0] = 0 if w_ else 1
    want[0, 0] = 0 if (n_ or w_ or L(-1, -1)) else 1
    want[0, 2] = 0 if (n_ or e_ or L(1, -1)) else 1
    want[2, 0] = 0 if (s_ or w_ or L(-1, 1)) else 1
    want[2, 2] = 0 if (s_ or e_ or L(1, 1)) else 1
    if want.min() == 1: return WATER
    w = np.array([[1, 1.5, 1], [1.5, 2, 1.5], [1, 1.5, 1]])
    best = min(catalog.items(), key=lambda kv: float((w * (kv[1] - want) ** 2).sum()))
    return best[0] | (1 << 12)
rng = np.random.RandomState(7)
words = np.zeros((N, N), '<u2')
for y in range(N):
    for x in range(N):
        c = cls[y, x]
        if c == '.':
            # open ground right above a tree: the tree's tip is drawn here
            words[y, x] = TIP[x % 2] if (y + 1 < N and cls[y + 1, x] == 'T' and (y + 1) % 2 == 0) else SNOW
        elif c == 'T':
            pat = TREE_D if dire[y - y % 2, x - x % 2] else TREE_R
            if y % 2 == 1 and not (y + 1 < N and cls[y + 1, x] == 'T'):
                words[y, x] = TRUNK[x % 2]               # nothing below: no tip of a next tree
            else:
                words[y, x] = wall(pat[y % 2][x % 2])
        elif c == '#': words[y, x] = wall(ROCK)
        elif c == '~': words[y, x] = shore(x, y)
        elif c == 'F': words[y, x] = 0x3185
        elif c in 'CPR': words[y, x] = COBBLE
        elif c == 'Q': words[y, x] = PILLAR
        elif c == 'K':
            w = CAVE[y - 29][x - 26]
            words[y, x] = (w | (1 << 10)) if w != 0x0A7 else (w | (3 << 12))
open(OUT + '/map.bin', 'wb').write(words.tobytes())
open(OUT + '/border.bin', 'wb').write(struct.pack('<4H', wall(ROCK), wall(ROCK), wall(ROCK), wall(ROCK)))
open(OUT + '/arena.txt', 'w').write('\n'.join(''.join(r) for r in cls))
json.dump({'size': [N, N], 'drop_off': [43, 43], 'radiant_spawn': list(FLAG_R), 'dire_spawn': list(FLAG_D), 'bridges': bridges}, open(OUT + '/arena.json', 'w'), indent=1)
print(collections.Counter(cls.flatten()))

# ---- a picture with the real tiles ----
cache = {}
def tile(w):
    mid = int(w) & 0x3FF
    if mid not in cache: cache[mid] = SH.metatile(mid)
    return cache[mid]
pic = Image.new('RGBA', (N * 16, N * 16))
for y in range(N):
    for x in range(N):
        pic.paste(tile(words[y, x]), (x * 16, y * 16))
pic.convert('RGB').save(OUT + '/arena_tiles.png')
pic.convert('RGB').resize((N * 8, N * 8), Image.LANCZOS).save(OUT + '/arena_tiles_small.png')
print('done')
