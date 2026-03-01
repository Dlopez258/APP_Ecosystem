"""
DTO de Entrega.
Objeto simple para transferir datos de entrega entre capas.
"""


class EntregaDTO:
    """
    Data Transfer Object para la entidad Entrega.

    Encapsula los datos de una entrega de dispositivo RAEE
    para transferirlos entre capas sin exponer el modelo ORM.
    """

    def __init__(self, usuario_id, dispositivo_id, punto_recoleccion_id):
        """
        Inicializa el DTO con los datos del formulario de entrega.

        Args:
            usuario_id (int):            ID del usuario que hace la entrega.
            dispositivo_id (int):        ID del dispositivo que se entrega.
            punto_recoleccion_id (int):  ID del punto donde se entrega.
        """
        self.usuario_id = usuario_id
        self.dispositivo_id = dispositivo_id
        self.punto_recoleccion_id = punto_recoleccion_id
        self.estado = 'pendiente'
        self.puntos_otorgados = 0
        self.hash_blockchain = None

    @staticmethod
    def desde_modelo(entrega):
        """
        Crea un DTO a partir de un objeto modelo Entrega.

        Args:
            entrega (Entrega): Instancia del modelo.

        Returns:
            EntregaDTO: DTO con los datos del modelo.
        """
        dto = EntregaDTO(
            usuario_id=entrega.usuario_id,
            dispositivo_id=entrega.dispositivo_id,
            punto_recoleccion_id=entrega.punto_recoleccion_id
        )
        dto.id = entrega.id
        dto.estado = entrega.estado
        dto.puntos_otorgados = entrega.puntos_otorgados
        dto.hash_blockchain = entrega.hash_blockchain
        dto.fecha_entrega = entrega.fecha_entrega
        return dto

