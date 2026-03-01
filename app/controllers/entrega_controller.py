"""
Controlador de Entrega.
Gestiona el flujo completo de entrega de dispositivos RAEE:
registro → puntos → blockchain.
"""

import json
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from app.dao.entrega_dao import EntregaDAO
from app.dao.dispositivo_dao import DispositivoDAO
from app.dao.punto_recoleccion_dao import PuntoRecoleccionDAO
from app.dao.usuario_dao import UsuarioDAO
from app.dao.bloque_dao import BloqueDAO
from app.dto.entrega_dto import EntregaDTO
from app.services.blockchain_service import CadenaBloques
from app.services.gamificacion_service import GamificacionService
from app.controllers.decoradores import requiere_rol

entrega_bp = Blueprint('entrega', __name__, url_prefix='/entregas')


class FormularioEntrega(FlaskForm):
    """Formulario para registrar una nueva entrega de dispositivo."""
    dispositivo_id = SelectField('Dispositivo a entregar',
                                 coerce=int, validators=[DataRequired()])
    punto_recoleccion_id = SelectField('Punto de recolección',
                                       coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar entrega')


@entrega_bp.route('/')
@login_required
def listar():
    """Muestra las entregas del usuario actual (o todas si es gobierno)."""
    if current_user.tipo_usuario == 'gobierno':
        entregas = EntregaDAO.obtener_todas()
    else:
        entregas = EntregaDAO.obtener_por_usuario(current_user.id)
    return render_template('entrega/listar.html', entregas=entregas, titulo='Mis entregas')


@entrega_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@requiere_rol('ciudadano', 'empresa')
def nueva():
    """
    Registra una nueva entrega de dispositivo.

    Flujo completo:
    1. Crear el registro de entrega en la BD.
    2. Calcular los puntos según la categoría del dispositivo.
    3. Sumar los puntos al usuario.
    4. Agregar un bloque a la cadena de bloques con los datos de la entrega.
    5. Persistir el bloque en la BD y guardar el hash en la entrega.
    """
    # Obtener dispositivos del usuario que aún no tienen entrega
    dispositivos_disponibles = DispositivoDAO.obtener_sin_entrega(current_user.id)
    puntos_activos = PuntoRecoleccionDAO.obtener_todos()

    formulario = FormularioEntrega()
    # Cargar las opciones dinámicas en los SelectField
    formulario.dispositivo_id.choices = [
        (d.id, f'{d.nombre} ({d.categoria})') for d in dispositivos_disponibles
    ]
    formulario.punto_recoleccion_id.choices = [
        (p.id, f'{p.nombre} — {p.ciudad}') for p in puntos_activos
    ]

    if formulario.validate_on_submit():
        dispositivo = DispositivoDAO.obtener_por_id(formulario.dispositivo_id.data)

        # Paso 1: Crear el DTO y registrar la entrega
        dto = EntregaDTO(
            usuario_id=current_user.id,
            dispositivo_id=formulario.dispositivo_id.data,
            punto_recoleccion_id=formulario.punto_recoleccion_id.data
        )

        # Paso 2: Calcular los puntos según la categoría del dispositivo
        puntos = GamificacionService.calcular_puntos(dispositivo.categoria)
        dto.puntos_otorgados = puntos

        # Paso 3: Guardar la entrega en la BD
        entrega = EntregaDAO.crear(dto)

        # Paso 4: Sumar los puntos al usuario
        UsuarioDAO.sumar_puntos(current_user.id, puntos)

        # Paso 5: Agregar el bloque a la cadena de bloques
        datos_bloque = {
            'entrega_id': entrega.id,
            'usuario_id': current_user.id,
            'usuario_nombre': current_user.nombre,
            'dispositivo': dispositivo.nombre,
            'categoria': dispositivo.categoria,
            'punto_recoleccion_id': entrega.punto_recoleccion_id,
            'puntos_otorgados': puntos,
            'fecha': entrega.fecha_entrega.isoformat()
        }
        cadena = CadenaBloques.obtener_instancia()
        bloque = cadena.agregar_bloque(datos_bloque)

        # Paso 6: Persistir el bloque en la BD
        BloqueDAO.guardar_bloque(bloque)

        # Paso 7: Guardar el hash del bloque en la entrega para trazabilidad
        EntregaDAO.actualizar_hash_blockchain(entrega.id, bloque.hash_actual)

        flash(f'¡Entrega registrada! Ganaste {puntos} puntos. '
              f'Hash blockchain: {bloque.hash_actual[:16]}...', 'success')
        return redirect(url_for('entrega.listar'))

    return render_template('entrega/formulario.html',
                           formulario=formulario, titulo='Nueva entrega')


@entrega_bp.route('/<int:entrega_id>')
@login_required
def detalle(entrega_id):
    """Muestra el detalle completo de una entrega, incluyendo el hash blockchain."""
    entrega = EntregaDAO.obtener_por_id(entrega_id)
    if not entrega:
        flash('Entrega no encontrada.', 'warning')
        return redirect(url_for('entrega.listar'))
    return render_template('entrega/detalle.html',
                           entrega=entrega, titulo='Detalle de entrega')


@entrega_bp.route('/<int:entrega_id>/estado', methods=['POST'])
@login_required
@requiere_rol('empresa', 'gobierno')
def actualizar_estado(entrega_id):
    """Permite a empresas y gobierno actualizar el estado del proceso de una entrega."""
    from flask import request
    nuevo_estado = request.form.get('estado')
    estados_validos = ['pendiente', 'recibido', 'procesado', 'reciclado']

    if nuevo_estado not in estados_validos:
        flash('Estado no válido.', 'danger')
        return redirect(url_for('entrega.detalle', entrega_id=entrega_id))

    EntregaDAO.actualizar_estado(entrega_id, nuevo_estado)
    flash(f'Estado actualizado a "{nuevo_estado}" correctamente.', 'success')
    return redirect(url_for('entrega.detalle', entrega_id=entrega_id))

