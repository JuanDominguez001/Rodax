// @ts-nocheck
function renderGeneric(headSel, bodySel, items){
  const body = document.querySelector(bodySel), head = document.querySelector(headSel);
  if (!Array.isArray(items) || !items.length){ body.innerHTML = `<tr><td colspan="99" class="muted">Sin datos</td></tr>`; head.innerHTML=''; return; }
  const keys = Object.keys(items[0]);
  head.innerHTML = keys.map(k=>`<th>${k}</th>`).join('');
  body.innerHTML = items.map(r=>`<tr>${keys.map(k=>`<td>${(r[k]??'')}</td>`).join('')}</tr>`).join('');
}

async function cargarCombustible(){
  try{
    const data = await http.get('/combustibles/');
    const rows = Array.isArray(data)?data:(data?.results||data)||[];
    renderGeneric('#comb-head','#comb-body',rows);
    toast('Combustible cargado','success');
  }catch(e){ toast('Error cargando combustible','error'); log('combustible FAIL',e.message); }
}

async function crearCombustible(ev){
  ev.preventDefault();
  const fd  = new FormData(ev.target);
  const btn = document.querySelector('#btn-comb-crear'); const orig=btn.textContent; btn.disabled=true; btn.textContent='Guardando...';
  const errors = document.getElementById('comb-errors'); errors.textContent='';
  const payload = Object.fromEntries(fd.entries());
  try{
    await http.post('/combustibles/', payload);
    toast('Carga registrada','success');
    ev.target.reset(); await cargarCombustible();
  }catch(e){
    try{ const j=JSON.parse(String(e.message).replace(/^HTTP \d+: /,'')); errors.innerHTML = Object.entries(j).map(([k,v])=>`<div>• <b>${k}</b>: ${v}</div>`).join(''); }
    catch{ errors.textContent = e.message; }
    toast('No se pudo crear','error');
  }finally{ btn.disabled=false; btn.textContent=orig; }
}

document.getElementById('btn-comb-cargar')?.addEventListener('click', cargarCombustible);
document.getElementById('f-comb-crear')?.addEventListener('submit', crearCombustible);
