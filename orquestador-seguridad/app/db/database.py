"""Módulo de persistencia para historial de FFUF.

Soporta dos motores:
- sqlite (por defecto, para uso local)
- postgres (vía variables de entorno, para Docker Compose)
"""

import os
import sqlite3
from datetime import datetime

try:
    import psycopg2
except ImportError:  # pragma: no cover - se resuelve por requirements en runtime
    psycopg2 = None


TABLE_NAME = "ffuf_history"
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()
DB_PATH = os.path.join(os.path.dirname(__file__), "history.db")


def _is_postgres() -> bool:
    return DB_ENGINE == "postgres"


def get_connection():
    """Crea una conexión a la base de datos según el motor configurado."""
    if _is_postgres():
        if psycopg2 is None:
            raise RuntimeError("psycopg2 no está instalado. Ejecuta pip install -r requirements.txt")

        return psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "security_history"),
            user=os.getenv("DB_USER", "security_user"),
            password=os.getenv("DB_PASSWORD", "security_pass"),
        )

    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Inicializa la base de datos y crea la tabla si no existe.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if _is_postgres():
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                target_url TEXT NOT NULL,
                word TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(target_url, word)
            )
            """
        )
        cursor.execute(
            f"""
            CREATE INDEX IF NOT EXISTS idx_target ON {TABLE_NAME}(target_url)
            """
        )
    else:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT NOT NULL,
                word TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(target_url, word)
            )
            """
        )
        cursor.execute(
            f"""
            CREATE INDEX IF NOT EXISTS idx_target ON {TABLE_NAME}(target_url)
            """
        )

    conn.commit()
    conn.close()


def get_tested_words(target_url: str) -> set:
    """
    Obtiene todas las palabras ya probadas para un target.
    
    Args:
        target_url (str): URL del target (sin trailing slash).
    
    Returns:
        set: Conjunto de palabras ya probadas.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Normalizar URL (quitar trailing slash)
    target_url = target_url.rstrip("/")
    
    if _is_postgres():
        cursor.execute(
            f"SELECT word FROM {TABLE_NAME} WHERE target_url = %s",
            (target_url,),
        )
    else:
        cursor.execute(
            f"SELECT word FROM {TABLE_NAME} WHERE target_url = ?",
            (target_url,),
        )
    
    words = {row[0] for row in cursor.fetchall()}
    conn.close()
    
    return words


def save_tested_words(target_url: str, words_list: list):
    """
    Guarda un lote de palabras probadas para un target.
    
    Args:
        target_url (str): URL del target (sin trailing slash).
        words_list (list): Lista de palabras a guardar.
    """
    if not words_list:
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Normalizar URL
    target_url = target_url.rstrip("/")
    
    timestamp = datetime.now().isoformat()
    
    rows = [(target_url, word, timestamp) for word in words_list]

    if _is_postgres():
        cursor.executemany(
            f"""
            INSERT INTO {TABLE_NAME} (target_url, word, timestamp)
            VALUES (%s, %s, %s)
            ON CONFLICT (target_url, word) DO NOTHING
            """,
            rows,
        )
    else:
        # Insertar ignorando duplicados
        cursor.executemany(
            f"INSERT OR IGNORE INTO {TABLE_NAME} (target_url, word, timestamp) VALUES (?, ?, ?)",
            rows,
        )
    
    conn.commit()
    conn.close()
