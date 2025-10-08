// --- Toast helper (global) ---
var showToast = (window && window.showToast) ? window.showToast : function (msg, type) {
  alert((type ? '[' + String(type).toUpperCase() + '] ' : '') + msg);
};

// --- CSRF helper ---
function getCookie(name){
  var m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}
var CSRF = getCookie('csrftoken');

// --- Fetch wrapper ---
function api(url, opts){
  opts = opts || {};
  var method = opts.method || 'GET';
  var headers = { 'X-Requested-With': 'XMLHttpRequest' };
  if (method !== 'GET') {
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = CSRF;
  }
  var fetchOpts = { method: method, headers: headers };
  if (opts.body) fetchOpts.body = JSON.stringify(opts.body);

  return fetch(url, fetchOpts).then(function(res){
    return res.json().catch(function(){ return { ok:false, error:'Invalid JSON' }; })
      .then(function(json){ if(!res.ok || json.ok===false) throw new Error(json.error || ('HTTP '+res.status)); return json; });
  });
}

function buildUrl(base, params){
  params = params || {};
  var q = [];
  for (var k in params){
    var v = params[k];
    if (v !== undefined && v !== null && String(v).trim() !== '') {
      q.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
    }
  }
  return base + (q.length ? '?' + q.join('&') : '');
}

var elList      = document.getElementById('product-list');
var elLoading   = document.getElementById('state-loading');
var elEmpty     = document.getElementById('state-empty');
var elError     = document.getElementById('state-error');
var modalRoot   = document.getElementById('modal-root');

var filterForm  = document.getElementById('filter-form');
var filterClear = document.getElementById('filter-clear');
var filterInput = filterForm ? filterForm.querySelector('input[name="category"]') : null;

// --- state filter ---
var currentFilter = { category: '' };

(function(){
  var params = new URLSearchParams(location.search);
  var cat = params.get('category') || '';
  if (cat) {
    currentFilter.category = cat;
    if (filterInput) filterInput.value = cat;
  }
})();

function showState(opts){
  opts = opts || {};
  var loading = !!opts.loading, empty = !!opts.empty, error = opts.error || '';
  if (elLoading) elLoading.classList.toggle('hidden', !loading);
  if (elEmpty)   elEmpty.classList.toggle('hidden', !empty);
  if (elError) {
    elError.classList.toggle('hidden', !error);
    elError.textContent = error || '';
  }
}

// --- Modal helpers ---
function openModal(innerHTML){
  var node = document.createElement('div');
  node.className = 'backdrop';
  node.innerHTML = '<div class="modal">' + innerHTML + '</div>';
  node.addEventListener('click', function(e){ if(e.target===node) node.remove(); });
  modalRoot.appendChild(node);
  return { close: function(){ node.remove(); }, node: node };
}

// --- Card template ---
function cardHTML(p){
  var thumb = p.thumbnail || '/static/image/panda.png';
  var price = (p.price != null ? p.price : 0).toLocaleString('id-ID');
  return ''+
  '<div class="border-2 border-black rounded-md overflow-hidden" data-id="'+p.id+'">'+
    '<a href="/products/'+p.id+'/" class="block">'+
      '<img src="'+thumb+'" alt="'+(p.name||'')+'" class="w-full h-44 object-cover bg-white">'+
    '</a>'+
    '<div class="bg-white border-t-2 border-black p-3">'+
      '<h2 class="font-semibold text-lg text-black">'+(p.name||'')+'</h2>'+
      (p.description ? '<p class="text-sm text-black/80 mt-1">'+p.description+'</p>' : '')+
      '<div class="mt-1 text-sm text-black">'+
        (p.category ? '<span>#'+p.category+'</span>' : '')+
        (p.is_featured ? '<span class="ml-2">• Featured</span>' : '')+
      '</div>'+
      '<div class="mt-1 font-semibold text-black">Rp'+price+'</div>'+
      '<div class="mt-4 flex items-center justify-end gap-4">'+
        '<button class="btn-edit text-[#79B84C] hover:underline">edit</button>'+
        '<button class="btn-del  text-[#79B84C] hover:underline">delete</button>'+
      '</div>'+
    '</div>'+
  '</div>';
}

// --- LIST (with filter) ---
function loadList(params){
  params = params || {};
  currentFilter = Object.assign({}, currentFilter, params);
  showState({loading:true, empty:false, error:''});
  if (elList) elList.innerHTML = '';
  var url = buildUrl('/api/products/', currentFilter);
  api(url).then(function(res){
    var data = res.data || [];
    if(!data.length){
      showState({empty:true});
      var qsEmpty = new URLSearchParams(Object.entries(currentFilter).filter(function(kv){ return kv[1]; })).toString();
      history.replaceState(null, '', qsEmpty ? ('?'+qsEmpty) : location.pathname);
      return;
    }
    showState({});
    if (elList) elList.innerHTML = data.map(cardHTML).join('');
    var qs = new URLSearchParams(Object.entries(currentFilter).filter(function(kv){ return kv[1]; })).toString();
    history.replaceState(null, '', qs ? ('?'+qs) : location.pathname);
  }).catch(function(err){
    showState({error: err && err.message ? err.message : 'Gagal memuat data'});
  }).finally(function(){
    if (elLoading) elLoading.classList.add('hidden');
  });
}

// --- CREATE ---
function openCreateModal(){
  var m = openModal(''+
    '<h3 class="text-lg font-semibold mb-2">Tambah Produk</h3>'+
    '<form id="form-create" class="space-y-2">'+
      '<input class="w-full border rounded p-2" name="name" placeholder="Nama" required>'+
      '<input class="w-full border rounded p-2" name="price" type="number" placeholder="Harga">'+
      '<input class="w-full border rounded p-2" name="thumbnail" placeholder="URL Gambar">'+
      '<input class="w-full border rounded p-2" name="category" placeholder="Kategori">'+
      '<label class="flex items-center gap-2"><input type="checkbox" name="is_featured"> Featured</label>'+
      '<textarea class="w-full border rounded p-2" name="description" placeholder="Deskripsi"></textarea>'+
      '<div class="flex justify-end gap-2 pt-2">'+
        '<button type="button" id="cancel" class="px-3 py-2 rounded border">Batal</button>'+
        '<button class="px-3 py-2 rounded bg-blue-600 text-white">Simpan</button>'+
      '</div>'+
    '</form>'
  );
  m.node.querySelector('#cancel').onclick = m.close;
  m.node.querySelector('#form-create').onsubmit = function(e){
    e.preventDefault();
    var fd = new FormData(e.currentTarget);
    var body = {};
    fd.forEach(function(v,k){ body[k]=v; });
    body.is_featured = !!fd.get('is_featured');
    body.price = Number(body.price||0);
    api('/api/products/', {method:'POST', body:body})
      .then(function(){
        showToast('Produk dibuat','success');
        m.close();
        loadList();
      })
      .catch(function(err){ showToast(err.message,'error'); });
  };
}

// --- EDIT ---
function openEditModal(id){
  api('/api/products/'+id+'/').then(function(resp){
    var p = resp.data;
    var m = openModal(''+
      '<h3 class="text-lg font-semibold mb-2">Edit Produk</h3>'+
      '<form id="form-edit" class="space-y-2">'+
        '<input class="w-full border rounded p-2" name="name" value="'+(p.name||'')+'" required>'+
        '<input class="w-full border rounded p-2" name="price" type="number" value="'+(p.price!=null?p.price:0)+'">'+
        '<input class="w-full border rounded p-2" name="thumbnail" value="'+(p.thumbnail||'')+'">'+
        '<input class="w-full border rounded p-2" name="category" value="'+(p.category||'')+'">'+
        '<label class="flex items-center gap-2"><input type="checkbox" name="is_featured" '+(p.is_featured?'checked':'')+'> Featured</label>'+
        '<textarea class="w-full border rounded p-2" name="description">'+(p.description||'')+'</textarea>'+
        '<div class="flex justify-end gap-2 pt-2">'+
          '<button type="button" id="cancel" class="px-3 py-2 rounded border">Batal</button>'+
          '<button class="px-3 py-2 rounded bg-blue-600 text-white">Update</button>'+
        '</div>'+
      '</form>'
    );
    m.node.querySelector('#cancel').onclick = m.close;
    m.node.querySelector('#form-edit').onsubmit = function(e){
      e.preventDefault();
      var fd = new FormData(e.currentTarget);
      var body = {};
      fd.forEach(function(v,k){ body[k]=v; });
      body.is_featured = !!fd.get('is_featured');
      body.price = Number(body.price||0);
      api('/api/products/'+id+'/', {method:'PUT', body:body})
        .then(function(){
          showToast('Produk diupdate','success');
          m.close();
          loadList();
        })
        .catch(function(err){ showToast(err.message,'error'); });
    };
  }).catch(function(err){ showToast(err.message,'error'); });
}

// --- DELETE ---
function openDeleteConfirm(id){
  var m = openModal(''+
    '<h3 class="text-lg font-semibold mb-2">Hapus Produk?</h3>'+
    '<p class="text-sm text-gray-600">Tindakan ini tidak dapat dibatalkan.</p>'+
    '<div class="flex justify-end gap-2 pt-3">'+
      '<button id="cancel" class="px-3 py-2 rounded border">Batal</button>'+
      '<button id="confirm" class="px-3 py-2 rounded bg-red-600 text-white">Hapus</button>'+
    '</div>'
  );
  m.node.querySelector('#cancel').onclick = m.close;
  m.node.querySelector('#confirm').onclick = function(){
    api('/api/products/'+id+'/', {method:'DELETE'})
      .then(function(){
        showToast('Produk dihapus','success');
        m.close();
        loadList();
      })
      .catch(function(err){ showToast(err.message,'error'); });
  };
}

document.addEventListener('click', function(e){
  var t = e.target;

  // Navbar create (desktop)
  if (t.closest && t.closest('#btn-create-nav')) {
    e.preventDefault();
    openCreateModal();
    return;
  }
  // Navbar create (mobile)
  if (t.closest && t.closest('#btn-create-mobile')) {
    e.preventDefault();
    openCreateModal();
    var mob = document.getElementById('nav-mobile');
    if (mob) mob.classList.add('hidden');
    return;
  }
  // Refresh
  if (t.closest && t.closest('#btn-refresh')) {
    e.preventDefault();
    loadList();
    return;
  }
  // Edit/Delete on cards
  if (t.classList && t.classList.contains('btn-edit')) {
    var cardE = t.closest('[data-id]'); if (!cardE) return;
    openEditModal(cardE.getAttribute('data-id'));
    return;
  }
  if (t.classList && t.classList.contains('btn-del')) {
    var cardD = t.closest('[data-id]'); if (!cardD) return;
    openDeleteConfirm(cardD.getAttribute('data-id'));
    return;
  }
});

// Filter submit (no reload)
if (filterForm) {
  filterForm.addEventListener('submit', function(e){
    e.preventDefault();
    var category = (filterInput && filterInput.value ? filterInput.value : '').trim();
    loadList({ category: category });
  });
}
// Clear filter
if (filterClear) {
  filterClear.addEventListener('click', function(e){
    e.preventDefault();
    if (filterInput) filterInput.value = '';
    loadList({ category: '' });
  });
}

// Initial load
loadList();
