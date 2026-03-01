"""
Servicio de Gamificación.
Gestiona la asignación de puntos según la categoría de dispositivo entregado
y verifica las recompensas disponibles para el usuario.
"""

# Tabla de puntos por categoría de dispositivo según las reglas del negocio
PUNTOS_POR_CATEGORIA = {
    'celular': 50,
    'computador': 100,
    'bateria': 30,
    'electrodomestico': 80,
    'tarjeta_madre': 40,
    'otro': 20
}

# Puntos extra por participar en una jornada de reciclaje masiva
PUNTOS_JORNADA_RECICLAJE = 150


class GamificacionService:
    """
    Servicio que centraliza la lógica de gamificación de EcoSystem.

    Calcula los puntos por cada entrega y determina qué recompensas
    puede canjear un usuario según sus puntos acumulados.
    """

    @staticmethod
    def calcular_puntos(categoria_dispositivo):
        """
        Calcula los puntos que se otorgan por entregar un dispositivo
        según su categoría.

        Args:
            categoria_dispositivo (str): Categoría del dispositivo entregado.
                                         Debe ser una clave de PUNTOS_POR_CATEGORIA.

        Returns:
            int: Puntos a otorgar. Retorna 20 (valor de 'otro') si la categoría
                 no está reconocida.
        """
        return PUNTOS_POR_CATEGORIA.get(categoria_dispositivo, 20)

    @staticmethod
    def determinar_nivel(puntos_acumulados):
        """
        Determina el nivel/insignia del usuario según sus puntos acumulados.
        Sirve para mostrar el progreso en el perfil del ciudadano.

        Niveles:
            - Bronce:    0 - 199 puntos
            - Plata:   200 - 499 puntos
            - Oro:     500 - 999 puntos
            - Platino: 1000+ puntos

        Args:
            puntos_acumulados (int): Total de puntos del usuario.

        Returns:
            dict: Diccionario con 'nivel' (str) y 'color' (str) del nivel.
        """
        if puntos_acumulados >= 1000:
            return {'nivel': 'Platino', 'color': 'info'}
        elif puntos_acumulados >= 500:
            return {'nivel': 'Oro', 'color': 'warning'}
        elif puntos_acumulados >= 200:
            return {'nivel': 'Plata', 'color': 'secondary'}
        else:
            return {'nivel': 'Bronce', 'color': 'danger'}

    @staticmethod
    def puntos_para_siguiente_nivel(puntos_acumulados):
        """
        Calcula cuántos puntos le faltan al usuario para subir de nivel.

        Args:
            puntos_acumulados (int): Puntos actuales del usuario.

        Returns:
            int: Puntos restantes para el siguiente nivel. 0 si ya está en Platino.
        """
        if puntos_acumulados >= 1000:
            return 0
        elif puntos_acumulados >= 500:
            return 1000 - puntos_acumulados
        elif puntos_acumulados >= 200:
            return 500 - puntos_acumulados
        else:
            return 200 - puntos_acumulados

    @staticmethod
    def obtener_recompensas_disponibles(puntos_usuario):
        """
        Retorna las recompensas que el usuario puede canjear.
        Delega al DAO para hacer la consulta filtrada.

        Args:
            puntos_usuario (int): Puntos acumulados del usuario.

        Returns:
            list[Recompensa]: Lista de recompensas canjeables.
        """
        from app.dao.recompensa_dao import RecompensaDAO
        return RecompensaDAO.obtener_disponibles_para_usuario(puntos_usuario)

