from db.connection import testar_conexao
from cadastro import cadastro, login
from limpar import limpar_tela

def main():
    print("=== Sistema de Gestão de Pontos Turísticos de Alagoas ===\n")
    testar_conexao()
    print("Digite 1 - Cadastro  2 - Login  3 - Sair")
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        limpar_tela()
        cadastro()
    elif opcao == "2":
        limpar_tela()
        login()
    elif opcao == "3":
        limpar_tela()
        print("Saindo...")
    else:
        print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()