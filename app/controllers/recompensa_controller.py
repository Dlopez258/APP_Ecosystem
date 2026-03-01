"""
Controlador de Recompensa.
Gestiona el CRUD de recompensas y la vista de recompensas disponibles para el usuario.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

from app.dao.recompensa_dao import RecompensaDAO
from app.services.gamificacion_service import GamificacionService
from app.controllers.decoradores import requiere_rol

recompensa_bp = Blueprint('recompensa', __name__, url_prefix='/recompensas')


class FormularioRecompensa(FlaskForm):
    """Formulario para crear o editar una recompensa."""
    nombre = StringField('Nombre de la recompensa',
                         validators=[DataRequired(), Length(min=3, max=150)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
    puntos_requeridos = IntegerField('Puntos requeridos',
                                     validators=[DataRequired(),
                                                 NumberRange(min=1, message='Debe ser mayor a 0.')])
    tipo = SelectField('Tipo de recompensa',
                       choices=[('descuento', 'Descuento'),
                                ('producto', 'Producto'),
                                ('reconocimiento', 'Reconocimiento')])
    submit = SubmitField('Guardar recompensa')


@recompensa_bp.route('/')
@login_required
def listar():
    """
    Muestra las recompensas disponibles.
    El ciudadano ve solo las que puede canjear con sus puntos.
    El gobierno ve todas.
    """
    if current_user.tipo_usuario == 'gobierno':
        recompensas = RecompensaDAO.obtener_todas()
        recompensas_disponibles = []
    else:
        recompensas = RecompensaDAO.obtener_todas()
        recompensas_disponibles = GamificacionService.obtener_recompensas_disponibles(
            current_user.puntos_acumulados
        )
        # Determinar el nivel del usuario para mostrarlo en la vista
    nivel_info = GamificacionService.determinar_nivel(current_user.puntos_acumulados)
    puntos_faltantes = GamificacionService.puntos_para_siguiente_nivel(
        current_user.puntos_acumulados
    )

    return render_template('recompensa/listar.html',
                           recompensas=recompensas,
                           recompensas_disponibles=recompensas_disponibles,
                           nivel_info=nivel_info,
                           puntos_faltantes=puntos_faltantes,
                           titulo='Recompensas')


@recompensa_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@requiere_rol('gobierno')
def nueva():
    """Crea una nueva recompensa (solo gobierno)."""
    formulario = FormularioRecompensa()

    if formulario.validate_on_submit():
        RecompensaDAO.crear(
            nombre=formulario.nombre.data,
            descripcion=formulario.descripcion.data,
            puntos_requeridos=formulario.puntos_requeridos.data,
            tipo=formulario.tipo.data
        )
        flash('Recompensa creada correctamente.', 'success')
        return redirect(url_for('recompensa.listar'))

    return render_template('recompensa/formulario.html',
                           formulario=formulario, titulo='Nueva recompensa')


@recompensa_bp.route('/<int:recompensa_id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_rol('gobierno')
def editar(recompensa_id):
    """Edita una recompensa existente."""
    recompensa = RecompensaDAO.obtener_por_id(recompensa_id)
    if not recompensa:
        flash('Recompensa no encontrada.', 'warning')
        return redirect(url_for('recompensa.listar'))

    formulario = FormularioRecompensa(obj=recompensa)

    if formulario.validate_on_submit():
        RecompensaDAO.actualizar(
            recompensa_id=recompensa_id,
            nombre=formulario.nombre.data,
            descripcion=formulario.descripcion.data,
            puntos_requeridos=formulario.puntos_requeridos.data,
            tipo=formulario.tipo.data
        )
        flash('Recompensa actualizada correctamente.', 'success')
        return redirect(url_for('recompensa.listar'))

    return render_template('recompensa/formulario.html',
                           formulario=formulario, recompensa=recompensa,
                           titulo='Editar recompensa')


@recompensa_bp.route('/<int:recompensa_id>/eliminar', methods=['POST'])
@login_required
@requiere_rol('gobierno')
def eliminar(recompensa_id):
    """Desactiva una recompensa."""
    if RecompensaDAO.eliminar(recompensa_id):
        flash('Recompensa desactivada correctamente.', 'success')
    else:
        flash('No se encontró la recompensa.', 'warning')
    return redirect(url_for('recompensa.listar'))

