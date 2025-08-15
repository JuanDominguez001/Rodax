// @ts-nocheck
class Http {
  constructor({ base = CONFIG.BASE_URL, access = CONFIG.ACCESS } = {}) {
    this.base = base.replace(/\/+$/, '');
    this.access = access;
  }
  setBase(url){ this.base = url.replace(/\/+$/, ''); localStorage.setItem('BASE_URL', this.base); }
  setTokens({ access, refresh }){ if (access!=null){ this.access=access; localStorage.setItem('ACCESS', access); } if (refresh!=null){ localStorage.setItem('REFRESH', refresh); } }
  _join(path){ return path.startsWith('/') ? this.base + path : this.base + '/' + path; }

  async req(path, { method='GET', query, body, headers={}, timeout=15000, raw=false } = {}) {
    if (!/\/\d+\/?$/.test(path) && !path.endsWith('/') && !path.includes('?')) path += '/';
    let url = this._join(path);
    if (query && typeof query==='object'){ const qs = new URLSearchParams(query).toString(); url += (url.includes('?')?'&':'?') + qs; }

    const ctrl = new AbortController(); const timer = setTimeout(()=>ctrl.abort(), timeout);
    const opts = { method, headers: { Accept:'application/json', ...headers }, signal: ctrl.signal, mode:'cors', credentials:'omit' };
    if (this.access) opts.headers.Authorization = `Bearer ${this.access}`;
    if (body!=null){ if (body instanceof FormData) opts.body = body; else { opts.headers['Content-Type']=opts.headers['Content-Type']||'application/json'; opts.body = JSON.stringify(body); } }

    let res; try{ res = await fetch(url, opts); } catch(e){ clearTimeout(timer); throw new Error(`Network error: ${e.message}`); } finally{ clearTimeout(timer); }
    if (raw) return res;

    const ct = res.headers.get('content-type') || '';
    const data = ct.includes('json') ? await res.json().catch(()=>null) : await res.text().catch(()=>null);
    if (!res.ok){ const msg = typeof data==='string'? data : JSON.stringify(data); throw new Error(`HTTP ${res.status}: ${msg}`); }
    return data;
  }

  get(p,q){return this.req(p,{query:q});} post(p,b){return this.req(p,{method:'POST',body:b});}
  put(p,b){return this.req(p,{method:'PUT',body:b});} patch(p,b){return this.req(p,{method:'PATCH',body:b});} del(p){return this.req(p,{method:'DELETE'});}
  async download(path, { query, filename='archivo' } = {}){ const r = await this.req(path,{query,raw:true}); if(!r.ok) throw new Error(`HTTP ${r.status}`); const blob = await r.blob(); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename; document.body.appendChild(a); a.click(); URL.revokeObjectURL(a.href); a.remove(); }
}
window.http = new Http();
