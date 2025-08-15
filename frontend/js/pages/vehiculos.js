// @ts-nocheck
let _vehiculos = [];

function renderVehiculos(items){
  const tbody = document.querySelector('#tbody-vehiculos');
  if (!tbody) return;
  tbody.innerHTML = (items||[]).map(v => {
    const placa  = v.placa ?? v.id ?? '';
    const marca  = v.marca ?? '';
    const modelo = v.modelo ?? '';
    const anio   = v.anio  ?? v.ano ?? v.year ?? '';   // <- lee ambas variantes
    return `<tr data-id="${v.id}">
      <td>${placa}</td><td>${marca}</td><td>${modelo}</td><td>${anio}</td>
      <td class="right"><button class="btn btn--ghost del" data-id="${v.id}">Eliminar</button></td>
    </tr>`;
  }).join('') || `<tr><td colspan="5" class="muted">No hay registros</td></tr>`;
}

async function cargarVehiculos(){
  const skeleton = document.querySelector('#skeleton'); skeleton?.classList.remove('hidden');
  try{
    const data  = await http.get('/vehiculos/');
    const items = Array.isArray(data) ? data : (data?.results || data);
    _vehiculos  = items || [];
    renderVehiculos(_vehiculos);
    log('GET /vehiculos/ OK', data);
  }catch(e){
    renderVehiculos([]);
    toast('Error al cargar vehículos','error');
    log('GET /vehiculos/ FAIL',{error:e.message});
  }finally{
    skeleton?.classList.add('hidden');
  }
}

function filtrar(texto){
  const q=(texto||'').toLowerCase();
  if(!q) return renderVehiculos(_vehiculos);
  const out=_vehiculos.filter(v=> (v.placa??'').toLowerCase().includes(q)
    || (v.marca??'').toLowerCase().includes(q)
    || (v.modelo??'').toLowerCase().includes(q)
    || String(v.anio ?? v.ano ?? '').includes(q));
  renderVehiculos(out);
}

async function crearVehiculo(ev){
  ev.preventDefault();
  const fd = new FormData(ev.target); 
  const payload = Object.fromEntries(fd.entries());
  // Normaliza nombre del campo
  if (!payload.anio && payload.ano) { payload.anio = payload.ano; delete payload.ano; }

  const btn = document.querySelector('#btn-crear'); const orig = btn.textContent; 
  btn.disabled=true; btn.textContent='Guardando...';
  const errorsEl = document.querySelector('#form-errors'); errorsEl.textContent='';
  try{
    const r = await http.post('/vehiculos/', payload);
    toast('Vehículo creado','success'); log('POST /vehiculos/ OK', r);
    ev.target.reset(); await cargarVehiculos();
    const tbody=document.querySelector('#tbody-vehiculos'); 
    if (tbody && tbody.firstElementChild) tbody.firstElementChild.classList.add('added');
  }catch(e){
    const msg=String(e.message||'');
    try{ const json=JSON.parse(msg.replace(/^HTTP \d+: /,'')); 
         errorsEl.innerHTML = Object.entries(json).map(([k,arr])=>`<div>• <b>${k}</b>: ${arr.join(', ')}</div>`).join(''); }
    catch{ errorsEl.textContent=msg; }
    toast('No se pudo crear','error'); log('POST /vehiculos/ FAIL',{error:e.message,payload});
  }finally{ btn.disabled=false; btn.textContent=orig; }
}

async function eliminarVehiculo(id){
  if(!confirm('¿Eliminar vehículo?')) return;
  try{ await http.del(`/vehiculos/${id}/`); toast('Vehículo eliminado','success'); await cargarVehiculos(); }
  catch(e){ toast('No se pudo eliminar','error'); log('DELETE /vehiculos/{id}/ FAIL',{error:e.message,id}); }
}

// Eventos
document.getElementById('f-crear')?.addEventListener('submit', crearVehiculo);
document.getElementById('btn-cargar')?.addEventListener('click', cargarVehiculos);
document.getElementById('filtro')?.addEventListener('input', e=> filtrar(e.target.value));
document.addEventListener('click', (e)=>{ if (e.target?.classList?.contains('del')) eliminarVehiculo(e.target.dataset.id); });

// API pública para app.js
window.vehiculosUI = { cargarVehiculos, crearVehiculo, filtrar };
