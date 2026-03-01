"""
Controlador de Autenticación.
Gestiona el registro, login y logout de usuarios mediante Flask-Login.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.dao.usuario_dao import UsuarioDAO
from app.dto.usuario_dto import UsuarioDTO

# Blueprint de autenticación con prefijo /auth
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ────────────────────────── Formularios ──────────────────────────

class FormularioLogin(FlaskForm):
    """Formulario de inicio de sesión."""
    email = StringField('Correo electrónico',
                        validators=[DataRequired(message='El email es requerido.'),
                                    Email(message='Ingresa un email válido.')])
    password = PasswordField('Contraseña',
                             validators=[DataRequired(message='La contraseña es requerida.')])
    submit = SubmitField('Iniciar sesión')


class FormularioRegistro(FlaskForm):
    """Formulario de registro de nuevo usuario."""
    nombre = StringField('Nombre completo',
                         validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Correo electrónico',
                        validators=[DataRequired(), Email()])
    ciudad = StringField('Ciudad', validators=[Length(max=100)])
    tipo_usuario = SelectField('Tipo de usuario',
                               choices=[('ciudadano', 'Ciudadano'),
                                        ('empresa', 'Empresa'),
                                        ('gobierno', 'Gobierno')])
    password = PasswordField('Contraseña',
                             validators=[DataRequired(), Length(min=6)])
    confirmar_password = PasswordField('Confirmar contraseña',
                                       validators=[DataRequired(),
                                                   EqualTo('password',
                                                           message='Las contraseñas no coinciden.')])
    submit = SubmitField('Registrarse')


# ────────────────────────── Rutas ──────────────────────────

@auth_bp.route('/')
def index():
    """Página de inicio — redirige según el estado de autenticación."""
    if current_user.is_authenticated:
        return redirect(url_for('entrega.listar'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Muestra el formulario de login (GET) y procesa el inicio de sesión (POST).
    Si el usuario ya está autenticado, lo redirige directamente.
    """
    if current_user.is_authenticated:
        return redirect(url_for('entrega.listar'))

    formulario = FormularioLogin()

    if formulario.validate_on_submit():
        usuario = UsuarioDAO.obtener_por_email(formulario.email.data)

        # Verificar que el usuario existe, está activo y la contraseña es correcta
        if usuario and usuario.activo and usuario.verificar_password(formulario.password.data):
            login_user(usuario)
            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            # Redirigir a la página que el usuario intentaba visitar antes del login
            siguiente = request.args.get('next')
            return redirect(siguiente or url_for('entrega.listar'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html', formulario=formulario, titulo='Iniciar sesión')


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Muestra el formulario de registro (GET) y crea el nuevo usuario (POST).
    """
    if current_user.is_authenticated:
        return redirect(url_for('entrega.listar'))

    formulario = FormularioRegistro()

    if formulario.validate_on_submit():
        # Verificar que el email no esté ya registrado
        if UsuarioDAO.email_existe(formulario.email.data):
            flash('Ese correo electrónico ya está registrado.', 'warning')
            return render_template('auth/registro.html', formulario=formulario, titulo='Registro')

        dto = UsuarioDTO(
            nombre=formulario.nombre.data,
            email=formulario.email.data,
            password=formulario.password.data,
            tipo_usuario=formulario.tipo_usuario.data,
            ciudad=formulario.ciudad.data
        )
        usuario = UsuarioDAO.crear(dto)
        flash('¡Cuenta creada exitosamente! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/registro.html', formulario=formulario, titulo='Crear cuenta')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario actual y redirige al login."""
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))

