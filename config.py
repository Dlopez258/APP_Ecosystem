"""
Configuración de la aplicación EcoSystem.
Define diferentes entornos: desarrollo, pruebas y producción.
"""

import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


class Config:
    """Configuración base compartida por todos los entornos."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-desarrollo-ecosistema')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Protección CSRF activada por defecto
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """
    Configuración para el entorno de desarrollo.
    Usa SQLite para no depender de MySQL durante el desarrollo local.
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///ecosystem_dev.db'  # SQLite por defecto en desarrollo
    )


class TestingConfig(Config):
    """
    Configuración para el entorno de pruebas.
    Usa SQLite en memoria para que cada test sea independiente.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Desactivar CSRF en pruebas para simplificar los tests
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """
    Configuración para el entorno de producción.
    Requiere la variable DATABASE_URL configurada en el servidor.
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


# Diccionario para seleccionar la configuración según la variable de entorno FLASK_ENV
configuraciones = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

