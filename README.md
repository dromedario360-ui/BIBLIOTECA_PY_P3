# Sistema de Gestion de Biblioteca - API REST

Proyecto Final de Programacion III. API REST desarrollada con FastAPI, SQLAlchemy y SQLite, siguiendo Clean Architecture (models, repositories, services, routers).

## Como ejecutar
Luego abre http://127.0.0.1:8000/docs

## Endpoints principales

- **Libros**: CRUD completo + busqueda (`GET /libros/?q=texto`)
- **Usuarios**: CRUD completo
- **Prestamos**: crear prestamo (`POST /prestamos/`) y devolver (`PUT /prestamos/{id}/devolver`)

## Arquitectura

- `models/`: entidades SQLAlchemy
- `repositories/`: interfaces (contratos) + implementacion SQLAlchemy
- `services/`: logica de negocio (ej. no prestar sin stock)
- `routers/`: endpoints FastAPI
- `schemas/`: validacion Pydantic
