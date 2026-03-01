"""
Modelo de Recompensa para la base de datos.
Representa los premios que los usuarios pueden canjear con sus puntos acumulados.
"""

from app import db


class Recompensa(db.Model):
    """
    Modelo de recompensa del sistema de gamificación.

    Los usuarios acumulan puntos entregando dispositivos y pueden
    canjearlos por recompensas de diferentes tipos.

    Tipos:
        - descuento:       Descuento en algún servicio o producto.
        - producto:        Producto físico o digital.
        - reconocimiento:  Certificado, medalla o distinción.
    """

    __tablename__ = 'recompensas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    puntos_requeridos = db.Column(db.Integer, nullable=False)
    tipo = db.Column(
        db.Enum('descuento', 'producto', 'reconocimiento', name='tipo_recompensa_enum'),
        nullable=False
    )
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Recompensa {self.nombre} - {self.puntos_requeridos} pts>'

