import hashlib
import json
from datetime import datetime

class Bloque:
    def __init__(self, indice, datos, hash_previo):
        self.indice = indice
        self.timestamp = datetime.now().isoformat()
        self.datos = datos
        self.hash_previo = hash_previo
        self.nonce = 0
        # El hash se calcula al crear el bloque para garantizar integridad
        self.hash_actual = self.calcular_hash()

    def calcular_hash(self):
        contenido = json.dumps({
            "indice": self.indice,
            "timestamp": self.timestamp,
            "datos": self.datos,
            "hash_previo": self.hash_previo,
            "nonce": self.nonce
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(contenido.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            'indice': self.indice,
            'timestamp': self.timestamp,
            'datos': self.datos,
            'hash_previo': self.hash_previo,
            'hash_actual': self.hash_actual,
            'nonce': self.nonce
        }

class CadenaBloques:
    _instancia = None
    def __init__(self):
        self.cadena = []
        self._crear_bloque_genesis()

    @classmethod
    def obtener_instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
    def _crear_bloque_genesis(self):
        bloque_genesis = Bloque(
            indice=0,
            datos={"mensaje": "Bloque génesis — EcoSystem"},
            hash_previo="0"
        )
        self.cadena.append(bloque_genesis)

    def agregar_bloque(self, datos_entrega):
        bloque_anterior = self.cadena[-1]
        nuevo_bloque = Bloque(
            indice=len(self.cadena),
            datos=datos_entrega,
            hash_previo=bloque_anterior.hash_actual
        )
        self.cadena.append(nuevo_bloque)
        return nuevo_bloque

    def es_cadena_valida(self):
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
        for bloque in self.cadena:
            if bloque.hash_actual == hash_buscado:
                return bloque
        return None

    def obtener_todos_como_dict(self):
        return [bloque.to_dict() for bloque in self.cadena]

    def sincronizar_desde_bd(self, bloques_bd):
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

