"""
Punto de entrada principal de la aplicación EcoSystem.
Ejecutar con: python run.py
"""

import os
from app import create_app

# Seleccionar configuración según la variable de entorno FLASK_ENV
entorno = os.getenv('FLASK_ENV', 'development')
app = create_app(entorno)

if __name__ == '__main__':
    # Ejecutar el servidor de desarrollo de Flask
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)

