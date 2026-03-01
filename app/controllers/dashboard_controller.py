"""
Controlador de Dashboard.
Proporciona estadísticas y gráficas para usuarios de tipo gobierno.
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.dao.entrega_dao import EntregaDAO
from app.dao.usuario_dao import UsuarioDAO
from app.dao.punto_recoleccion_dao import PuntoRecoleccionDAO
from app.dao.dispositivo_dao import DispositivoDAO
from app.controllers.decoradores import requiere_rol

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Nombres de los meses en español para las etiquetas del gráfico
MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']


@dashboard_bp.route('/')
@login_required
@requiere_rol('gobierno')
def index():
    """
    Dashboard principal de estadísticas para gobierno.
    Recopila datos agregados de todas las entidades para mostrar gráficas con Chart.js.
    """
    # ── Datos por categoría de dispositivo ──
    datos_categoria = EntregaDAO.contar_por_categoria()
    labels_categoria = [row[0] for row in datos_categoria]
    valores_categoria = [row[1] for row in datos_categoria]

    # ── Datos por ciudad ──
    datos_ciudad = EntregaDAO.contar_por_ciudad()
    labels_ciudad = [row[0] for row in datos_ciudad]
    valores_ciudad = [row[1] for row in datos_ciudad]

    # ── Tendencia mensual ──
    datos_mensuales = EntregaDAO.tendencia_mensual()
    # Construir un dict {mes: total} y rellenar los 12 meses
    mapa_mensual = {int(row[0]): int(row[1]) for row in datos_mensuales}
    valores_mensuales = [mapa_mensual.get(mes, 0) for mes in range(1, 13)]

    # ── Estadísticas generales ──
    total_usuarios = len(UsuarioDAO.obtener_todos())
    total_entregas = len(EntregaDAO.obtener_todas())
    total_puntos = PuntoRecoleccionDAO.obtener_todos()
    total_puntos_activos = len(total_puntos)

    # ── Ranking de puntos de recolección más activos ──
    from app import db
    from app.models.entrega import Entrega
    from app.models.punto_recoleccion import PuntoRecoleccion
    ranking_puntos = db.session.query(
        PuntoRecoleccion.nombre,
        PuntoRecoleccion.ciudad,
        db.func.count(Entrega.id).label('total')
    ).join(Entrega, Entrega.punto_recoleccion_id == PuntoRecoleccion.id)\
     .group_by(PuntoRecoleccion.id)\
     .order_by(db.func.count(Entrega.id).desc())\
     .limit(5).all()

    return render_template(
        'dashboard/index.html',
        titulo='Dashboard de Gobierno',
        # Datos para gráfica de categorías
        labels_categoria=labels_categoria,
        valores_categoria=valores_categoria,
        # Datos para gráfica de ciudades
        labels_ciudad=labels_ciudad,
        valores_ciudad=valores_ciudad,
        # Datos para gráfica de tendencia mensual
        labels_meses=MESES,
        valores_mensuales=valores_mensuales,
        # Estadísticas generales
        total_usuarios=total_usuarios,
        total_entregas=total_entregas,
        total_puntos_activos=total_puntos_activos,
        # Ranking
        ranking_puntos=ranking_puntos
    )

