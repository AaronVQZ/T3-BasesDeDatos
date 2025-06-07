// empleado.js

// Función para leer la cookie CSRF (Django la pone en 'csrftoken')
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
      }
    });
  }
  return cookieValue;
}

async function fetchPlanilla(url) {
  console.log("[JS] fetchPlanilla -> URL:", url);
  const csrftoken = getCookie('csrftoken');
  console.log("[JS] fetchPlanilla -> csrftoken:", csrftoken);

  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({})  // No necesita otros datos
    });
    console.log("[JS] fetchPlanilla -> status HTTP:", resp.status);

    const json = await resp.json();
    console.log("[JS] fetchPlanilla -> respuesta JSON:", json);

    if (json.success) {
      console.log("[JS] fetchPlanilla -> datos recibidos:", json.data);
      renderResultado(json.data);
    } else {
      console.error("[JS] fetchPlanilla -> error de negocio:", json.message);
      alert(json.message || 'Error al consultar planilla');
    }
  } catch (err) {
    console.error("[JS] fetchPlanilla -> excepción en fetch:", err);
    alert('No se pudo conectar al servidor');
  }
}

function renderResultado(data) {
  console.log("[JS] renderResultado -> empezando renderizado");
  const cont = document.getElementById('resultado');
  cont.innerHTML = '';

  if (!data.length) {
    console.log("[JS] renderResultado -> no hay datos");
    cont.textContent = 'No hay registros para mostrar.';
    return;
  }

  const table = document.createElement('table');
  table.classList.add('tabla');

  // Cabecera
  console.log("[JS] renderResultado -> columnas:", Object.keys(data[0]));
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  Object.keys(data[0]).forEach(col => {
    const th = document.createElement('th');
    th.textContent = col;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Cuerpo
  const tbody = document.createElement('tbody');
  data.forEach(row => {
    const tr = document.createElement('tr');
    Object.values(row).forEach(val => {
      const td = document.createElement('td');
      td.textContent = val;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  cont.appendChild(table);
  console.log("[JS] renderResultado -> tabla inyectada");
}

// Asocia eventos al cargar el DOM
document.addEventListener('DOMContentLoaded', () => {
  console.log("[JS] DOMContentLoaded -> asignando handlers");
  document
    .getElementById('btn_planilla_semanal')
    .addEventListener('click', () => {
      const url = document.getElementById('btn_planilla_semanal').dataset.url;
      fetchPlanilla(url);
    });

  document
    .getElementById('btn_planilla_mensual')
    .addEventListener('click', () => {
      const url = document.getElementById('btn_planilla_mensual').dataset.url;
      fetchPlanilla(url);
    });
});
