"""
Tests de los controladores (rutas HTTP) de la aplicación EcoSystem.
Verifica que las rutas responden correctamente y gestionan la autenticación.
"""

import pytest
from app import create_app, db
from app.models.usuario import Usuario


@pytest.fixture
def app():
    """Fixture que crea la app en modo testing con BD en memoria."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def cliente(app):
    """Fixture del cliente HTTP de pruebas."""
    return app.test_client()


@pytest.fixture
def usuario_registrado(app):
    """Crea un usuario de prueba autenticable en la BD."""
    with app.app_context():
        usuario = Usuario(
            nombre='Test User',
            email='test@ecosys.com',
            tipo_usuario='ciudadano',
            ciudad='Medellín'
        )
        usuario.establecer_password('clave123')
        db.session.add(usuario)
        db.session.commit()
        return usuario.id


class TestRutasAuth:
    """Tests de las rutas de autenticación."""

    def test_login_get(self, cliente):
        """La página de login debe responder 200."""
        respuesta = cliente.get('/auth/login')
        assert respuesta.status_code == 200
        assert b'Iniciar' in respuesta.data or b'EcoSystem' in respuesta.data

    def test_registro_get(self, cliente):
        """La página de registro debe responder 200."""
        respuesta = cliente.get('/auth/registro')
        assert respuesta.status_code == 200

    def test_login_credenciales_incorrectas(self, cliente, usuario_registrado):
        """El login con credenciales incorrectas debe mostrar error."""
        respuesta = cliente.post('/auth/login', data={
            'email': 'test@ecosys.com',
            'password': 'clave-incorrecta',
            'csrf_token': 'dummy'
        }, follow_redirects=True)
        assert respuesta.status_code == 200

    def test_ruta_protegida_sin_login(self, cliente):
        """Acceder a rutas protegidas sin login debe redirigir al login."""
        respuesta = cliente.get('/entregas/', follow_redirects=False)
        # Debe redirigir (302) o devolver 401
        assert respuesta.status_code in [302, 401]

    def test_registro_nuevo_usuario(self, cliente, app):
        """El registro de un nuevo usuario debe funcionar correctamente."""
        with app.app_context():
            respuesta = cliente.post('/auth/registro', data={
                'nombre': 'Nuevo Usuario',
                'email': 'nuevo@test.com',
                'ciudad': 'Cali',
                'tipo_usuario': 'ciudadano',
                'password': 'clave123',
                'confirmar_password': 'clave123',
                'csrf_token': 'dummy'
            }, follow_redirects=True)
            # La respuesta debe ser exitosa
            assert respuesta.status_code == 200


class TestRutasDispositivo:
    """Tests de las rutas de dispositivos."""

    def test_listar_dispositivos_sin_auth(self, cliente):
        """Listar dispositivos sin autenticación debe redirigir."""
        respuesta = cliente.get('/dispositivos/', follow_redirects=False)
        assert respuesta.status_code in [302, 401]

    def test_nuevo_dispositivo_sin_auth(self, cliente):
        """Crear dispositivo sin autenticación debe redirigir."""
        respuesta = cliente.get('/dispositivos/nuevo', follow_redirects=False)
        assert respuesta.status_code in [302, 401]

