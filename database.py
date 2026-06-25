import sqlite3

DB_NAME = "database.db"


def get_connection():
    """Abre uma conexão com o banco. row_factory permite acessar colunas pelo nome."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas se elas ainda não existirem. Chamado uma vez quando o app inicia."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            resumo TEXT,
            dificuldade INTEGER NOT NULL DEFAULT 1,
            data_revisao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        )
    """)

    conn.commit()
    conn.close()
