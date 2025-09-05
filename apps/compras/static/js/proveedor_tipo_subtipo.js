// Filtrado dinámico de subtipos según el tipo seleccionado
const SUBTIPOS_POR_TIPO = {
    'COMIDA': [
        {value: 'CADUCABLE', text: 'Caducable'},
        {value: 'NO_CADUCABLE', text: 'No caducable'},
        {value: 'REFRIGERADO', text: 'Refrigerado'},
        {value: 'NO_REFRIGERADO', text: 'No refrigerado'},
        {value: 'BEBIDA', text: 'Bebida'},
        {value: 'LICOR', text: 'Licor'}
    ],
    'BIENES': [
        {value: 'REPUESTOS', text: 'Repuestos'},
        {value: 'LIMPIEZA', text: 'Materiales de limpieza'},
        {value: 'MEDICOS', text: 'Materiales médicos'},
        {value: 'ACTIVOS', text: 'Bienes activos'}
    ]
};

document.addEventListener('DOMContentLoaded', function() {
    const tipoSelect = document.getElementById('id_tipo');
    const subtipoSelect = document.getElementById('id_subtipo');
    if (!tipoSelect || !subtipoSelect) return;

    function updateSubtipos() {
        const tipo = tipoSelect.value;
        subtipoSelect.innerHTML = '';
        if (SUBTIPOS_POR_TIPO[tipo]) {
            SUBTIPOS_POR_TIPO[tipo].forEach(function(opt) {
                const option = document.createElement('option');
                option.value = opt.value;
                option.textContent = opt.text;
                subtipoSelect.appendChild(option);
            });
        }
    }
    tipoSelect.addEventListener('change', updateSubtipos);
    updateSubtipos(); // Inicializa al cargar
});
