"""
DAO de Usuario.
Centraliza todas las operaciones de base de datos relacionadas con usuarios.
Los controladores no deben hacer queries directamente; siempre pasan por aquí.
"""

from app import db
from app.models.usuario import Usuario


class UsuarioDAO:
    """
    Data Access Object para la entidad Usuario.
    Encapsula todas las consultas SQL/ORM relacionadas con usuarios.
    """

    @staticmethod
    def crear(dto):
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            dto (UsuarioDTO): Datos del nuevo usuario.

        Returns:
            Usuario: El objeto usuario creado y persistido.
        """
        usuario = Usuario(
            nombre=dto.nombre,
            email=dto.email,
            tipo_usuario=dto.tipo_usuario,
            ciudad=dto.ciudad
        )
        # Hashear la contraseña antes de guardar
        usuario.establecer_password(dto.password)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def obtener_por_id(usuario_id):
        """
        Busca un usuario por su ID.

        Args:
            usuario_id (int): ID del usuario.

        Returns:
            Usuario | None: El usuario encontrado o None.
        """
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def obtener_por_email(email):
        """
        Busca un usuario por su correo electrónico.
        Se usa principalmente en el proceso de login.

        Args:
            email (str): Correo electrónico del usuario.

        Returns:
            Usuario | None: El usuario encontrado o None.
        """
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def obtener_todos():
        """
        Retorna todos los usuarios activos registrados.

        Returns:
            list[Usuario]: Lista de usuarios activos.
        """
        return Usuario.query.filter_by(activo=True).all()

    @staticmethod
    def actualizar(usuario_id, dto):
        """
        Actualiza los datos de un usuario existente.

        Args:
            usuario_id (int): ID del usuario a actualizar.
            dto (UsuarioDTO): Nuevos datos del usuario.

        Returns:
            Usuario | None: El usuario actualizado o None si no existe.
        """
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            return None
        usuario.nombre = dto.nombre
        usuario.ciudad = dto.ciudad
        # Solo actualizar tipo si viene en el DTO
        if dto.tipo_usuario:
            usuario.tipo_usuario = dto.tipo_usuario
        # Solo actualizar contraseña si viene una nueva
        if dto.password:
            usuario.establecer_password(dto.password)
        db.session.commit()
        return usuario

    @staticmethod
    def eliminar(usuario_id):
        """
        Desactiva un usuario (eliminación lógica, no física).
        Se prefiere la eliminación lógica para preservar el historial.

        Args:
            usuario_id (int): ID del usuario a desactivar.

        Returns:
            bool: True si se desactivó correctamente, False si no existe.
        """
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            return False
        usuario.activo = False
        db.session.commit()
        return True

    @staticmethod
    def sumar_puntos(usuario_id, puntos):
        """
        Agrega puntos al acumulado de un usuario por entregar dispositivos.

        Args:
            usuario_id (int): ID del usuario.
            puntos (int):     Cantidad de puntos a agregar.

        Returns:
            int: Total de puntos acumulados después de la operación.
        """
        usuario = db.session.get(Usuario, usuario_id)
        if usuario:
            usuario.puntos_acumulados += puntos
            db.session.commit()
            return usuario.puntos_acumulados
        return 0

    @staticmethod
    def email_existe(email):
        """
        Verifica si ya existe un usuario con ese email.

        Args:
            email (str): Email a verificar.

        Returns:
            bool: True si el email ya está registrado.
        """
        return Usuario.query.filter_by(email=email).first() is not None

