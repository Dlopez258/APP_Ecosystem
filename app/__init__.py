"""
Factory principal de la aplicación EcoSystem.
Usa el patrón Factory para crear instancias configurables de Flask.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import configuraciones

# Instancias de extensiones (se inicializan sin app para soportar el factory pattern)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

#Creación y configuración de la aplicación Flask
#Argumento: entorno: Permite cargar la configuración adecuada según el entorno (desarrollo, pruebas, producción).
#Retorna: Instancia de la aplicación Flask configurada y lista para usar.
def create_app(entorno='development'):
    app = Flask(
        __name__,
        template_folder='views',   # Las vistas están en app/views/
        static_folder='static'
    )

    # Cargar la configuración según el entorno
    app.config.from_object(configuraciones.get(entorno, configuraciones['default']))

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Configurar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesion para acceder a esta pagina.'
    login_manager.login_message_category = 'warning'

    # Importar modelos para que Flask-Migrate los detecte
    from app.models import usuario, dispositivo, punto_recoleccion, entrega, recompensa, bloque

    # Registrar función de carga de usuario para Flask-Login
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def cargar_usuario(user_id):
        """Carga el usuario desde la base de datos usando su ID."""
        return db.session.get(Usuario, int(user_id))

    # Registrar todos los Blueprints (controladores)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.usuario_controller import usuario_bp
    from app.controllers.dispositivo_controller import dispositivo_bp
    from app.controllers.punto_recoleccion_controller import punto_recoleccion_bp
    from app.controllers.entrega_controller import entrega_bp
    from app.controllers.recompensa_controller import recompensa_bp
    from app.controllers.blockchain_controller import blockchain_bp
    from app.controllers.dashboard_controller import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(dispositivo_bp)
    app.register_blueprint(punto_recoleccion_bp)
    app.register_blueprint(entrega_bp)
    app.register_blueprint(recompensa_bp)
    app.register_blueprint(blockchain_bp)
    app.register_blueprint(dashboard_bp)

    # Registrar manejadores de errores personalizados
    registrar_errores(app)

    return app

# Registro de errores 404 y 500
def registrar_errores(app):
    from flask import render_template

    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template('errores/404.html'), 404

    @app.errorhandler(403)
    def acceso_denegado(error):
        return render_template('errores/403.html'), 403

    @app.errorhandler(500)
    def error_interno(error):
        return render_template('errores/500.html'), 500

