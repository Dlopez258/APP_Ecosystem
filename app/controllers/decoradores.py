"""
Decoradores de roles para proteger rutas según el tipo de usuario.
Se usan como @requiere_rol('gobierno') sobre las funciones de vista.
"""

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def requiere_rol(*roles):
    """
    Decorador que restringe el acceso a una ruta a usuarios con roles específicos.

    Uso:
        @requiere_rol('gobierno')
        @requiere_rol('empresa', 'gobierno')

    Args:
        *roles: Uno o más tipos de usuario permitidos.

    Returns:
        function: Decorador que verifica el rol antes de ejecutar la vista.
    """
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

