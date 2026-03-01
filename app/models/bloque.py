"""
Modelo de Bloque para la blockchain simulada.
Persiste los bloques de la cadena en la base de datos para consultas históricas.
"""

from datetime import datetime
from app import db


class Bloque(db.Model):
    """
    Modelo de bloque en la cadena de bloques simulada.

    Cada entrega genera un bloque que se persiste aquí.
    La cadena se puede verificar comparando hashes consecutivos.
    """

    __tablename__ = 'bloques_blockchain'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    indice = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Datos de la entrega en formato JSON (texto)
    datos = db.Column(db.Text, nullable=False)
    hash_previo = db.Column(db.String(256), nullable=False)
    hash_actual = db.Column(db.String(256), nullable=False)
    nonce = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Bloque #{self.indice} - Hash: {self.hash_actual[:16]}...>'

