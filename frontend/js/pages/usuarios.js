// @ts-nocheck

// Render genérico: pinta cabeceras según las llaves del primer item
function renderGeneric(headSel, bodySel, items){
  const body = document.querySelector(bodySel), head = document.querySelector(headSel);
  if (!Array.isArray(items) || !items.length){
    body.innerHTML = `<tr><td colspan="99" class="muted">Sin datos</td></tr>`;
    head.innerHTML = '';
    return;
  }
  const keys = Object.keys(items[0]);
  head.innerHTML = keys.map(k=>`<th>${k}</th>`).join('');
  body.innerHTML = items.map(row =>
    `<tr>${keys.map(k=>`<td>${row[k] ?? ''}</td>`).join('')}</tr>`
  ).join('');
}

async function cargarUsuarios(){
  try{
    const data = await http.get('/usuarios/');
    const rows = Array.isArray(data) ? data : (data?.results || data) || [];
    renderGeneric('#users-head','#users-body', rows);
    toast('Usuarios cargados','success');
  }catch(e){
    toast('Error cargando usuarios','error');
    log('usuarios GET FAIL', e.message);
  }
}

async function crearUsuario(ev){
  ev.preventDefault();
  const fd   = new FormData(ev.target);
  const btn  = document.getElementById('btn-user-crear');
  const orig = btn.textContent;
  btn.disabled = true; btn.textContent = 'Guardando...';

  const errors = document.getElementById('user-errors');
  errors.textContent = '';

  const email     = String(fd.get('email')||'').trim();
  const nombre    = String(fd.get('nombre')||'').trim();
  const role      = String(fd.get('role')||'').trim();
  const password  = String(fd.get('password')||'');
  const password2 = String(fd.get('password2')||'');

  if (password !== password2){
    errors.textContent = 'Las contraseñas no coinciden.';
    btn.disabled = false; btn.textContent = orig;
    return;
  }

  const payload = { email, nombre, role, password };
  // Si tu API exige "username" además del email, descomenta:
  // payload.username = email;

  try{
    await http.post('/usuarios/', payload);
    toast('Usuario creado','success');
    ev.target.reset();
    await cargarUsuarios();
  }catch(e){
    // Mostrar errores del serializer si vienen en JSON
    const msg = String(e.message||'');
    try{
      const json = JSON.parse(msg.replace(/^HTTP \d+: /,''));
      errors.innerHTML = Object.entries(json)
        .map(([k,v])=>`<div>• <b>${k}</b>: ${Array.isArray(v)?v.join(', '):v}</div>`)
        .join('');
    }catch{
      errors.textContent = msg;
    }
    toast('No se pudo crear','error');
    log('usuarios POST FAIL', { error: e.message, payload });
  }finally{
    btn.disabled = false; btn.textContent = orig;
  }
}

document.getElementById('btn-users-cargar')?.addEventListener('click', cargarUsuarios);
document.getElementById('f-user-crear')?.addEventListener('submit', crearUsuario);

// opcionalmente expone utilidades
window.usuariosUI = { cargarUsuarios, crearUsuario };
