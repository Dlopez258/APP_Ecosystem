"""
DAO de Bloque.
Centraliza la persistencia de los bloques de la blockchain en la base de datos.
"""

import json
from app import db
from app.models.bloque import Bloque as BloqueModelo


class BloqueDAO:
    """
    Data Access Object para la entidad Bloque.
    Persiste los bloques de la cadena en la BD para que sobrevivan reinicios del servidor.
    """

    @staticmethod
    def guardar_bloque(bloque_servicio):
        """
        Persiste un bloque del servicio de blockchain en la base de datos.

        Args:
            bloque_servicio (Bloque): Instancia del bloque del servicio blockchain.

        Returns:
            BloqueModelo: El bloque guardado en la BD.
        """
        from datetime import datetime
        bloque_bd = BloqueModelo(
            indice=bloque_servicio.indice,
            timestamp=datetime.fromisoformat(bloque_servicio.timestamp),
            datos=json.dumps(bloque_servicio.datos, ensure_ascii=False),
            hash_previo=bloque_servicio.hash_previo,
            hash_actual=bloque_servicio.hash_actual,
            nonce=bloque_servicio.nonce
        )
        db.session.add(bloque_bd)
        db.session.commit()
        return bloque_bd

    @staticmethod
    def obtener_todos():
        """
        Retorna todos los bloques persistidos ordenados por índice.

        Returns:
            list[BloqueModelo]: Lista de bloques ordenados.
        """
        return BloqueModelo.query.order_by(BloqueModelo.indice.asc()).all()

    @staticmethod
    def obtener_por_hash(hash_buscado):
        """
        Busca un bloque por su hash.

        Args:
            hash_buscado (str): Hash SHA-256 a buscar.

        Returns:
            BloqueModelo | None: El bloque encontrado o None.
        """
        return BloqueModelo.query.filter_by(hash_actual=hash_buscado).first()

