// Players: a name and a password, and one save per player. The browser derives two keys from the password
// (PBKDF2 with a salt kept here): one it sends to log in, one it keeps to encrypt the save. The server only ever
// sees the first, and keeps a scrypt hash of it. The save arrives already compressed and encrypted, and is stored as it came.
const crypto = require('crypto');

const NAME_RE = /[^\p{L}\p{N} '_-]/gu;
const MAX_SAVE_B64 = 400000;        // a compressed, encrypted save is far smaller than this
const TOKEN_HOURS = 12;
const FAIL_MAX = 5, FAIL_LOCK_MS = 10 * 60 * 1000;      // wrong passwords for one name
const IP_MAX = 40, IP_WINDOW_MS = 10 * 60 * 1000;       // login attempts from one address
const SAVE_GAP_MS = 8000;                               // a save at most this often per player

function cleanName(s) { return String(s || '').normalize('NFC').replace(NAME_RE, '').trim().slice(0, 12); }
function lower(s) { return s.toLocaleLowerCase('en'); }

module.exports = function accounts(store, secretSeed) {
  const secret = crypto.createHash('sha256').update('klondike-session|' + (secretSeed || crypto.randomBytes(32).toString('hex'))).digest();
  const fails = new Map(), ips = new Map(), lastSave = new Map(), chains = new Map();

  const keyFor = (name) => 'players/' + crypto.createHash('sha256').update(lower(name)).digest('hex').slice(0, 32) + '.json';
  const hmac = (s) => crypto.createHmac('sha256', secret).update(s).digest();
  const fakeSalt = (name) => hmac('salt|' + lower(name)).subarray(0, 16).toString('hex');
  const scrypt = (auth, salt) => new Promise((res, rej) => crypto.scrypt(auth, Buffer.from(salt, 'hex'), 32, { N: 16384, r: 8, p: 1 }, (e, k) => e ? rej(e) : res(k)));
  const okB64 = (s, n) => typeof s === 'string' && /^[A-Za-z0-9+/=]+$/.test(s) && Buffer.from(s, 'base64').length === n;

  // work on one player's record one at a time
  function serial(key, fn) {
    const prev = chains.get(key) || Promise.resolve();
    const next = prev.catch(() => {}).then(fn);
    chains.set(key, next);
    next.finally(() => { if (chains.get(key) === next) chains.delete(key); }).catch(() => {});
    return next;
  }

  function token(name) {
    const exp = Date.now() + TOKEN_HOURS * 3600 * 1000;
    const body = Buffer.from(JSON.stringify({ n: name, e: exp })).toString('base64url');
    return body + '.' + hmac('tok|' + body).toString('base64url');
  }
  function who(tok) {
    const [body, sig] = String(tok || '').split('.');
    if (!body || !sig) return null;
    const want = hmac('tok|' + body);
    let got; try { got = Buffer.from(sig, 'base64url'); } catch (e) { return null; }
    if (got.length !== want.length || !crypto.timingSafeEqual(got, want)) return null;
    try { const j = JSON.parse(Buffer.from(body, 'base64url').toString()); return j.e > Date.now() && typeof j.n === 'string' ? j.n : null; } catch (e) { return null; }
  }

  async function read(name) {
    const r = await store.get(keyFor(name));
    return r ? { rec: JSON.parse(r.text), version: r.version } : null;
  }

  async function prelogin(rawName) {
    const name = cleanName(rawName);
    if (!name) throw httpErr(400, 'Type a name first.');
    const r = await read(name);
    return { name, salt: r ? r.rec.salt : fakeSalt(name) };
  }

  function httpErr(status, msg) { const e = new Error(msg); e.status = status; return e; }

  async function login(rawName, auth, ip) {
    const name = cleanName(rawName);
    if (!name) throw httpErr(400, 'Type a name first.');
    if (!okB64(auth, 32)) throw httpErr(400, 'That did not look right. Reload the page and try again.');
    const now = Date.now();
    const ipe = ips.get(ip) || { n: 0, t: now };
    if (now - ipe.t > IP_WINDOW_MS) { ipe.n = 0; ipe.t = now; }
    if (++ipe.n > IP_MAX) { ips.set(ip, ipe); throw httpErr(429, 'Too many tries. Wait a few minutes.'); }
    ips.set(ip, ipe);
    const lk = lower(name), f = fails.get(lk) || { n: 0, until: 0 };
    if (f.until > now) throw httpErr(429, 'That name is locked for a few minutes after wrong passwords.');

    return serial(keyFor(name), async () => {
      let cur = await read(name);
      if (!cur) {                                   // a new name: this password becomes its password
        const salt = fakeSalt(name), pws = crypto.randomBytes(16).toString('hex');
        const rec = { v: 1, name, salt, pw: { s: pws, h: (await scrypt(Buffer.from(auth, 'base64'), pws)).toString('hex') }, created: new Date().toISOString(), save: null };
        try { await store.put(keyFor(name), JSON.stringify(rec, null, 1), null); }
        catch (e) { if (e.code !== 'conflict') throw e; cur = await read(name); }
        if (!cur) return { name, token: token(name), created: true, hasSave: false };
      }
      const hash = (await scrypt(Buffer.from(auth, 'base64'), cur.rec.pw.s)).toString('hex');
      const a = Buffer.from(hash, 'hex'), b = Buffer.from(cur.rec.pw.h, 'hex');
      if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
        f.n++; if (f.n >= FAIL_MAX) { f.until = Date.now() + FAIL_LOCK_MS; f.n = 0; }
        fails.set(lk, f);
        throw httpErr(401, 'Wrong password for that name.');
      }
      fails.delete(lk);
      return { name: cur.rec.name, token: token(cur.rec.name), created: false, hasSave: !!cur.rec.save };
    });
  }

  async function getSave(tok) {
    const name = who(tok);
    if (!name) throw httpErr(401, 'Sign in again.');
    const cur = await read(name);
    if (!cur || !cur.rec.save) return { save: null };
    return { save: cur.rec.save };
  }

  async function putSave(tok, data, ts) {
    const name = who(tok);
    if (!name) throw httpErr(401, 'Sign in again.');
    if (typeof data !== 'string' || data.length < 16 || data.length > MAX_SAVE_B64 || !/^[A-Za-z0-9+/=]+$/.test(data)) throw httpErr(400, 'That save is not valid.');
    const lk = lower(name), now = Date.now();
    if (now - (lastSave.get(lk) || 0) < SAVE_GAP_MS) throw httpErr(429, 'Saving too often.');
    lastSave.set(lk, now);
    return serial(keyFor(name), async () => {
      for (let i = 0; i < 3; i++) {
        const cur = await read(name);
        if (!cur) throw httpErr(404, 'No such player.');
        cur.rec.save = { v: 1, ts: now, data };
        try { await store.put(keyFor(name), JSON.stringify(cur.rec), cur.version); return { ok: true, ts: now }; }
        catch (e) { if (e.code !== 'conflict') throw e; }
      }
      throw httpErr(409, 'Could not save. Try again.');
    });
  }

  return { cleanName, prelogin, login, getSave, putSave, who };
};
