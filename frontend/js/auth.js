// @ts-nocheck
async function login(userInput, password){
  const attempts = [
    { username: userInput, password }, // username clásico
    { email: userInput,    password }, // USERNAME_FIELD=email
  ];
  let lastErr;
  for (const body of attempts) {
    try {
      const data = await http.post('/token/', body); // {access, refresh}
      http.setTokens(data);
      return data;
    } catch (e) { lastErr = e; }
  }
  throw lastErr;
}
async function refresh(){
  const refresh = localStorage.getItem('REFRESH');
  if (!refresh) throw new Error('No refresh token');
  const data = await http.post('/token/refresh/', { refresh });
  http.setTokens({ access: data.access });
  return data;
}
function logout(){
  http.setTokens({ access:'', refresh:'' });
  localStorage.removeItem('ACCESS'); localStorage.removeItem('REFRESH');
}
window.auth = { login, refresh, logout };
