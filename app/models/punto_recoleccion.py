"""
Modelo de Punto de Recolección para la base de datos.
Representa los centros de acopio donde los ciudadanos entregan sus dispositivos.
"""

from datetime import datetime, timezone
from app import db


class PuntoRecoleccion(db.Model):
    """
    Modelo de punto de recolección / centro de acopio de RAEE.

    Estos puntos son gestionados por empresas o gobiernos.
    El campo tipos_aceptados almacena las categorías separadas por coma.
    """

    __tablename__ = 'puntos_recoleccion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.Numeric(10, 8))
    longitud = db.Column(db.Numeric(11, 8))
    horario = db.Column(db.String(200))
    # Categorías de dispositivos que acepta este punto, separadas por coma
    tipos_aceptados = db.Column(db.String(255))
    # Campos integrados del aporte del compañero de equipo
    entidad = db.Column(db.String(120))
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    activo = db.Column(db.Boolean, default=True)

    # Relación: un punto puede recibir muchas entregas
    entregas = db.relationship('Entrega', backref='punto_recoleccion', lazy=True)

    def get_tipos_lista(self):
        """
        Retorna los tipos aceptados como una lista de strings.

        Returns:
            list: Lista de categorías aceptadas.
        """
        if self.tipos_aceptados:
            return [t.strip() for t in self.tipos_aceptados.split(',')]
        return []

    def __repr__(self):
        return f'<PuntoRecoleccion {self.nombre} - {self.ciudad}>'

