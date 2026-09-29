import json


print("================================")
print("          HELPFLOW")
print("================================")


def carregar_chamados():
    try:
        with open("chamados.json", "r") as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        return []


def salvar_chamados(chamados):
    with open("chamados.json", "w") as arquivo:
        json.dump(chamados, arquivo, indent=4)


def criar_chamado(chamados, proximo_id):
    print()
    print("=== NOVO CHAMADO ===")

    titulo = input("Título: ")
    descricao = input("Descrição: ")

    chamado = {
        "id": proximo_id,
        "titulo": titulo,
        "descricao": descricao,
        "status": "Aberto"
    }

    chamados.append(chamado)
    salvar_chamados(chamados)

    print()
    print("Chamado criado!")
    print("ID do chamado:", proximo_id)

    return proximo_id + 1


def listar_chamados(chamados):
    print()
    print("=== CHAMADOS ===")

    if len(chamados) == 0:
        print("Nenhum chamado cadastrado.")
        return

    for chamado in chamados:
        print()
        print("ID:", chamado["id"])
        print("Título:", chamado["titulo"])
        print("Descrição:", chamado["descricao"])
        print("Status:", chamado["status"])
        print("--------------------")


def resolver_chamado(chamados):
    if len(chamados) == 0:
        print()
        print("Não existem chamados para resolver.")
        return

    print()
    print("=== CHAMADOS ===")

    for chamado in chamados:
        print(
            chamado["id"],
            "-",
            chamado["titulo"],
            "-",
            chamado["status"]
        )

    try:
        id_escolhido = int(
            input("Digite o ID do chamado que deseja resolver: ")
        )

    except ValueError:
        print("Digite apenas números.")
        return

    for chamado in chamados:

        if chamado["id"] == id_escolhido:

            if chamado["status"] == "Resolvido":
                print("Esse chamado já foi resolvido.")
                return

            chamado["status"] = "Resolvido"
            salvar_chamados(chamados)

            print()
            print("Chamado #", id_escolhido, " resolvido!", sep="")
            return

    print("ID de chamado inválido.")


def excluir_chamado(chamados):
    if len(chamados) == 0:
        print()
        print("Não existem chamados para excluir.")
        return

    print()
    print("=== EXCLUIR CHAMADO ===")

    chamados_resolvidos = []

    for chamado in chamados:

        if chamado["status"] == "Resolvido":
            chamados_resolvidos.append(chamado)

    if len(chamados_resolvidos) == 0:
        print("Não existem chamados resolvidos para excluir.")
        return

    for chamado in chamados_resolvidos:
        print(
            chamado["id"],
            "-",
            chamado["titulo"],
            "-",
            chamado["status"]
        )

    try:
        id_escolhido = int(
            input("Digite o ID do chamado que deseja excluir: ")
        )

    except ValueError:
        print("Digite apenas números.")
        return

    for chamado in chamados_resolvidos:

        if chamado["id"] == id_escolhido:

            print()
            print("Chamado encontrado:")
            print("Título:", chamado["titulo"])
            print("Status:", chamado["status"])

            confirmacao = input(
                "Deseja realmente excluir? (s/n): "
            )

            if confirmacao.lower() == "s":

                chamados.remove(chamado)
                salvar_chamados(chamados)

                print()
                print(
                    "Chamado #",
                    id_escolhido,
                    " excluído com sucesso!",
                    sep=""
                )

            else:
                print()
                print("Exclusão cancelada.")

            return

    print("Esse chamado não existe ou ainda não foi resolvido.")


chamados = carregar_chamados()


if len(chamados) > 0:
    proximo_id = chamados[-1]["id"] + 1
else:
    proximo_id = 1


while True:

    print()
    print("1 - Abrir chamado")
    print("2 - Ver chamados")
    print("3 - Resolver chamado")
    print("4 - Excluir chamado")
    print("5 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        proximo_id = criar_chamado(
            chamados,
            proximo_id
        )

    elif opcao == "2":

        listar_chamados(chamados)

    elif opcao == "3":

        resolver_chamado(chamados)

    elif opcao == "4":

        excluir_chamado(chamados)

    elif opcao == "5":

        print("Saindo do HelpFlow...")
        break

    else:

        print("Opção inválida.")