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
    excluir_conta,

    # categorias
    mostrar_categorias,
    mostrar_pontos_por_categoria,
    cadastrar_categoria
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


def menu_categorias():
    while True:
        limpar_tela()
        print("╔══════════════════════════════════════╗")
        print("║            🗂️  Categorias            ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Cadastrar categoria               ║")
        print("║ 2. Ver categorias existentes         ║")
        print("║ 3. Ver pontos por categoria          ║")
        print("║ 4. Voltar                            ║")
        print("╚══════════════════════════════════════╝")

        opc = input("Escolha uma opção: ").strip()
        limpar_tela()

        if opc == "1":
            cadastrar_categoria()

        elif opc == "2":
            mostrar_categorias()

        elif opc == "3":
            mostrar_pontos_por_categoria()

        elif opc == "4":
            break

        else:
            print("Opção inválida!")
            time.sleep(2)
            limpar_tela()


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
        print("9. Categorias")
        print("10. Sair")

        opcao = input("Escolha uma opção: ").strip()
        limpar_tela()

        if opcao == "1":
            mostrar_pontos_turisticos()

        elif opcao == "2":
            mostrar_avaliacoes_usuario(usuario["id"])

        elif opcao == "3":
            nome_ponto = input("Digite o nome do ponto turístico: ")
            mostrar_avaliacoes_ponto(nome_ponto)

        elif opcao == "4":
            print("Os campos com '*' são obrigatórios. Aperte Enter nos opcionais.\n")
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
            certeza = input("Tem certeza que deseja excluir sua conta? (s/n): ").lower().strip()
            while certeza not in ("s", "n"):
                certeza = input("Opção inválida. Tente novamente (s/n): ").lower().strip()

            if certeza == "s":
                excluir_conta(usuario["id"])
                print("\nConta excluída... Encerrando sessão.")
                time.sleep(2)
                break
            else:
                print("\nExclusão de conta cancelada.")
                time.sleep(2)

        elif opcao == "9":
            menu_categorias()

        elif opcao == "10":
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
            continue

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
            print("Opção inválida!")
            time.sleep(1.5)