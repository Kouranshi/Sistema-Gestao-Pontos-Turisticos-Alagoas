import db.connection
from functions.limpar import limpar_tela
import unicodedata
import time
from decimal import Decimal, InvalidOperation
from datetime import datetime

def normalizar(texto):
    if not texto:
        return ""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

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


def ponto_existe_por_nome(nome_digitado):
    nome_normalizado = normalizar(nome_digitado)

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id_ponto_turistico
            FROM ponto_turistico
            WHERE nome = %s;
        """, (nome_normalizado,))

        r = cur.fetchone()
        return r[0] if r else None

    finally:
        cur.close()
        conn.close()

def mostrar_pontos_turisticos():
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id_ponto_turistico, nome_exibicao, cidade, estado, cep
            FROM ponto_turistico
            ORDER BY id_ponto_turistico ASC;
        """)
        rows = cur.fetchall()

        if rows:
            headers = ("ID", "Nome", "Cidade", "Estado", "CEP")
            print("\n" + _format_table(rows, headers))
            input("\nPressione ENTER para voltar ao menu...")
        else:
            print("\nNenhum ponto turístico cadastrado.")
            time.sleep(2)

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
            rows_formatado = []
            for ponto, nota, comentario, data in rows:
                data_formatada = data.strftime("%d/%m/%Y às %H:%M:%S")
                rows_formatado.append((ponto, nota, comentario, data_formatada))

            headers = ("Ponto", "Nota", "Comentário", "Data")
            print("\nAvaliações do usuário:\n" + _format_table(rows_formatado, headers))
            input("\nPressione ENTER para voltar ao menu...")
        else:
            print("\nEsse usuário não tem avaliações.")
            time.sleep(2)
            limpar_tela()
    finally:
        cur.close()
        conn.close()

def mostrar_avaliacoes_ponto(nome_ponto):
    nome_normalizado = normalizar(nome_ponto)

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT u.nome, a.nota, a.comentario, a.data_avaliacao
            FROM avaliacao a
            JOIN usuario u ON u.id_usuario = a.id_usuario
            JOIN ponto_turistico p ON p.id_ponto_turistico = a.id_ponto_turistico
            WHERE p.nome = %s
            ORDER BY a.data_avaliacao DESC;
        """, (nome_normalizado,))
        rows = cur.fetchall()
        if rows:
            rows_formatado = []
            for usuario, nota, comentario, data in rows:
                data_formatada = data.strftime("%d/%m/%Y às %H:%M:%S")
                rows_formatado.append((usuario, nota, comentario, data_formatada))

            headers = ("Usuário", "Nota", "Comentário", "Data")
            print(f"\nAvaliações do ponto '{nome_ponto}':\n" + _format_table(rows_formatado, headers))
            input("\nPressione ENTER para voltar ao menu...")
        else:
            print(f"\nNenhuma avaliação encontrada para '{nome_ponto}'.")
            time.sleep(2)
            limpar_tela()
    finally:
        cur.close()
        conn.close()

def cadastrar_ponto_turistico():
    nome_exibicao = input("Nome do ponto turístico (*): ")
    # validações obrigatórias
    while not nome_exibicao or len(nome_exibicao) < 3:
        print("Nome muito curto.")
        nome_exibicao = input("Digite novamente: ")

    descricao = input("Descrição: ")
    horario_funcionamento = input("Horário de funcionamento: ")
    custo_entrada = input("Custo de entrada (ou 0 se gratuito): ")
    logradouro = input("Logradouro: ")

    cep = input("CEP (Apenas números) (*): ")
    while not cep:
        print("CEP é obrigatório.")
        cep = input("CEP: ")

    estado = input("Estado (*): ")
    while not estado:
        print("Estado é obrigatório.")
        estado = input("Estado: ")

    cidade = input("Cidade (*): ")
    while not cidade:
        print("Cidade é obrigatório.")
        cidade = input("Cidade: ")

    def latitude_longitude_opcional(string):
        while True:
            valor = input(string).strip().replace(",", ".")

            if valor == "":
                return None
            
            try:
                return Decimal(valor)
            except InvalidOperation:
                print("Valor inválido! Digite números como: -9.665432 ou deixe em branco.")
    
    latitude = latitude_longitude_opcional("Latitude: ")
    longitude = latitude_longitude_opcional("Longitude: ")

    # nome normalizado
    nome_normalizado = normalizar(nome_exibicao)

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO ponto_turistico
            (nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada,
             logradouro, cidade, estado, cep, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_ponto_turistico;
        """, (
            nome_normalizado,
            nome_exibicao,
            descricao,
            horario_funcionamento,
            custo_entrada,
            logradouro,
            cidade,
            estado,
            cep,
            latitude,
            longitude
        ))

        novo_id = cur.fetchone()[0]
        conn.commit()

        print(f"Ponto turístico '{nome_exibicao}' cadastrado com ID {novo_id}.")
        time.sleep(2)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar:", e)
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
        print("Nota deve ser entre 0 e 5.")
        nota_int = int(nota)
        return

    # valida usuário
    if not usuario_existe(id_usuario):
        print("Usuário não existe.")
        limpar_tela()
        return

    # busca ponto
    id_ponto = ponto_existe_por_nome(nome_ponto)
    if not id_ponto:
        print("Ponto não encontrado.")
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
        print(f"\nAvaliação registrada com ID {inserted}.")
        time.sleep(1.5)
        limpar_tela()
    except Exception as e:
        conn.rollback()
        print("Erro ao registrar avaliação:", e)
    finally:
        cur.close()
        conn.close()

def atualizar_nome_usuario(id_usuario, novo_nome):
    if not novo_nome or len(novo_nome) < 3:
        print("Nome inválido. Digite pelo menos 3 caracteres.")
        return

    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE usuario
            SET nome = %s
            WHERE id_usuario = %s;
        """, (novo_nome, id_usuario))
        
        conn.commit()
        print("\nNome atualizado com sucesso!")
        time.sleep(1.5)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar nome:", e)
    finally:
        cur.close()
        conn.close()

def excluir_conta(id_usuario):
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        # apagar avaliações primeiro (FK)
        cur.execute("""
            DELETE FROM avaliacao WHERE id_usuario = %s;
        """, (id_usuario,))

        # apagar o usuário
        cur.execute("""
            DELETE FROM usuario WHERE id_usuario = %s;
        """, (id_usuario,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Erro ao excluir conta:", e)
    finally:
        cur.close()
        conn.close()

def excluir_avaliacao(id_usuario, id_avaliacao):
    conn = db.connection.get_connection()
    cur = conn.cursor()
    try:
        # verificar se a avaliação é dele
        cur.execute("""
            SELECT 1 FROM avaliacao
            WHERE id_avaliacao = %s AND id_usuario = %s;
        """, (id_avaliacao, id_usuario))

        if not cur.fetchone():
            print("\nVocê não pode apagar essa avaliação (não é sua).")
            time.sleep(2)
            limpar_tela()
            return

        # apagar
        cur.execute("""
            DELETE FROM avaliacao
            WHERE id_avaliacao = %s;
        """, (id_avaliacao,))

        conn.commit()
        print("\nAvaliação excluída com sucesso!")
        time.sleep(1.5)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro ao excluir avaliação:", e)
    finally:
        cur.close()
        conn.close()