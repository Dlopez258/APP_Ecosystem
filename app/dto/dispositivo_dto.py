"""
DTO de Dispositivo.
Objeto simple para transferir datos de dispositivo entre capas.
"""


class DispositivoDTO:
    """
    Data Transfer Object para la entidad Dispositivo.

    Encapsula los datos de un dispositivo electrónico (RAEE)
    para transferirlos entre capas sin exponer el modelo ORM.
    """

    def __init__(self, nombre, categoria, estado, usuario_id,
                 marca=None, peso_kg=None, descripcion=None):
        """
        Inicializa el DTO con los datos del formulario.

        Args:
            nombre (str):      Nombre del dispositivo.
            categoria (str):   Categoría: celular, computador, bateria, etc.
            estado (str):      Estado: funcional, dañado, obsoleto.
            usuario_id (int):  ID del usuario propietario.
            marca (str):       Marca del dispositivo (opcional).
            peso_kg (float):   Peso en kilogramos (opcional).
            descripcion (str): Descripción adicional (opcional).
        """
        self.nombre = nombre
        self.categoria = categoria
        self.estado = estado
        self.usuario_id = usuario_id
        self.marca = marca
        self.peso_kg = peso_kg
        self.descripcion = descripcion

    @staticmethod
    def desde_modelo(dispositivo):
        """
        Crea un DTO a partir de un objeto modelo Dispositivo.

        Args:
            dispositivo (Dispositivo): Instancia del modelo.

        Returns:
            DispositivoDTO: DTO con los datos del modelo.
        """
        dto = DispositivoDTO(
            nombre=dispositivo.nombre,
            categoria=dispositivo.categoria,
            estado=dispositivo.estado,
            usuario_id=dispositivo.usuario_id,
            marca=dispositivo.marca,
            peso_kg=float(dispositivo.peso_kg) if dispositivo.peso_kg else None,
            descripcion=dispositivo.descripcion
        )
        dto.id = dispositivo.id
        dto.fecha_registro = dispositivo.fecha_registro
        return dto

