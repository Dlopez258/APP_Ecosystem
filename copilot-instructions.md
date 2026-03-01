# 🌍 EcoSystem — Plataforma de Gestión de Residuos Electrónicos (RAEE)

## Descripción General

EcoSystem es una aplicación web desarrollada en **Python con Flask** que conecta a ciudadanos, empresas y gobiernos locales para reducir los residuos de aparatos eléctricos y electrónicos (RAEE): baterías, celulares, computadores, tarjetas madre, electrodomésticos, etc.

**Objetivo:** Facilitar la recolección responsable de e-waste mediante puntos de acopio, gamificación ciudadana, trazabilidad simulada con blockchain y dashboards estadísticos para gobiernos.

---

## Contexto del Desarrollador

- **Nivel de Python:** Básico-Intermedio.
- **Equipo:** Un solo desarrollador.
- **Proyecto universitario** de Ingeniería de Sistemas (7.° semestre).
- **Patrón obligatorio:** MVC (Model-View-Controller).
- Priorizar código **claro, legible y bien comentado en español** por encima de soluciones avanzadas.
- Cuando generes código, **incluye docstrings explicativos** en cada clase y función.

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework web | Flask 3.x |
| Motor de plantillas | Jinja2 (incluido en Flask) |
| Base de datos | MySQL 8.x |
| ORM | SQLAlchemy + Flask-SQLAlchemy |
| Migraciones | Flask-Migrate (Alembic) |
| Formularios | Flask-WTF (WTForms) |
| Autenticación | Flask-Login |
| Hashing de contraseñas | Werkzeug (generate_password_hash / check_password_hash) |
| Frontend | HTML5, CSS3 (Bootstrap 5), JavaScript vanilla |
| Blockchain simulado | Implementación propia en Python puro (hashlib + json) |
| Variables de entorno | python-dotenv |
| Testing | pytest |

---

## Arquitectura — MVC Obligatorio

```
ecosystem/
│
├── app/
│   ├── __init__.py              # Factory de la app Flask (create_app)
│   │
│   ├── models/                  # MODELO — Clases ORM (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── usuario.py           # Modelo Usuario (ciudadano, empresa, gobierno)
│   │   ├── dispositivo.py       # Modelo Dispositivo electrónico
│   │   ├── punto_recoleccion.py # Modelo Punto de recolección / centro de acopio
│   │   ├── entrega.py           # Modelo Entrega (registro de cada entrega de RAEE)
│   │   ├── recompensa.py        # Modelo Recompensa / puntos de gamificación
│   │   └── bloque.py            # Modelo Bloque para blockchain simulado
│   │
│   ├── controllers/             # CONTROLADOR — Lógica de negocio y rutas
│   │   ├── __init__.py
│   │   ├── auth_controller.py   # Registro, login, logout
│   │   ├── usuario_controller.py
│   │   ├── dispositivo_controller.py
│   │   ├── punto_recoleccion_controller.py
│   │   ├── entrega_controller.py
│   │   ├── recompensa_controller.py
│   │   ├── blockchain_controller.py
│   │   └── dashboard_controller.py  # Estadísticas para gobiernos
│   │
│   ├── views/                   # VISTA — Templates Jinja2
│   │   ├── layout/
│   │   │   └── base.html        # Template base con navbar y footer
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── registro.html
│   │   ├── usuario/
│   │   ├── dispositivo/
│   │   ├── punto_recoleccion/
│   │   ├── entrega/
│   │   ├── recompensa/
│   │   ├── blockchain/
│   │   └── dashboard/
│   │
│   ├── static/                  # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   │
│   ├── dto/                     # DTO — Data Transfer Objects
│   │   ├── __init__.py
│   │   ├── usuario_dto.py
│   │   ├── dispositivo_dto.py
│   │   └── entrega_dto.py
│   │
│   ├── dao/                     # DAO — Data Access Objects
│   │   ├── __init__.py
│   │   ├── usuario_dao.py
│   │   ├── dispositivo_dao.py
│   │   ├── punto_recoleccion_dao.py
│   │   ├── entrega_dao.py
│   │   └── recompensa_dao.py
│   │
│   └── services/                # Servicios auxiliares
│       ├── __init__.py
│       ├── blockchain_service.py  # Lógica de la cadena de bloques simulada
│       └── gamificacion_service.py # Lógica de puntos y recompensas
│
├── migrations/                  # Generado por Flask-Migrate
├── tests/                       # Tests con pytest
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_blockchain.py
│
├── .env                         # Variables de entorno (NO subir a Git)
├── .env.example                 # Ejemplo de variables de entorno
├── .gitignore
├── config.py                    # Configuración de la app (dev, prod, test)
├── requirements.txt
├── run.py                       # Punto de entrada de la aplicación
└── README.md
```

### Reglas de la Arquitectura MVC

1. **Modelos (`models/`):** Solo definen la estructura de datos con SQLAlchemy. No contienen lógica de negocio ni acceso HTTP.
2. **Controladores (`controllers/`):** Reciben las peticiones HTTP, invocan la lógica de negocio a través de los DAOs/Services y retornan la respuesta (render_template o redirect).
3. **Vistas (`views/`):** Solo templates Jinja2 con HTML y Bootstrap. No contienen lógica de Python compleja.
4. **DAOs (`dao/`):** Encapsulan todas las operaciones de base de datos (CRUD). Los controladores nunca hacen queries directamente.
5. **DTOs (`dto/`):** Objetos simples para transferir datos entre capas sin exponer los modelos directamente.
6. **Services (`services/`):** Lógica de negocio compleja que no pertenece a un controlador específico (blockchain, gamificación).

---

## Patrones de Diseño Implementados

| Patrón | Dónde se usa | Propósito |
|---|---|---|
| **MVC** | Toda la app | Separación de responsabilidades (obligatorio) |
| **DAO** | `app/dao/` | Abstracción del acceso a datos, centraliza queries |
| **DTO** | `app/dto/` | Transferencia de datos entre capas sin acoplar modelos |
| **Factory** | `app/__init__.py` | `create_app()` para crear instancias configurables de Flask |
| **Singleton** | `blockchain_service.py` | Una única instancia de la cadena de bloques |

---

## Modelo de Base de Datos (MySQL)

### Tablas principales:

**usuarios**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `nombre` VARCHAR(100) NOT NULL
- `email` VARCHAR(150) UNIQUE NOT NULL
- `password_hash` VARCHAR(256) NOT NULL
- `tipo_usuario` ENUM('ciudadano', 'empresa', 'gobierno') NOT NULL
- `puntos_acumulados` INT DEFAULT 0
- `ciudad` VARCHAR(100)
- `fecha_registro` DATETIME DEFAULT CURRENT_TIMESTAMP
- `activo` BOOLEAN DEFAULT TRUE

**dispositivos**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `nombre` VARCHAR(100) NOT NULL
- `categoria` ENUM('celular', 'computador', 'bateria', 'electrodomestico', 'tarjeta_madre', 'otro') NOT NULL
- `marca` VARCHAR(100)
- `estado` ENUM('funcional', 'dañado', 'obsoleto') NOT NULL
- `peso_kg` DECIMAL(6,2)
- `descripcion` TEXT
- `usuario_id` INT FOREIGN KEY → usuarios(id)
- `fecha_registro` DATETIME DEFAULT CURRENT_TIMESTAMP

**puntos_recoleccion**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `nombre` VARCHAR(150) NOT NULL
- `direccion` VARCHAR(255) NOT NULL
- `ciudad` VARCHAR(100) NOT NULL
- `latitud` DECIMAL(10,8)
- `longitud` DECIMAL(11,8)
- `horario` VARCHAR(200)
- `tipos_aceptados` VARCHAR(255) — categorías separadas por coma
- `activo` BOOLEAN DEFAULT TRUE

**entregas**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `usuario_id` INT FOREIGN KEY → usuarios(id)
- `dispositivo_id` INT FOREIGN KEY → dispositivos(id)
- `punto_recoleccion_id` INT FOREIGN KEY → puntos_recoleccion(id)
- `fecha_entrega` DATETIME DEFAULT CURRENT_TIMESTAMP
- `estado` ENUM('pendiente', 'recibido', 'procesado', 'reciclado') DEFAULT 'pendiente'
- `puntos_otorgados` INT DEFAULT 0
- `hash_blockchain` VARCHAR(256) — referencia al bloque en la cadena

**recompensas**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `nombre` VARCHAR(150) NOT NULL
- `descripcion` TEXT
- `puntos_requeridos` INT NOT NULL
- `tipo` ENUM('descuento', 'producto', 'reconocimiento') NOT NULL
- `activo` BOOLEAN DEFAULT TRUE

**bloques_blockchain**
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `indice` INT NOT NULL
- `timestamp` DATETIME NOT NULL
- `datos` TEXT NOT NULL — JSON con los datos de la entrega
- `hash_previo` VARCHAR(256) NOT NULL
- `hash_actual` VARCHAR(256) NOT NULL
- `nonce` INT DEFAULT 0

### Relaciones:
- Un **usuario** puede registrar muchos **dispositivos** (1:N).
- Un **usuario** puede hacer muchas **entregas** (1:N).
- Un **dispositivo** tiene una **entrega** (1:1).
- Un **punto de recolección** recibe muchas **entregas** (1:N).
- Cada **entrega** genera un registro en **bloques_blockchain**.

---

## Operaciones CRUD por Entidad

Cada entidad debe tener las 4 operaciones básicas implementadas en su DAO correspondiente:

| Operación | Método DAO | Ruta Flask (ejemplo: dispositivos) |
|---|---|---|
| **Create** | `crear(dto)` | `POST /dispositivos/nuevo` |
| **Read** | `obtener_por_id(id)` / `obtener_todos()` | `GET /dispositivos/<id>` / `GET /dispositivos` |
| **Update** | `actualizar(id, dto)` | `PUT /dispositivos/<id>/editar` |
| **Delete** | `eliminar(id)` | `DELETE /dispositivos/<id>/eliminar` |

---

## Blockchain Simulado — Especificación

La blockchain es una **simulación educativa en Python puro** (no usa librerías externas de blockchain). Su propósito es demostrar el concepto de trazabilidad.

### Implementación:

```python
# Estructura de un bloque (referencia para Copilot)
import hashlib
import json
from datetime import datetime

class Bloque:
    """Representa un bloque en la cadena de bloques simulada."""

    def __init__(self, indice, datos, hash_previo):
        self.indice = indice
        self.timestamp = datetime.now().isoformat()
        self.datos = datos           # dict con info de la entrega
        self.hash_previo = hash_previo
        self.nonce = 0
        self.hash_actual = self.calcular_hash()

    def calcular_hash(self):
        """Genera el hash SHA-256 del bloque."""
        contenido = json.dumps({
            "indice": self.indice,
            "timestamp": self.timestamp,
            "datos": self.datos,
            "hash_previo": self.hash_previo,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(contenido.encode()).hexdigest()


class CadenaBloques:
    """Cadena de bloques simulada — Singleton."""

    def __init__(self):
        self.cadena = []
        self.crear_bloque_genesis()

    def crear_bloque_genesis(self):
        """Crea el primer bloque de la cadena."""
        bloque = Bloque(0, {"mensaje": "Bloque génesis"}, "0")
        self.cadena.append(bloque)

    def agregar_bloque(self, datos_entrega):
        """Agrega un nuevo bloque con los datos de una entrega."""
        bloque_previo = self.cadena[-1]
        nuevo_bloque = Bloque(
            indice=len(self.cadena),
            datos=datos_entrega,
            hash_previo=bloque_previo.hash_actual
        )
        self.cadena.append(nuevo_bloque)
        return nuevo_bloque

    def es_cadena_valida(self):
        """Verifica la integridad de toda la cadena."""
        for i in range(1, len(self.cadena)):
            actual = self.cadena[i]
            previo = self.cadena[i - 1]
            if actual.hash_actual != actual.calcular_hash():
                return False
            if actual.hash_previo != previo.hash_actual:
                return False
        return True
```

### Flujo:
1. Un ciudadano entrega un dispositivo en un punto de recolección.
2. Se crea el registro en la tabla `entregas`.
3. Se crea un bloque con los datos de esa entrega y se agrega a la cadena.
4. El `hash_actual` del bloque se guarda en `entregas.hash_blockchain`.
5. Se pueden consultar los bloques para verificar la trazabilidad.

---

## Sistema de Gamificación

| Acción | Puntos |
|---|---|
| Entregar un celular | 50 |
| Entregar un computador | 100 |
| Entregar una batería | 30 |
| Entregar un electrodoméstico | 80 |
| Entregar tarjeta madre | 40 |
| Entregar otro dispositivo | 20 |
| Participar en jornada de reciclaje | 150 |

Los puntos se acumulan en `usuarios.puntos_acumulados` y se pueden canjear por recompensas.

---

## Dashboard para Gobiernos

Los usuarios de tipo `gobierno` acceden a un dashboard con:

- Total de dispositivos recolectados por categoría.
- Volumen en kg de RAEE recolectados por ciudad.
- Ranking de puntos de recolección más activos.
- Tendencia mensual de entregas.
- Cantidad de ciudadanos activos en la plataforma.

Usar **Chart.js** (via CDN) para las gráficas en el frontend.

---

## Roles y Permisos

| Funcionalidad | Ciudadano | Empresa | Gobierno |
|---|---|---|---|
| Registrar dispositivos | ✅ | ✅ | ❌ |
| Hacer entregas | ✅ | ✅ | ❌ |
| Ver puntos y recompensas | ✅ | ✅ | ❌ |
| Gestionar puntos de recolección | ❌ | ✅ | ✅ |
| Ver dashboard estadístico | ❌ | ❌ | ✅ |
| Verificar blockchain | ✅ | ✅ | ✅ |

---

## Configuración del Proyecto

### Archivo `config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base de la aplicación."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-desarrollo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost:3306/ecosystem_db'
    )

class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

### Archivo `.env.example`:
```
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ecosystem_db
FLASK_ENV=development
FLASK_DEBUG=1
```

---

## Convenciones de Código

- **Idioma del código:** Variables, funciones, clases y comentarios en **español**.
- **Estilo:** PEP 8.
- **Nombres de clases:** PascalCase (`PuntoRecoleccion`, `EntregaDTO`).
- **Nombres de funciones y variables:** snake_case (`obtener_por_id`, `puntos_acumulados`).
- **Nombres de tablas:** snake_case plural (`usuarios`, `puntos_recoleccion`).
- **Docstrings:** En cada clase y función pública, explicando qué hace.
- **Comentarios:** Explicar el "por qué", no el "qué".
- **Imports:** Agrupados en estándar, terceros y locales.

---

## Flujo de Desarrollo Sugerido (Fases)

### Fase 1 — Base del proyecto
- [ ] Inicializar Flask con factory pattern (`create_app`).
- [ ] Configurar conexión a MySQL con SQLAlchemy.
- [ ] Crear modelos de `Usuario` y `Dispositivo`.
- [ ] Implementar DAOs y DTOs para ambas entidades.
- [ ] CRUD completo de usuarios y dispositivos.
- [ ] Template base con Bootstrap 5.

### Fase 2 — Puntos de recolección y entregas
- [ ] Modelo, DAO, DTO y CRUD de `PuntoRecoleccion`.
- [ ] Modelo, DAO, DTO y CRUD de `Entrega`.
- [ ] Vincular entregas con usuarios, dispositivos y puntos.

### Fase 3 — Autenticación y roles
- [ ] Registro e inicio de sesión con Flask-Login.
- [ ] Hashing de contraseñas con Werkzeug.
- [ ] Protección de rutas por tipo de usuario.
- [ ] Decoradores para verificar roles.

### Fase 4 — Blockchain simulado
- [ ] Implementar clases `Bloque` y `CadenaBloques`.
- [ ] Integrar con el flujo de entregas.
- [ ] Vista para consultar y verificar la cadena.

### Fase 5 — Gamificación
- [ ] Asignación automática de puntos al registrar entregas.
- [ ] CRUD de recompensas.
- [ ] Vista de ranking / perfil con puntos.

### Fase 6 — Dashboard gobierno
- [ ] Rutas protegidas para usuarios tipo gobierno.
- [ ] Consultas agregadas (por categoría, ciudad, mes).
- [ ] Gráficas con Chart.js.

### Fase 7 — Pulido final
- [ ] Tests con pytest.
- [ ] Manejo de errores (páginas 404, 500).
- [ ] Validación de formularios con Flask-WTF.
- [ ] Revisión de seguridad básica (CSRF, SQL injection vía ORM).

---

## Comandos Útiles

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos (después de configurar MySQL)
flask db init
flask db migrate -m "Migración inicial"
flask db upgrade

# Ejecutar la aplicación
python run.py

# Ejecutar tests
pytest tests/ -v
```

---

## Dependencias (`requirements.txt`)

```
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.1.0
Flask-Login==0.6.3
Flask-WTF==1.2.2
PyMySQL==1.1.1
cryptography==44.0.0
python-dotenv==1.1.0
pytest==8.3.5
```

---

> **Nota para Copilot:** Este es un proyecto universitario. Prioriza generar código simple, bien estructurado y comentado en español. Sigue estrictamente el patrón MVC con las capas DAO y DTO. Cada sugerencia debe respetar la estructura de carpetas definida y usar SQLAlchemy como ORM. Cuando generes código nuevo, incluye siempre docstrings explicativas.