import { showToast } from "/static/js/toast.js";

function getCookie(name){
  const m = document.cookie.match('(^|;)\\s*'+name+'=\\s*([^;]+)');
  return m ? m.pop() : '';
}
const CSRF = getCookie('csrftoken');

async function postJSON(url, body){
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken': CSRF,
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: JSON.stringify(body)
  });
  const json = await res.json().catch(()=>({ok:false,error:'Invalid JSON'}));
  if (!res.ok || json.ok === false) throw new Error(json.error || `HTTP ${res.status}`);
  return json;
}

// LOGIN
const loginForm = document.getElementById('login-form');
if (loginForm){
  loginForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(loginForm);
    try{
      await postJSON('/api/auth/login/', Object.fromEntries(fd.entries()));
      showToast('Login berhasil', 'success');
      setTimeout(()=> location.href = '/products/', 600);
    }catch(err){ showToast(err.message, 'error'); }
  });
}

// REGISTER
const regForm = document.getElementById('register-form');
if (regForm){
  regForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(regForm);
    try{
      await postJSON('/api/auth/register/', Object.fromEntries(fd.entries()));
      showToast('Register sukses, silakan login', 'success');
      setTimeout(()=> location.href = '/login/', 600);
    }catch(err){ showToast(err.message, 'error'); }
  });
}

// LOGOUT 
const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn){
  logoutBtn.addEventListener('click', async (e)=>{
    e.preventDefault();
    try{
      await postJSON('/api/auth/logout/', {});
      showToast('Logout berhasil', 'success');
      setTimeout(()=> location.href = '/login/', 600);
    }catch(err){ showToast(err.message, 'error'); }
  });
}
