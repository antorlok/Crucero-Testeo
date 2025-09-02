// Eliminar proveedor
function agregarEventosEliminarProveedor() {
    document.querySelectorAll('.eliminar-proveedor-btn').forEach(btn => {
        btn.onclick = function() {
            const proveedorId = this.getAttribute('data-id');
            const csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]')?.value;
            if (confirm('¿Seguro que deseas eliminar este proveedor?')) {
                if (!csrftoken) {
                    alert('No se encontró el token CSRF.');
                    return;
                }
                fetch('/proveedores/eliminar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ proveedor_id: proveedorId })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        this.closest('tr').remove();
                    } else {
                        alert('Error al eliminar proveedor: ' + (data.error || 'Error desconocido'));
                    }
                })
                .catch((err) => {
                    alert('Error de red o del servidor.');
                    console.error('Error eliminando proveedor:', err);
                });
            }
        };
    });
}

// --- FUSIÓN DE script.js Y script-frontend.js ---
let paises = [];
let materiales = [];

function addPais() {
    const input = document.getElementById('pais-input');
    const value = input.value.trim();
    if (value && !paises.includes(value)) {
        paises.push(value);
        updatePaisList();
        input.value = '';
    }
}
function removePais(index) {
    paises.splice(index, 1);
    updatePaisList();
}
function updatePaisList() {
    const ul = document.getElementById('pais-list');
    ul.innerHTML = '';
    paises.forEach((pais, idx) => {
        const li = document.createElement('li');
        li.textContent = pais + ' ';
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = 'Eliminar';
        btn.onclick = () => removePais(idx);
        li.appendChild(btn);
        ul.appendChild(li);
    });
    const paisesJson = document.getElementById('paises-json');
    if (paisesJson) paisesJson.value = JSON.stringify(paises);
}

function addMaterial() {
    const input = document.getElementById('material-input');
    const value = input.value.trim();
    if (value && !materiales.includes(value)) {
        materiales.push(value);
        updateMaterialList();
        input.value = '';
    }
}
function removeMaterial(index) {
    materiales.splice(index, 1);
    updateMaterialList();
}
function updateMaterialList() {
    const ul = document.getElementById('material-list');
    ul.innerHTML = '';
    materiales.forEach((mat, idx) => {
        const li = document.createElement('li');
        li.textContent = mat + ' ';
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = 'Eliminar';
        btn.onclick = () => removeMaterial(idx);
        li.appendChild(btn);
        ul.appendChild(li);
    });
    const materialesJson = document.getElementById('materiales-json');
    if (materialesJson) materialesJson.value = JSON.stringify(materiales);
}

function devolverDashboard() {
    const proveedoresContent = document.getElementById('proveedores-content');
    const comprasContent = document.getElementById('compras-content');
    if (proveedoresContent && comprasContent) {
        proveedoresContent.style.display = 'none';
        comprasContent.style.display = 'block';
    }
    const pageTitle = document.querySelector('.page-title');
    const pageSubtitle = document.querySelector('.page-subtitle');
    if (pageTitle) pageTitle.textContent = 'Compras';
    if (pageSubtitle) pageSubtitle.textContent = 'Gestión de compras, proveedores y solicitudes';
}

function actualizarTablaProveedores(proveedores) {
    const tbody = document.getElementById('proveedores-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';
    proveedores.forEach(prov => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${prov.name}</td>
            <td>${prov.service_or_product}</td>
            <td>${prov.categorie}</td>
            <td>${prov.contact}</td>
            <td>${Array.isArray(prov.countries) ? prov.countries.join(', ') : prov.countries}</td>
            <td>${prov.sucursal}</td>
            <td>${Array.isArray(prov.materiales) ? prov.materiales.join(', ') : prov.materiales}</td>
            <td><button type="button" class="eliminar-proveedor-btn" data-id="${prov.id}">Eliminar</button></td>
        `;
        tbody.appendChild(tr);
    });
    agregarEventosEliminarProveedor();
    agregarEventosEliminarProveedor();
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('proveedor-form');
    if(form) {
        form.onsubmit = function(e) {
            e.preventDefault();
            // Actualizar los campos ocultos antes de enviar
            updateMaterialList();
            updatePaisList();
            const formData = new FormData(form);
            fetch('/proveedores/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    form.reset();
                    materiales = [];
                    paises = [];
                    updateMaterialList();
                    updatePaisList();
                    actualizarTablaProveedores(data.proveedores);
                } else {
                    alert('Error al registrar proveedor');
                }
            })
            .catch(() => alert('Error de red o del servidor.'));
        };
    }
    agregarEventosEliminarProveedor();
});
