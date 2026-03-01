"""
Controlador de Punto de Recolección.
Gestiona el CRUD de centros de acopio (solo empresa y gobierno pueden administrarlos).
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from app.dao.punto_recoleccion_dao import PuntoRecoleccionDAO
from app.controllers.decoradores import requiere_rol

punto_recoleccion_bp = Blueprint('punto_recoleccion', __name__, url_prefix='/puntos-recoleccion')


class FormularioPunto(FlaskForm):
    """Formulario para crear o editar un punto de recolección."""
    nombre = StringField('Nombre del punto', validators=[DataRequired(), Length(min=3, max=150)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=255)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(max=100)])
    horario = StringField('Horario de atención', validators=[Optional(), Length(max=200)])
    tipos_aceptados = StringField('Tipos aceptados (separados por coma)',
                                  validators=[Optional(), Length(max=255)])
    latitud = DecimalField('Latitud', validators=[Optional()], places=8)
    longitud = DecimalField('Longitud', validators=[Optional()], places=8)
    submit = SubmitField('Guardar punto')


@punto_recoleccion_bp.route('/')
@login_required
def listar():
    """Muestra todos los puntos de recolección activos."""
    puntos = PuntoRecoleccionDAO.obtener_todos()
    return render_template('punto_recoleccion/listar.html',
                           puntos=puntos, titulo='Puntos de recolección')


@punto_recoleccion_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_rol('empresa', 'gobierno')
def nuevo():
    """Crea un nuevo punto de recolección (solo empresa/gobierno)."""
    formulario = FormularioPunto()

    if formulario.validate_on_submit():
        PuntoRecoleccionDAO.crear(
            nombre=formulario.nombre.data,
            direccion=formulario.direccion.data,
            ciudad=formulario.ciudad.data,
            latitud=formulario.latitud.data,
            longitud=formulario.longitud.data,
            horario=formulario.horario.data,
            tipos_aceptados=formulario.tipos_aceptados.data
        )
        flash('Punto de recolección creado correctamente.', 'success')
        return redirect(url_for('punto_recoleccion.listar'))

    return render_template('punto_recoleccion/formulario.html',
                           formulario=formulario, titulo='Nuevo punto de recolección')


@punto_recoleccion_bp.route('/<int:punto_id>')
@login_required
def detalle(punto_id):
    """Muestra el detalle de un punto de recolección."""
    punto = PuntoRecoleccionDAO.obtener_por_id(punto_id)
    if not punto:
        flash('Punto de recolección no encontrado.', 'warning')
        return redirect(url_for('punto_recoleccion.listar'))
    return render_template('punto_recoleccion/detalle.html',
                           punto=punto, titulo='Detalle del punto')


@punto_recoleccion_bp.route('/<int:punto_id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_rol('empresa', 'gobierno')
def editar(punto_id):
    """Edita un punto de recolección existente."""
    punto = PuntoRecoleccionDAO.obtener_por_id(punto_id)
    if not punto:
        flash('Punto de recolección no encontrado.', 'warning')
        return redirect(url_for('punto_recoleccion.listar'))

    formulario = FormularioPunto(obj=punto)

    if formulario.validate_on_submit():
        PuntoRecoleccionDAO.actualizar(
            punto_id=punto_id,
            nombre=formulario.nombre.data,
            direccion=formulario.direccion.data,
            ciudad=formulario.ciudad.data,
            latitud=formulario.latitud.data,
            longitud=formulario.longitud.data,
            horario=formulario.horario.data,
            tipos_aceptados=formulario.tipos_aceptados.data
        )
        flash('Punto de recolección actualizado correctamente.', 'success')
        return redirect(url_for('punto_recoleccion.detalle', punto_id=punto_id))

    return render_template('punto_recoleccion/formulario.html',
                           formulario=formulario, punto=punto,
                           titulo='Editar punto de recolección')


@punto_recoleccion_bp.route('/<int:punto_id>/eliminar', methods=['POST'])
@login_required
@requiere_rol('empresa', 'gobierno')
def eliminar(punto_id):
    """Desactiva un punto de recolección (eliminación lógica)."""
    if PuntoRecoleccionDAO.eliminar(punto_id):
        flash('Punto de recolección desactivado correctamente.', 'success')
    else:
        flash('No se encontró el punto de recolección.', 'warning')
    return redirect(url_for('punto_recoleccion.listar'))

