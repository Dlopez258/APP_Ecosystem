"""Script para inicializar la base de datos SQLite de EcoSystem."""
import sys
import traceback

log_path = "init_db.log"

def escribir(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()

# Limpiar log anterior
open(log_path, "w", encoding="utf-8").close()

try:
    from app import create_app, db
    app = create_app('development')
    with app.app_context():
        db.create_all()
        escribir("OK - Tablas creadas correctamente en SQLite")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tablas = inspector.get_table_names()
        escribir(f"Tablas creadas: {tablas}")
except Exception as e:
    escribir(f"ERROR: {e}")
    escribir(traceback.format_exc())
    sys.exit(1)
