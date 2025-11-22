from functions.cadastro_login import cadastro, login
from functions.limpar import limpar_tela
import time
from db.funcoes import (
    mostrar_pontos_turisticos,
    mostrar_avaliacoes_usuario,
    mostrar_avaliacoes_ponto,
    cadastrar_ponto_turistico,
    avaliar_ponto_turistico,
    atualizar_nome_usuario,
    excluir_avaliacao,
    excluir_conta
)

def menu_cadastro():
    print("╔══════════════════════════════════════╗")
    print("║        📝 Cadastro de Usuário        ║")
    print("╠══════════════════════════════════════╣")
    print("║ Por favor, insira os dados abaixo:   ║")
    print("╚══════════════════════════════════════╝")

def menu_login():
    print("╔══════════════════════════════════════╗")
    print("║            🔑 Fazer Login            ║")
    print("╠══════════════════════════════════════╣")
    email = input("Email: ")
    senha = input("Senha: ")
    return email, senha

def menu_logado(usuario):
    while True:
        print("\n=== MENU LOGADO ===")
        print(f"Bem-vindo, {usuario['nome']}!")
        print("1. Ver pontos turísticos")
        print("2. Ver minhas avaliações")
        print("3. Ver avaliações de um ponto turístico")
        print("4. Cadastrar ponto turístico")
        print("5. Fazer avaliação")
        print("6. Alterar meu nome")
        print("7. Excluir uma avaliação minha")
        print("8. Excluir minha conta")
        print("9. Sair")

        opcao = input("Escolha uma opção: ")
        limpar_tela()

        if opcao == "1":
            mostrar_pontos_turisticos()
        elif opcao == "2":
            mostrar_avaliacoes_usuario(usuario["id"])
        elif opcao == "3":
            nome_ponto = input("Digite o nome do ponto turístico: ")
            mostrar_avaliacoes_ponto(nome_ponto)
        elif opcao == "4":
            print("Os campos com '*' São obrigatórios. Aperte Enter caso queira pular os campos não-obrigatórios.\n")
            cadastrar_ponto_turistico()
        elif opcao == "5":
            nome_ponto = input("Nome do ponto turístico a avaliar: ")
            nota = input("Nota (0 a 5): ")
            comentario = input("Comentário: ")
            avaliar_ponto_turistico(usuario["id"], nome_ponto, nota, comentario)
        elif opcao == "6":
            novo_nome = input("Digite seu novo nome: ")
            atualizar_nome_usuario(usuario["id"], novo_nome)
        elif opcao == "7":
            id_avaliacao = input("Digite o ID da avaliação que deseja excluir: ")
            excluir_avaliacao(usuario["id"], id_avaliacao)
        elif opcao == "8":
            certeza = input("Tem certeza que deseja excluir sua conta? (s/n): ").lower()
            while certeza != "s" and certeza != "n":
                certeza = input("Opção inválida. Tente novamente (s/n): ")
            if certeza == "s":
                excluir_conta(usuario["id"])
                print("\nConta excluída... Encerrando sessão.")
                time.sleep(2)
                break
            elif certeza == "n":
                print("\nExclusão de conta abortada... Voltando ao Menu Logado.")
                time.sleep(2)

        elif opcao == "9":
            print("Saindo do menu logado...")
            time.sleep(1.5)
            break
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(2)

def menu_principal():
    while True:
        limpar_tela()
        print("╔═══════════════════════════════════════╗")
        print("║   🌴 Sistema de Usuários - Alagoas    ║")
        print("╠═══════════════════════════════════════╣")
        print("║ 1. 📝 Cadastrar novo usuário          ║")
        print("║ 2. 🔑 Fazer login                     ║")
        print("║ 3. ❌ Sair                            ║")
        print("╚═══════════════════════════════════════╝")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida! Por favor, insira um número.")
            time.sleep(1.5)
            continue  # volta p o menu

        if opcao == 1:
            limpar_tela()
            menu_cadastro()
            cadastro()
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == 2:
            limpar_tela()
            email, senha = menu_login()
            sucesso, usuario = login(email, senha)
            if sucesso:
                menu_logado(usuario)
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == 3:
            print("\nSaindo do sistema... 👋")
            time.sleep(1)
            break

        else:
            print("Opção inválida! Tente novamente.")
            time.sleep(1.5)