"""
Modelo de Dispositivo electrónico para la base de datos.
Representa los aparatos eléctricos y electrónicos (RAEE) que los usuarios registran.
"""

from datetime import datetime
from app import db


class Dispositivo(db.Model):
    """
    Modelo de dispositivo electrónico (RAEE).

    Categorías aceptadas: celular, computador, bateria,
    electrodomestico, tarjeta_madre, otro.

    Estados posibles: funcional, dañado, obsoleto.
    """

    __tablename__ = 'dispositivos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(
        db.Enum('celular', 'computador', 'bateria', 'electrodomestico',
                'tarjeta_madre', 'otro', name='categoria_dispositivo_enum'),
        nullable=False
    )
    marca = db.Column(db.String(100))
    estado = db.Column(
        db.Enum('funcional', 'dañado', 'obsoleto', name='estado_dispositivo_enum'),
        nullable=False
    )
    peso_kg = db.Column(db.Numeric(6, 2))
    descripcion = db.Column(db.Text)

    # Clave foránea: cada dispositivo pertenece a un usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación inversa con entregas (un dispositivo tiene una entrega)
    entrega = db.relationship('Entrega', backref='dispositivo', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Dispositivo {self.nombre} ({self.categoria})>'

