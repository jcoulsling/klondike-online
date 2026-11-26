"""arena_render.py: reads arena_spec.json and draws the arena from its exact data (class grid, towers, camps, objects), to check a reading of the spec.
Usage: python3 arena_render.py arena_spec.json out.png"""
import json, sys
from PIL import Image, ImageDraw
spec = json.load(open(sys.argv[1]))
S = 10
col = {'.': (226, 238, 248), 'T': (40, 96, 60), '#': (110, 110, 118), '~': (70, 130, 200), 'F': (150, 205, 235), 'R': (200, 190, 170), 'Q': (250, 250, 250), 'K': (60, 40, 40)}
img = Image.new('RGB', (86 * S, 86 * S)); d = ImageDraw.Draw(img)
for y, row in enumerate(spec['class_grid']):
    for x, c in enumerate(row[:86]): d.rectangle([x * S, y * S, x * S + S - 1, y * S + S - 1], fill=col.get(c, (255, 0, 255)))
mark = lambda x, y, c: d.rectangle([x * S + 1, y * S + 1, x * S + S - 2, y * S + S - 2], outline=c, width=2)
for c in spec['camps']:
    for x, y in c['members']: mark(x, y, (210, 40, 40))
for m in spec['merchants']: mark(*m['at'], (150, 60, 200))
oc = {'ITEM_BALL': (230, 150, 0), 'CUT_TREE': (60, 200, 60), 'ROCK_SMASH_ROCK': (170, 120, 220), 'PUSHABLE_BOULDER': (120, 110, 100)}
for o in spec['objects']: mark(o['x'], o['y'], oc[o['kind']])
img.save(sys.argv[2])
