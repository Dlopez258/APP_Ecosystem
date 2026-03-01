# Eje 2: Arquitectura de Software - Fundación Universitaria del Area Andina 

Integrantes:
- Diego Andrés Lopez Rodriguez
- Juan Danilo Vera Romero
- Luis Alejandro Vargas Vanegas
- Sandrith Natalia Barreto Alfonso



# 🌍 EcoSystem — Plataforma de Gestión de Residuos Electrónicos (RAEE)

Aplicación web desarrollada en **Python + Flask** que conecta ciudadanos, empresas y gobiernos para facilitar la recolección responsable de e-waste (RAEE) mediante puntos de acopio, gamificación y trazabilidad blockchain.

---

## 🚀 Instalación y ejecución

> ⚠️ **Requisito previo:** Tener instalado [Python 3.10+](https://www.python.org/downloads/)

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Eje2_ArquitecturaSoftware
```

### 2. Crear el entorno virtual
El entorno virtual **no se sube a GitHub**, por eso debes crearlo en tu máquina:
```bash
# Windows
python -m venv .venv

# Linux / Mac
python3 -m venv .venv
```

### 3. Activar el entorno virtual
```bash
# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```
> Sabrás que está activo porque verás `(.venv)` al inicio de tu terminal.

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```
> Para desarrollo local con SQLite **no necesitas cambiar nada**. El `.env` ya viene preconfigurado para funcionar sin MySQL.

### 6. Inicializar la base de datos
```bash
python init_db.py
```
> Esto crea automáticamente el archivo `ecosystem_dev.db` con todas las tablas necesarias.

### 7. Ejecutar la aplicación
```bash
python run.py
```
Abre tu navegador en: **http://localhost:5000**

---

## 🧪 Ejecutar tests
```bash
pytest tests/ -v
```

---

## 📁 Estructura del proyecto

```
Eje2_ArquitecturaSoftware/
├── app/
│   ├── __init__.py          # Factory de la app (create_app)
│   ├── models/              # Modelos SQLAlchemy
│   ├── controllers/         # Controladores y rutas (Blueprints)
│   ├── views/               # Templates Jinja2
│   ├── dao/                 # Data Access Objects (acceso a BD)
│   ├── dto/                 # Data Transfer Objects
│   ├── services/            # Servicios (Blockchain, Gamificación)
│   └── static/              # CSS, JS, imágenes
├── tests/                   # Tests con pytest
├── config.py                # Configuración por entorno
├── run.py                   # Punto de entrada
└── requirements.txt
```

---

## 👥 Roles de usuario

| Rol        | Descripción                                              |
|------------|----------------------------------------------------------|
| Ciudadano  | Registra dispositivos y hace entregas. Gana puntos.      |
| Empresa    | Gestiona puntos de recolección. Hace entregas.           |
| Gobierno   | Accede al dashboard estadístico. Administra el sistema.  |

---

## ⛓️ Blockchain simulado

Cada entrega genera un bloque con hash SHA-256 que encadena todos los registros. Se puede explorar y verificar la integridad en `/blockchain`.

---

## 🏆 Sistema de puntos

| Dispositivo      | Puntos |
|------------------|--------|
| Computador       | 100    |
| Electrodoméstico | 80     |
| Celular          | 50     |
| Tarjeta madre    | 40     |
| Batería          | 30     |
| Otro             | 20     |

