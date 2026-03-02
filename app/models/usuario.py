"""
Modelo de Usuario para la base de datos.
Representa a los ciudadanos, empresas y gobiernos que usan EcoSystem.
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Usuario(UserMixin, db.Model):
    """
    Modelo de usuario en la base de datos.

    Hereda de UserMixin para integración con Flask-Login,
    lo que proporciona los métodos is_authenticated, is_active, etc.

    Tipos de usuario:
        - ciudadano: Puede registrar dispositivos y hacer entregas.
        - empresa:   Puede además gestionar puntos de recolección.
        - gobierno:  Accede al dashboard estadístico.
    """

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    tipo_usuario = db.Column(
        db.Enum('ciudadano', 'empresa', 'gobierno', name='tipo_usuario_enum'),
        nullable=False,
        default='ciudadano'
    )
    puntos_acumulados = db.Column(db.Integer, default=0)
    ciudad = db.Column(db.String(100))
    # Campos integrados del aporte del compañero de equipo
    telefono = db.Column(db.String(20))
    barrio = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    activo = db.Column(db.Boolean, default=True)

    # Relaciones: un usuario puede tener muchos dispositivos y muchas entregas
    dispositivos = db.relationship('Dispositivo', backref='propietario', lazy=True)
    entregas = db.relationship('Entrega', backref='usuario', lazy=True)

    def establecer_password(self, password):
        """
        Genera y guarda el hash de la contraseña usando Werkzeug.

        Args:
            password (str): Contraseña en texto plano.
        """
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        """
        Verifica si la contraseña ingresada coincide con el hash guardado.

        Args:
            password (str): Contraseña en texto plano a verificar.

        Returns:
            bool: True si la contraseña es correcta, False si no.
        """
        return check_password_hash(self.password_hash, password)

    def es_ciudadano(self):
        """Retorna True si el usuario es de tipo ciudadano."""
        return self.tipo_usuario == 'ciudadano'

    def es_empresa(self):
        """Retorna True si el usuario es de tipo empresa."""
        return self.tipo_usuario == 'empresa'

    def es_gobierno(self):
        """Retorna True si el usuario es de tipo gobierno."""
        return self.tipo_usuario == 'gobierno'

    def puede_gestionar_puntos(self):
        """Retorna True si el usuario puede gestionar puntos de recolección."""
        return self.tipo_usuario in ['empresa', 'gobierno']

    def __repr__(self):
        return f'<Usuario {self.nombre} ({self.tipo_usuario})>'

