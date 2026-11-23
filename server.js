// Pokémon Klondike Version, online: serves the page and relays where each player is.
// No game, patch or save ever reaches this server. It holds a small record per player and nothing else.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 3000;
const PUBLIC = path.join(__dirname, 'public');
const MAX_PER_ROOM = 5;              // the game has room for four others on the map
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.wasm': 'application/wasm',
                '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.txt': 'text/plain; charset=utf-8' };

const server = http.createServer((req, res) => {
  const url = decodeURIComponent((req.url || '/').split('?')[0]);
  // The emulator uses threads, which a page may only use when it is cross-origin isolated.
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  res.setHeader('Cross-Origin-Resource-Policy', 'same-origin');
  if (url === '/health') { res.writeHead(200); return res.end('ok'); }
  const file = path.join(PUBLIC, url === '/' ? 'index.html' : url);
  if (!file.startsWith(PUBLIC)) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(data);
  });
});

const rooms = new Map();             // code -> Map(id -> client)
let nextId = 1;

function roomList() {
  return [...rooms.entries()].map(([code, m]) => ({ code, players: m.size, max: MAX_PER_ROOM }));
}
function send(ws, obj) { if (ws.readyState === 1) ws.send(JSON.stringify(obj)); }
function leave(c) {
  if (!c.room) return;
  const m = rooms.get(c.room);
  if (m) {
    m.delete(c.id);
    for (const o of m.values()) send(o.ws, { t: 'left', id: c.id });
    if (m.size === 0) rooms.delete(c.room);
  }
  c.room = null;
}

const wss = new WebSocketServer({ server, path: '/ws', maxPayload: 4096 });
wss.on('connection', (ws) => {
  const c = { id: nextId++, ws, name: 'Player', room: null, last: 0 };
  send(ws, { t: 'hello', id: c.id, rooms: roomList() });
  ws.on('message', (raw) => {
    let m; try { m = JSON.parse(raw); } catch (e) { return; }
    if (m.t === 'list') return send(ws, { t: 'rooms', rooms: roomList() });
    if (m.t === 'join') {
      leave(c);
      const code = String(m.room || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8) || 'KLONDIKE';
      c.name = String(m.name || 'Player').replace(/[^\p{L}\p{N} '_-]/gu, '').slice(0, 12) || 'Player';
      let r = rooms.get(code);
      if (!r) { r = new Map(); rooms.set(code, r); }
      if (r.size >= MAX_PER_ROOM) return send(ws, { t: 'full', room: code });
      r.set(c.id, c); c.room = code;
      send(ws, { t: 'joined', room: code, id: c.id, others: [...r.values()].filter(o => o.id !== c.id).map(o => ({ id: o.id, name: o.name })) });
      for (const o of r.values()) if (o.id !== c.id) send(o.ws, { t: 'arrived', id: c.id, name: c.name });
      return;
    }
    if (m.t === 's' && c.room && Array.isArray(m.s) && m.s.length >= 8 && m.s.length <= 12) {
      const now = Date.now();
      if (now - c.last < 40) return;           // at most 25 a second
      c.last = now;
      const s = m.s.map((v) => v | 0);   // [active, group, num, facing, x, y, gfx, walking, picture, palette, follower]
      const r = rooms.get(c.room);
      if (r) for (const o of r.values()) if (o.id !== c.id) send(o.ws, { t: 's', id: c.id, s });
      return;
    }
    if (m.t === 'trade' && c.room) {          // a trade message to one player of the room: kind 1 to 7, a Pokémon (80 bytes) or none
      const r = rooms.get(c.room), to = r && r.get(m.to | 0);
      const kind = m.kind | 0;
      if (!to || to.id === c.id || kind < 1 || kind > 7) return;
      const mon = Array.isArray(m.mon) && m.mon.length === 80 ? m.mon.map((v) => v & 255) : null;
      send(to.ws, { t: 'trade', from: c.id, kind, mon });
      return;
    }
    if (m.t === 'lnk' && c.room) {            // the cable of a battle: k 'b' a block (up to 256 bytes), 's' a stand-by count, 'c' ready to close
      const r = rooms.get(c.room), to = r && r.get(m.to | 0);
      if (!to || to.id === c.id) return;
      if (m.k === 'b') {
        if (!Array.isArray(m.d) || m.d.length > 256) return;
        send(to.ws, { t: 'lnk', from: c.id, k: 'b', d: m.d.map((v) => v & 255) });
      } else if (m.k === 's') send(to.ws, { t: 'lnk', from: c.id, k: 's', n: m.n & 255 });
      else if (m.k === 'c') send(to.ws, { t: 'lnk', from: c.id, k: 'c' });
      return;
    }
    if (m.t === 'leave') return leave(c);
  });
  ws.on('close', () => leave(c));
  ws.on('error', () => leave(c));
});

server.listen(PORT, () => console.log('Klondike online on port ' + PORT));
