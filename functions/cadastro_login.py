import db.connection
import bcrypt
import psycopg2
import time
from functions.limpar import limpar_tela

def cadastro():
    conn = db.connection.get_connection()
    cur = conn.cursor()

    nome = input("Digite seu nome: ")

    while len(nome) > 255 or len(nome) < 5:
        print("Nome inválido! Nome deve conter de 5 à 255 carecteres.")
        nome = input("Digite seu nome novamente: ")

    email = input("Digite seu e-mail: ")

    while (
        "@" not in email
        or "." not in email
        or email.startswith("@")
        or email.endswith("@")
        or email.count("@") != 1
    ):
        print("E-mail inválido. Tente novamente.")
        email = input("Digite seu e-mail novamente: ")

    senha = input("Digite sua senha: ")

    while len(senha) < 6 or len(senha) > 24:
        print("Senha inválida! A senha deve ter de 6 à 24 caracteres.")
        senha = input("Digite sua senha novamente: ")

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
    try:
        cur.execute(
            f"INSERT INTO usuario (nome, email, senha_hash) VALUES (%s, %s, %s);", (nome, email, senha_hash)
        )
        conn.commit()
        print(f"O usuário '{nome}' foi criado com sucesso.")
    
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Erro: Este e-mail já está cadastrado.")
    
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar usuário: ", e)
    
    finally:
        cur.close()
        conn.close()

def login(email, senha):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_usuario, nome, senha_hash FROM usuario WHERE email = %s;", (email,))
    resultado = cur.fetchone()

    cur.close()
    conn.close()

    if not resultado:
        print("\nUsuario não encontrado.")
        return False, None
    
    id_usuario = resultado[0]
    nome_usuario = resultado[1]
    senha_hash = resultado[2]

    if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
        print("\nLogin bem-sucedido! Aguarde um instante...")
        
        usuario = {
            "id": id_usuario,
            "nome": nome_usuario,
            "email": email
        }
        time.sleep(2)
        limpar_tela()
        
        return True, usuario # ou também o indice q o id tá
    else:
        print("\nSenha incorreta!")
        return False, None