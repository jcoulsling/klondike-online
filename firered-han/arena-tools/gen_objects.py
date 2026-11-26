"""gen_objects.py: puts the arena's objects into the game: item balls, strength boulders, rock smash rocks, cut trees (map.json),
their scripts (data/scripts/han_arena.inc) and the camps and merchants (src/data/han_wild_camps.h). Run after classify_arena.py."""
import json, sys, numpy as np
sys.path.insert(0, '/home/claude/hoenn/wildtiles')
import classify_arena as C
FR = '/home/claude/pokefirered'
land = set(C.seen)
p = json.load(open('/home/claude/arena/placement3.json')); o = json.load(open('/home/claude/arena/obstacles.json'))
bases = json.load(open('/home/claude/arena/bases.json'))
rows = open('/home/claude/arena/out/arena.txt').read().split('\n')
used = set((x, y) for _, _, x, y in bases) | {(11, 73), (72, 17)}
def free(x, y): return (x, y) in land and (x, y) not in used and rows[y][x] == '.'
def snap(x, y, rad=6):
    best = None
    for yy in range(y - rad, y + rad + 1):
        for xx in range(x - rad, x + rad + 1):
            if free(xx, yy):
                d = (xx - x) ** 2 + (yy - y) ** 2
                if best is None or d < best[0]: best = (d, xx, yy)
    used.add((best[1], best[2])); return best[1], best[2]
# camps first: they stand in the nooks. members: the nook and its nearest free land tiles
camps = []
for side, n, x, y in sorted(p['camps']):
    cx, cy = snap(x, y)
    members = [(cx, cy)]
    for _ in range({1: 2, 2: 1, 3: 1}[n]):
        members.append(snap(cx, cy, 3))
    camps.append((n, members))
shops = [snap(x, y) for _, x, y in p['shops']]
items = [snap(x, y) for _, x, y in p['items']]
want = ['ITEM_RARE_CANDY', 'ITEM_NUGGET', 'ITEM_MAX_REVIVE', 'ITEM_FULL_RESTORE', 'ITEM_PP_UP', 'ITEM_ULTRA_BALL']
item_ids = [want[i % 6] for i in range(len(items))]
cut = [snap(x, y) for _, x, y in o['cuttrees']]
smash = [snap(x, y) for _, x, y in o['rocksmash']]
bould = [snap(x, y) for _, x, y in o['boulders']]
ev = []
def obj(gfx, x, y, script, flag, trainer='TRAINER_TYPE_NONE', rng=1, mv='MOVEMENT_TYPE_FACE_DOWN'):
    ev.append({'type': 'object', 'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': mv, 'movement_range_x': rng, 'movement_range_y': rng,
               'trainer_type': trainer, 'trainer_sight_or_berry_tree_id': '0', 'script': script, 'flag': flag})
t = 1
inc = ['@ The Dash Arena (Wild Area map): item balls and the merchants. Made by arena/gen_objects.py.', '']
for i, ((x, y), it) in enumerate(zip(items, item_ids)):
    obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'HanArena_EventScript_Item%d' % i, 'FLAG_TEMP_%X' % t); t += 1
    inc += ['HanArena_EventScript_Item%d::' % i, '\tfinditem %s, 1' % it, '\tend', '']
for x, y in cut: obj('OBJ_EVENT_GFX_CUT_TREE', x, y, 'EventScript_CutTree', 'FLAG_TEMP_%X' % t); t += 1
for x, y in smash: obj('OBJ_EVENT_GFX_ROCK_SMASH_ROCK', x, y, 'EventScript_RockSmash', 'FLAG_TEMP_%X' % t, mv='MOVEMENT_TYPE_LOOK_AROUND'); t += 1
for x, y in bould: obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', x, y, 'EventScript_StrengthBoulder', '0', rng=0)
assert t <= 0x20, t
m = json.load(open(FR + '/data/maps/HanWildArea/map.json')); m['object_events'] = ev
json.dump(m, open(FR + '/data/maps/HanWildArea/map.json', 'w'), indent=2)
inc += ['@ The merchants at the secret shops (src/han_wild.c opens these when the player walks up to them).',
        'HanArena_EventScript_ShopKecleon::', '\tlock', '\tmessage Text_MayIHelpYou', '\twaitmessage', '\tpokemart HanArena_Items_Kecleon', '\tmsgbox Text_PleaseComeAgain', '\trelease', '\tend', '',
        '\t.align 2', 'HanArena_Items_Kecleon::'] + ['\t.2byte %s' % i for i in ('ITEM_ULTRA_BALL', 'ITEM_HYPER_POTION', 'ITEM_FULL_HEAL', 'ITEM_REVIVE', 'ITEM_NONE')] + ['', 
        'HanArena_EventScript_ShopSableye::', '\tlock', '\tmessage Text_MayIHelpYou', '\twaitmessage', '\tpokemart HanArena_Items_Sableye', '\tmsgbox Text_PleaseComeAgain', '\trelease', '\tend', '',
        '\t.align 2', 'HanArena_Items_Sableye::'] + ['\t.2byte %s' % i for i in ('ITEM_MAX_POTION', 'ITEM_MAX_REVIVE', 'ITEM_PP_UP', 'ITEM_RARE_CANDY', 'ITEM_NONE')] + ['']
open(FR + '/data/scripts/han_arena.inc', 'w').write('\n'.join(inc))
h = ['// Made by arena/gen_objects.py. The camps (6, in the nooks of the trees; members: x, y) and the two merchants.',
     '#define CAMP_COUNT 6', '#define CAMP_MEMBERS 14', 'static const u8 sCampSize[CAMP_COUNT] = {%s};' % ', '.join(str(len(mm)) for _, mm in camps),
     'static const u8 sCampBand[CAMP_COUNT] = {%s}; // 0 small, 1 medium, 2 large' % ', '.join(str(n - 1) for n, _ in camps),
     'static const u8 sCampTiles[CAMP_MEMBERS][2] = {' + ', '.join('{%d, %d}' % t for _, mm in camps for t in mm) + '};',
     'static const u8 sShopTiles[2][2] = {%s}; // Kecleon at the Radiant shop, Sableye at the Dire one' % ', '.join('{%d, %d}' % s for s in shops), '']
open(FR + '/src/data/han_wild_camps.h', 'w').write('\n'.join(h))
print('camps', camps, 'shops', shops, 'items', len(items), 'cut', cut, 'smash', smash, 'boulders', bould)

# the lowest level each Pokémon of the pool can be, from the evolution table: a level evolution needs its level (and the one before it
# must be as high), any other kind (stone, trade, friendship) is 10 levels above the Pokémon it comes from
import re
ev_src = open(FR + '/src/data/pokemon/evolution.h').read()
frm = {}
for blk in re.split(r'\n\s*\[SPECIES_', ev_src)[1:]:
    name = blk.split(']')[0]
    for m in re.finditer(r'\{(EVO_\w+),\s*(\w+),\s*SPECIES_(\w+)\}', blk):
        frm.setdefault(m.group(3), []).append((name, m.group(1), m.group(2)))
LEVELEVO = {'EVO_LEVEL', 'EVO_LEVEL_ATK_GT_DEF', 'EVO_LEVEL_ATK_EQ_DEF', 'EVO_LEVEL_ATK_LT_DEF', 'EVO_LEVEL_SILCOON', 'EVO_LEVEL_CASCOON', 'EVO_LEVEL_NINJASK', 'EVO_LEVEL_SHEDINJA'}
def minlv(sp, depth=0):
    if sp not in frm or depth > 4: return 1
    best = None
    for pre, method, param in frm[sp]:
        base = minlv(pre, depth + 1)
        lv = max(int(param), base) if method in LEVELEVO else base + 10
        best = lv if best is None else min(best, lv)
    return best
src = open(FR + '/src/han_wild.c').read()
a = src.index('static const u16 sPool[]'); pool = re.findall(r'SPECIES_(\w+)', src[a:src.index('};', a)])
lv = [min(minlv(n), 100) for n in pool]
open(FR + '/src/data/han_camp_levels.h', 'w').write('// Made by arena/gen_objects.py: the lowest level of each Pokémon of sPool (same order).\nstatic const u8 sPoolMinLevel[%d] = {%s};\n' % (len(pool), ', '.join(map(str, lv))))
print({n: l for n, l in zip(pool, lv) if n in ('CHARIZARD', 'GOLEM', 'RAICHU', 'ALAKAZAM', 'TYRANITAR', 'GRANBULL', 'TREECKO', 'SALAMENCE')})
