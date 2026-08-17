const API = "";
let editandoLibroId = null;
let editandoUsuarioId = null;
let libroParaSubirImagen = null;
let usuarioParaSubirFoto = null;

document.querySelectorAll(".pestana").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".pestana").forEach(b => b.classList.remove("activa"));
        document.querySelectorAll(".contenido-tab").forEach(t => t.classList.add("oculto"));
        btn.classList.add("activa");
        document.getElementById("tab-" + btn.dataset.tab).classList.remove("oculto");
    });
});

function mostrarMensaje(texto, esError = false) {
    const el = document.getElementById("mensaje-flotante");
    el.textContent = texto;
    el.classList.remove("oculto", "error");
    if (esError) el.classList.add("error");
    setTimeout(() => el.classList.add("oculto"), 3000);
}

function celdaMiniatura(url, tipo, id) {
    const clase = tipo === "libro" ? "miniatura-libro" : "miniatura-usuario";
    const accion = tipo === "libro" ? "abrir-imagen-libro" : "abrir-foto-usuario";
    if (url) {
        return `<div class="miniatura-contenedor" data-accion="${accion}" data-id="${id}">
                    <img src="${url}" class="${clase}">
                </div>`;
    }
    const texto = tipo === "libro" ? "Sin portada" : "Sin foto";
    return `<div class="miniatura-contenedor" data-accion="${accion}" data-id="${id}">
                <div class="miniatura-vacia ${clase}">${texto}</div>
            </div>`;
}

// ---------- LIBROS ----------
async function cargarLibros(filtro = "") {
    const url = filtro ? `${API}/libros/?q=${encodeURIComponent(filtro)}` : `${API}/libros/`;
    const respuesta = await fetch(url);
    const libros = await respuesta.json();
    const tbody = document.querySelector("#tabla-libros tbody");
    tbody.innerHTML = "";
    libros.forEach(libro => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${celdaMiniatura(libro.imagen, "libro", libro.id)}</td>
            <td>${libro.titulo}</td>
            <td>${libro.autor}</td>
            <td>${libro.categoria || "-"}</td>
            <td>${libro.stock}</td>
            <td>${libro.disponible ? "Si" : "No"}</td>
            <td>
                <button class="accion-btn accion-editar" data-id="${libro.id}">Editar</button>
                <button class="accion-btn accion-eliminar" data-id="${libro.id}">Eliminar</button>
            </td>`;
        tbody.appendChild(fila);
    });
    await cargarSelectLibros(libros);
}

document.getElementById("form-libro").addEventListener("submit", async e => {
    e.preventDefault();
    const datos = {
        titulo: document.getElementById("libro-titulo").value,
        autor: document.getElementById("libro-autor").value,
        isbn: document.getElementById("libro-isbn").value,
        categoria: document.getElementById("libro-categoria").value,
        stock: parseInt(document.getElementById("libro-stock").value),
    };
    const metodo = editandoLibroId ? "PUT" : "POST";
    const url = editandoLibroId ? `${API}/libros/${editandoLibroId}` : `${API}/libros/`;
    const respuesta = await fetch(url, { method: metodo, headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) });
    if (respuesta.ok) {
        mostrarMensaje(editandoLibroId ? "Libro actualizado" : "Libro creado. Ahora puedes subirle una portada.");
        document.getElementById("form-libro").reset();
        editandoLibroId = null;
        document.getElementById("btn-cancelar-libro").style.display = "none";
        cargarLibros();
    } else {
        mostrarMensaje("Error al guardar el libro", true);
    }
});

document.getElementById("btn-cancelar-libro").addEventListener("click", () => {
    editandoLibroId = null;
    document.getElementById("form-libro").reset();
    document.getElementById("btn-cancelar-libro").style.display = "none";
});

document.querySelector("#tabla-libros tbody").addEventListener("click", async e => {
    const contenedor = e.target.closest("[data-accion='abrir-imagen-libro']");
    if (contenedor) {
        libroParaSubirImagen = contenedor.dataset.id;
        document.getElementById("input-imagen-libro").click();
        return;
    }
    const id = e.target.dataset.id;
    if (!id) return;
    if (e.target.classList.contains("accion-eliminar")) {
        if (confirm("Eliminar este libro?")) {
            await fetch(`${API}/libros/${id}`, { method: "DELETE" });
            mostrarMensaje("Libro eliminado");
            cargarLibros();
        }
    }
    if (e.target.classList.contains("accion-editar")) {
        const respuesta = await fetch(`${API}/libros/${id}`);
        const libro = await respuesta.json();
        document.getElementById("libro-titulo").value = libro.titulo;
        document.getElementById("libro-autor").value = libro.autor;
        document.getElementById("libro-isbn").value = libro.isbn;
        document.getElementById("libro-categoria").value = libro.categoria || "";
        document.getElementById("libro-stock").value = libro.stock;
        editandoLibroId = id;
        document.getElementById("btn-cancelar-libro").style.display = "inline-block";
    }
});

document.getElementById("input-imagen-libro").addEventListener("change", async e => {
    const archivo = e.target.files[0];
    if (!archivo || !libroParaSubirImagen) return;
    const formData = new FormData();
    formData.append("archivo", archivo);
    const respuesta = await fetch(`${API}/libros/${libroParaSubirImagen}/imagen`, { method: "POST", body: formData });
    if (respuesta.ok) {
        mostrarMensaje("Portada actualizada");
        cargarLibros();
    } else {
        mostrarMensaje("Error al subir la portada", true);
    }
    e.target.value = "";
    libroParaSubirImagen = null;
});

document.getElementById("buscar-libro").addEventListener("input", e => cargarLibros(e.target.value));

// ---------- USUARIOS ----------
async function cargarUsuarios() {
    const respuesta = await fetch(`${API}/usuarios/`);
    const usuarios = await respuesta.json();
    const tbody = document.querySelector("#tabla-usuarios tbody");
    tbody.innerHTML = "";
    usuarios.forEach(u => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${celdaMiniatura(u.foto, "usuario", u.id)}</td>
            <td>${u.nombre}</td>
            <td>${u.correo}</td>
            <td>${u.telefono || "-"}</td>
            <td>
                <button class="accion-btn accion-editar" data-id="${u.id}">Editar</button>
                <button class="accion-btn accion-eliminar" data-id="${u.id}">Eliminar</button>
            </td>`;
        tbody.appendChild(fila);
    });
    await cargarSelectUsuarios(usuarios);
}

document.getElementById("form-usuario").addEventListener("submit", async e => {
    e.preventDefault();
    const datos = {
        nombre: document.getElementById("usuario-nombre").value,
        correo: document.getElementById("usuario-correo").value,
        telefono: document.getElementById("usuario-telefono").value,
    };
    const metodo = editandoUsuarioId ? "PUT" : "POST";
    const url = editandoUsuarioId ? `${API}/usuarios/${editandoUsuarioId}` : `${API}/usuarios/`;
    const respuesta = await fetch(url, { method: metodo, headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) });
    if (respuesta.ok) {
        mostrarMensaje(editandoUsuarioId ? "Usuario actualizado" : "Usuario creado. Ahora puedes subirle una foto.");
        document.getElementById("form-usuario").reset();
        editandoUsuarioId = null;
        document.getElementById("btn-cancelar-usuario").style.display = "none";
        cargarUsuarios();
    } else {
        mostrarMensaje("Error al guardar el usuario", true);
    }
});

document.getElementById("btn-cancelar-usuario").addEventListener("click", () => {
    editandoUsuarioId = null;
    document.getElementById("form-usuario").reset();
    document.getElementById("btn-cancelar-usuario").style.display = "none";
});

document.querySelector("#tabla-usuarios tbody").addEventListener("click", async e => {
    const contenedor = e.target.closest("[data-accion='abrir-foto-usuario']");
    if (contenedor) {
        usuarioParaSubirFoto = contenedor.dataset.id;
        document.getElementById("input-foto-usuario").click();
        return;
    }
    const id = e.target.dataset.id;
    if (!id) return;
    if (e.target.classList.contains("accion-eliminar")) {
        if (confirm("Eliminar este usuario?")) {
            await fetch(`${API}/usuarios/${id}`, { method: "DELETE" });
            mostrarMensaje("Usuario eliminado");
            cargarUsuarios();
        }
    }
    if (e.target.classList.contains("accion-editar")) {
        const respuesta = await fetch(`${API}/usuarios/${id}`);
        const usuario = await respuesta.json();
        document.getElementById("usuario-nombre").value = usuario.nombre;
        document.getElementById("usuario-correo").value = usuario.correo;
        document.getElementById("usuario-telefono").value = usuario.telefono || "";
        editandoUsuarioId = id;
        document.getElementById("btn-cancelar-usuario").style.display = "inline-block";
    }
});

document.getElementById("input-foto-usuario").addEventListener("change", async e => {
    const archivo = e.target.files[0];
    if (!archivo || !usuarioParaSubirFoto) return;
    const formData = new FormData();
    formData.append("archivo", archivo);
    const respuesta = await fetch(`${API}/usuarios/${usuarioParaSubirFoto}/foto`, { method: "POST", body: formData });
    if (respuesta.ok) {
        mostrarMensaje("Foto de perfil actualizada");
        cargarUsuarios();
    } else {
        mostrarMensaje("Error al subir la foto", true);
    }
    e.target.value = "";
    usuarioParaSubirFoto = null;
});

// ---------- PRESTAMOS ----------
async function cargarSelectLibros(libros) {
    const select = document.getElementById("prestamo-libro");
    select.innerHTML = "";
    libros.filter(l => l.stock > 0).forEach(l => {
        const opcion = document.createElement("option");
        opcion.value = l.id;
        opcion.textContent = `${l.titulo} (stock: ${l.stock})`;
        select.appendChild(opcion);
    });
}

async function cargarSelectUsuarios(usuarios) {
    const select = document.getElementById("prestamo-usuario");
    select.innerHTML = "";
    usuarios.forEach(u => {
        const opcion = document.createElement("option");
        opcion.value = u.id;
        opcion.textContent = u.nombre;
        select.appendChild(opcion);
    });
}

async function cargarPrestamosActivos() {
    const respuesta = await fetch(`${API}/prestamos/activos`);
    const prestamos = await respuesta.json();
    const tbody = document.querySelector("#tabla-prestamos tbody");
    tbody.innerHTML = "";
    for (const p of prestamos) {
        const libro = await (await fetch(`${API}/libros/${p.libro_id}`)).json();
        const usuario = await (await fetch(`${API}/usuarios/${p.usuario_id}`)).json();
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${libro.titulo}</td>
            <td>${usuario.nombre}</td>
            <td>${new Date(p.fecha_prestamo).toLocaleString()}</td>
            <td><button class="accion-btn accion-devolver" data-id="${p.id}">Marcar devuelto</button></td>`;
        tbody.appendChild(fila);
    }
}

document.getElementById("form-prestamo").addEventListener("submit", async e => {
    e.preventDefault();
    const datos = {
        libro_id: parseInt(document.getElementById("prestamo-libro").value),
        usuario_id: parseInt(document.getElementById("prestamo-usuario").value),
    };
    const respuesta = await fetch(`${API}/prestamos/`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) });
    if (respuesta.ok) {
        mostrarMensaje("Prestamo registrado");
        cargarLibros();
        cargarPrestamosActivos();
    } else {
        const error = await respuesta.json();
        mostrarMensaje(error.detail || "Error al registrar el prestamo", true);
    }
});

document.querySelector("#tabla-prestamos tbody").addEventListener("click", async e => {
    const id = e.target.dataset.id;
    if (!id || !e.target.classList.contains("accion-devolver")) return;
    await fetch(`${API}/prestamos/${id}/devolver`, { method: "PUT" });
    mostrarMensaje("Devolucion registrada");
    cargarLibros();
    cargarPrestamosActivos();
});

// ---------- INICIALIZACION ----------
cargarLibros();
cargarUsuarios();
cargarPrestamosActivos();
