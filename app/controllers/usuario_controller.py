"""
Controlador de Usuario.
Gestiona el CRUD de usuarios (solo accesible para administradores/gobierno).
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from app.dao.usuario_dao import UsuarioDAO
from app.dto.usuario_dto import UsuarioDTO
from app.controllers.decoradores import requiere_rol

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')


class FormularioUsuario(FlaskForm):
    """Formulario para editar datos de un usuario."""
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    ciudad = StringField('Ciudad', validators=[Length(max=100)])
    tipo_usuario = SelectField('Tipo de usuario',
                               choices=[('ciudadano', 'Ciudadano'),
                                        ('empresa', 'Empresa'),
                                        ('gobierno', 'Gobierno')])
    submit = SubmitField('Guardar cambios')


@usuario_bp.route('/')
@login_required
@requiere_rol('gobierno')
def listar():
    """Muestra la lista de todos los usuarios activos del sistema."""
    usuarios = UsuarioDAO.obtener_todos()
    return render_template('usuario/listar.html', usuarios=usuarios, titulo='Usuarios')


@usuario_bp.route('/<int:usuario_id>')
@login_required
def detalle(usuario_id):
    """Muestra el perfil y detalle de un usuario específico."""
    usuario = UsuarioDAO.obtener_por_id(usuario_id)
    if not usuario:
        flash('Usuario no encontrado.', 'warning')
        return redirect(url_for('usuario.listar'))
    return render_template('usuario/detalle.html', usuario=usuario, titulo='Perfil de usuario')


@usuario_bp.route('/<int:usuario_id>/editar', methods=['GET', 'POST'])
@login_required
@requiere_rol('gobierno')
def editar(usuario_id):
    """Muestra el formulario de edición (GET) y guarda los cambios (POST)."""
    usuario = UsuarioDAO.obtener_por_id(usuario_id)
    if not usuario:
        flash('Usuario no encontrado.', 'warning')
        return redirect(url_for('usuario.listar'))

    formulario = FormularioUsuario(obj=usuario)

    if formulario.validate_on_submit():
        dto = UsuarioDTO(
            nombre=formulario.nombre.data,
            email=formulario.email.data,
            password=None,
            tipo_usuario=formulario.tipo_usuario.data,
            ciudad=formulario.ciudad.data
        )
        UsuarioDAO.actualizar(usuario_id, dto)
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuario.detalle', usuario_id=usuario_id))

    return render_template('usuario/editar.html', formulario=formulario,
                           usuario=usuario, titulo='Editar usuario')


@usuario_bp.route('/<int:usuario_id>/eliminar', methods=['POST'])
@login_required
@requiere_rol('gobierno')
def eliminar(usuario_id):
    """Desactiva un usuario del sistema (eliminación lógica)."""
    if UsuarioDAO.eliminar(usuario_id):
        flash('Usuario desactivado correctamente.', 'success')
    else:
        flash('No se encontró el usuario.', 'warning')
    return redirect(url_for('usuario.listar'))

