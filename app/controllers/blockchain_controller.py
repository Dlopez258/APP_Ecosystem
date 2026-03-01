"""
Controlador de Blockchain.
Permite explorar y verificar la integridad de la cadena de bloques simulada.
Accesible para todos los tipos de usuario.
"""

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from app.dao.bloque_dao import BloqueDAO
from app.services.blockchain_service import CadenaBloques

blockchain_bp = Blueprint('blockchain', __name__, url_prefix='/blockchain')


@blockchain_bp.route('/')
@login_required
def explorar():
    """
    Muestra todos los bloques de la cadena de bloques simulada.
    Carga los bloques desde la BD y sincroniza la cadena en memoria.
    """
    bloques_bd = BloqueDAO.obtener_todos()

    # Sincronizar la cadena en memoria con lo que está en la BD
    cadena = CadenaBloques.obtener_instancia()
    if len(cadena.cadena) <= 1 and bloques_bd:
        # Si la cadena en memoria está vacía (reinicio del servidor),
        # reconstruirla desde la base de datos
        cadena.sincronizar_desde_bd(bloques_bd)

    bloques = cadena.obtener_todos_como_dict()
    es_valida = cadena.es_cadena_valida()

    return render_template('blockchain/explorar.html',
                           bloques=bloques,
                           es_valida=es_valida,
                           total_bloques=len(bloques),
                           titulo='Explorador de Blockchain')


@blockchain_bp.route('/verificar')
@login_required
def verificar():
    """
    Verifica la integridad de la cadena completa recalculando todos los hashes.
    Muestra si la cadena es válida o si fue alterada.
    """
    cadena = CadenaBloques.obtener_instancia()
    bloques_bd = BloqueDAO.obtener_todos()

    # Reconstruir desde BD si es necesario
    if len(cadena.cadena) <= 1 and bloques_bd:
        cadena.sincronizar_desde_bd(bloques_bd)

    es_valida = cadena.es_cadena_valida()

    if es_valida:
        flash(f'✅ La cadena de {len(cadena.cadena)} bloques es completamente válida e íntegra.',
              'success')
    else:
        flash('❌ ¡Alerta! La integridad de la cadena está comprometida. '
              'Se detectaron alteraciones.', 'danger')

    return redirect(url_for('blockchain.explorar'))


@blockchain_bp.route('/bloque/<string:hash_bloque>')
@login_required
def detalle_bloque(hash_bloque):
    """
    Muestra el detalle completo de un bloque específico buscado por su hash.

    Args:
        hash_bloque (str): Hash SHA-256 del bloque a consultar.
    """
    cadena = CadenaBloques.obtener_instancia()
    bloque = cadena.obtener_bloque_por_hash(hash_bloque)

    if not bloque:
        # Intentar buscar directamente en la BD
        bloque_bd = BloqueDAO.obtener_por_hash(hash_bloque)
        if not bloque_bd:
            flash('Bloque no encontrado en la cadena.', 'warning')
            return redirect(url_for('blockchain.explorar'))
        # Convertir el modelo BD a diccionario para la vista
        import json
        bloque_dict = {
            'indice': bloque_bd.indice,
            'timestamp': bloque_bd.timestamp.isoformat(),
            'datos': json.loads(bloque_bd.datos),
            'hash_previo': bloque_bd.hash_previo,
            'hash_actual': bloque_bd.hash_actual,
            'nonce': bloque_bd.nonce
        }
    else:
        bloque_dict = bloque.to_dict()

    return render_template('blockchain/detalle_bloque.html',
                           bloque=bloque_dict, titulo='Detalle del bloque')

