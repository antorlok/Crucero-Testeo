// script-frontend.js: Código original de /static/js/script.js

let materiales = [];
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
    document.getElementById('materiales-json').value = JSON.stringify(materiales);
}
function devolverDashboard() {
    document.getElementById('proveedores-content').style.display = 'none';
    document.getElementById('compras-content').style.display = 'block';
    document.querySelector('.page-title').textContent = 'Compras';
    document.querySelector('.page-subtitle').textContent = 'Gestión de compras, proveedores y solicitudes';
}
// AJAX para enviar el formulario de proveedores y actualizar la tabla
function actualizarTablaProveedores(proveedores) {
    const tbody = document.getElementById('proveedores-table-body');
    tbody.innerHTML = '';
    proveedores.forEach(prov => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${prov.name}</td>
            <td>${prov.service_or_product}</td>
            <td>${prov.categorie}</td>
            <td>${prov.contact}</td>
            <td>${prov.countries}</td>
            <td>${prov.sucursal}</td>
            <td>${prov.materiales.join(', ')}</td>
        `;
        tbody.appendChild(tr);
    });
}
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('proveedor-form');
    if(form) {
        form.onsubmit = function(e) {
            e.preventDefault();
            document.getElementById('materiales-json').value = JSON.stringify(materiales);
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
                    updateMaterialList();
                    actualizarTablaProveedores(data.proveedores);
                } else {
                    alert('Error al registrar proveedor');
                }
            })
            .catch(() => alert('Error de red o del servidor.'));
        };
    }
});
