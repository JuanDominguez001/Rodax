// @ts-nocheck
function renderGeneric(headSel, bodySel, items){
  const body = document.querySelector(bodySel), head = document.querySelector(headSel);
  if (!Array.isArray(items) || !items.length){ body.innerHTML = `<tr><td colspan="99" class="muted">Sin datos</td></tr>`; head.innerHTML=''; return; }
  const keys = Object.keys(items[0]);
  head.innerHTML = keys.map(k=>`<th>${k}</th>`).join('');
  body.innerHTML = items.map(r=>`<tr>${keys.map(k=>`<td>${(r[k]??'')}</td>`).join('')}</tr>`).join('');
}

async function cargarMantenimiento(){
  try{
    const data = await http.get('/mantenimientos/');
    const rows = Array.isArray(data)?data:(data?.results||data)||[];
    renderGeneric('#mant-head','#mant-body',rows);
    toast('Mantenimiento cargado','success');
  }catch(e){ toast('Error cargando mantenimiento','error'); log('mantenimiento FAIL',e.message); }
}

async function crearMantenimiento(ev){
  ev.preventDefault();
  const fd  = new FormData(ev.target);
  const btn = document.querySelector('#btn-mant-crear'); const orig=btn.textContent; btn.disabled=true; btn.textContent='Guardando...';
  const errors = document.getElementById('mant-errors'); errors.textContent='';
  const payload = Object.fromEntries(fd.entries());
  // Si quieres setear un estado por defecto:
  if (!payload.estado) payload.estado = 'PENDIENTE';
  try{
    await http.post('/mantenimientos/', payload);
    toast('Mantenimiento creado','success');
    ev.target.reset(); await cargarMantenimiento();
  }catch(e){
    try{ const j=JSON.parse(String(e.message).replace(/^HTTP \d+: /,'')); errors.innerHTML = Object.entries(j).map(([k,v])=>`<div>• <b>${k}</b>: ${v}</div>`).join(''); }
    catch{ errors.textContent = e.message; }
    toast('No se pudo crear','error');
  }finally{ btn.disabled=false; btn.textContent=orig; }
}

document.getElementById('btn-mant-cargar')?.addEventListener('click', cargarMantenimiento);
document.getElementById('f-mant-crear')?.addEventListener('submit', crearMantenimiento);
