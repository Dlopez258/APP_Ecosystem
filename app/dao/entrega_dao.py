"""
DAO de Entrega.
Centraliza todas las operaciones de base de datos relacionadas con entregas de RAEE.
"""

from app import db
from app.models.entrega import Entrega


class EntregaDAO:
    """
    Data Access Object para la entidad Entrega.
    Encapsula todas las consultas relacionadas con entregas de dispositivos.
    """

    @staticmethod
    def crear(dto):
        """
        Registra una nueva entrega en la base de datos.

        Args:
            dto (EntregaDTO): Datos de la entrega a registrar.

        Returns:
            Entrega: La entrega creada y persistida.
        """
        entrega = Entrega(
            usuario_id=dto.usuario_id,
            dispositivo_id=dto.dispositivo_id,
            punto_recoleccion_id=dto.punto_recoleccion_id,
            estado=dto.estado,
            puntos_otorgados=dto.puntos_otorgados,
            hash_blockchain=dto.hash_blockchain
        )
        db.session.add(entrega)
        db.session.commit()
        return entrega

    @staticmethod
    def obtener_por_id(entrega_id):
        """
        Busca una entrega por su ID.

        Args:
            entrega_id (int): ID de la entrega.

        Returns:
            Entrega | None: La entrega encontrada o None.
        """
        return db.session.get(Entrega, entrega_id)

    @staticmethod
    def obtener_todas():
        """
        Retorna todas las entregas registradas, ordenadas por fecha descendente.

        Returns:
            list[Entrega]: Lista de todas las entregas.
        """
        return Entrega.query.order_by(Entrega.fecha_entrega.desc()).all()

    @staticmethod
    def obtener_por_usuario(usuario_id):
        """
        Retorna todas las entregas realizadas por un usuario específico.

        Args:
            usuario_id (int): ID del usuario.

        Returns:
            list[Entrega]: Lista de entregas del usuario.
        """
        return Entrega.query.filter_by(usuario_id=usuario_id)\
            .order_by(Entrega.fecha_entrega.desc()).all()

    @staticmethod
    def obtener_por_punto(punto_id):
        """
        Retorna todas las entregas realizadas en un punto de recolección específico.

        Args:
            punto_id (int): ID del punto de recolección.

        Returns:
            list[Entrega]: Lista de entregas en ese punto.
        """
        return Entrega.query.filter_by(punto_recoleccion_id=punto_id).all()

    @staticmethod
    def actualizar_estado(entrega_id, nuevo_estado):
        """
        Actualiza el estado del proceso de una entrega.

        Args:
            entrega_id (int):   ID de la entrega a actualizar.
            nuevo_estado (str): Nuevo estado: 'recibido', 'procesado' o 'reciclado'.

        Returns:
            Entrega | None: La entrega actualizada o None si no existe.
        """
        entrega = db.session.get(Entrega, entrega_id)
        if not entrega:
            return None
        entrega.estado = nuevo_estado
        db.session.commit()
        return entrega

    @staticmethod
    def actualizar_hash_blockchain(entrega_id, hash_bloque):
        """
        Guarda el hash del bloque blockchain asociado a esta entrega.
        Se llama después de agregar el bloque a la cadena.

        Args:
            entrega_id (int):   ID de la entrega.
            hash_bloque (str):  Hash SHA-256 del bloque generado.

        Returns:
            Entrega | None: La entrega actualizada o None si no existe.
        """
        entrega = db.session.get(Entrega, entrega_id)
        if not entrega:
            return None
        entrega.hash_blockchain = hash_bloque
        db.session.commit()
        return entrega

    @staticmethod
    def contar_por_categoria():
        """
        Cuenta las entregas agrupadas por categoría de dispositivo.
        Se usa en el dashboard de gobierno.

        Returns:
            list[tuple]: Lista de (categoria, total).
        """
        from app.models.dispositivo import Dispositivo
        return db.session.query(
            Dispositivo.categoria,
            db.func.count(Entrega.id).label('total')
        ).join(Entrega, Entrega.dispositivo_id == Dispositivo.id)\
         .group_by(Dispositivo.categoria).all()

    @staticmethod
    def contar_por_ciudad():
        """
        Cuenta las entregas agrupadas por ciudad del punto de recolección.
        Se usa en el dashboard de gobierno para ver el volumen por ciudad.

        Returns:
            list[tuple]: Lista de (ciudad, total).
        """
        from app.models.punto_recoleccion import PuntoRecoleccion
        return db.session.query(
            PuntoRecoleccion.ciudad,
            db.func.count(Entrega.id).label('total')
        ).join(Entrega, Entrega.punto_recoleccion_id == PuntoRecoleccion.id)\
         .group_by(PuntoRecoleccion.ciudad).all()

    @staticmethod
    def tendencia_mensual():
        """
        Cuenta las entregas agrupadas por mes del año actual.
        Se usa en el dashboard para mostrar la tendencia temporal.

        Returns:
            list[tuple]: Lista de (mes, total).
        """
        from sqlalchemy import extract
        from datetime import datetime, timezone
        anio_actual = datetime.now(timezone.utc).year
        return db.session.query(
            extract('month', Entrega.fecha_entrega).label('mes'),
            db.func.count(Entrega.id).label('total')
        ).filter(
            extract('year', Entrega.fecha_entrega) == anio_actual
        ).group_by('mes').order_by('mes').all()

    @staticmethod
    def resumen_por_usuario():
        from app.models.usuario import Usuario
        from sqlalchemy import func
        return db.session.query(
            Usuario.id,
            Usuario.nombre,
            Usuario.ciudad,
            Usuario.puntos_acumulados,
            func.count(Entrega.id).label('total_entregas'),
            func.coalesce(func.sum(Entrega.cantidad), 0).label('total_dispositivos'),
            func.round(func.coalesce(func.sum(Entrega.peso_kg), 0), 2).label('total_kg'),
            func.max(Entrega.fecha_entrega).label('ultima_entrega')
        ).outerjoin(Entrega, Entrega.usuario_id == Usuario.id)\
         .filter(Usuario.activo == True)\
         .group_by(Usuario.id, Usuario.nombre, Usuario.ciudad, Usuario.puntos_acumulados)\
         .order_by(func.count(Entrega.id).desc()).all()

