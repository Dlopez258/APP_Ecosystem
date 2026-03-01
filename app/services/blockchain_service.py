"""
Servicio de Blockchain simulado.
Implementa las clases Bloque y CadenaBloques para registrar
entregas de RAEE con trazabilidad mediante hashes SHA-256.

Patrón de diseño: Singleton (una única instancia de CadenaBloques en la app).
"""

import hashlib
import json
from datetime import datetime


class Bloque:
    """
    Representa un bloque individual en la cadena de bloques simulada.

    Cada bloque contiene los datos de una entrega de dispositivo,
    su propio hash y el hash del bloque anterior, formando así la cadena.
    """

    def __init__(self, indice, datos, hash_previo):
        """
        Inicializa un nuevo bloque con sus datos básicos.

        Args:
            indice (int):      Posición del bloque en la cadena (empieza en 0).
            datos (dict):      Información de la entrega en formato diccionario.
            hash_previo (str): Hash SHA-256 del bloque anterior.
        """
        self.indice = indice
        self.timestamp = datetime.now().isoformat()
        self.datos = datos
        self.hash_previo = hash_previo
        self.nonce = 0
        # El hash se calcula al crear el bloque para garantizar integridad
        self.hash_actual = self.calcular_hash()

    def calcular_hash(self):
        """
        Genera el hash SHA-256 del bloque a partir de todos sus campos.
        Si cualquier campo cambia, el hash cambia, detectando alteraciones.

        Returns:
            str: Hash SHA-256 en formato hexadecimal (64 caracteres).
        """
        contenido = json.dumps({
            "indice": self.indice,
            "timestamp": self.timestamp,
            "datos": self.datos,
            "hash_previo": self.hash_previo,
            "nonce": self.nonce
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(contenido.encode('utf-8')).hexdigest()

    def to_dict(self):
        """
        Convierte el bloque a un diccionario serializable para la vista.

        Returns:
            dict: Representación del bloque como diccionario.
        """
        return {
            'indice': self.indice,
            'timestamp': self.timestamp,
            'datos': self.datos,
            'hash_previo': self.hash_previo,
            'hash_actual': self.hash_actual,
            'nonce': self.nonce
        }


class CadenaBloques:
    """
    Cadena de bloques simulada — implementa el patrón Singleton.

    La instancia única se obtiene con CadenaBloques.obtener_instancia().
    Mantiene la cadena en memoria durante la sesión del servidor.
    """

    # Atributo de clase que almacena la única instancia (Singleton)
    _instancia = None

    def __init__(self):
        """
        Inicializa la cadena creando el bloque génesis.
        No llamar directamente; usar obtener_instancia().
        """
        self.cadena = []
        self._crear_bloque_genesis()

    @classmethod
    def obtener_instancia(cls):
        """
        Retorna la única instancia de CadenaBloques (patrón Singleton).
        Si no existe, la crea. Si ya existe, la retorna directamente.

        Returns:
            CadenaBloques: La instancia única de la cadena.
        """
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def _crear_bloque_genesis(self):
        """
        Crea el bloque génesis (bloque #0), que es el origen de la cadena.
        Su hash_previo es '0' porque no tiene bloque anterior.
        """
        bloque_genesis = Bloque(
            indice=0,
            datos={"mensaje": "Bloque génesis — EcoSystem"},
            hash_previo="0"
        )
        self.cadena.append(bloque_genesis)

    def agregar_bloque(self, datos_entrega):
        """
        Agrega un nuevo bloque a la cadena con los datos de una entrega.

        El hash_previo del nuevo bloque es el hash_actual del último bloque,
        creando así el encadenamiento que garantiza la inmutabilidad.

        Args:
            datos_entrega (dict): Información de la entrega:
                                  usuario_id, dispositivo, punto, fecha, etc.

        Returns:
            Bloque: El bloque recién creado y agregado a la cadena.
        """
        bloque_anterior = self.cadena[-1]
        nuevo_bloque = Bloque(
            indice=len(self.cadena),
            datos=datos_entrega,
            hash_previo=bloque_anterior.hash_actual
        )
        self.cadena.append(nuevo_bloque)
        return nuevo_bloque

    def es_cadena_valida(self):
        """
        Verifica la integridad de toda la cadena recalculando los hashes.

        Si algún bloque fue alterado, su hash no coincidirá con el recalculado
        o con el hash_previo del bloque siguiente.

        Returns:
            bool: True si la cadena es íntegra, False si fue alterada.
        """
        for i in range(1, len(self.cadena)):
            bloque_actual = self.cadena[i]
            bloque_previo = self.cadena[i - 1]

            # Verificar que el hash almacenado sigue siendo válido
            if bloque_actual.hash_actual != bloque_actual.calcular_hash():
                return False

            # Verificar que el enlace entre bloques es correcto
            if bloque_actual.hash_previo != bloque_previo.hash_actual:
                return False

        return True

    def obtener_bloque_por_hash(self, hash_buscado):
        """
        Busca un bloque en la cadena por su hash.

        Args:
            hash_buscado (str): Hash SHA-256 a buscar.

        Returns:
            Bloque | None: El bloque encontrado o None si no existe.
        """
        for bloque in self.cadena:
            if bloque.hash_actual == hash_buscado:
                return bloque
        return None

    def obtener_todos_como_dict(self):
        """
        Retorna todos los bloques de la cadena como lista de diccionarios.
        Se usa en la vista de exploración de blockchain.

        Returns:
            list[dict]: Lista de bloques serializados.
        """
        return [bloque.to_dict() for bloque in self.cadena]

    def sincronizar_desde_bd(self, bloques_bd):
        """
        Reconstruye la cadena en memoria a partir de los bloques
        persistidos en la base de datos al reiniciar el servidor.

        Args:
            bloques_bd (list[Bloque]): Lista de objetos Bloque del modelo ORM.
        """
        # Limpiar la cadena actual (incluyendo el génesis)
        self.cadena = []
        for b in bloques_bd:
            bloque = Bloque.__new__(Bloque)
            bloque.indice = b.indice
            bloque.timestamp = b.timestamp.isoformat()
            bloque.datos = json.loads(b.datos)
            bloque.hash_previo = b.hash_previo
            bloque.nonce = b.nonce
            bloque.hash_actual = b.hash_actual
            self.cadena.append(bloque)

        # Si la BD estaba vacía, crear el génesis
        if not self.cadena:
            self._crear_bloque_genesis()

