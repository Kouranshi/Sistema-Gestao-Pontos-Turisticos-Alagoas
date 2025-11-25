import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import time

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def criar_banco_se_nao_existir():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), [DB_NAME])
        existe = cur.fetchone()

        if not existe:
            cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DB_NAME)))
            print(f"Banco de dados '{DB_NAME}' criado com sucesso!")
            time.sleep(1.5)
        else:
            print(f"O banco de dados '{DB_NAME}' já existe.")
            time.sleep(1.5)

    except psycopg2.Error as e:
        print("Erro ao verificar/criar o banco:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return connection
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None


def testar_conexao():
    try:
        criar_banco_se_nao_existir()
        conn = get_connection()
        if conn:
            print(f"Conexão com o banco '{DB_NAME}' bem-sucedida!")
            conn.close()
            time.sleep(1.5)
            return True
        else:
            print("Falha na conexão com o banco de dados.")
            return False
    except Exception as e:
        print("Erro ao testar conexão: ", e)