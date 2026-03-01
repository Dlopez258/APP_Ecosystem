"""
Tests de los modelos de la aplicación EcoSystem.
Verifica que los modelos se crean correctamente y sus métodos funcionan.
"""

import pytest
from app import create_app, db
from app.models.usuario import Usuario
from app.models.dispositivo import Dispositivo
from app.models.recompensa import Recompensa


@pytest.fixture
def app():
    """
    Fixture que crea una instancia de la app en modo testing.
    Usa SQLite en memoria para que cada test sea independiente.
    """
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def cliente(app):
    """Fixture que provee el cliente HTTP de pruebas."""
    return app.test_client()


@pytest.fixture
def usuario_ejemplo(app):
    """Fixture que crea un usuario de prueba en la BD."""
    with app.app_context():
        usuario = Usuario(
            nombre='Juan Pérez',
            email='juan@test.com',
            tipo_usuario='ciudadano',
            ciudad='Bogotá'
        )
        usuario.establecer_password('password123')
        db.session.add(usuario)
        db.session.commit()
        return usuario.id


class TestModeloUsuario:
    """Tests del modelo Usuario."""

    def test_crear_usuario(self, app):
        """Verifica que un usuario se crea y persiste correctamente."""
        with app.app_context():
            usuario = Usuario(
                nombre='María López',
                email='maria@test.com',
                tipo_usuario='ciudadano'
            )
            usuario.establecer_password('clave123')
            db.session.add(usuario)
            db.session.commit()

            encontrado = Usuario.query.filter_by(email='maria@test.com').first()
            assert encontrado is not None
            assert encontrado.nombre == 'María López'
            assert encontrado.tipo_usuario == 'ciudadano'

    def test_password_hashing(self, app):
        """Verifica que la contraseña se hashea y verifica correctamente."""
        with app.app_context():
            usuario = Usuario(nombre='Test', email='test@test.com', tipo_usuario='ciudadano')
            usuario.establecer_password('mi-clave-secreta')

            # La contraseña no debe guardarse en texto plano
            assert usuario.password_hash != 'mi-clave-secreta'
            # La verificación debe funcionar
            assert usuario.verificar_password('mi-clave-secreta') is True
            assert usuario.verificar_password('clave-incorrecta') is False

    def test_roles_usuario(self, app):
        """Verifica que los métodos de verificación de rol funcionan."""
        with app.app_context():
            ciudadano = Usuario(nombre='C', email='c@test.com', tipo_usuario='ciudadano')
            empresa = Usuario(nombre='E', email='e@test.com', tipo_usuario='empresa')
            gobierno = Usuario(nombre='G', email='g@test.com', tipo_usuario='gobierno')

            assert ciudadano.es_ciudadano() is True
            assert ciudadano.es_empresa() is False
            assert empresa.puede_gestionar_puntos() is True
            assert gobierno.puede_gestionar_puntos() is True
            assert ciudadano.puede_gestionar_puntos() is False

    def test_puntos_iniciales_en_cero(self, app):
        """Verifica que los puntos acumulados empiezan en 0."""
        with app.app_context():
            usuario = Usuario(nombre='T', email='t@test.com', tipo_usuario='ciudadano')
            usuario.establecer_password('clave123')  # password_hash es NOT NULL
            db.session.add(usuario)
            db.session.commit()
            assert usuario.puntos_acumulados == 0


class TestModeloDispositivo:
    """Tests del modelo Dispositivo."""

    def test_crear_dispositivo(self, app, usuario_ejemplo):
        """Verifica que un dispositivo se crea y asocia al usuario correctamente."""
        with app.app_context():
            dispositivo = Dispositivo(
                nombre='iPhone 12',
                categoria='celular',
                estado='obsoleto',
                usuario_id=usuario_ejemplo
            )
            db.session.add(dispositivo)
            db.session.commit()

            encontrado = Dispositivo.query.filter_by(nombre='iPhone 12').first()
            assert encontrado is not None
            assert encontrado.categoria == 'celular'
            assert encontrado.usuario_id == usuario_ejemplo


class TestModeloRecompensa:
    """Tests del modelo Recompensa."""

    def test_crear_recompensa(self, app):
        """Verifica que una recompensa se crea correctamente."""
        with app.app_context():
            recompensa = Recompensa(
                nombre='Descuento 10%',
                puntos_requeridos=100,
                tipo='descuento'
            )
            db.session.add(recompensa)
            db.session.commit()

            encontrada = Recompensa.query.first()
            assert encontrada is not None
            assert encontrada.puntos_requeridos == 100
            assert encontrada.activo is True


