import db.connection

def cadastrar_categoria(nome, descricao = None):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO categoria(nome, descricao) VALUES (%s, %s);", (nome, descricao)
        )
        conn.commit()
        print(f"Categoria: '{nome}' inserida com sucesso.")

    except Exception as e:
        conn.rollback()
        print("Erro ao criar categoria: ", e)

    finally:
        cur.close()
        conn.close()