import db.connection

def vincular_ponto_turistico_categoria(id_ponto_turistico, id_categoria):
    conn = db.connection.get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO ponto_turistico_categoria(id_ponto_turistico, id_categoria) VALUES (%s, %s);", (id_ponto_turistico, id_categoria)
        )
        conn.commit()
        print(f"Ponto: '{id_ponto_turistico}' vinculado à categoria: {id_categoria}")
    
    except Exception as e:
        conn.rollback()
        print("Erro ao vincular ponto e categoria: ", e)

    finally:
        cur.close()
        conn.close()