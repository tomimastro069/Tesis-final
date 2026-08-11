"""Módulo de persistencia para historial de FFUF.

Soporta dos motores:
- sqlite (por defecto, para uso local)
- postgres (vía variables de entorno, para Docker Compose)
"""

import os
import sqlite3
from datetime import datetime, timezone

try:
    import psycopg2
except ImportError:  # pragma: no cover - se resuelve por requirements en runtime
    psycopg2 = None


TABLE_NAME = "ffuf_history"
SQLMAP_TABLE = "sqlmap_history"
SQLMAP_TABLES_HISTORY = "sqlmap_tables_history"
VULN_TABLE = "vulnerable_urls"
SCANS_HISTORY_TABLE = "scans_history"
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()
DB_PATH = os.path.join(os.path.dirname(__file__), "history.db")


def _is_postgres() -> bool:
    return DB_ENGINE == "postgres"


def get_connection():
    """Crea una conexión a la base de datos según el motor configurado."""
    if _is_postgres():
        if psycopg2 is None:
            raise RuntimeError("psycopg2 no está instalado. Ejecuta pip install -r requirements.txt")

        import time
        max_retries = 3
        retry_delay = 1.0
        for i in range(max_retries):
            try:
                return psycopg2.connect(
                    host=os.getenv("DB_HOST", "db"),
                    port=int(os.getenv("DB_PORT", "5432")),
                    dbname=os.getenv("DB_NAME", "security_history"),
                    user=os.getenv("DB_USER", "security_user"),
                    password=os.getenv("DB_PASSWORD", "security_pass"),
                )
            except psycopg2.OperationalError as e:
                if i < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                raise e

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
                wordlist_name TEXT NOT NULL DEFAULT 'default',
                word TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(target_url, wordlist_name, word)
            )
            """
        )
        cursor.execute(
            f"""
            CREATE INDEX IF NOT EXISTS idx_target ON {TABLE_NAME}(target_url)
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SQLMAP_TABLE} (
                url TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {VULN_TABLE} (
                url TEXT NOT NULL,
                tool TEXT NOT NULL,
                vulnerabilidad TEXT NOT NULL,
                severidad TEXT NOT NULL DEFAULT 'Desconocida',
                primera_vez TEXT NOT NULL,
                ultima_vez TEXT NOT NULL,
                PRIMARY KEY (url, tool, vulnerabilidad)
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SCANS_HISTORY_TABLE} (
                scan_id TEXT PRIMARY KEY,
                target_url TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                results_raw TEXT,
                is_active BOOLEAN DEFAULT TRUE
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SQLMAP_TABLES_HISTORY} (
                id SERIAL PRIMARY KEY,
                target_url TEXT NOT NULL,
                db_name TEXT NOT NULL,
                table_name TEXT NOT NULL,
                columns_data TEXT NOT NULL,
                rows_data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
    else:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT NOT NULL,
                wordlist_name TEXT NOT NULL DEFAULT 'default',
                word TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(target_url, wordlist_name, word)
            )
            """
        )
        cursor.execute(
            f"""
            CREATE INDEX IF NOT EXISTS idx_target ON {TABLE_NAME}(target_url)
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SQLMAP_TABLE} (
                url TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {VULN_TABLE} (
                url TEXT NOT NULL,
                tool TEXT NOT NULL,
                vulnerabilidad TEXT NOT NULL,
                severidad TEXT NOT NULL DEFAULT 'Desconocida',
                primera_vez TEXT NOT NULL,
                ultima_vez TEXT NOT NULL,
                PRIMARY KEY (url, tool, vulnerabilidad)
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SCANS_HISTORY_TABLE} (
                scan_id TEXT PRIMARY KEY,
                target_url TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                results_raw TEXT,
                is_active BOOLEAN DEFAULT TRUE
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {SQLMAP_TABLES_HISTORY} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT NOT NULL,
                db_name TEXT NOT NULL,
                table_name TEXT NOT NULL,
                columns_data TEXT NOT NULL,
                rows_data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )

    conn.commit()

    # Migration for existing tables
    if _is_postgres():
        try:
            cursor.execute(f"ALTER TABLE {SCANS_HISTORY_TABLE} ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
            conn.commit()
        except Exception:
            conn.rollback()
    else:
        try:
            cursor.execute(f"ALTER TABLE {SCANS_HISTORY_TABLE} ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
            conn.commit()
        except Exception:
            pass

    conn.close()

def create_scan(scan_id: str, target_url: str):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    if _is_postgres():
        cursor.execute(
            f"INSERT INTO {SCANS_HISTORY_TABLE} (scan_id, target_url, status, created_at, results_raw, is_active) VALUES (%s, %s, %s, %s, %s, %s)",
            (scan_id, target_url, 'scanning', now, None, True)
        )
    else:
        cursor.execute(
            f"INSERT INTO {SCANS_HISTORY_TABLE} (scan_id, target_url, status, created_at, results_raw, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            (scan_id, target_url, 'scanning', now, None, True)
        )
    conn.commit()
    conn.close()

def soft_delete_scan(scan_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    if _is_postgres():
        cursor.execute(
            f"UPDATE {SCANS_HISTORY_TABLE} SET is_active = FALSE WHERE scan_id = %s",
            (scan_id,)
        )
    else:
        cursor.execute(
            f"UPDATE {SCANS_HISTORY_TABLE} SET is_active = 0 WHERE scan_id = ?",
            (scan_id,)
        )
    conn.commit()
    conn.close()

def update_scan_status(scan_id: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    if _is_postgres():
        cursor.execute(
            f"UPDATE {SCANS_HISTORY_TABLE} SET status = %s WHERE scan_id = %s",
            (status, scan_id)
        )
    else:
        cursor.execute(
            f"UPDATE {SCANS_HISTORY_TABLE} SET status = ? WHERE scan_id = ?",
            (status, scan_id)
        )
    conn.commit()
    conn.close()

def save_scan_results(scan_id: str, results_raw: str):
    conn = get_connection()
    cursor = conn.cursor()
    if _is_postgres():
        cursor.execute(
            f"UPDATE {SCANS_HISTORY_TABLE} SET status = %s, results_raw = %s WHERE scan_id = %s",
            ('completed', results_raw, scan_id)
        )
    else:
        cursor.execute(
            f"UPDATE {SCANS_HISTORY_TABLE} SET status = ?, results_raw = ? WHERE scan_id = ?",
            ('completed', results_raw, scan_id)
        )
    conn.commit()
    conn.close()

def get_scan_by_id(scan_id: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    if _is_postgres():
        cursor.execute(f"SELECT scan_id, target_url, status, created_at, results_raw FROM {SCANS_HISTORY_TABLE} WHERE scan_id = %s", (scan_id,))
    else:
        cursor.execute(f"SELECT scan_id, target_url, status, created_at, results_raw FROM {SCANS_HISTORY_TABLE} WHERE scan_id = ?", (scan_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "scan_id": row[0],
            "target_url": row[1],
            "status": row[2],
            "created_at": row[3],
            "results_raw": row[4]
        }
    return None

def get_all_scans() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    # is_active = TRUE in Postgres, 1 in SQLite
    if _is_postgres():
        cursor.execute(f"SELECT scan_id, target_url, status, created_at, results_raw FROM {SCANS_HISTORY_TABLE} WHERE is_active = TRUE ORDER BY created_at DESC")
    else:
        cursor.execute(f"SELECT scan_id, target_url, status, created_at, results_raw FROM {SCANS_HISTORY_TABLE} WHERE is_active = 1 ORDER BY created_at DESC")
        
    rows = cursor.fetchall()
    conn.close()
    
    scans = []
    for row in rows:
        scans.append({
            "scan_id": row[0],
            "target_url": row[1],
            "status": row[2],
            "created_at": row[3],
            "results_raw": row[4]
        })
    return scans


def get_tested_words(target_url: str, wordlist_name: str = "default") -> set:
    """
    Obtiene todas las palabras ya probadas para un target Y una wordlist específica.
    
    La clave de caché es (target_url + wordlist_name), así 'small' y 'medium'
    son cachés independientes y no se contaminan entre sí.
    
    Args:
        target_url (str): URL del target (sin trailing slash).
        wordlist_name (str): Nombre de la wordlist usada (ej: 'small', 'medium').
    
    Returns:
        set: Conjunto de palabras ya probadas para esa combinación.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Normalizar URL (quitar trailing slash)
    target_url = target_url.rstrip("/")
    
    if _is_postgres():
        cursor.execute(
            f"SELECT word FROM {TABLE_NAME} WHERE target_url = %s AND wordlist_name = %s",
            (target_url, wordlist_name),
        )
    else:
        cursor.execute(
            f"SELECT word FROM {TABLE_NAME} WHERE target_url = ? AND wordlist_name = ?",
            (target_url, wordlist_name),
        )
    
    words = {row[0] for row in cursor.fetchall()}
    conn.close()
    
    return words


def save_tested_words(target_url: str, words_list: list, wordlist_name: str = "default"):
    """
    Guarda un lote de palabras probadas para un target Y una wordlist específica.
    
    Args:
        target_url (str): URL del target (sin trailing slash).
        words_list (list): Lista de palabras a guardar.
        wordlist_name (str): Nombre de la wordlist usada (ej: 'small', 'medium').
    """
    if not words_list:
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Normalizar URL
    target_url = target_url.rstrip("/")
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    rows = [(target_url, wordlist_name, word, timestamp) for word in words_list]

    if _is_postgres():
        cursor.executemany(
            f"""
            INSERT INTO {TABLE_NAME} (target_url, wordlist_name, word, timestamp)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (target_url, wordlist_name, word) DO NOTHING
            """,
            rows,
        )
    else:
        # Insertar ignorando duplicados
        cursor.executemany(
            f"INSERT OR IGNORE INTO {TABLE_NAME} (target_url, wordlist_name, word, timestamp) VALUES (?, ?, ?, ?)",
            rows,
        )
    
    conn.commit()
    conn.close()


def is_url_tested_in_sqlmap(url: str) -> bool:
    """Verifica si una URL ya fue analizada por SQLMap."""
    conn = get_connection()
    cursor = conn.cursor()
    if _is_postgres():
        cursor.execute(f"SELECT 1 FROM {SQLMAP_TABLE} WHERE url = %s", (url,))
    else:
        cursor.execute(f"SELECT 1 FROM {SQLMAP_TABLE} WHERE url = ?", (url,))
    
    result = cursor.fetchone() is not None
    conn.close()
    return result


def save_tested_sqlmap_url(url: str):
    """Guarda una URL como probada en SQLMap."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now(timezone.utc).isoformat()
    
    if _is_postgres():
        cursor.execute(
            f"INSERT INTO {SQLMAP_TABLE} (url, timestamp) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING",
            (url, timestamp)
        )
    else:
        cursor.execute(
            f"INSERT OR IGNORE INTO {SQLMAP_TABLE} (url, timestamp) VALUES (?, ?)",
            (url, timestamp)
        )
        
    conn.commit()
    conn.close()


def save_vulnerable_url(url: str, tool: str, vulnerabilidad: str, severidad: str = "Desconocida"):
    """
    Marca una URL como vulnerable para que siempre sea re-testeada.
    
    Si la URL+tool+vulnerabilidad ya existe, actualiza 'ultima_vez' para
    registrar cuándo fue confirmada por última vez. Así se puede ver si
    sigue siendo débil en escaneos futuros.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    
    if _is_postgres():
        cursor.execute(
            f"""
            INSERT INTO {VULN_TABLE} (url, tool, vulnerabilidad, severidad, primera_vez, ultima_vez)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (url, tool, vulnerabilidad)
            DO UPDATE SET ultima_vez = EXCLUDED.ultima_vez, severidad = EXCLUDED.severidad
            """,
            (url, tool, vulnerabilidad, severidad, now, now)
        )
    else:
        # Intentar insertar nueva. Si ya existe, solo actualizar ultima_vez.
        cursor.execute(
            f"""
            INSERT INTO {VULN_TABLE} (url, tool, vulnerabilidad, severidad, primera_vez, ultima_vez)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (url, tool, vulnerabilidad)
            DO UPDATE SET ultima_vez = excluded.ultima_vez, severidad = excluded.severidad
            """,
            (url, tool, vulnerabilidad, severidad, now, now)
        )
    
    conn.commit()
    conn.close()


def get_vulnerable_urls(tool: str = None) -> set:
    """
    Devuelve el set de URLs que fueron vulnerables en algún escaneo anterior.
    SQLMap siempre las re-testeará sin importar el caché.
    
    Args:
        tool: Si se especifica (ej: "SQLMap"), solo devuelve URLs de esa herramienta.
              Si es None, devuelve todas.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if tool:
        if _is_postgres():
            cursor.execute(f"SELECT DISTINCT url FROM {VULN_TABLE} WHERE tool = %s", (tool,))
        else:
            cursor.execute(f"SELECT DISTINCT url FROM {VULN_TABLE} WHERE tool = ?", (tool,))
    else:
        cursor.execute(f"SELECT DISTINCT url FROM {VULN_TABLE}")
    
    urls = {row[0] for row in cursor.fetchall()}
    
    conn.close()
    return urls

import json

def save_sqlmap_tables(target_url: str, tables_data: dict):
    """
    Guarda las tablas extraídas de SQLMap en la base de datos.
    `tables_data` es el diccionario retornado por `parsear_tablas_log_sqlmap`.
    """
    if not tables_data:
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    
    rows_to_insert = []
    for db_name, tables in tables_data.items():
        for table_name, data in tables.items():
            cols_json = json.dumps(data.get("columns", []))
            rows_json = json.dumps(data.get("rows", []))
            rows_to_insert.append((target_url, db_name, table_name, cols_json, rows_json, now))

    if _is_postgres():
        cursor.executemany(
            f"""
            INSERT INTO {SQLMAP_TABLES_HISTORY} (target_url, db_name, table_name, columns_data, rows_data, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            rows_to_insert
        )
    else:
        cursor.executemany(
            f"""
            INSERT INTO {SQLMAP_TABLES_HISTORY} (target_url, db_name, table_name, columns_data, rows_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows_to_insert
        )
        
    conn.commit()
    conn.close()

def get_sqlmap_tables_history(target_url: str) -> list:
    """
    Recupera el historial de tablas extraídas para un target.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if _is_postgres():
        cursor.execute(f"SELECT db_name, table_name, columns_data, rows_data, timestamp FROM {SQLMAP_TABLES_HISTORY} WHERE target_url = %s ORDER BY timestamp DESC", (target_url,))
    else:
        cursor.execute(f"SELECT db_name, table_name, columns_data, rows_data, timestamp FROM {SQLMAP_TABLES_HISTORY} WHERE target_url = ? ORDER BY timestamp DESC", (target_url,))
        
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        result.append({
            "db_name": row[0],
            "table_name": row[1],
            "columns": json.loads(row[2]),
            "rows": json.loads(row[3]),
            "timestamp": row[4]
        })
    return result

def limpiar_cache_completa():
    """
    Borra todo el historial de FFUF, SQLMap y URLs vulnerables.
    Útil para empezar escaneos desde cero con nuevas configuraciones.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    tablas = [TABLE_NAME, SQLMAP_TABLE, VULN_TABLE, SQLMAP_TABLES_HISTORY]
    
    if _is_postgres():
        tablas_str = ", ".join(tablas)
        cursor.execute(f"TRUNCATE TABLE {tablas_str} CASCADE;")
    else:
        for tabla in tablas:
            cursor.execute(f"DELETE FROM {tabla};")
            
    conn.commit()
    conn.close()
    print("[✓] Caché de base de datos limpiada por completo.")
