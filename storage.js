// Where the players' records are kept. One small JSON file per player, found by a key such as "players/ab12….json".
// The rest of the server only calls get(key) and put(key, text), so this file is the only thing to change
// to move to another place (R2, S3, a database): write a new class with the same two methods and pick it in open().
//
//   get(key)        -> { text, version } or null if there is no such record
//   put(key, text, version) -> new version. Pass the version from get(), or null to create. Throws {code:'conflict'}
//                      if the record changed (or already exists) since.
//
// The default is a private GitHub repository, written through GitHub's contents API with a token that can only
// touch that one repository. SAVES_TOKEN is the token (a Render environment variable, never in code); SAVES_REPO is
// "owner/name" (it defaults to jcoulsling/klondike-saves). Without a token, records are kept in memory only (nothing
// survives a restart) and the server says so.
const https = require('https');

class GitHubStore {
  constructor(repo, token, branch) {
    this.repo = repo; this.token = token; this.branch = branch || null;
    this.sha = new Map();       // key -> blob sha, from the last get/put
  }
  req(method, key, body) {
    return new Promise((resolve, reject) => {
      const path = '/repos/' + this.repo + '/contents/' + key.split('/').map(encodeURIComponent).join('/') + (method === 'GET' && this.branch ? '?ref=' + this.branch : '');
      const data = body ? JSON.stringify(body) : null;
      const r = https.request({ host: 'api.github.com', path, method, timeout: 20000, headers: {
        'Authorization': 'Bearer ' + this.token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'klondike-online', ...(data ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) } : {}) } }, (res) => {
        const chunks = []; res.on('data', (d) => chunks.push(d));
        res.on('end', () => { let j = null; try { j = JSON.parse(Buffer.concat(chunks).toString('utf8')); } catch (e) {} resolve({ status: res.statusCode, json: j }); });
      });
      r.on('timeout', () => r.destroy(new Error('GitHub timed out')));
      r.on('error', reject);
      if (data) r.write(data);
      r.end();
    });
  }
  async get(key) {
    const { status, json } = await this.req('GET', key);
    if (status === 404) { this.sha.delete(key); return null; }
    if (status !== 200 || !json || typeof json.content !== 'string') throw new Error('storage read failed (' + status + ')');
    this.sha.set(key, json.sha);
    return { text: Buffer.from(json.content, 'base64').toString('utf8'), version: json.sha };
  }
  async put(key, text, version) {
    const body = { message: 'save ' + key.slice(0, 40), content: Buffer.from(text, 'utf8').toString('base64') };
    if (this.branch) body.branch = this.branch;
    if (version) body.sha = version;
    const { status, json } = await this.req('PUT', key, body);
    if (status === 409 || status === 422) { const e = new Error('conflict'); e.code = 'conflict'; throw e; }
    if (status !== 200 && status !== 201) throw new Error('storage write failed (' + status + ')');
    const v = json && json.content && json.content.sha;
    this.sha.set(key, v);
    return v;
  }
}

class MemoryStore {
  constructor() { this.m = new Map(); this.n = 0; }
  async get(key) { const r = this.m.get(key); return r ? { text: r.text, version: r.version } : null; }
  async put(key, text, version) {
    const r = this.m.get(key);
    if ((r && r.version !== version) || (!r && version)) { const e = new Error('conflict'); e.code = 'conflict'; throw e; }
    const v = 'm' + (++this.n); this.m.set(key, { text, version: v }); return v;
  }
}

function open(env) {
  if (env.SAVES_TOKEN) {
    const repo = env.SAVES_REPO || 'jcoulsling/klondike-saves';
    console.log('Players are kept in the private repository ' + repo);
    return { store: new GitHubStore(repo, env.SAVES_TOKEN, env.SAVES_BRANCH), durable: true };
  }
  console.log('SAVES_TOKEN / SAVES_REPO are not set: players and saves are kept in memory only, and are lost when the server restarts.');
  return { store: new MemoryStore(), durable: false };
}

module.exports = { open, GitHubStore, MemoryStore };
