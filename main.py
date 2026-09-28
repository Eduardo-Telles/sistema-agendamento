"""
Sistema de agendamento projeto da faculdade - 1º semestre 2026!

Cadastra clientes, serviços e agendamentos, guardando tudo em arquivos .txt.
Cada linha do arquivo é um registro com os campos separados por ponto e vírgula:
    clientes.txt -> cpf;nome;endereço;telefone fixo;celulares;nascimento;
    servicos.txt -> codigo;nome;descrição;preço;
    agendamentos.txt-> cpf;nome do cliente;nome do serviço;codigo do serviço;data;
"""
import os
# Nomes dos arquivos (se precisar mudar, muda só aqui)
ARQ_CLIENTES = "clientes.txt"
ARQ_SERVICOS = "servicos.txt"
ARQ_AGENDAMENTOS = "agendamentos.txt"
ARQ_RELATORIOS = "relatorios.txt"

# Arquivos

def existe_arquivo(nome):
    return os.path.exists(nome)

def carregar_arquivo(arquivo):
    """Lê o arquivo e devolve uma lista com as linhas.
    Se o arquivo não existir, ele é criado vazio (modo a+)."""
    if existe_arquivo(arquivo) == True:
        arq = open(arquivo, "r", encoding="utf-8")
    else:
        arq = open(arquivo, "a+", encoding="utf-8")
    lista = []
    for linha in arq:
        lista.append(linha)
    arq.close()
    return lista

def salvar_arquivo(arquivo, lista):
    """Sobrescreve o arquivo com o conteúdo atual da lista."""
    arq = open(arquivo, "w", encoding="utf-8")
    for linha in lista:
        arq.write(linha)
    arq.close()

def incluir_no_arquivo(lista_clientes, lista_servicos, lista_agendamentos, lista_relatorios):
    salvar_arquivo(ARQ_CLIENTES, lista_clientes)
    salvar_arquivo(ARQ_SERVICOS, lista_servicos)
    salvar_arquivo(ARQ_AGENDAMENTOS, lista_agendamentos)
    salvar_arquivo(ARQ_RELATORIOS, lista_relatorios)

# Clientes
def mostrar_cliente(info):
    """Imprime um cliente (info é a linha já separada por ';')."""
    print(f"CPF: {info[0]}")
    print(f"Nome: {info[1]}")
    print(f"Endereço: {info[2]}")
    print(f"Telefone fixo: {info[3]}")
    print(f"Telefone celular: {info[4].rstrip(',')}")
    print(f"Nascimento: {info[5]}")
    print("-" * 20)

def imprimir_clientes(lista_clientes):
    if lista_clientes == []:
        print("Não há nenhum cliente cadastrado!")
    else:
        for linha in lista_clientes:
            mostrar_cliente(linha.split(";"))

def procurar_cliente(lista_clientes):
    busca_nome = input("Digite o nome da pessoa que deseja buscar: ")
    busca_cpf = input("Digite o CPF da pessoa que deseja buscar: ")
    for linha in lista_clientes:
        info = linha.split(";")
        if info[1] == busca_nome and info[0] == busca_cpf:
            mostrar_cliente(info)
            return info
    print("Cliente não encontrado")
    return False

def incluir_clientes(lista_clientes):
    quantos_clientes = int(input("Quantos clientes você vai adicionar? "))
    for i in range(quantos_clientes):
        # CPF: repete até ter 11 dígitos e não existir ainda
        cpf_valido = False
        while cpf_valido == False:
            cpf = input(f"Digite o CPF do cliente {i + 1}: ")
            ja_existe = False
            for linha in lista_clientes:
                info = linha.split(";")
                if cpf == info[0]:
                    ja_existe = True
            if ja_existe == True:
                print("Esse CPF já existe, coloque outro CPF para o cadastro")
            elif len(cpf) != 11:
                print("O CPF tem que ter 11 dígitos")
            else:
                cpf_valido = True

        nome = input(f"Digite o nome do cliente {i + 1}: ")
        endereco = input(f"Digite o endereço do cliente {i + 1}: ")
        fixo = input(f"Digite o telefone fixo do cliente {i + 1}: ")

        # celulares ficam juntos no mesmo campo, separados por vírgula
        qtd_cel = int(input(f"Quantos celulares o cliente {i + 1} tem? "))
        celulares = ""
        for p in range(qtd_cel):
            celulares = celulares + input(f"Digite o celular {p + 1}: ") + ","

        nascimento = input("Digite a data de nascimento do cliente: ")

        cliente = cpf + ";" + nome + ";" + endereco + ";" + fixo + ";" + celulares + ";" + nascimento + ";\n"
        lista_clientes.append(cliente)
    return lista_clientes

def alterar_cliente(lista_clientes):
    if lista_clientes == []:
        print("Não existe nenhum cliente cadastrado ainda!")
    else:
        cpf = input("Qual o CPF do cliente que deseja alterar os dados? ")
        posicao = -1
        for i in range(len(lista_clientes)):
            info = lista_clientes[i].split(";")
            if info[0] == cpf:
                posicao = i
        if posicao == -1:
            print("Esse cliente não existe.")
        else:
            opcao = input("\n1. Endereço\n2. Telefone fixo\n3. Telefone celular\n4. Nascimento\n"
                          "Informe qual dado do cliente deseja alterar: ")
            if opcao in ["1", "2", "3", "4"]:
                nova_info = input("Digite a alteração: ")
                info = lista_clientes[posicao].split(";")
                # opção 1 -> info[2], opção 2 -> info[3], ...
                info[int(opcao) + 1] = nova_info
                lista_clientes[posicao] = ";".join(info)
                print("Cadastro alterado com sucesso!")
            else:
                print("Não tem essa escolha")

def excluir_cliente(lista_clientes):
    if lista_clientes == []:
        print("Não existe nenhum cliente cadastrado ainda!")
    else:
        cpf = input("Qual o CPF do cliente que deseja excluir o cadastro? ")
        achou = False
        # [:] percorre uma cópia, pois não se deve remover itens da lista que está sendo percorrida
        for linha in lista_clientes[:]:
            info = linha.split(";")
            if cpf == info[0]:
                lista_clientes.remove(linha)
                achou = True
        if achou == True:
            print("Cadastro excluído")
        else:
            print("Cliente não encontrado")

# Serviços
def listar(lista_servicos):
    if lista_servicos == []:
        print("Não há nenhum serviço cadastrado!")
    else:
        for linha in lista_servicos:
            info = linha.split(";")
            print(f"{info[0]} - {info[1]} - {info[2]} - R$ {info[3]}")

def codigo_existe(lista, codigo):
    """Imprime o serviço com esse código e devolve True se ele existir."""
    achou = False
    for linha in lista:
        partes = linha.split(";")
        if codigo == partes[0]:
            print(f"{partes[0]} - {partes[1]} - {partes[2]} - R$ {partes[3]}")
            achou = True
    return achou

def listar_unico(lista_servicos):
    if lista_servicos == []:
        print("Não há nenhum serviço cadastrado!")
    else:
        codigo = input("Informe o código do serviço a ser procurado: ")
        if codigo_existe(lista_servicos, codigo) == False:
            print("Esse código não foi encontrado!")

def incluir_servicos(lista_servicos):
    codigo = input("Digite o código desse novo serviço: ")
    # confere se o código já existe
    ja_existe = False
    for linha in lista_servicos:
        info = linha.split(";")
        if info[0] == codigo:
            ja_existe = True
    if ja_existe == True:
        print("Esse código já existe")
    else:
        servico = input("Digite o novo serviço: ")
        descricao = input("Dê uma descrição a esse serviço: ")
        preco = float(input("Digite o preço do serviço: ").replace(",", "."))
        lista_servicos.append(codigo + ";" + servico + ";" + descricao + ";" + str(preco) + ";\n")
        print("Serviço cadastrado")

def alterar_servico(lista_servicos):
    if lista_servicos == []:
        print("Não existe nenhum serviço cadastrado ainda!")
    else:
        print("Os serviços já cadastrados são:")
        listar(lista_servicos)
        codigo = input("Digite o código do serviço para alterá-lo: ")
        posicao = -1
        for i in range(len(lista_servicos)):
            info = lista_servicos[i].split(";")
            if info[0] == codigo:
                posicao = i
        if posicao == -1:
            print("Esse serviço não existe")
        else:
            opcao = input("1-Serviço\n2-Descrição\n3-Preço\nDigite qual você quer alterar: ")
            if opcao in ["1", "2", "3"]:
                nova_info = input("Digite a nova informação: ")
                if opcao == "3":
                    nova_info = str(float(nova_info.replace(",", ".")))
                info = lista_servicos[posicao].split(";")
                info[int(opcao)] = nova_info
                lista_servicos[posicao] = ";".join(info)
                print("Alterado com sucesso")
            else:
                print("Não tem essa escolha")

def excluir_servico(lista_servicos):
    if lista_servicos == []:
        print("Não existe nenhum serviço cadastrado ainda!")
    else:
        print("Os serviços já cadastrados são:")
        listar(lista_servicos)
        codigo = input("Digite o código do serviço para excluí-lo: ")
        achou = False
        for linha in lista_servicos[:]:
            info = linha.split(";")
            if codigo == info[0]:
                lista_servicos.remove(linha)
                achou = True
        if achou == True:
            print("Serviço excluído")
        else:
            print("Serviço não encontrado")

# Agendamentos
def mostrar_agendamento(linha):
    info = linha.split(";")
    print(f"CPF: {info[0]} | Cliente: {info[1]} | Serviço: {info[2]} (cód. {info[3]}) | Data: {info[4]}")

def imprimir_agendamentos(lista_agendamentos):
    if lista_agendamentos == []:
        print("Não há nenhum agendamento marcado!")
    else:
        for linha in lista_agendamentos:
            mostrar_agendamento(linha)

def imprimir_um_agendamento(lista_agendamentos):
    cpf = input("Qual o CPF do cliente que agendou o horário? ")
    servico = input("Qual o código do serviço agendado? ")
    achou = False
    for linha in lista_agendamentos:
        info = linha.split(";")
        if info[0] == cpf and info[3] == servico:
            mostrar_agendamento(linha)
            achou = True
    if achou == False:
        print("Esse agendamento não existe")

def incluir_agendamento(lista_agendamentos, lista_clientes, lista_servicos):
    quantos = int(input("Quantos agendamentos vão ser feitos? "))
    for i in range(quantos):
        # 1) procura o cliente pelo CPF
        cpf = input("Qual o CPF do cliente que está agendando? ")
        nome_cliente = ""
        for linha in lista_clientes:
            info = linha.split(";")
            if cpf == info[0]:
                nome_cliente = info[1]
        if nome_cliente == "":
            print("Cliente não encontrado")
        else:
            # 2) procura o serviço pelo código
            codigo = input(f"Qual é o código do serviço que {nome_cliente} quer agendar? ")
            nome_servico = ""
            for linha in lista_servicos:
                serv = linha.split(";")
                if serv[0] == codigo:
                    nome_servico = serv[1]
            if nome_servico == "":
                print("Serviço não encontrado")
            else:
                # 3) confere se esse cliente já agendou esse serviço
                ja_agendado = False
                for linha in lista_agendamentos:
                    info = linha.split(";")
                    if info[0] == cpf and info[3] == codigo:
                        ja_agendado = True
                if ja_agendado == True:
                    print("Esse agendamento já foi feito antes")
                else:
                    data = input("Qual horário e data ele quer agendar? ")
                    lista_agendamentos.append(cpf + ";" + nome_cliente + ";" + nome_servico + ";" + codigo + ";" + data + ";\n")
                    print("Agendamento incluído")

def alterar_agendamento(lista_agendamentos, lista_servicos):
    cpf = input("Qual o CPF do cliente que agendou o horário? ")
    servico = input("Qual o código do serviço agendado? ")
    posicao = -1
    for i in range(len(lista_agendamentos)):
        info = lista_agendamentos[i].split(";")
        if info[0] == cpf and info[3] == servico:
            posicao = i
    if posicao == -1:
        print("Agendamento não encontrado")
    else:
        info = lista_agendamentos[posicao].split(";")
        opcao = input("1-Serviço\n2-Data\nQual você quer alterar? ")
        if opcao == "1":
            novo_codigo = input("Digite o código do novo serviço: ")
            novo_nome = ""
            for linha in lista_servicos:
                serv = linha.split(";")
                if serv[0] == novo_codigo:
                    novo_nome = serv[1]
            if novo_nome == "":
                print("Serviço não encontrado")
            else:
                lista_agendamentos[posicao] = info[0] + ";" + info[1] + ";" + novo_nome + ";" + novo_codigo + ";" + info[4] + ";\n"
                print("Alterado com sucesso")
        elif opcao == "2":
            nova_data = input("Escreva a nova data e horário: ")
            lista_agendamentos[posicao] = info[0] + ";" + info[1] + ";" + info[2] + ";" + info[3] + ";" + nova_data + ";\n"
            print("Alterado com sucesso")
        else:
            print("Não é uma escolha válida")

def excluir_agendamento(lista_agendamentos):
    cpf = input("Qual o CPF do cliente que agendou o horário? ")
    servico = input("Qual o código do serviço agendado? ")
    achou = False
    for linha in lista_agendamentos[:]:
        info = linha.split(";")
        if info[0] == cpf and info[3] == servico:
            lista_agendamentos.remove(linha)
            achou = True
    if achou == True:
        print("Agendamento excluído")
    else:
        print("Agendamento não encontrado")

# Menus
def carregar_submenu1(lista_clientes):
    print("1. Listar clientes\n"
          "2. Listar um cliente\n"
          "3. Incluir um cliente\n"
          "4. Alterar cadastro de um cliente\n"
          "5. Excluir cadastro de cliente")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        imprimir_clientes(lista_clientes)
    elif escolha == "2":
        procurar_cliente(lista_clientes)
    elif escolha == "3":
        incluir_clientes(lista_clientes)
    elif escolha == "4":
        alterar_cliente(lista_clientes)
    elif escolha == "5":
        excluir_cliente(lista_clientes)
    else:
        print("Não existe essa opção")

def carregar_submenu2(lista_servicos):
    print("1. Listar serviços\n"
          "2. Listar um serviço\n"
          "3. Incluir um serviço\n"
          "4. Alterar cadastro de um serviço\n"
          "5. Excluir cadastro de um serviço")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        listar(lista_servicos)
    elif escolha == "2":
        listar_unico(lista_servicos)
    elif escolha == "3":
        incluir_servicos(lista_servicos)
    elif escolha == "4":
        alterar_servico(lista_servicos)
    elif escolha == "5":
        excluir_servico(lista_servicos)
    else:
        print("Não existe essa opção")

def carregar_submenu3(lista_agendamentos, lista_clientes, lista_servicos):
    print("1. Listar horários marcados\n"
          "2. Listar um horário marcado\n"
          "3. Incluir um agendamento\n"
          "4. Alterar agendamento\n"
          "5. Excluir agendamento")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        imprimir_agendamentos(lista_agendamentos)
    elif escolha == "2":
        imprimir_um_agendamento(lista_agendamentos)
    elif escolha == "3":
        incluir_agendamento(lista_agendamentos, lista_clientes, lista_servicos)
    elif escolha == "4":
        alterar_agendamento(lista_agendamentos, lista_servicos)
    elif escolha == "5":
        excluir_agendamento(lista_agendamentos)
    else:
        print("Não existe essa opção")

def carregar_submenu4(lista_relatorios):
    print("1. Listar relatórios\n"
          "2. Listar um relatório\n"
          "3. Incluir um relatório\n"
          "4. Alterar relatório\n"
          "5. Excluir relatório")
    escolha = input("Escolha uma opção: ")
    if escolha in ["1", "2", "3", "4", "5"]:
        print("Funcionalidade em desenvolvimento.")
    else:
        print("Não existe essa opção")

# Programa principal
def main():
    # carrega os arquivos para listas
    lista_clientes = carregar_arquivo(ARQ_CLIENTES)
    lista_servicos = carregar_arquivo(ARQ_SERVICOS)
    lista_agendamentos = carregar_arquivo(ARQ_AGENDAMENTOS)
    lista_relatorios = carregar_arquivo(ARQ_RELATORIOS)

    # menu principal
    sair = False
    while sair == False:
        print("\n1. Submenu de Clientes\n"
              "2. Submenu de Serviços\n"
              "3. Submenu de Agendamentos\n"
              "4. Submenu de Relatórios\n"
              "5. Sair")
        opcao = input("Digite qual você quer escolher: ")
        if opcao == "1":
            carregar_submenu1(lista_clientes)
        elif opcao == "2":
            carregar_submenu2(lista_servicos)
        elif opcao == "3":
            carregar_submenu3(lista_agendamentos, lista_clientes, lista_servicos)
        elif opcao == "4":
            carregar_submenu4(lista_relatorios)
        elif opcao == "5":
            # só grava nos arquivos ao sair
            incluir_no_arquivo(lista_clientes, lista_servicos, lista_agendamentos, lista_relatorios)
            print("Dados salvos. Até logo!")
            sair = True
        else:
            print("Não existe essa opção")

if __name__ == "__main__":
    main()
