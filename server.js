// Pokémon Klondike Version, online: serves the page and relays where each player is.
// No game, patch or save ever reaches this server. It holds a small record per player and nothing else.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 3000;
const PUBLIC = path.join(__dirname, 'public');
const MAX_PER_ROOM = 5;              // the game has room for four others on the map
const MAX_IN_ROOM = 30;              // people in a room, counting those who only use the teaching board and chat
const MAX_POINTS = 60000;            // points of whiteboard drawing a room keeps
const MAX_CHAT = 60;                 // chat lines a room keeps for people who arrive later
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
    else if (m.host === c.id) {                 // the first person to join runs the board; when they go, the next one does
      m.host = m.values().next().value.id;
      for (const o of m.values()) send(o.ws, { t: 'host', id: m.host });
    }
  }
  c.room = null;
}
function newRoom() {
  const r = new Map();
  r.host = 0; r.locked = false; r.chat = []; r.strokes = []; r.byKey = new Map(); r.points = 0;
  return r;
}
function everyone(r, obj) { for (const o of r.values()) send(o.ws, obj); }
function people(r) { return [...r.values()].map(o => ({ id: o.id, name: o.name, b: o.board ? 1 : 0 })); }
const COLOUR = /^#[0-9a-f]{6}$/i;

const wss = new WebSocketServer({ server, path: '/ws', maxPayload: 16384 });
wss.on('connection', (ws) => {
  const c = { id: nextId++, ws, name: 'Player', room: null, last: 0, board: false, lastChat: 0, count: 0, countAt: 0 };
  send(ws, { t: 'hello', id: c.id, rooms: roomList() });
  ws.on('message', (raw) => {
    let m; try { m = JSON.parse(raw); } catch (e) { return; }
    if (m.t === 'list') return send(ws, { t: 'rooms', rooms: roomList() });
    if (m.t === 'join') {
      leave(c);
      const code = String(m.room || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 8) || 'KLONDIKE';
      c.name = String(m.name || 'Player').replace(/[^\p{L}\p{N} '_-]/gu, '').slice(0, 12) || 'Player';
      let r = rooms.get(code);
      if (!r) { r = newRoom(); rooms.set(code, r); }
      c.board = !!m.board;                        // only the teaching board and chat, no game
      const players = [...r.values()].filter(o => !o.board).length;
      if (r.size >= MAX_IN_ROOM || (!c.board && players >= MAX_PER_ROOM)) { if (r.size === 0) rooms.delete(code); return send(ws, { t: 'full', room: code }); }
      r.set(c.id, c); c.room = code;
      if (!r.host) r.host = c.id;
      send(ws, { t: 'joined', room: code, id: c.id, host: r.host, locked: r.locked, chat: r.chat,
                 others: [...r.values()].filter(o => o.id !== c.id).map(o => ({ id: o.id, name: o.name, b: o.board ? 1 : 0 })) });
      if (r.strokes.length) send(ws, { t: 'wbfull', strokes: r.strokes.map(k => ({ key: k.key, k: k.k, c: k.c, w: k.w, p: k.p, s: k.s })) });
      for (const o of r.values()) if (o.id !== c.id) send(o.ws, { t: 'arrived', id: c.id, name: c.name, b: c.board ? 1 : 0 });
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
    if (m.t === 'chat' && c.room) {           // a line of chat for everyone in the room
      const now = Date.now();
      if (now - c.lastChat < 400) return;
      c.lastChat = now;
      const text = String(m.s || '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, 300);
      const r = rooms.get(c.room);
      if (!text || !r) return;
      const line = { id: c.id, name: c.name, s: text, ts: now };
      r.chat.push(line); if (r.chat.length > MAX_CHAT) r.chat.shift();
      everyone(r, { t: 'chat', line });
      return;
    }
    if (m.t === 'wb' && c.room) {             // whiteboard: pieces of a stroke (pen 'p', eraser 'e') or a line of text 't'
      const r = rooms.get(c.room);
      if (!r || (r.locked && c.id !== r.host)) return send(ws, { t: 'wbdenied' });
      const now = Date.now();
      if (now - c.countAt > 1000) { c.countAt = now; c.count = 0; }
      if (++c.count > 80) return;
      const kind = m.k === 'e' ? 'e' : m.k === 't' ? 't' : 'p';
      const id = String(m.id || '').replace(/[^a-z0-9]/gi, '').slice(0, 10);
      if (!id || !Array.isArray(m.p) || m.p.length < 2 || m.p.length > 80) return;
      const p = m.p.map((v) => Math.max(0, Math.min(1000, v | 0)));
      if (p.length % 2) p.pop();
      const key = c.id + ':' + id;
      let st = r.byKey.get(key);
      if (!st) {
        if (r.points > MAX_POINTS) return;
        st = { key, owner: c.id, k: kind, c: COLOUR.test(m.c) ? m.c : '#000000', w: Math.max(1, Math.min(60, m.w | 0 || 3)), p: [],
               s: kind === 't' ? String(m.s || '').replace(/[\u0000-\u001f]/g, ' ').slice(0, 120) : '' };
        if (kind === 't' && !st.s.trim()) return;
        r.byKey.set(key, st); r.strokes.push(st);
      } else if (st.k === 't') return;
      st.p.push(...(kind === 't' ? p.slice(0, 2) : p)); r.points += p.length / 2;
      for (const o of r.values()) if (o.id !== c.id) send(o.ws, { t: 'wb', by: c.id, key, k: st.k, c: st.c, w: st.w, p, s: st.s, first: st.p.length === p.length ? 1 : 0 });
      return;
    }
    if (m.t === 'wbtype' && c.room) {         // someone is typing a line of text: show it to the others letter by letter (not kept)
      const r = rooms.get(c.room);
      if (!r || (r.locked && c.id !== r.host)) return;
      const now = Date.now();
      if (now - c.countAt > 1000) { c.countAt = now; c.count = 0; }
      if (++c.count > 80) return;
      const msg = { t: 'wbtype', by: c.id, x: Math.max(0, Math.min(1000, m.x | 0)), y: Math.max(0, Math.min(1000, m.y | 0)),
                    c: COLOUR.test(m.c) ? m.c : '#000000', w: Math.max(1, Math.min(60, m.w | 0 || 3)),
                    s: String(m.s || '').replace(/[\u0000-\u001f]/g, ' ').slice(0, 120) };
      for (const o of r.values()) if (o.id !== c.id) send(o.ws, msg);
      return;
    }
    if (m.t === 'wbundo' && c.room) {         // takes back your own last stroke
      const r = rooms.get(c.room);
      if (!r || (r.locked && c.id !== r.host)) return;
      for (let i = r.strokes.length - 1; i >= 0; i--) {
        if (r.strokes[i].owner === c.id) {
          const [st] = r.strokes.splice(i, 1);
          r.byKey.delete(st.key); r.points -= st.p.length / 2;
          everyone(r, { t: 'wbundo', key: st.key });
          break;
        }
      }
      return;
    }
    if (m.t === 'wbclear' && c.room) {        // wipes the board: the host any time, others only while it is not locked
      const r = rooms.get(c.room);
      if (!r || (r.locked && c.id !== r.host)) return;
      r.strokes = []; r.byKey = new Map(); r.points = 0;
      everyone(r, { t: 'wbclear', by: c.id });
      return;
    }
    if (m.t === 'wblock' && c.room) {         // the host says only they may draw
      const r = rooms.get(c.room);
      if (!r || r.host !== c.id) return;
      r.locked = !!m.on;
      everyone(r, { t: 'wblock', on: r.locked });
      return;
    }
    if (m.t === 'leave') return leave(c);
  });
  ws.on('close', () => leave(c));
  ws.on('error', () => leave(c));
});

server.listen(PORT, () => console.log('Klondike online on port ' + PORT));
