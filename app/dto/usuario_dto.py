"""
DTO de Usuario.
Objeto simple para transferir datos de usuario entre capas
sin exponer el modelo de base de datos directamente.
"""


class UsuarioDTO:
    """
    Data Transfer Object para la entidad Usuario.

    Se usa para pasar datos de usuario entre el controlador,
    los servicios y la vista sin acoplar las capas al modelo ORM.
    """

    def __init__(self, nombre, email, password, tipo_usuario, ciudad=None):
        """
        Inicializa el DTO con los datos del formulario.

        Args:
            nombre (str):       Nombre completo del usuario.
            email (str):        Correo electrónico único.
            password (str):     Contraseña en texto plano (se hasheará en el DAO).
            tipo_usuario (str): Tipo: 'ciudadano', 'empresa' o 'gobierno'.
            ciudad (str):       Ciudad de residencia (opcional).
        """
        self.nombre = nombre
        self.email = email
        self.password = password
        self.tipo_usuario = tipo_usuario
        self.ciudad = ciudad

    @staticmethod
    def desde_modelo(usuario):
        """
        Crea un DTO a partir de un objeto modelo Usuario.

        Args:
            usuario (Usuario): Instancia del modelo.

        Returns:
            UsuarioDTO: DTO con los datos del modelo.
        """
        dto = UsuarioDTO(
            nombre=usuario.nombre,
            email=usuario.email,
            password=None,  # No se transfiere el hash de contraseña
            tipo_usuario=usuario.tipo_usuario,
            ciudad=usuario.ciudad
        )
        dto.id = usuario.id
        dto.puntos_acumulados = usuario.puntos_acumulados
        dto.activo = usuario.activo
        dto.fecha_registro = usuario.fecha_registro
        return dto

