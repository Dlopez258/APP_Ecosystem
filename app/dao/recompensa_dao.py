"""
DAO de Recompensa.
Centraliza todas las operaciones de base de datos relacionadas con recompensas.
"""

from app import db
from app.models.recompensa import Recompensa


class RecompensaDAO:
    """
    Data Access Object para la entidad Recompensa.
    Encapsula todas las consultas relacionadas con las recompensas del sistema de gamificación.
    """

    @staticmethod
    def crear(nombre, descripcion, puntos_requeridos, tipo):
        """
        Crea una nueva recompensa en la base de datos.

        Args:
            nombre (str):             Nombre de la recompensa.
            descripcion (str):        Descripción detallada.
            puntos_requeridos (int):  Puntos necesarios para canjear.
            tipo (str):               Tipo: 'descuento', 'producto' o 'reconocimiento'.

        Returns:
            Recompensa: La recompensa creada y persistida.
        """
        recompensa = Recompensa(
            nombre=nombre,
            descripcion=descripcion,
            puntos_requeridos=puntos_requeridos,
            tipo=tipo
        )
        db.session.add(recompensa)
        db.session.commit()
        return recompensa

    @staticmethod
    def obtener_por_id(recompensa_id):
        """
        Busca una recompensa por su ID.

        Args:
            recompensa_id (int): ID de la recompensa.

        Returns:
            Recompensa | None: La recompensa encontrada o None.
        """
        return db.session.get(Recompensa, recompensa_id)

    @staticmethod
    def obtener_todas():
        """
        Retorna todas las recompensas activas, ordenadas por puntos requeridos.

        Returns:
            list[Recompensa]: Lista de recompensas activas.
        """
        return Recompensa.query.filter_by(activo=True)\
            .order_by(Recompensa.puntos_requeridos.asc()).all()

    @staticmethod
    def obtener_disponibles_para_usuario(puntos_usuario):
        """
        Retorna las recompensas que el usuario puede canjear según sus puntos.

        Args:
            puntos_usuario (int): Puntos acumulados del usuario.

        Returns:
            list[Recompensa]: Recompensas que el usuario puede canjear.
        """
        return Recompensa.query.filter(
            Recompensa.activo == True,
            Recompensa.puntos_requeridos <= puntos_usuario
        ).order_by(Recompensa.puntos_requeridos.asc()).all()

    @staticmethod
    def actualizar(recompensa_id, nombre, descripcion, puntos_requeridos, tipo):
        """
        Actualiza los datos de una recompensa existente.

        Args:
            recompensa_id (int):      ID de la recompensa a actualizar.
            nombre (str):             Nuevo nombre.
            descripcion (str):        Nueva descripción.
            puntos_requeridos (int):  Nuevos puntos requeridos.
            tipo (str):               Nuevo tipo.

        Returns:
            Recompensa | None: La recompensa actualizada o None si no existe.
        """
        recompensa = db.session.get(Recompensa, recompensa_id)
        if not recompensa:
            return None
        recompensa.nombre = nombre
        recompensa.descripcion = descripcion
        recompensa.puntos_requeridos = puntos_requeridos
        recompensa.tipo = tipo
        db.session.commit()
        return recompensa

    @staticmethod
    def eliminar(recompensa_id):
        """
        Desactiva una recompensa (eliminación lógica).

        Args:
            recompensa_id (int): ID de la recompensa a desactivar.

        Returns:
            bool: True si se desactivó correctamente, False si no existe.
        """
        recompensa = db.session.get(Recompensa, recompensa_id)
        if not recompensa:
            return False
        recompensa.activo = False
        db.session.commit()
        return True

