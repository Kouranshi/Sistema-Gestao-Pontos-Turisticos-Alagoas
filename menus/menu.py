from functions.cadastro_login import cadastro, login
from functions.limpar import limpar_tela
import time
from db.funcoes import (
    mostrar_pontos_turisticos,
    mostrar_avaliacoes_usuario,
    mostrar_avaliacoes_ponto,
    cadastrar_ponto_turistico,
    avaliar_ponto_turistico
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
        print("6. Sair")

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
            nome = input("Nome do ponto turístico: ")
            descricao = input("Descrição: ")
            horario = input("Horário de funcionamento: ")
            custo = input("Custo de entrada (ou 0 se gratuito): ")
            cadastrar_ponto_turistico(nome, descricao, horario, custo)
        elif opcao == "5":
            nome_ponto = input("Nome do ponto turístico a avaliar: ")
            nota = input("Nota (0 a 5): ")
            comentario = input("Comentário: ")
            avaliar_ponto_turistico(usuario["id"], nome_ponto, nota, comentario)
        elif opcao == "6":
            print("Saindo do menu logado...")
            break
        else:
            print("Opção inválida. Tente novamente.")

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