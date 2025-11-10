from db.connection import testar_conexao
from werkzeug.security import generate_password_hash, check_password_hash
from getpass import getpass 

def cadastro(nome, email, senha_hash):
    conn = testar_conexao()
    print("\n=== Cadastro de Usuário ===")
    nome = input("Nome: ")

    # abre o cursor
    cursor = conn.cursor()

    # valida se o email é unico
    while True:
        email = input("Email: ")
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            print("Erro: Email já cadastrado. Tente outro.\n")
        else:
            print("Email válido!\n")
            break

    #valida a senha
    while True:
        senha = getpass("Digite sua senha (8 a 24 caracteres): ")
        if len(senha) < 8 or len(senha) > 24:
            print("Erro: A senha deve ter entre 8 e 24 caracteres.\n")
        else:
            print("Senha válida!\n")
            break

    senha_hash = generate_password_hash(senha)
    
    #insere no banco
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha_hash)
        )
        data_cadastro = cursor.fetchone()
        conn.commit()

        print("Usuário cadastrado com sucesso!")

    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar usuário:", e)

    # fecha o cursor e a conexão
    finally:
        cursor.close()
        conn.close()

def login():
    conn = testar_conexao()
    print("\n=== Login de Usuário ===")

    email = input("Email: ")
    senha = getpass("Senha: ")
 
    # abre o cursor
    cursor = conn.cursor()

    # verifica credenciais
    cursor.execute("SELECT id_usuario, senha_hash FROM usuario WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    # valida login
    if usuario and check_password_hash(usuario[1], senha):
        print("Login bem-sucedido!")
    else:
        print("Erro: Email ou senha inválidos.")

    cursor.close()
    conn.close()
    return