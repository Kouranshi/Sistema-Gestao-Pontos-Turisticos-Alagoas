from db.connection import testar_conexao

def menu_principal():
    print("=== Sistema de Gestão de Pontos Turísticos de Alagoas ===\n")
    print("1 - Cadastrar novo usuário")
    print("2 - Login")
    print("3 - Sair")
    opcao = int(input("Escolha uma opção: "))
    return opcao

def main():
    testar_conexao()

if __name__ == "__main__":
    main()