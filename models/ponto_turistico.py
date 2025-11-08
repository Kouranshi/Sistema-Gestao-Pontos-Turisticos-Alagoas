import db.connection

def cadastrar_ponto_turistico(nome, estado, cidade, cep, logradouro = None, descricao = None, custo_entrada = None, horario_funcionamento = None, latitude = None, longitude = None, url_imagem_principal = None):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO ponto_turistico (nome, descricao, horario_funcionamento, custo_entrada, logradouro, estado, cidade, cep, latitude, longitude, url_imagem_principal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (nome, descricao, horario_funcionamento, custo_entrada, logradouro, estado, cidade, cep, latitude, longitude, url_imagem_principal)
        )
        conn.commit()
        print(f"Ponto Turístico: '{nome}' cadastrado com sucesso!")
    
    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar ponto turístico: ", e)
    
    finally:
        cur.close()
        conn.close()