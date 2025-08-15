// @ts-nocheck
function renderGeneric(headSel, bodySel, items){
  const body = document.querySelector(bodySel), head = document.querySelector(headSel);
  if (!Array.isArray(items) || !items.length){ body.innerHTML = `<tr><td colspan="99" class="muted">Sin datos</td></tr>`; head.innerHTML=''; return; }
  const keys = Object.keys(items[0]);
  head.innerHTML = keys.map(k=>`<th>${k}</th>`).join('');
  body.innerHTML = items.map(r=>`<tr>${keys.map(k=>`<td>${(r[k]??'')}</td>`).join('')}</tr>`).join('');
}

async function cargarAsignaciones(){
  try{
    const data = await http.get('/asignaciones/');
    const rows = Array.isArray(data)?data:(data?.results||data)||[];
    renderGeneric('#asig-head','#asig-body',rows);
    toast('Asignaciones cargadas','success');
  }catch(e){ toast('Error cargando asignaciones','error'); log('asignaciones FAIL',e.message); }
}

async function crearAsignacion(ev){
  ev.preventDefault();
  const fd  = new FormData(ev.target);
  const btn = document.querySelector('#btn-asig-crear'); const orig=btn.textContent; btn.disabled=true; btn.textContent='Guardando...';
  const errors = document.getElementById('asig-errors'); errors.textContent='';
  const payload = Object.fromEntries(fd.entries());
  try{
    // fecha_salida de <input type="datetime-local">
    // DRF suele aceptar 'YYYY-MM-DDTHH:mm' directamente.
    await http.post('/asignaciones/', payload);
    toast('Asignación creada','success');
    ev.target.reset(); await cargarAsignaciones();
  }catch(e){
    try{ const j=JSON.parse(String(e.message).replace(/^HTTP \d+: /,'')); errors.innerHTML = Object.entries(j).map(([k,v])=>`<div>• <b>${k}</b>: ${v}</div>`).join(''); }
    catch{ errors.textContent = e.message; }
    toast('No se pudo crear','error');
  }finally{ btn.disabled=false; btn.textContent=orig; }
}

document.getElementById('btn-asig-cargar')?.addEventListener('click', cargarAsignaciones);
document.getElementById('f-asig-crear')?.addEventListener('submit', crearAsignacion);
