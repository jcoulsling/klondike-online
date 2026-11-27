"""check6.py ROM X Y: from a save at (X,Y) walks around and lists every wild sprite near the player with its species, screen distance and palette number."""
import re, struct, subprocess, sys, os, shutil
SB1 = re.search(r'(0x[0-9a-f]+)\s+gSaveBlock1Ptr', open('/home/claude/pokefirered/pokefirered.map').read()).group(1)
rom, X, Y = sys.argv[1], sys.argv[2], sys.argv[3]
N = int(os.environ.get('N', '30'))
moves = ['press RIGHT 24', 'press RIGHT 24', 'press DOWN 24', 'press LEFT 24', 'press LEFT 24', 'press UP 24']
shutil.copy(rom, '/tmp/t/c6.gba')
subprocess.run(['python3', '/home/claude/emu/mksave.py', '/tmp/b2/rt.sav', '/tmp/t/c6.sav', '43', '50', X, Y], capture_output=True)
s = 'wait 300\npress A 6\nwait 200\npress START 6\nwait 150\npress A 6\nwait 200\npress A 6\nwait 100\n'
for k in range(N):
    s += moves[k % len(moves)] + '\nwait 20\npeek 0x0202063c 2176 a%d\npeek 0x2020ebc 2176 b%d\npeekptr %s 0 px%d\npeekptr %s 2 py%d\n' % (k, k, SB1, k, SB1, k)
open('/tmp/t/c6.txt', 'w').write(s)
out = subprocess.run(['/home/claude/emu/harness4', '/tmp/t/c6.gba', '/tmp/t/c6.txt'], capture_output=True, text=True, env=dict(os.environ, SAVEPATH='1')).stdout
for k in range(N):
    b = b''
    for lab in ('a', 'b'):
        seg = out.split('%s%d:' % (lab, k))[1].split('\n')[0]
        b += bytes(int(v, 16) for v in re.findall(r'\b[0-9a-f]{2}\b', seg))
    px = int(re.search(r'px%d: (\w+)' % k, out).group(1), 16); py = int(re.search(r'py%d: (\w+)' % k, out).group(1), 16)
    row = []
    for i in range(len(b) // 68):
        q = b[i * 68:(i + 1) * 68]; d = struct.unpack_from('<8h', q, 0x2E)
        if not (q[0x3E] & 1) or (d[7] & 0xFFFF) != 0x57A5: continue
        t = ((d[0] + 8) >> 4, (d[1] + 8) >> 4)
        dist = max(2 * abs(t[0] - px), 3 * abs(t[1] - py))
        row.append((dist, d[2], q[5] >> 4, 'inv' if q[0x3E] & 4 else 'vis'))
    row.sort()
    print(k, (px, py), ' '.join('d%d:sp%d:p%d:%s' % r for r in row[:6]))
