"""
Controlador de Dispositivo.
Gestiona el CRUD de dispositivos electrónicos (RAEE) de los usuarios.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from app.dao.dispositivo_dao import DispositivoDAO
from app.dto.dispositivo_dto import DispositivoDTO

dispositivo_bp = Blueprint('dispositivo', __name__, url_prefix='/dispositivos')


class FormularioDispositivo(FlaskForm):
    """Formulario para registrar o editar un dispositivo electrónico."""
    nombre = StringField('Nombre del dispositivo',
                         validators=[DataRequired(), Length(min=2, max=100)])
    categoria = SelectField('Categoría',
                            choices=[('celular', 'Celular'),
                                     ('computador', 'Computador'),
                                     ('bateria', 'Batería'),
                                     ('electrodomestico', 'Electrodoméstico'),
                                     ('tarjeta_madre', 'Tarjeta Madre'),
                                     ('tablet', 'Tablet'),
                                     ('impresora', 'Impresora'),
                                     ('otro', 'Otro')])
    marca = StringField('Marca', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado',
                         choices=[('nuevo', 'Nuevo'),
                                  ('funcional', 'Funcional'),
                                  ('dañado', 'Dañado'),
                                  ('obsoleto', 'Obsoleto'),
                                  ('irreparable', 'Irreparable')])
    peso_kg = DecimalField('Peso (kg)', validators=[Optional()], places=2)
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Guardar dispositivo')


@dispositivo_bp.route('/')
@login_required
def listar():
    """Muestra los dispositivos del usuario actual (o todos si es gobierno)."""
    if current_user.tipo_usuario == 'gobierno':
        dispositivos = DispositivoDAO.obtener_todos()
    else:
        dispositivos = DispositivoDAO.obtener_por_usuario(current_user.id)
    return render_template('dispositivo/listar.html',
                           dispositivos=dispositivos, titulo='Mis dispositivos')


@dispositivo_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Muestra el formulario de registro (GET) y crea el dispositivo (POST)."""
    # Los usuarios de tipo gobierno no pueden registrar dispositivos
    if current_user.tipo_usuario == 'gobierno':
        flash('Los usuarios de gobierno no pueden registrar dispositivos.', 'warning')
        return redirect(url_for('dispositivo.listar'))

    formulario = FormularioDispositivo()

    if formulario.validate_on_submit():
        dto = DispositivoDTO(
            nombre=formulario.nombre.data,
            categoria=formulario.categoria.data,
            estado=formulario.estado.data,
            usuario_id=current_user.id,
            marca=formulario.marca.data,
            peso_kg=formulario.peso_kg.data,
            descripcion=formulario.descripcion.data
        )
        DispositivoDAO.crear(dto)
        flash('Dispositivo registrado correctamente.', 'success')
        return redirect(url_for('dispositivo.listar'))

    return render_template('dispositivo/formulario.html',
                           formulario=formulario, titulo='Registrar dispositivo')


@dispositivo_bp.route('/<int:dispositivo_id>')
@login_required
def detalle(dispositivo_id):
    """Muestra el detalle de un dispositivo específico."""
    dispositivo = DispositivoDAO.obtener_por_id(dispositivo_id)
    if not dispositivo:
        flash('Dispositivo no encontrado.', 'warning')
        return redirect(url_for('dispositivo.listar'))
    return render_template('dispositivo/detalle.html',
                           dispositivo=dispositivo, titulo='Detalle del dispositivo')


@dispositivo_bp.route('/<int:dispositivo_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(dispositivo_id):
    """Muestra el formulario de edición (GET) y guarda los cambios (POST)."""
    dispositivo = DispositivoDAO.obtener_por_id(dispositivo_id)
    if not dispositivo:
        flash('Dispositivo no encontrado.', 'warning')
        return redirect(url_for('dispositivo.listar'))

    # Solo el propietario o un gobierno puede editar el dispositivo
    if (current_user.tipo_usuario != 'gobierno' and
            dispositivo.usuario_id != current_user.id):
        flash('No tienes permiso para editar este dispositivo.', 'danger')
        return redirect(url_for('dispositivo.listar'))

    formulario = FormularioDispositivo(obj=dispositivo)

    if formulario.validate_on_submit():
        dto = DispositivoDTO(
            nombre=formulario.nombre.data,
            categoria=formulario.categoria.data,
            estado=formulario.estado.data,
            usuario_id=dispositivo.usuario_id,
            marca=formulario.marca.data,
            peso_kg=formulario.peso_kg.data,
            descripcion=formulario.descripcion.data
        )
        DispositivoDAO.actualizar(dispositivo_id, dto)
        flash('Dispositivo actualizado correctamente.', 'success')
        return redirect(url_for('dispositivo.detalle', dispositivo_id=dispositivo_id))

    return render_template('dispositivo/formulario.html',
                           formulario=formulario, dispositivo=dispositivo,
                           titulo='Editar dispositivo')


@dispositivo_bp.route('/<int:dispositivo_id>/eliminar', methods=['POST'])
@login_required
def eliminar(dispositivo_id):
    """Elimina un dispositivo de la base de datos."""
    dispositivo = DispositivoDAO.obtener_por_id(dispositivo_id)
    if not dispositivo:
        flash('Dispositivo no encontrado.', 'warning')
        return redirect(url_for('dispositivo.listar'))

    if (current_user.tipo_usuario != 'gobierno' and
            dispositivo.usuario_id != current_user.id):
        flash('No tienes permiso para eliminar este dispositivo.', 'danger')
        return redirect(url_for('dispositivo.listar'))

    DispositivoDAO.eliminar(dispositivo_id)
    flash('Dispositivo eliminado correctamente.', 'success')
    return redirect(url_for('dispositivo.listar'))

