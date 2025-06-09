document.addEventListener('DOMContentLoaded', function() {
//------------------------------------------------------------------------------------------------------------------------
    // Inicialización de variables y elementos del DOM
    const searchInput  = document.getElementById('search-bar');
    const searchButton = document.getElementById('search-button');
    const tabla        = document.getElementById('tabla_empleados');
    
    

    

//-------------------------------------------------------------------------------------------------------------------------
    // Función para actualizar la tabla con los empleados
    function actualizarTabla(empleados) {
        // Envabezado de la Tabla
        let tableContent = `
            <tr class="encabezado">
                <th>Nombre</th>
                <th>Puesto</th>
                <th>Acciones</th>
            </tr>
        `;

        // Construye la tabla fila por fila con cada empleado
        empleados.forEach(empleado => {
            tableContent += `
                <tr>
                    <td>${empleado.nombre}</td>
                    <td>${empleado.puesto}</td>
                    <td class="acciones">
                        <button class="boton_consultar" onclick="consultarEmpleado('${empleado.id}')">
                            Consultar
                        </button>
                        <button class="boton_modificar" onclick="modificarEmpleado('${empleado.id}')">
                            Modificar
                        </button>
                        <button class="boton_borrar" onclick="borrarEmpleado('${empleado.identificacion}', '${empleado.nombre}')">
                            Borrar
                        </button>
                        <button class="boton_movimientos" onclick="verMovimientos('${empleado.identificacion}','${empleado.nombre}')">Movimientos
                        </button>
                    </td>
                </tr>
            `;
        });
        tabla.innerHTML = tableContent;
    }

//------------------------------------------------------------------------------------------------------------------------
    // Funcion para validar que el término de búsqueda solo contenga letras o números
    function validarTermino(termino) {
        const soloLetras   = /^[a-záéíóúñA-ZÁÉÍÓÚÑ\s]+$/;
        const soloNumeros  = /^[0-9]+$/;

        if (!termino) return { valido: true };
        if (!soloLetras.test(termino) && !soloNumeros.test(termino)) {
            return { valido: false, mensaje: 'El término de búsqueda solo puede contener letras o números.' };
        }
        return { valido: true};
    }

//------------------------------------------------------------------------------------------------------------------------
    // Eventos de búsqueda
    searchButton.addEventListener('click', buscar);
    searchInput.addEventListener('keyup', e => { if (e.key === 'Enter') buscar(); });

    function buscar() {
        const term = searchInput.value.trim();
        const v    = validarTermino(term);
        if (!v.valido) {
            tabla.innerHTML = `<tr><td colspan="3">${v.mensaje}</td></tr>`;
            return;
        }
        fetchEmpleados(term);
    }

//------------------------------------------------------------------------------------------------------------------------
    // Funcion para hacer la peticion AJAX para buscar empleados
    function fetchEmpleados(term) {
        tabla.innerHTML = '<tr><td colspan="3">Buscando...</td></tr>';
        fetch(`buscar_empleados/?term=${encodeURIComponent(term)}`, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => {
            if (!r.ok) throw new Error(`Error del servidor: ${r.status}`);
            return r.json();
        })
        .then(data => {
            if (data.success && Array.isArray(data.empleados)) {
                if (data.empleados.length === 0) {
                    tabla.innerHTML = '<tr><td colspan="3">No hubo coincidencias</td></tr>';
                } else {
                    actualizarTabla(data.empleados);
                }
            } else {
                throw new Error('Formato de respuesta inválido');
            }
        })
        .catch(err => {
            console.error('Error en la búsqueda:', err);
            tabla.innerHTML = `<tr><td colspan="3">Error: ${err.message}</td></tr>`;
        });
    }
    
    
    //------------------------------------------------------------------------------------------------------------------------
    // Modal de Inserción para Agregar un nuevo empleado
    
    //Botones y fomrulario del modal
    const btnAgregar = document.getElementById('boton_agregar');
    const modalIns   = document.getElementById('modalInsertarEmpleado');
    const spanCerrar = modalIns.querySelector('.cerrar');
    const formIns    = document.getElementById('formInsertarEmpleado');
    
    // Mostrar el modal al hacer clic en el botón "Agregar"
    btnAgregar.addEventListener('click', () => {
        formIns.reset();
        modalIns.style.display = 'flex';
    });

    // Cerrar el modal al hacer clic en la "X" o fuera del modal
    spanCerrar.addEventListener('click', () => modalIns.style.display = 'none');
    window.addEventListener('click', e => { if (e.target === modalIns) modalIns.style.display = 'none'; });
    
    formIns.addEventListener('submit', e => {
        e.preventDefault();
        fetch('insertar_empleado/', {
            method: 'POST',
            body: new FormData(formIns),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: '¡Éxito!',
                    text: 'El Empleado ha sido agregado correctamente',
                    timer: 2000,
                    showConfirmButton: false,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }
                }).then(() => {
                    location.reload();
                });
            }
        })
        .catch(console.error);
    });

//------------------------------------------------------------------------------------------------------------------------
    // Modal de Consulta para ver información de un empleado
    window.consultarEmpleado = function(id) {
        fetch(`consultar_empleado/?id_empleado=${encodeURIComponent(id)}`, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const emp = data.empleado;
                document.getElementById('info-nombre').textContent        = emp.nombre;
                document.getElementById('info-identificacion').textContent = emp.valorDocumento;
                document.getElementById('info-fecha-nacimiento').textContent = emp.fechaNacimiento;
                document.getElementById('info-puesto').textContent        = emp.puesto;
                document.getElementById('info-departamento').textContent  = emp.departamento;
                document.getElementById('modalConsultarEmpleado').style.display = 'flex';
            } else {
                alert(data.error || 'Error al obtener información');
            }
        })
        .catch(err => { console.error(err); alert('Error de conexión'); });
    };    const spanCerrarConsultar = document.querySelector('.cerrar-consultar');
    const modalConsultar = document.getElementById('modalConsultarEmpleado');
    
    spanCerrarConsultar.addEventListener('click', () => modalConsultar.style.display = 'none');
    window.addEventListener('click', e => {
        if (e.target === modalConsultar) modalConsultar.style.display = 'none';
    });

//------------------------------------------------------------------------------------------------------------------------
    // Modal Borrar. Para borardo logico de un empleado
    window.borrarEmpleado = function(id, nombre) {
        // Mostrar el modal de confirmación de borrado
        document.getElementById('borrar-identificacion').textContent = id;
        document.getElementById('borrar-nombre').textContent         = nombre;
        document.getElementById('modalBorrarEmpleado').style.display = 'flex';
    };
    const spanCerrarBorrar = document.querySelector('.cerrar-borrar');
    const modalBorrar = document.getElementById('modalBorrarEmpleado');
    
    spanCerrarBorrar.addEventListener('click', () => modalBorrar.style.display = 'none');
    window.addEventListener('click', e => {
        if (e.target === modalBorrar) modalBorrar.style.display = 'none';
    });

    const csrfToken = getCookie('csrftoken');

    //Botones de confirmación y cancelación del modal de borrado
    document.getElementById('cancelar-borrar').addEventListener('click', () => enviarBorrado(0));
    document.getElementById('confirmar-borrar').addEventListener('click', () => enviarBorrado(1));

    // Función para enviar la solicitud de borrado
    function enviarBorrado(confirmar) {
        const id = document.getElementById('borrar-identificacion').textContent;
        const fd = new FormData();
        fd.append('identificacion', id);
        fd.append('confirmar', confirmar);
        fetch('borrar-empleado/', {
            method: 'POST',
            body: fd,
            credentials: 'same-origin',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(r => r.json())
        .then(data => { 
            if (confirmar) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Eliminado',
                    text: 'Los datos del empleado han sido eliminados del sistema',
                    timer: 2000,
                    showConfirmButton: false,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }
                }).then(() => {
                    location.reload();
                });
            }
                
        })
        .catch(err => { console.error(err); alert('Error de conexión'); })
        .finally(() => document.getElementById('modalBorrarEmpleado').style.display = 'none');
    }

    //------------------------------------------------------------------------------------------------------------------------
    // Modal Modificar
    window.modificarEmpleado = function(id) {
        fetch(`consultar_empleado/?id_empleado=${encodeURIComponent(id)}`, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.json())
        .then(data => {
            if (!data.success) return alert(data.error || 'Empleado no encontrado');
            const emp = data.empleado;
            document.getElementById('E-id-empleado').value        = id;
            document.getElementById('E-nombre').placeholder        = emp.nombre;
            document.getElementById('E-identificacion').placeholder = emp.valorDocumento;
            document.getElementById('modalModificarEmpleado').style.display = 'flex';
        })
        .catch(err => { console.error(err); alert('Error de conexión'); });
    };    const spanCerrarModificar = document.querySelector('.cerrar-modificar');
    const modalModificar = document.getElementById('modalModificarEmpleado');
    
    spanCerrarModificar.addEventListener('click', () => modalModificar.style.display = 'none');
    window.addEventListener('click', e => {
        if (e.target === modalModificar) modalModificar.style.display = 'none';
        if (e.target === modalIns) modalIns.style.display = 'none';
    });

    document.getElementById('formModificarEmpleado').addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('editar_empleado/', {
            method: 'POST',
            body: new FormData(this),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.json())
        .then(data => { 
            if (data.success) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: '¡Éxito!',
                    text: 'Los datos del empleado han sido actualizados',
                    timer: 2000,
                    showConfirmButton: false,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }
                }).then(() => {
                    location.reload();
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '¡Error!',
                    text: data.error || 'Error al actualizar empleado',
                    timer: 2000,
                    showConfirmButton: false
                });
            }
        })     
    });

    //------------------------------------------------------------------------------------------------------------------------
    // Helper para CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                const [key, val] = cookie.trim().split('=');
                if (key === name) cookieValue = decodeURIComponent(val);
            });
        }
        return cookieValue;
    }


});
//comentario
function verMovimientos(identificacion, nombre) {
    window.open(
    //window.location.href = `/home/movimientos/${identificacion}?nombre=${encodeURIComponent(nombre)}`;
    `/home/movimientos/${identificacion}?nombre=${encodeURIComponent(nombre)}`,
    'movimientos', // Nombre de la ventana
    );
    

}

// Control de visibilidad de campos de empleado
const tipoUsuario = document.getElementById('tipo_usuario');
const camposEmpleado = document.getElementById('campos_empleado');
const idPuesto = document.getElementById('id_puesto');
const idDepartamento = document.getElementById('id_departamento');
const formInsertarEmpleado = document.getElementById('formInsertarEmpleado');

if (tipoUsuario) {
    tipoUsuario.addEventListener('change', function() {
        const esEmpleado = this.value === '2';
        camposEmpleado.style.display = esEmpleado ? 'block' : 'none';
        
        // Solo hacer los campos requeridos si es empleado
        if (esEmpleado) {
            idPuesto.setAttribute('required', '');
            idDepartamento.setAttribute('required', '');
        } else {
            idPuesto.removeAttribute('required');
            idDepartamento.removeAttribute('required');
            // Limpiar los valores cuando no son requeridos
            idPuesto.value = '';
            idDepartamento.value = '';
        }
    });
}

// Validación del formulario
if (formInsertarEmpleado) {
    formInsertarEmpleado.addEventListener('submit', function(e) {
        if (tipoUsuario.value === '2') {
            if (!idPuesto.value || !idDepartamento.value) {
                e.preventDefault();
                alert('Por favor complete todos los campos requeridos');
            }
        }
    });
}
