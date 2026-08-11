import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crear_libro():
    respuesta = client.post("/libros/", json={
        "titulo": "1984", "autor": "George Orwell", "isbn": "978-0451524935",
        "categoria": "Distopia", "stock": 2
    })
    assert respuesta.status_code == 201
    assert respuesta.json()["disponible"] is True


def test_listar_libros():
    respuesta = client.get("/libros/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def test_buscar_libro_por_titulo():
    client.post("/libros/", json={
        "titulo": "Rayuela", "autor": "Julio Cortazar", "isbn": "978-8437604572",
        "categoria": "Novela", "stock": 1
    })
    respuesta = client.get("/libros/?q=Rayuela")
    assert respuesta.status_code == 200
    assert any(l["titulo"] == "Rayuela" for l in respuesta.json())


def test_crear_usuario():
    respuesta = client.post("/usuarios/", json={
        "nombre": "Deury De La Cruz", "correo": "deury@itla.edu.do", "telefono": "8091234567"
    })
    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "Deury De La Cruz"


def test_flujo_prestamo_y_devolucion():
    libro = client.post("/libros/", json={
        "titulo": "El Quijote", "autor": "Cervantes", "isbn": "978-8420412146",
        "categoria": "Clasico", "stock": 1
    }).json()
    usuario = client.post("/usuarios/", json={
        "nombre": "Usuario Prueba", "correo": "prueba@itla.edu.do", "telefono": "8090000000"
    }).json()

    prestamo = client.post("/prestamos/", json={
        "libro_id": libro["id"], "usuario_id": usuario["id"]
    })
    assert prestamo.status_code == 201
    assert prestamo.json()["devuelto"] is False

    libro_actualizado = client.get(f"/libros/{libro['id']}").json()
    assert libro_actualizado["stock"] == 0
    assert libro_actualizado["disponible"] is False

    devolucion = client.put(f"/prestamos/{prestamo.json()['id']}/devolver")
    assert devolucion.status_code == 200
    assert devolucion.json()["devuelto"] is True

    libro_final = client.get(f"/libros/{libro['id']}").json()
    assert libro_final["stock"] == 1


def test_prestamo_sin_stock_falla():
    libro = client.post("/libros/", json={
        "titulo": "Sin Stock", "autor": "Autor X", "isbn": "978-0000000001",
        "categoria": "Prueba", "stock": 0
    }).json()
    usuario = client.post("/usuarios/", json={
        "nombre": "Usuario Sin Stock", "correo": "sinstock@itla.edu.do", "telefono": "8090000001"
    }).json()

    respuesta = client.post("/prestamos/", json={
        "libro_id": libro["id"], "usuario_id": usuario["id"]
    })
    assert respuesta.status_code == 409
