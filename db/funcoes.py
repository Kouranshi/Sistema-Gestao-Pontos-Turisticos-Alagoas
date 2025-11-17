# db/funcoes.py
import db.connection
from functions.limpar import limpar_tela
import time

# Helpers / Validações
def _format_table(rows, headers):
    if not rows:
        return "(sem resultados)"
    widths = [max(len(str(c)) for c in col) for col in zip(*([headers] + rows))]
    sep = " | "
    line = "-+-".join("-" * w for w in widths)
    out = sep.join(h.ljust(w) for h, w in zip(headers, widths)) + "\n"
    out += line + "\n"
    for r in rows:
        out += sep.join(str(c).ljust(w) for c, w in zip(r, widths)) + "\n"
    return out

def usuario_existe(id_usuario):
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM usuario WHERE id_usuario = %s;", (id_usuario,))
        return cur.fetchone() is not None
    finally:
        cur.close()
        conn.close()

def ponto_existe_por_nome(nome):
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id_ponto_turistico FROM ponto_turistico WHERE LOWER(nome) = LOWER(%s);", (nome,))
        r = cur.fetchone()
        return r[0] if r else None
    finally:
        cur.close()
        conn.close()

# Listagem / Consultas
def mostrar_pontos_turisticos():
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id_ponto_turistico, nome, cidade, estado, cep
            FROM ponto_turistico
            ORDER BY nome;
        """)
        rows = cur.fetchall()
        if rows:
            headers = ("ID", "Nome", "Cidade", "Estado", "CEP")
            print("\n" + _format_table(rows, headers))
        else:
            print("\nNenhum ponto turístico cadastrado.")
            time.sleep(2)
            print("Voltando ao Menu Logado...")
            time.sleep(1.5)
            limpar_tela()
    except Exception as e:
        print("Erro ao listar pontos:", e)
    finally:
        cur.close()
        conn.close()

def mostrar_avaliacoes_usuario(id_usuario):
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                p.nome AS ponto_turistico,
                a.nota,
                a.comentario,
                a.data_avaliacao
            FROM avaliacao a
            JOIN ponto_turistico p ON a.id_ponto_turistico = p.id_ponto_turistico
            WHERE a.id_usuario = %s
            ORDER BY a.data_avaliacao DESC;
        """, (id_usuario,))
        rows = cur.fetchall()
        if rows:
            headers = ("Ponto", "Nota", "Comentário", "Data")
            print("\nAvaliações do usuário:\n" + _format_table(rows, headers))
        else:
            print("\nEsse usuário não tem avaliações.")
            time.sleep(2)
            print("Voltando ao Menu Logado...")
            time.sleep(1.5)
            limpar_tela()
    except Exception as e:
        print("Erro ao buscar avaliações do usuário:", e)
    finally:
        cur.close()
        conn.close()

def mostrar_avaliacoes_ponto(nome_ponto):
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                u.nome AS usuario,
                a.nota,
                a.comentario,
                a.data_avaliacao
            FROM avaliacao a
            JOIN usuario u ON a.id_usuario = u.id_usuario
            JOIN ponto_turistico p ON a.id_ponto_turistico = p.id_ponto_turistico
            WHERE LOWER(p.nome) = LOWER(%s)
            ORDER BY a.data_avaliacao DESC;
        """, (nome_ponto,))
        rows = cur.fetchall()
        if rows:
            headers = ("Usuário", "Nota", "Comentário", "Data")
            print(f"\nAvaliações do ponto '{nome_ponto}':\n" + _format_table(rows, headers))
        else:
            print(f"\nNenhuma avaliação encontrada para '{nome_ponto}'.")
            time.sleep(2)
            print("Voltando ao Menu Logado...")
            time.sleep(1.5)
            limpar_tela()
    except Exception as e:
        print("Erro ao buscar avaliações do ponto:", e)
    finally:
        cur.close()
        conn.close()

# ----------------------
# Cadastrar / Inserir
# ----------------------
def cadastrar_ponto_turistico(
    nome,
    estado,
    cep,
    cidade,
    descricao=None,
    horario_funcionamento=None,
    custo_entrada=None,
    logradouro=None,
    latitude=None,
    longitude=None,
    url_imagem_principal=None
):
    # Validações básicas
    while not nome or len(nome) < 3:
        print("Nome do ponto muito curto.")
        time.sleep(1.5)
        nome = input("Digite o nome do ponto turístico novamente: ")
    while not estado:
        print("Estado é obrigatório.")
        time.sleep(1.5)
        estado = input("Digite o nome do estado novamente: ")
    while not cep:
        print("CEP é obrigatório.")
        time.sleep(1.5)
        cep = input("Digite o CEP novamente: ")
    while not cidade:
        print("Cidade é obrigatório.")
        time.sleep(1.5)
        cidade = input("Digite o nome da cidade novamente: ")

    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO ponto_turistico
            (nome, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, url_imagem_principal)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_ponto_turistico;
        """, (nome, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, url_imagem_principal))
        inserted = cur.fetchone()[0]
        conn.commit()
        print(f"Ponto turístico '{nome}' cadastrado com ID {inserted}.")
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar ponto turístico:", e)
    finally:
        cur.close()
        conn.close()

def avaliar_ponto_turistico(id_usuario, nome_ponto, nota, comentario=None):
    # valida nota
    try:
        nota_int = int(nota)
    except ValueError:
        print("Nota inválida. Use um número inteiro (0-5).")
        return
    while nota_int < 0 or nota_int > 5:
        print("Nota fora do intervalo (0-5).")
        time.sleep(1.5)
        nota_int = int(input("Digite a nota novamente: "))
        return

    # valida usuario
    if not usuario_existe(id_usuario):
        print("Usuário não existe.")
        time.sleep(1.5)
        print("Voltando ao Menu Logado...")
        time.sleep(2)
        limpar_tela()
        return

    # busca ponto por nome
    id_ponto = ponto_existe_por_nome(nome_ponto)
    if not id_ponto:
        print("Ponto turístico não encontrado com esse nome.")
        time.sleep(1.5)
        print("Voltando ao Menu Logado...")
        time.sleep(2)
        limpar_tela()
        return

    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO avaliacao (id_usuario, id_ponto_turistico, nota, comentario)
            VALUES (%s, %s, %s, %s)
            RETURNING id_avaliacao;
        """, (id_usuario, id_ponto, nota_int, comentario))
        inserted = cur.fetchone()[0]
        conn.commit()
        print(f"Avaliação registrada com ID {inserted}.")
    except Exception as e:
        conn.rollback()
        print("Erro ao registrar avaliação:", e)
    finally:
        cur.close()
        conn.close()