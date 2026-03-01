"""
DAO de Dispositivo.
Centraliza todas las operaciones de base de datos relacionadas con dispositivos.
"""

from app import db
from app.models.dispositivo import Dispositivo


class DispositivoDAO:
    """
    Data Access Object para la entidad Dispositivo.
    Encapsula todas las consultas SQL/ORM relacionadas con dispositivos electrónicos.
    """

    @staticmethod
    def crear(dto):
        """
        Registra un nuevo dispositivo en la base de datos.

        Args:
            dto (DispositivoDTO): Datos del dispositivo a registrar.

        Returns:
            Dispositivo: El dispositivo creado y persistido.
        """
        dispositivo = Dispositivo(
            nombre=dto.nombre,
            categoria=dto.categoria,
            marca=dto.marca,
            estado=dto.estado,
            peso_kg=dto.peso_kg,
            descripcion=dto.descripcion,
            usuario_id=dto.usuario_id
        )
        db.session.add(dispositivo)
        db.session.commit()
        return dispositivo

    @staticmethod
    def obtener_por_id(dispositivo_id):
        """
        Busca un dispositivo por su ID.

        Args:
            dispositivo_id (int): ID del dispositivo.

        Returns:
            Dispositivo | None: El dispositivo encontrado o None.
        """
        return db.session.get(Dispositivo, dispositivo_id)

    @staticmethod
    def obtener_todos():
        """
        Retorna todos los dispositivos registrados.

        Returns:
            list[Dispositivo]: Lista de todos los dispositivos.
        """
        return Dispositivo.query.order_by(Dispositivo.fecha_registro.desc()).all()

    @staticmethod
    def obtener_por_usuario(usuario_id):
        """
        Retorna todos los dispositivos de un usuario específico.

        Args:
            usuario_id (int): ID del usuario propietario.

        Returns:
            list[Dispositivo]: Lista de dispositivos del usuario.
        """
        return Dispositivo.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def obtener_sin_entrega(usuario_id):
        """
        Retorna los dispositivos de un usuario que aún no han sido entregados.
        Se usa para mostrar solo las opciones disponibles al crear una entrega.

        Args:
            usuario_id (int): ID del usuario propietario.

        Returns:
            list[Dispositivo]: Dispositivos sin entrega asociada.
        """
        return Dispositivo.query.filter_by(
            usuario_id=usuario_id
        ).filter(
            ~Dispositivo.entrega.has()
        ).all()

    @staticmethod
    def actualizar(dispositivo_id, dto):
        """
        Actualiza los datos de un dispositivo existente.

        Args:
            dispositivo_id (int):  ID del dispositivo a actualizar.
            dto (DispositivoDTO):  Nuevos datos.

        Returns:
            Dispositivo | None: El dispositivo actualizado o None si no existe.
        """
        dispositivo = db.session.get(Dispositivo, dispositivo_id)
        if not dispositivo:
            return None
        dispositivo.nombre = dto.nombre
        dispositivo.categoria = dto.categoria
        dispositivo.marca = dto.marca
        dispositivo.estado = dto.estado
        dispositivo.peso_kg = dto.peso_kg
        dispositivo.descripcion = dto.descripcion
        db.session.commit()
        return dispositivo

    @staticmethod
    def eliminar(dispositivo_id):
        """
        Elimina un dispositivo de la base de datos.

        Args:
            dispositivo_id (int): ID del dispositivo a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.
        """
        dispositivo = db.session.get(Dispositivo, dispositivo_id)
        if not dispositivo:
            return False
        db.session.delete(dispositivo)
        db.session.commit()
        return True

