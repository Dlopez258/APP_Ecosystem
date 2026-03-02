from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def requiere_rol(*roles):
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            # Verificar que el usuario esté autenticado y tenga el rol requerido
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.tipo_usuario not in roles:
                # Acceso denegado — el usuario no tiene permiso
                abort(403)
            return f(*args, **kwargs)
        return funcion_decorada
    return decorador

