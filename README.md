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

---

## 🏛️ Patrones de Diseño y Estilos Arquitectónicos

EcoSystem implementa múltiples patrones de diseño que se complementan para lograr un código mantenible, desacoplado y escalable.

---

### 1. Estilo Arquitectónico — MVC (Model-View-Controller)

**¿Qué es?** El estilo MVC divide la aplicación en tres capas con responsabilidades claramente separadas: los datos (Model), la presentación (View) y la lógica de control (Controller).

**¿Cómo se aplica en EcoSystem?**

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| **Model** | `app/models/` | Define las entidades de la base de datos con SQLAlchemy. No contiene lógica de negocio ni HTTP. |
| **View** | `app/views/` | Templates Jinja2 con HTML y Bootstrap 5. Solo presentación, sin lógica Python compleja. |
| **Controller** | `app/controllers/` | Recibe peticiones HTTP, invoca DAOs/Services y retorna respuestas (`render_template` o `redirect`). |

**Extensiones del MVC implementadas:**

| Capa adicional | Carpeta | Rol en la arquitectura |
|---|---|---|
| **DAO** (Data Access Object) | `app/dao/` | Encapsula todas las queries a la base de datos. Los controladores **nunca** hacen queries directas. |
| **DTO** (Data Transfer Object) | `app/dto/` | Objetos simples para mover datos entre capas sin acoplarlas al modelo ORM. |
| **Services** | `app/services/` | Lógica de negocio compleja independiente de un controlador (blockchain, gamificación). |

**Diagrama del flujo de una petición:**

```
[Navegador]
    ↓  HTTP Request
[Controller] — app/controllers/dispositivo_controller.py
    ↓  Usa DTO para encapsular datos
[DTO] — app/dto/dispositivo_dto.py
    ↓  Delega operación de BD
[DAO] — app/dao/dispositivo_dao.py
    ↓  Opera sobre el modelo ORM
[Model] — app/models/dispositivo.py
    ↓  SQLAlchemy ↔ SQLite/MySQL
[Base de Datos]
    ↑  Datos
[Controller]
    ↓  render_template(...)
[View] — app/views/dispositivo/listar.html
    ↑  HTML renderizado
[Navegador]
```

**Archivos clave del MVC:**

```
app/
├── models/
│   ├── usuario.py               ← Entidad Usuario (tabla usuarios)
│   ├── dispositivo.py           ← Entidad Dispositivo (tabla dispositivos)
│   ├── entrega.py               ← Entidad Entrega (tabla entregas)
│   ├── punto_recoleccion.py     ← Entidad PuntoRecoleccion
│   ├── recompensa.py            ← Entidad Recompensa
│   └── bloque.py                ← Entidad Bloque (tabla bloques_blockchain)
├── controllers/
│   ├── auth_controller.py       ← Rutas: /auth/login, /auth/registro, /auth/logout
│   ├── usuario_controller.py    ← Rutas: /usuarios/
│   ├── dispositivo_controller.py← Rutas: /dispositivos/
│   ├── entrega_controller.py    ← Rutas: /entregas/
│   ├── punto_recoleccion_controller.py ← Rutas: /puntos-recoleccion/
│   ├── recompensa_controller.py ← Rutas: /recompensas/
│   ├── blockchain_controller.py ← Rutas: /blockchain/
│   └── dashboard_controller.py  ← Rutas: /dashboard/ (solo gobierno)
├── views/
│   ├── layout/base.html         ← Template base con navbar y footer
│   ├── auth/                    ← login.html, registro.html
│   ├── dispositivo/             ← listar.html, formulario.html, detalle.html
│   ├── entrega/                 ← listar.html, formulario.html, detalle.html
│   ├── punto_recoleccion/       ← listar.html, formulario.html, detalle.html
│   ├── recompensa/              ← listar.html, formulario.html
│   ├── blockchain/              ← explorar.html, detalle_bloque.html
│   ├── dashboard/               ← index.html (gráficas Chart.js)
│   └── errores/                 ← 403.html, 404.html, 500.html
├── dao/
│   ├── usuario_dao.py           ← CRUD de usuarios en BD
│   ├── dispositivo_dao.py       ← CRUD de dispositivos en BD
│   ├── entrega_dao.py           ← CRUD de entregas + consultas analíticas
│   ├── punto_recoleccion_dao.py ← CRUD de puntos de recolección en BD
│   ├── recompensa_dao.py        ← CRUD de recompensas en BD
│   └── bloque_dao.py            ← Persistencia de bloques blockchain en BD
└── dto/
    ├── usuario_dto.py           ← DTO para transferir datos de usuario
    ├── dispositivo_dto.py       ← DTO para transferir datos de dispositivo
    └── entrega_dto.py           ← DTO para transferir datos de entrega
```

---

### 2. Patrón de Diseño — Factory Method

**📄 Archivo:** `app/__init__.py`

**¿Qué es?** El patrón Factory encapsula la creación de objetos complejos en una función o clase fábrica, permitiendo crear instancias con diferentes configuraciones sin acoplar el código al proceso de construcción.

**¿Cómo se aplica?** La función `create_app()` es la fábrica que construye y configura la instancia de Flask según el entorno (`development`, `testing`, `production`). Esto permite que los tests usen una configuración diferente a producción sin cambiar el código fuente.

```
# app/__init__.py — línea 21
def create_app(entorno='development'):
    """Crea y configura la aplicación Flask (Factory Pattern)."""
    app = Flask(__name__, template_folder='views', static_folder='static')

    # Carga la config según el entorno: DevelopmentConfig, TestingConfig o ProductionConfig
    app.config.from_object(configuraciones.get(entorno, configuraciones['default']))

    # Inicializa extensiones SIN la app al principio (soporte al Factory)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Registra todos los Blueprints (controladores)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dispositivo_bp)
    # ... etc.

    return app  # Retorna la instancia totalmente configurada
```

**Beneficio concreto:** Los tests llaman `create_app('testing')` y obtienen la app con SQLite en memoria. En producción se llama `create_app('production')` y apunta a MySQL. El mismo código funciona para ambos.

---

### 3. Patrón de Diseño — Singleton

**📄 Archivo:** `app/services/blockchain_service.py`

**¿Qué es?** El patrón Singleton garantiza que una clase tenga **una única instancia** durante toda la vida del programa, y provee un punto de acceso global a ella.

**¿Por qué se usa aquí?** La cadena de bloques debe ser **una sola** en toda la aplicación. Si cada petición HTTP creara su propia instancia de `CadenaBloques`, cada usuario vería una cadena diferente y los bloques no estarían encadenados correctamente.

```
# app/services/blockchain_service.py — línea 79
class CadenaBloques:
    """Cadena de bloques simulada — implementa el patrón Singleton."""

    _instancia = None  # ← Atributo de clase: guarda la única instancia

    @classmethod
    def obtener_instancia(cls):
        """
        Retorna la única instancia de CadenaBloques.
        Si no existe, la crea. Si ya existe, la retorna directamente.
        """
        if cls._instancia is None:
            cls._instancia = cls()   # Primera y única creación
        return cls._instancia        # Siempre retorna la misma instancia
```

**Uso en el controlador de entregas:**
```
# app/controllers/entrega_controller.py — línea 108
cadena = CadenaBloques.obtener_instancia()   # Obtiene LA instancia (no crea una nueva)
bloque = cadena.agregar_bloque(datos_bloque)  # Agrega a la cadena compartida
```

---

### 4. Patrón de Diseño — DAO (Data Access Object)

**📄 Archivos:** `app/dao/usuario_dao.py`, `app/dao/dispositivo_dao.py`, `app/dao/entrega_dao.py`, `app/dao/punto_recoleccion_dao.py`, `app/dao/recompensa_dao.py`, `app/dao/bloque_dao.py`

**¿Qué es?** El patrón DAO abstrae y encapsula todo el acceso a la fuente de datos (base de datos). Cada entidad tiene su propio DAO con los métodos CRUD y consultas específicas.

**Beneficio principal:** Si mañana se cambia SQLite por PostgreSQL, o SQLAlchemy por otro ORM, solo se modifican los DAOs. Los controladores no necesitan cambiar.

```python
# app/dao/dispositivo_dao.py — estructura completa
class DispositivoDAO:
    @staticmethod
    def crear(dto): ...           # INSERT
    @staticmethod
    def obtener_por_id(id): ...   # SELECT WHERE id = ?
    @staticmethod
    def obtener_todos(): ...      # SELECT ALL
    @staticmethod
    def obtener_por_usuario(usuario_id): ...   # SELECT WHERE usuario_id = ?
    @staticmethod
    def obtener_sin_entrega(usuario_id): ...   # SELECT con subquery NOT EXISTS
    @staticmethod
    def actualizar(id, dto): ...  # UPDATE
    @staticmethod
    def eliminar(id): ...         # DELETE físico
```

**Regla estricta aplicada:** Ningún controlador tiene una sola línea de `db.session.query(...)` directa. Todo pasa por el DAO correspondiente.

---

### 5. Patrón de Diseño — DTO (Data Transfer Object)

**📄 Archivos:** `app/dto/usuario_dto.py`, `app/dto/dispositivo_dto.py`, `app/dto/entrega_dto.py`

**¿Qué es?** El patrón DTO define objetos simples (sin lógica) cuya única función es transportar datos entre capas (del formulario → al controlador → al DAO), sin exponer directamente los modelos ORM.

```python
# app/dto/dispositivo_dto.py
class DispositivoDTO:
    def __init__(self, nombre, categoria, estado, usuario_id,
                 marca=None, peso_kg=None, descripcion=None):
        self.nombre = nombre
        self.categoria = categoria
        self.estado = estado
        self.usuario_id = usuario_id
        self.marca = marca
        self.peso_kg = peso_kg
        self.descripcion = descripcion

    @staticmethod
    def desde_modelo(dispositivo):
        """Convierte un objeto ORM a DTO (sentido inverso)."""
        ...
```

**Flujo concreto en registro de dispositivo:**
```
FormularioDispositivo (WTForms)
    ↓  datos del POST
DispositivoDTO(nombre=..., categoria=..., estado=..., usuario_id=...)
    ↓  DTO pasado al DAO
DispositivoDAO.crear(dto)
    ↓  DAO construye el modelo
Dispositivo(nombre=dto.nombre, ...)  →  db.session.add()  →  BD
```

---

### 6. Patrón de Diseño — Decorator (para control de acceso por roles)

**📄 Archivo:** `app/controllers/decoradores.py`

**¿Qué es?** El patrón Decorator añade comportamiento a una función existente sin modificarla, envolviéndola en otra función. En Python se implementa con `@functools.wraps`.

**¿Cómo se aplica?** El decorador `@requiere_rol(...)` protege las rutas verificando el tipo de usuario antes de ejecutar la función de vista. Si el usuario no tiene el rol requerido, recibe un error 403.

```
# app/controllers/decoradores.py
def requiere_rol(*roles):
    """Decorador que restringe el acceso según el tipo de usuario."""
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.tipo_usuario not in roles:
                abort(403)          # Acceso denegado
            return f(*args, **kwargs)   # Ejecuta la vista original
        return funcion_decorada
    return decorador
```

**Uso en los controladores:**
```
# Solo empresa y gobierno pueden crear puntos de recolección
@punto_recoleccion_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_rol('empresa', 'gobierno')   # ← Decorator en acción
def nuevo(): ...

# Solo gobierno puede ver el dashboard
@dashboard_bp.route('/')
@login_required
@requiere_rol('gobierno')              # ← Decorator en acción
def index(): ...

# Solo gobierno puede eliminar usuarios
@usuario_bp.route('/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
@requiere_rol('gobierno')              # ← Decorator en acción
def eliminar(usuario_id): ...
```

---

### Resumen de patrones implementados

| Patrón | Archivo(s) principal(es) | Propósito en EcoSystem |
|---|---|---|
| **MVC** | `app/models/`, `app/controllers/`, `app/views/` | Separación de responsabilidades en toda la app |
| **Factory Method** | `app/__init__.py` | Crear instancias de Flask con configuración por entorno |
| **Singleton** | `app/services/blockchain_service.py` | Una única cadena de bloques compartida por toda la app |
| **DAO** | `app/dao/*.py` | Abstracción y centralización del acceso a la base de datos |
| **DTO** | `app/dto/*.py` | Transferencia de datos entre capas sin exponer modelos ORM |
| **Decorator** | `app/controllers/decoradores.py` | Control de acceso por roles en las rutas HTTP |

---

## 🧩 Programación Orientada a Objetos (POO)

EcoSystem aplica los cuatro pilares de la POO a lo largo de toda su estructura. A continuación se detalla cada pilar con sus archivos y ejemplos concretos.

---

### 1. Encapsulamiento

El encapsulamiento agrupa datos y los métodos que los manipulan en una misma clase, ocultando la complejidad interna.

**📄 `app/models/usuario.py` — Encapsulamiento de la contraseña**

El atributo `password_hash` nunca se expone directamente. Para interactuar con la contraseña se usan exclusivamente los métodos `establecer_password()` y `verificar_password()`, que encapsulan el proceso de hashing con Werkzeug.

```
class Usuario(UserMixin, db.Model):
    password_hash = db.Column(db.String(256), nullable=False)  # Nunca accedido directamente

    def establecer_password(self, password):
        """Hashea la contraseña antes de guardarla. El controlador nunca toca el hash."""
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        """Compara texto plano con el hash sin exponerlo."""
        return check_password_hash(self.password_hash, password)
```

**📄 `app/dao/usuario_dao.py` — Encapsulamiento de queries**

Todas las consultas SQL están encapsuladas dentro de la clase `UsuarioDAO`. Los controladores nunca escriben queries directamente; solo llaman a los métodos del DAO.

```
class UsuarioDAO:
    @staticmethod
    def obtener_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def sumar_puntos(usuario_id, puntos):
        usuario = db.session.get(Usuario, usuario_id)
        if usuario:
            usuario.puntos_acumulados += puntos
            db.session.commit()
```

**📄 `app/services/blockchain_service.py` — Encapsulamiento del hash**

El cálculo del hash SHA-256 está encapsulado en el método `calcular_hash()` de la clase `Bloque`. Ningún código externo replica esa lógica.

```
class Bloque:
    def calcular_hash(self):
        contenido = json.dumps({
            "indice": self.indice,
            "timestamp": self.timestamp,
            "datos": self.datos,
            "hash_previo": self.hash_previo,
            "nonce": self.nonce
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(contenido.encode('utf-8')).hexdigest()
```

---

### 2. Herencia

La herencia permite que una clase hija reutilice atributos y métodos de una clase padre, extendiendo o especializando su comportamiento.

**📄 `app/models/usuario.py` — Herencia múltiple con `UserMixin` y `db.Model`**

`Usuario` hereda de dos clases padre:
- `db.Model` → provee toda la integración con SQLAlchemy (mapeo ORM, sesiones, queries).
- `UserMixin` (Flask-Login) → provee automáticamente los métodos `is_authenticated`, `is_active`, `is_anonymous` y `get_id()` necesarios para el sistema de autenticación.

```python
from flask_login import UserMixin
from app import db

class Usuario(UserMixin, db.Model):
    # Hereda de UserMixin: is_authenticated, is_active, get_id(), etc.
    # Hereda de db.Model: save(), query, relaciones ORM, etc.
    __tablename__ = 'usuarios'
    ...
```

**📄 `app/models/dispositivo.py`, `entrega.py`, `punto_recoleccion.py`, `recompensa.py`, `bloque.py`**

Todos los modelos de la aplicación heredan de `db.Model`, lo que les proporciona la capacidad de mapearse a tablas de la base de datos, usar el sistema de sesiones y definir relaciones entre entidades.

```
class Dispositivo(db.Model): ...       # app/models/dispositivo.py
class Entrega(db.Model): ...           # app/models/entrega.py
class PuntoRecoleccion(db.Model): ...  # app/models/punto_recoleccion.py
class Recompensa(db.Model): ...        # app/models/recompensa.py
class Bloque(db.Model): ...            # app/models/bloque.py
```

**📄 `config.py` — Jerarquía de configuración**

Las clases de configuración forman una jerarquía de herencia. `Config` es la clase base con los atributos comunes, y cada entorno la especializa sobrescribiendo solo lo necesario.

```
class Config:                    # Clase base — atributos compartidos
    SECRET_KEY = ...
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config): # Hereda Config, agrega DEBUG y SQLite
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecosystem_dev.db'

class TestingConfig(Config):     # Hereda Config, agrega TESTING y SQLite en memoria
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):  # Hereda Config, apunta a MySQL en producción
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

**📄 `app/controllers/*.py` — Formularios WTForms con herencia**

Todos los formularios de la aplicación heredan de `FlaskForm`, que les provee validación CSRF, el método `validate_on_submit()` y la integración con Jinja2.

```
class FormularioDispositivo(FlaskForm): ...     # dispositivo_controller.py
class FormularioEntrega(FlaskForm): ...         # entrega_controller.py
class FormularioPunto(FlaskForm): ...           # punto_recoleccion_controller.py
class FormularioRecompensa(FlaskForm): ...      # recompensa_controller.py
class FormularioLogin(FlaskForm): ...           # auth_controller.py
class FormularioRegistro(FlaskForm): ...        # auth_controller.py
class FormularioUsuario(FlaskForm): ...         # usuario_controller.py
```

---

### 3. Polimorfismo

El polimorfismo permite que distintos objetos respondan al mismo mensaje (método) de formas diferentes. En Python se expresa mediante duck typing y métodos especiales como `__repr__`.

**📄 Todos los modelos — Método `__repr__` polimórfico**

Cada modelo implementa `__repr__` con su propia representación. Cuando Python necesita mostrar cualquier objeto de la aplicación (en logs, debugger o consola), llama a `__repr__` sin importar de qué clase concreta se trate.

```
# app/models/usuario.py
def __repr__(self):
    return f'<Usuario {self.nombre} ({self.tipo_usuario})>'

# app/models/dispositivo.py
def __repr__(self):
    return f'<Dispositivo {self.nombre} ({self.categoria})>'

# app/models/entrega.py
def __repr__(self):
    return f'<Entrega #{self.id} - Usuario {self.usuario_id} - Estado: {self.estado}>'

# app/models/punto_recoleccion.py
def __repr__(self):
    return f'<PuntoRecoleccion {self.nombre} - {self.ciudad}>'

# app/models/recompensa.py
def __repr__(self):
    return f'<Recompensa {self.nombre} - {self.puntos_requeridos} pts>'

# app/services/blockchain_service.py (Bloque en memoria)
def __repr__(self):
    return f'<Bloque #{self.indice} - Hash: {self.hash_actual[:16]}...>'
```

**📄 `app/models/usuario.py` — Métodos de rol polimórficos**

El modelo `Usuario` expone una interfaz uniforme para consultar el rol, pero cada implementación retorna un resultado diferente según el estado interno del objeto.

```python
def es_ciudadano(self):
    return self.tipo_usuario == 'ciudadano'

def es_empresa(self):
    return self.tipo_usuario == 'empresa'

def es_gobierno(self):
    return self.tipo_usuario == 'gobierno'

def puede_gestionar_puntos(self):
    return self.tipo_usuario in ['empresa', 'gobierno']
```

**📄 `app/dto/*.py` — Método estático `desde_modelo()` polimórfico**

Cada DTO implementa `desde_modelo()` adaptado a su propia entidad, pero todos siguen la misma interfaz (reciben un modelo y retornan un DTO).

```
# app/dto/usuario_dto.py
@staticmethod
def desde_modelo(usuario): ...   # Convierte Usuario → UsuarioDTO

# app/dto/dispositivo_dto.py
@staticmethod
def desde_modelo(dispositivo): ... # Convierte Dispositivo → DispositivoDTO

# app/dto/entrega_dto.py
@staticmethod
def desde_modelo(entrega): ...   # Convierte Entrega → EntregaDTO
```

---

### 4. Abstracción

La abstracción oculta los detalles de implementación y expone solo lo esencial al usuario de la clase.

**📄 `app/services/blockchain_service.py` — Abstracción de la cadena de bloques**

Los controladores no saben cómo se calcula un hash SHA-256, cómo se estructura el JSON del bloque ni cómo funciona el encadenamiento. Solo llaman a `agregar_bloque(datos)` y reciben el bloque resultante.

```
# Lo que ve el controlador (interfaz abstracta):
cadena = CadenaBloques.obtener_instancia()
bloque = cadena.agregar_bloque(datos_entrega)  # "Agrega esto a la cadena"
es_valida = cadena.es_cadena_valida()          # "¿La cadena es íntegra?"

# Lo que hace internamente (detalles ocultos):
# - Toma el hash del último bloque como hash_previo
# - Serializa los datos con json.dumps(sort_keys=True)
# - Calcula hashlib.sha256(...).hexdigest()
# - Incrementa el índice y agrega el bloque a self.cadena
```

**📄 `app/services/gamificacion_service.py` — Abstracción de las reglas de puntos**

Los controladores no conocen la tabla de puntos por categoría. Solo llaman a `calcular_puntos(categoria)` y reciben el resultado.

```
# Lo que ve el controlador:
puntos = GamificacionService.calcular_puntos(dispositivo.categoria)
nivel_info = GamificacionService.determinar_nivel(current_user.puntos_acumulados)
puntos_faltantes = GamificacionService.puntos_para_siguiente_nivel(puntos_acumulados)

# Lo que hace internamente (oculto en el servicio):
PUNTOS_POR_CATEGORIA = {
    'celular': 50, 'computador': 100, 'bateria': 30,
    'electrodomestico': 80, 'tarjeta_madre': 40, 'otro': 20
}
```

**📄 `app/dao/*.py` — Abstracción del acceso a datos**

Los controladores no escriben SQL ni conocen el esquema de la base de datos. Delegan completamente en los DAOs, que abstraen esa complejidad.

```
# Lo que ve el controlador (interfaz abstracta):
dispositivos = DispositivoDAO.obtener_sin_entrega(current_user.id)
puntos = PuntoRecoleccionDAO.obtener_todos()

# Lo que hace el DAO internamente (detalles ocultos):
return Dispositivo.query.filter_by(usuario_id=usuario_id).filter(
    ~Dispositivo.entrega.has()
).all()
```

---

### Resumen de archivos con POO

| Pilar POO | Archivos donde se aplica |
|---|---|
| **Encapsulamiento** | `app/models/usuario.py`, `app/dao/*.py`, `app/services/blockchain_service.py` |
| **Herencia** | `app/models/*.py` (→ `db.Model`), `app/models/usuario.py` (→ `UserMixin`), `config.py`, `app/controllers/*.py` (formularios → `FlaskForm`) |
| **Polimorfismo** | `app/models/*.py` (`__repr__`), `app/dto/*.py` (`desde_modelo()`), `app/models/usuario.py` (métodos de rol) |
| **Abstracción** | `app/services/blockchain_service.py`, `app/services/gamificacion_service.py`, `app/dao/*.py` |

---

## 🔄 Implementación de CRUD

Cada entidad principal del sistema tiene sus cuatro operaciones CRUD implementadas de forma completa: en el **Modelo** (estructura), el **DAO** (acceso a datos), el **Controlador** (rutas HTTP) y la **Vista** (formularios HTML).

---

### CRUD de Usuarios

**Entidad:** `Usuario` | **Tabla:** `usuarios`

| Operación | Método DAO | Ruta HTTP | Controlador | Descripción |
|---|---|---|---|---|
| **Create** | `UsuarioDAO.crear(dto)` | `POST /auth/registro` | `auth_controller.py` | Registro de nuevo usuario con hash de contraseña |
| **Read (uno)** | `UsuarioDAO.obtener_por_id(id)` | `GET /usuarios/<id>` | `usuario_controller.py` | Ver perfil de un usuario |
| **Read (todos)** | `UsuarioDAO.obtener_todos()` | `GET /usuarios/` | `usuario_controller.py` | Listar todos los usuarios (solo gobierno) |
| **Update** | `UsuarioDAO.actualizar(id, dto)` | `POST /usuarios/<id>/editar` | `usuario_controller.py` | Editar nombre, ciudad o tipo de usuario |
| **Delete** | `UsuarioDAO.eliminar(id)` | `POST /usuarios/<id>/eliminar` | `usuario_controller.py` | Desactivación lógica (`activo = False`) |

> ⚠️ **Eliminación lógica:** El usuario no se borra físicamente de la BD para preservar el historial de entregas. Se pone `activo = False`.

**Métodos adicionales del DAO:**
- `UsuarioDAO.obtener_por_email(email)` → usado en el login
- `UsuarioDAO.sumar_puntos(id, puntos)` → usado al registrar una entrega
- `UsuarioDAO.email_existe(email)` → validación antes de crear cuenta

---

### CRUD de Dispositivos

**Entidad:** `Dispositivo` | **Tabla:** `dispositivos`

| Operación | Método DAO | Ruta HTTP | Controlador | Descripción |
|---|---|---|---|---|
| **Create** | `DispositivoDAO.crear(dto)` | `POST /dispositivos/nuevo` | `dispositivo_controller.py` | Registra un nuevo RAEE con categoría, marca y estado |
| **Read (uno)** | `DispositivoDAO.obtener_por_id(id)` | `GET /dispositivos/<id>` | `dispositivo_controller.py` | Ver detalle de un dispositivo |
| **Read (todos)** | `DispositivoDAO.obtener_todos()` | `GET /dispositivos/` | `dispositivo_controller.py` | Listar todos (gobierno) o solo los propios (ciudadano/empresa) |
| **Update** | `DispositivoDAO.actualizar(id, dto)` | `POST /dispositivos/<id>/editar` | `dispositivo_controller.py` | Editar nombre, categoría, estado, peso, etc. |
| **Delete** | `DispositivoDAO.eliminar(id)` | `POST /dispositivos/<id>/eliminar` | `dispositivo_controller.py` | Eliminación física del dispositivo |

**Métodos adicionales del DAO:**
- `DispositivoDAO.obtener_por_usuario(usuario_id)` → lista dispositivos de un usuario
- `DispositivoDAO.obtener_sin_entrega(usuario_id)` → filtra solo los disponibles para entregar (sin entrega asociada)

**Control de permisos:**
- Ciudadanos y empresas pueden crear y ver sus propios dispositivos.
- Solo el propietario o gobierno puede editar/eliminar.
- Gobierno puede ver todos los dispositivos del sistema.

---

### CRUD de Entregas

**Entidad:** `Entrega` | **Tabla:** `entregas`

| Operación | Método DAO | Ruta HTTP | Controlador | Descripción |
|---|---|---|---|---|
| **Create** | `EntregaDAO.crear(dto)` | `POST /entregas/nueva` | `entrega_controller.py` | Registra entrega + genera bloque blockchain + suma puntos |
| **Read (uno)** | `EntregaDAO.obtener_por_id(id)` | `GET /entregas/<id>` | `entrega_controller.py` | Ver detalle con hash blockchain |
| **Read (todos)** | `EntregaDAO.obtener_todas()` | `GET /entregas/` | `entrega_controller.py` | Listar todas (gobierno) o solo las propias |
| **Update** | `EntregaDAO.actualizar_estado(id, estado)` | `POST /entregas/<id>/estado` | `entrega_controller.py` | Actualiza el estado del proceso (solo empresa/gobierno) |
| **Delete** | *(No implementado)* | — | — | Las entregas son registros inmutables para garantizar trazabilidad |

**Flujo especial del Create de Entrega (7 pasos):**
```
1. Crear el DTO con los datos del formulario
2. Calcular los puntos según la categoría del dispositivo (GamificacionService)
3. Guardar la entrega en BD (EntregaDAO.crear)
4. Sumar puntos al usuario (UsuarioDAO.sumar_puntos)
5. Agregar bloque a la cadena (CadenaBloques.agregar_bloque)
6. Persistir el bloque en BD (BloqueDAO.guardar_bloque)
7. Guardar el hash del bloque en la entrega (EntregaDAO.actualizar_hash_blockchain)
```

**Métodos adicionales del DAO:**
- `EntregaDAO.obtener_por_usuario(usuario_id)` → historial del ciudadano
- `EntregaDAO.obtener_por_punto(punto_id)` → entregas en un punto específico
- `EntregaDAO.actualizar_hash_blockchain(id, hash)` → vincula el bloque con la entrega
- `EntregaDAO.contar_por_categoria()` → datos para el dashboard
- `EntregaDAO.contar_por_ciudad()` → datos para el dashboard
- `EntregaDAO.tendencia_mensual()` → datos para gráfica de tendencia

---

### CRUD de Puntos de Recolección

**Entidad:** `PuntoRecoleccion` | **Tabla:** `puntos_recoleccion`

| Operación | Método DAO | Ruta HTTP | Controlador | Descripción |
|---|---|---|---|---|
| **Create** | `PuntoRecoleccionDAO.crear(...)` | `POST /puntos-recoleccion/nuevo` | `punto_recoleccion_controller.py` | Crea un nuevo centro de acopio (solo empresa/gobierno) |
| **Read (uno)** | `PuntoRecoleccionDAO.obtener_por_id(id)` | `GET /puntos-recoleccion/<id>` | `punto_recoleccion_controller.py` | Ver detalle del punto |
| **Read (todos)** | `PuntoRecoleccionDAO.obtener_todos()` | `GET /puntos-recoleccion/` | `punto_recoleccion_controller.py` | Listar todos los puntos activos |
| **Update** | `PuntoRecoleccionDAO.actualizar(id, ...)` | `POST /puntos-recoleccion/<id>/editar` | `punto_recoleccion_controller.py` | Editar nombre, dirección, horario, etc. |
| **Delete** | `PuntoRecoleccionDAO.eliminar(id)` | `POST /puntos-recoleccion/<id>/eliminar` | `punto_recoleccion_controller.py` | Desactivación lógica (`activo = False`) |

**Control de permisos:** Solo usuarios con rol `empresa` o `gobierno` pueden crear, editar y eliminar puntos.

---

### CRUD de Recompensas

**Entidad:** `Recompensa` | **Tabla:** `recompensas`

| Operación | Método DAO | Ruta HTTP | Controlador | Descripción |
|---|---|---|---|---|
| **Create** | `RecompensaDAO.crear(...)` | `POST /recompensas/nueva` | `recompensa_controller.py` | Crea recompensa canjeable (solo gobierno) |
| **Read (uno)** | `RecompensaDAO.obtener_por_id(id)` | `GET /recompensas/<id>` | `recompensa_controller.py` | Ver detalle de una recompensa |
| **Read (todos)** | `RecompensaDAO.obtener_todas()` | `GET /recompensas/` | `recompensa_controller.py` | Listar todas las activas |
| **Update** | `RecompensaDAO.actualizar(id, ...)` | `POST /recompensas/<id>/editar` | `recompensa_controller.py` | Editar nombre, puntos requeridos y tipo |
| **Delete** | `RecompensaDAO.eliminar(id)` | `POST /recompensas/<id>/eliminar` | `recompensa_controller.py` | Desactivación lógica (`activo = False`) |

**Método adicional del DAO:**
- `RecompensaDAO.obtener_disponibles_para_usuario(puntos)` → filtra recompensas cuyo costo ≤ puntos del usuario (integrado con `GamificacionService`)

---

### CRUD de Bloques Blockchain

**Entidad:** `Bloque` | **Tabla:** `bloques_blockchain`

| Operación | Método DAO | Ruta HTTP | Controlador | Descripción |
|---|---|---|---|---|
| **Create** | `BloqueDAO.guardar_bloque(bloque)` | *(Automático al crear entrega)* | `entrega_controller.py` | Persiste el bloque generado en la entrega |
| **Read (todos)** | `BloqueDAO.obtener_todos()` | `GET /blockchain/` | `blockchain_controller.py` | Explorar todos los bloques de la cadena |
| **Read (uno)** | `CadenaBloques.obtener_bloque_por_hash(hash)` | `GET /blockchain/bloque/<hash>` | `blockchain_controller.py` | Ver detalle de un bloque por su hash |
| **Verify** | `CadenaBloques.es_cadena_valida()` | `GET /blockchain/verificar` | `blockchain_controller.py` | Verificar integridad de toda la cadena |

> ⚠️ **Sin Update ni Delete:** Los bloques son **inmutables por diseño**. Modificar o eliminar un bloque rompería el hash del bloque siguiente, lo que es detectado por `es_cadena_valida()`.

---

### Resumen global del CRUD por entidad

| Entidad | Create | Read | Update | Delete | Archivos DAO + Controller |
|---|:---:|:---:|:---:|:---:|---|
| **Usuario** | ✅ | ✅ | ✅ | ✅ (lógico) | `usuario_dao.py` + `usuario_controller.py` / `auth_controller.py` |
| **Dispositivo** | ✅ | ✅ | ✅ | ✅ (físico) | `dispositivo_dao.py` + `dispositivo_controller.py` |
| **Entrega** | ✅ | ✅ | ✅ (estado) | ❌ (inmutable) | `entrega_dao.py` + `entrega_controller.py` |
| **PuntoRecoleccion** | ✅ | ✅ | ✅ | ✅ (lógico) | `punto_recoleccion_dao.py` + `punto_recoleccion_controller.py` |
| **Recompensa** | ✅ | ✅ | ✅ | ✅ (lógico) | `recompensa_dao.py` + `recompensa_controller.py` |
| **Bloque** | ✅ | ✅ | ❌ (inmutable) | ❌ (inmutable) | `bloque_dao.py` + `blockchain_controller.py` |

