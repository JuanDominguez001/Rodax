// @ts-nocheck
if (!CONFIG.ACCESS) { window.location.href = 'login.html'; } // guard

const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

function toast(msg,type){ const t=document.createElement('div'); t.className='toast '+(type==='success'?'ok':type==='error'?'err':''); t.textContent=msg; document.body.appendChild(t); setTimeout(()=>t.remove(),2500); }
function log(msg,obj){ const pre=$('#log'); const time=new Date().toLocaleTimeString(); pre.textContent = `[${time}] ${msg}\n` + (obj?JSON.stringify(obj,null,2)+'\n':'') + pre.textContent; }

function chipAuth(isAuth){
  const chip=$('#chip-auth');
  if(isAuth){ chip.className='chip chip--ok'; chip.textContent='Auth: conectado'; }
  else      { chip.className='chip chip--muted'; chip.textContent='Auth: invitado'; }
}
chipAuth(!!CONFIG.ACCESS);

function chipApi(state){
  const chip=$('#chip-api');
  if(state==='ok'){ chip.className='chip chip--ok'; chip.textContent='API: conectada'; }
  else if(state==='err'){ chip.className='chip chip--err'; chip.textContent='API: error'; }
  else { chip.className='chip chip--muted'; chip.textContent='API: desconocida'; }
}

// Ajustes
const dlg = $('#dlg-settings'), inBase = $('#in-base');
$('#btn-settings').onclick = ()=>{ inBase.value = CONFIG.BASE_URL || ''; dlg.showModal(); };
$('#btn-save-base').onclick = (e)=>{ e.preventDefault(); http.setBase(inBase.value.trim()); toast('BASE_URL guardada','success'); };
$('#btn-test').onclick = async ()=>{
  try {
    await http.get('/vehiculos/');     // endpoint real de tu API
    chipApi('ok');
    toast('Conexión OK','success');
  } catch (e) {
    chipApi('err');
    toast('Conexión fallida','error');
    log('Test API FAIL', { error: e.message });
  }
};

if (CONFIG.BASE_URL) $('#btn-test').click();

$('#btn-logout').onclick = ()=>{ auth.logout(); chipAuth(false); toast('Sesión cerrada'); setTimeout(()=>window.location.href='login.html',300); };

// Router simple
function showView(name){
  $$('.nav-link').forEach(a=>a.classList.toggle('active', a.getAttribute('href') === '#/'+name));
  $$('.view').forEach(v=>v.classList.add('hidden'));
  const el = document.querySelector(`[data-view="${name}"]`);
  if (el) el.classList.remove('hidden');

  if (name==='vehiculos') {
    if (!showView._vehFirst) { showView._vehFirst = true; setTimeout(()=> vehiculosUI.cargarVehiculos(), 0); }
  }
}
window.addEventListener('hashchange', ()=> showView(location.hash.replace('#/','') || 'home'));
showView(location.hash.replace('#/','') || 'home');

$('#btn-test-api').onclick = ()=> $('#btn-test').click();
$('#btn-open-settings').onclick = ()=> $('#btn-settings').click();

// expose helpers for pages/*
window.toast = toast; window.log = log;
