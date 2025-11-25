import db.connection
from functions.limpar import limpar_tela
import unicodedata
import time
from decimal import Decimal, InvalidOperation
import inflect

p = inflect.engine()

def normalizar(texto):
    if not texto:
        return ""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def singularizar(texto):
    """Tenta transformar plural em singular."""
    normalizado = normalizar(texto)
    singular = p.singular_noun(normalizado)
    return singular if singular else normalizado

def _format_table(rows, headers):
    if not rows:
        return "(sem resultados)"

    # Limite de caracteres por coluna (controle total)
    MAX_COL_WIDTH = 40

    # Função para cortar textos longos
    def truncate(text):
        text = str(text)
        return text if len(text) <= MAX_COL_WIDTH else text[:MAX_COL_WIDTH-3] + "..."

    # Aplica o truncate em todas as células
    processed_rows = [
        tuple(truncate(c) for c in row)
        for row in rows
    ]

    # Calcula largura ideal das colunas
    widths = [
        max(len(str(h)), *(len(str(c)) for c in col))
        for h, col in zip(headers, zip(*processed_rows))
    ]

    sep = " | "
    line = "-+-".join("-" * w for w in widths)

    # Cabeçalho
    out = sep.join(h.ljust(w) for h, w in zip(headers, widths)) + "\n"
    out += line + "\n"

    # Linhas dos dados
    for r in processed_rows:
        out += sep.join(str(c).ljust(w) for c, w in zip(r, widths)) + "\n"

    return out


def listar_categorias():
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id_categoria, nome FROM categoria ORDER BY id_categoria ASC;")
        return cur.fetchall()
    except Exception as e:
        print("Erro ao listar categorias:", e)
        return []
    finally:
        cur.close()
        conn.close()


def mostrar_categorias():
    categorias = listar_categorias()

    if not categorias:
        print("\nNenhuma categoria cadastrada.")
        input("\nPressione ENTER para voltar...")
        limpar_tela()
        return

    print("\nCategorias disponíveis:\n")
    for cid, nome in categorias:
        print(f"{cid} - {nome}")

    input("\nPressione ENTER para voltar...")


def buscar_id_categoria_por_nome(nome_categoria):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    nome_normalizado = normalizar(nome_categoria)

    try:
        cur.execute("SELECT id_categoria, nome FROM categoria;")
        categorias = cur.fetchall()

        for cid, nome in categorias:
            if normalizar(nome) == nome_normalizado:
                return cid

        return None
    except Exception as e:
        print("Erro ao buscar ID da categoria:", e)
        return None
    finally:
        cur.close()
        conn.close()


def cadastrar_categoria():
    print("\n--- CADASTRAR NOVA CATEGORIA ---")
    nome_categoria = input("Digite o nome da nova categoria: ").strip()

    if not nome_categoria:
        print("\nO nome da categoria não pode estar vazio.")
        input("\nPressione ENTER para voltar...")
        limpar_tela()
        return

    # Normaliza e singulariza
    nome_normalizado = normalizar(nome_categoria)
    nome_singular = singularizar(nome_normalizado)

    # Nome exibível sem alterar o sentido, apenas formatando
    nome_exibicao = nome_singular.capitalize()

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        # Buscar todas categorias e evitar duplicados
        cur.execute("SELECT nome FROM categoria;")
        existentes = cur.fetchall()

        for (nome_existente,) in existentes:
            if singularizar(normalizar(nome_existente)) == nome_singular:
                print("\n❌ A categoria já existe (mesmo em plural ou acento diferente)!")
                input("\nPressione ENTER para voltar...")
                return

        # Inserção final
        cur.execute("""
            INSERT INTO categoria (nome, nome_exibicao)
            VALUES (%s, %s);
        """, (nome_singular, nome_exibicao))

        conn.commit()

        print(f"\n✅ Categoria '{nome_exibicao}' cadastrada com sucesso!")

    except Exception as e:
        conn.rollback()
        print("\nErro ao cadastrar categoria:", e)

    finally:
        input("\nPressione ENTER para voltar...")
        cur.close()
        conn.close()


def escolher_categoria():
    categorias = listar_categorias()

    if not categorias:
        print("\nNenhuma categoria cadastrada. Cadastre categorias na aba de 'Categorias' antes de usar o sistema.")
        input("\nPressione ENTER para voltar...")
        return None

    while True:
        print("\nSelecione a CATEGORIA do ponto turístico (*):\n")
        print("0. Voltar\n")

        for index, (_, nome) in enumerate(categorias, start=1):
            print(f"{index}. {nome}")

        escolha = input("\nDigite o número da categoria: ").strip()

        # Voltar
        if escolha == "0":
            print("\nVoltando ao menu anterior...")
            time.sleep(1)
            return None

        # Opção válida
        if escolha.isdigit():
            escolha_num = int(escolha)
            if 1 <= escolha_num <= len(categorias):
                id_categoria = categorias[escolha_num - 1][0]
                return id_categoria

        print("\nOpção inválida. Tente novamente.\n")


def listar_pontos_por_categoria(id_categoria):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT nome_exibicao, cidade, estado
            FROM ponto_turistico
            WHERE id_categoria = %s
            ORDER BY nome_exibicao;
        """, (id_categoria,))
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def mostrar_pontos_por_categoria():
    categorias = listar_categorias()

    if not categorias:
        print("\nNenhuma categoria cadastrada.")
        input("\nPressione ENTER...")
        limpar_tela()
        return

    print("\nCategorias:\n")
    for _, nome in categorias:
        print(f"- {nome}")

    nome_categoria = input("\nDigite o nome da categoria: ").strip()

    id_categoria = buscar_id_categoria_por_nome(nome_categoria)

    if id_categoria is None:
        print("\nCategoria não encontrada!")
        input("\nPressione ENTER...")
        return

    pontos = listar_pontos_por_categoria(id_categoria)

    if not pontos:
        print(f"\nNenhum ponto cadastrado na categoria '{nome_categoria}'.")
        input("\nPressione ENTER...")
        return

    print(f"\nPontos turísticos da categoria '{nome_categoria}':\n")
    headers = ("Nome", "Cidade", "Estado")
    rows = [(p[0], p[1], p[2]) for p in pontos]

    print(_format_table(rows, headers))

    input("\nPressione ENTER para voltar...")


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
        cur.execute("SELECT id_ponto_turistico, nome FROM ponto_turistico;")
        pontos = cur.fetchall()

        for pid, nome in pontos:
            if normalizar(nome) == nome_normalizado:
                return pid

        return None

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

        if not rows:
            print("\nNenhum ponto turístico cadastrado.")
            time.sleep(2)
            return

        headers = ("ID", "Nome", "Cidade", "Estado", "CEP")
        print("\n" + _format_table(rows, headers))
        input("\nPressione ENTER...")
    finally:
        cur.close()
        conn.close()


def cadastrar_ponto_turistico():
    nome_exibicao = input("Nome do ponto turístico (*): ").strip()
    while len(nome_exibicao) < 3:
        print("Nome muito curto.")
        nome_exibicao = input("Digite novamente: ").strip()

    descricao = input("Descrição: ")
    horario_funcionamento = input("Horário de funcionamento: ")
    custo_entrada = input("Custo de entrada (0 = grátis): ")
    logradouro = input("Logradouro: ")

    cep = input("CEP (*): ").strip()
    while not cep:
        print("CEP é obrigatório.")
        cep = input("CEP: ").strip()
    while not cep.isdigit():
        print("CEP deve conter apenas dígitos.")
        cep = input("CEP: ").strip()

    estado = input("Estado (*): ").strip()
    while not estado:
        print("Estado obrigatório.")
        estado = input("Estado: ").strip()

    cidade = input("Cidade (*): ").strip()
    while not cidade:
        print("Cidade obrigatória.")
        cidade = input("Cidade: ").strip()

    def latitude_longitude_opcional(msg):
        while True:
            valor = input(msg).strip().replace(",", ".")
            if valor == "":
                return None
            try:
                return Decimal(valor)
            except InvalidOperation:
                print("Valor inválido!")

    latitude = latitude_longitude_opcional("Latitude: ")
    longitude = latitude_longitude_opcional("Longitude: ")

    nome_normalizado = normalizar(nome_exibicao)

    print("\n--- Categoria do Ponto (*) ---")
    id_categoria = escolher_categoria()

    if id_categoria is None:
        return

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO ponto_turistico
            (nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada,
             logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_ponto_turistico;
        """, (
            nome_normalizado, nome_exibicao, descricao,
            horario_funcionamento, custo_entrada,
            logradouro, cidade, estado, cep,
            latitude, longitude, id_categoria
        ))

        novo_id = cur.fetchone()[0]
        conn.commit()

        print(f"\nPonto turístico '{nome_exibicao}' cadastrado! (ID {novo_id})")
        time.sleep(2)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar:", e)

    finally:
        cur.close()
        conn.close()


def mostrar_avaliacoes_usuario(id_usuario):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                a.id_avaliacao,
                p.nome_exibicao, 
                a.nota, 
                a.comentario, 
                a.data_avaliacao
            FROM avaliacao a
            JOIN ponto_turistico p 
                ON a.id_ponto_turistico = p.id_ponto_turistico
            WHERE a.id_usuario = %s
            ORDER BY a.data_avaliacao DESC;
        """, (id_usuario,))

        rows = cur.fetchall()

        if not rows:
            print("\nVocê não possui avaliações.")
            time.sleep(2)
            return

        formatado = []
        for id_av, ponto, nota, comentario, data in rows:
            formatado.append((
                id_av,
                ponto,
                nota,
                comentario,
                data.strftime("%d/%m/%Y às %H:%M:%S")
            ))

        headers = ("ID", "Ponto", "Nota", "Comentário", "Data")
        print("\nMinhas Avaliações:\n" + _format_table(formatado, headers))
        input("\nENTER para voltar...")

    finally:
        cur.close()
        conn.close()


def mostrar_avaliacoes_ponto(nome_ponto):
    id_ponto = ponto_existe_por_nome(nome_ponto)
    if not id_ponto:
        print("\nPonto não encontrado.")
        time.sleep(2)
        return

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT u.nome, a.nota, a.comentario, a.data_avaliacao
            FROM avaliacao a
            JOIN usuario u ON u.id_usuario = a.id_usuario
            WHERE a.id_ponto_turistico = %s
            ORDER BY a.data_avaliacao DESC;
        """, (id_ponto,))

        rows = cur.fetchall()

        if not rows:
            print("\nNenhuma avaliação para este ponto.")
            time.sleep(2)
            return

        formatado = []
        for usuario, nota, comentario, data in rows:
            formatado.append((usuario, nota, comentario, data.strftime("%d/%m/%Y às %H:%M:%S")))

        headers = ("Usuário", "Nota", "Comentário", "Data")
        print(f"\nAvaliações de '{nome_ponto}':\n" + _format_table(formatado, headers))
        input("\nENTER para voltar...")

    finally:
        cur.close()
        conn.close()


def avaliar_ponto_turistico(id_usuario, nome_ponto, nota, comentario):
    try:
        nota_int = int(nota)
        if nota_int < 0 or nota_int > 5:
            raise ValueError
    except:
        print("A nota deve ser um número entre 0 e 5.")
        return

    id_ponto = ponto_existe_por_nome(nome_ponto)

    if not id_ponto:
        print("Ponto não encontrado.")
        time.sleep(2)
        return

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO avaliacao (id_usuario, id_ponto_turistico, nota, comentario)
            VALUES (%s, %s, %s, %s);
        """, (id_usuario, id_ponto, nota_int, comentario))

        conn.commit()
        print("\nAvaliação registrada!")
        time.sleep(2)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro ao avaliar:", e)

    finally:
        cur.close()
        conn.close()


def atualizar_nome_usuario(id_usuario, novo_nome):
    if len(novo_nome.strip()) < 3:
        print("Nome inválido!")
        return

    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE usuario SET nome = %s WHERE id_usuario = %s;",
                    (novo_nome, id_usuario))
        conn.commit()

        print("\nNome atualizado!")
        time.sleep(1.5)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro:", e)

    finally:
        cur.close()
        conn.close()


def excluir_avaliacao(id_usuario, id_avaliacao):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 1 FROM avaliacao 
            WHERE id_avaliacao = %s AND id_usuario = %s;
        """, (id_avaliacao, id_usuario))

        if not cur.fetchone():
            print("Você só pode excluir suas próprias avaliações!")
            time.sleep(2)
            return

        cur.execute("DELETE FROM avaliacao WHERE id_avaliacao = %s;", (id_avaliacao,))
        conn.commit()

        print("\nAvaliação excluída!")
        time.sleep(1.5)
        limpar_tela()

    except Exception as e:
        conn.rollback()
        print("Erro ao excluir:", e)

    finally:
        cur.close()
        conn.close()


def excluir_conta(id_usuario):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM avaliacao WHERE id_usuario = %s;", (id_usuario,))
        cur.execute("DELETE FROM usuario WHERE id_usuario = %s;", (id_usuario,))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Erro ao excluir conta:", e)

    finally:
        cur.close()
        conn.close()