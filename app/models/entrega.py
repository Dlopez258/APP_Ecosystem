"""
Modelo de Entrega para la base de datos.
Registra cada vez que un usuario entrega un dispositivo en un punto de recolección.
"""

from datetime import datetime, timezone
from app import db


class Entrega(db.Model):
    """
    Modelo de entrega de dispositivo RAEE.

    Vincula un usuario, un dispositivo y un punto de recolección.
    También almacena el hash del bloque blockchain generado para esta entrega,
    lo que permite verificar la trazabilidad.

    Estados del proceso:
        - pendiente:  La entrega fue registrada pero no confirmada.
        - recibido:   El punto de recolección confirmó la recepción.
        - procesado:  El dispositivo está siendo tratado.
        - reciclado:  El dispositivo fue reciclado correctamente.
    """

    __tablename__ = 'entregas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Claves foráneas que vinculan la entrega con las demás entidades
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivos.id'), nullable=False)
    punto_recoleccion_id = db.Column(db.Integer, db.ForeignKey('puntos_recoleccion.id'), nullable=False)

    fecha_entrega = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    estado = db.Column(
        db.Enum('pendiente', 'recibido', 'verificado', 'en_proceso',
                'procesado', 'reutilizado', 'reciclado',
                name='estado_entrega_enum'),
        default='pendiente'
    )
    puntos_otorgados = db.Column(db.Integer, default=0)
    # Hash del bloque en la cadena blockchain simulada para trazabilidad
    hash_blockchain = db.Column(db.String(256))
    # Campos integrados del aporte del compañero de equipo
    cantidad = db.Column(db.SmallInteger, default=1)
    peso_kg = db.Column(db.Numeric(6, 2))
    observaciones = db.Column(db.Text)

    def __repr__(self):
        return f'<Entrega #{self.id} - Usuario {self.usuario_id} - Estado: {self.estado}>'

