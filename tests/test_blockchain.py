"""
Tests del servicio de Blockchain simulado de EcoSystem.
Verifica la creación de bloques, el encadenamiento y la detección de alteraciones.
"""

import pytest
from app.services.blockchain_service import Bloque, CadenaBloques


@pytest.fixture(autouse=True)
def resetear_singleton():
    """
    Resetea el singleton de CadenaBloques antes de cada test
    para que no haya interferencia entre pruebas.
    """
    CadenaBloques._instancia = None
    yield
    CadenaBloques._instancia = None


class TestBloque:
    """Tests de la clase Bloque."""

    def test_calcular_hash_es_reproducible(self):
        """El mismo bloque debe siempre producir el mismo hash."""
        bloque = Bloque(1, {'dato': 'valor'}, 'hash_previo_ejemplo')
        hash1 = bloque.calcular_hash()
        hash2 = bloque.calcular_hash()
        assert hash1 == hash2

    def test_hash_cambia_si_datos_cambian(self):
        """Modificar los datos del bloque debe cambiar su hash."""
        bloque = Bloque(1, {'dato': 'valor_original'}, '0')
        hash_original = bloque.hash_actual

        bloque.datos = {'dato': 'valor_alterado'}
        hash_nuevo = bloque.calcular_hash()

        assert hash_original != hash_nuevo

    def test_hash_es_sha256(self):
        """El hash debe ser una cadena hexadecimal de 64 caracteres (SHA-256)."""
        bloque = Bloque(0, {'test': True}, '0')
        assert len(bloque.hash_actual) == 64
        assert all(c in '0123456789abcdef' for c in bloque.hash_actual)

    def test_to_dict(self):
        """El método to_dict debe retornar todos los campos del bloque."""
        bloque = Bloque(1, {'entrega_id': 42}, 'hash_previo')
        resultado = bloque.to_dict()
        assert 'indice' in resultado
        assert 'timestamp' in resultado
        assert 'datos' in resultado
        assert 'hash_previo' in resultado
        assert 'hash_actual' in resultado


class TestCadenaBloques:
    """Tests de la clase CadenaBloques (Singleton)."""

    def test_singleton(self):
        """Dos llamadas a obtener_instancia deben retornar la misma instancia."""
        cadena1 = CadenaBloques.obtener_instancia()
        cadena2 = CadenaBloques.obtener_instancia()
        assert cadena1 is cadena2

    def test_bloque_genesis(self):
        """La cadena debe iniciarse con el bloque génesis (#0)."""
        cadena = CadenaBloques.obtener_instancia()
        assert len(cadena.cadena) == 1
        assert cadena.cadena[0].indice == 0
        assert cadena.cadena[0].hash_previo == '0'

    def test_agregar_bloque(self):
        """Agregar un bloque debe incrementar la longitud de la cadena."""
        cadena = CadenaBloques.obtener_instancia()
        datos = {'entrega_id': 1, 'categoria': 'celular', 'puntos': 50}
        cadena.agregar_bloque(datos)

        assert len(cadena.cadena) == 2
        assert cadena.cadena[1].indice == 1
        assert cadena.cadena[1].datos == datos

    def test_encadenamiento_correcto(self):
        """El hash_previo de cada bloque debe ser el hash_actual del anterior."""
        cadena = CadenaBloques.obtener_instancia()
        cadena.agregar_bloque({'test': 1})
        cadena.agregar_bloque({'test': 2})

        for i in range(1, len(cadena.cadena)):
            assert cadena.cadena[i].hash_previo == cadena.cadena[i - 1].hash_actual

    def test_cadena_valida(self):
        """Una cadena sin alteraciones debe ser válida."""
        cadena = CadenaBloques.obtener_instancia()
        cadena.agregar_bloque({'entrega': 'test'})
        assert cadena.es_cadena_valida() is True

    def test_cadena_invalida_si_alterada(self):
        """Alterar los datos de un bloque debe invalidar la cadena."""
        cadena = CadenaBloques.obtener_instancia()
        cadena.agregar_bloque({'entrega': 'original'})

        # Alterar los datos del bloque 1 directamente
        cadena.cadena[1].datos = {'entrega': 'ALTERADO'}
        # El hash no se recalculó, entonces la cadena es inválida
        assert cadena.es_cadena_valida() is False

    def test_obtener_bloque_por_hash(self):
        """Buscar un bloque por su hash debe retornarlo correctamente."""
        cadena = CadenaBloques.obtener_instancia()
        bloque = cadena.agregar_bloque({'entrega_id': 99})
        encontrado = cadena.obtener_bloque_por_hash(bloque.hash_actual)

        assert encontrado is not None
        assert encontrado.indice == bloque.indice

    def test_obtener_todos_como_dict(self):
        """La lista de bloques debe retornarse como lista de diccionarios."""
        cadena = CadenaBloques.obtener_instancia()
        cadena.agregar_bloque({'dato': 'x'})
        todos = cadena.obtener_todos_como_dict()

        assert isinstance(todos, list)
        assert len(todos) == 2
        assert isinstance(todos[0], dict)

