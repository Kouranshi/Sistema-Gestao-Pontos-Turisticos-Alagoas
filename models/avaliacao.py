import db.connection

def cadastrar_avaliacao(id_usuario, id_ponto_turistico, data_avaliacao, nota, comentario = None):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO avaliacao(nota, comentario, data_avaliacao, id_usuario, id_ponto_turistico) VALUES (%s, %s, %s, %s, %s);", (nota, comentario, data_avaliacao, id_usuario, id_ponto_turistico)
        )
        conn.commit()
        print("Avaliação registrada com sucesso!")

    except Exception as e:
        conn.rollback()
        print("Erro ao fazer avaliação: ", e)

    finally:
        cur.close()
        conn.close()

def mostrar_avaliacoes_usuario(id_usuario):
    query = "SELECT usuario.nome AS usuario, avaliacao.id_ponto_turistico, avaliacao.nota, avaliacao.data_avaliacao, avaliacao.comentario FROM usuario LEFT JOIN avaliacao ON usuario.id_usuario = avaliacao.id_usuario WHERE usuario.id_usuario = %s;", (id_usuario)
    return query

def mostrar_avaliacoes_ponto_turistico(nome_ponto_turistico):
    query = "SELECT ponto_turistico.nome AS ponto_turistico, usuario.nome AS usuario, avaliacao.nota, avaliacao.data_avaliacao, avaliacao.comentario FROM ponto_turistico LEFT JOIN avaliacao ON ponto_turistico.id_ponto_turistico = avaliacao.id_ponto_turistico LEFT JOIN usuario ON avaliacao.id_usuario = usuario.id_usuario WHERE LOWER(ponto_turistico.nome) = LOWER(%s);", (nome_ponto_turistico)
    return query