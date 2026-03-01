"""
DAO de Punto de Recolección.
Centraliza todas las operaciones de base de datos relacionadas con puntos de acopio.
"""

from app import db
from app.models.punto_recoleccion import PuntoRecoleccion


class PuntoRecoleccionDAO:
    """
    Data Access Object para la entidad PuntoRecoleccion.
    Encapsula todas las consultas relacionadas con centros de acopio de RAEE.
    """

    @staticmethod
    def crear(nombre, direccion, ciudad, latitud=None, longitud=None,
              horario=None, tipos_aceptados=None):
        """
        Crea un nuevo punto de recolección en la base de datos.

        Args:
            nombre (str):           Nombre del punto de recolección.
            direccion (str):        Dirección física.
            ciudad (str):           Ciudad donde está ubicado.
            latitud (float):        Coordenada latitud (opcional).
            longitud (float):       Coordenada longitud (opcional).
            horario (str):          Descripción del horario de atención (opcional).
            tipos_aceptados (str):  Categorías aceptadas, separadas por coma (opcional).

        Returns:
            PuntoRecoleccion: El punto creado y persistido.
        """
        punto = PuntoRecoleccion(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            latitud=latitud,
            longitud=longitud,
            horario=horario,
            tipos_aceptados=tipos_aceptados
        )
        db.session.add(punto)
        db.session.commit()
        return punto

    @staticmethod
    def obtener_por_id(punto_id):
        """
        Busca un punto de recolección por su ID.

        Args:
            punto_id (int): ID del punto.

        Returns:
            PuntoRecoleccion | None: El punto encontrado o None.
        """
        return db.session.get(PuntoRecoleccion, punto_id)

    @staticmethod
    def obtener_todos():
        """
        Retorna todos los puntos de recolección activos.

        Returns:
            list[PuntoRecoleccion]: Lista de puntos activos.
        """
        return PuntoRecoleccion.query.filter_by(activo=True).all()

    @staticmethod
    def obtener_por_ciudad(ciudad):
        """
        Busca puntos de recolección activos en una ciudad específica.

        Args:
            ciudad (str): Nombre de la ciudad.

        Returns:
            list[PuntoRecoleccion]: Puntos en esa ciudad.
        """
        return PuntoRecoleccion.query.filter_by(ciudad=ciudad, activo=True).all()

    @staticmethod
    def actualizar(punto_id, nombre, direccion, ciudad, latitud=None,
                   longitud=None, horario=None, tipos_aceptados=None):
        """
        Actualiza los datos de un punto de recolección.

        Args:
            punto_id (int): ID del punto a actualizar.
            (demás argumentos igual que crear)

        Returns:
            PuntoRecoleccion | None: El punto actualizado o None si no existe.
        """
        punto = db.session.get(PuntoRecoleccion, punto_id)
        if not punto:
            return None
        punto.nombre = nombre
        punto.direccion = direccion
        punto.ciudad = ciudad
        punto.latitud = latitud
        punto.longitud = longitud
        punto.horario = horario
        punto.tipos_aceptados = tipos_aceptados
        db.session.commit()
        return punto

    @staticmethod
    def eliminar(punto_id):
        """
        Desactiva un punto de recolección (eliminación lógica).

        Args:
            punto_id (int): ID del punto a desactivar.

        Returns:
            bool: True si se desactivó correctamente, False si no existe.
        """
        punto = db.session.get(PuntoRecoleccion, punto_id)
        if not punto:
            return False
        punto.activo = False
        db.session.commit()
        return True

