"""
Sistema de agendamento para salão de beleza (projeto da faculdade - 1º semestre)

Gerencia clientes, serviços e os serviços agendados para cada cliente,
guardando tudo em arquivos .txt. Cada linha do arquivo é um registro com os
campos separados por ponto e vírgula:

    clientes.txt-> cpf;nome;endereço;telefone fixo;celulares;nascimento;
    servicos.txt-> codigo;nome;descrição;preço;
    agendamentos.txt-> cpf;codigo do serviço;data (DD/MM/AAAA);
    relatorios.txt-> texto dos relatórios já gerados

Chaves (não podem se repetir):
    cliente-> CPF| serviço-> código| agendamento-> CPF + código + data
"""
import os
from datetime import datetime, date, timedelta

# Nomes dos arquivos
ARQ_CLIENTES = "clientes.txt"
ARQ_SERVICOS = "servicos.txt"
ARQ_AGENDAMENTOS = "agendamentos.txt"
ARQ_RELATORIOS = "relatorios.txt"
FORMATO_DATA = "%d/%m/%Y"

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

# Funções auxiliares (datas, confirmação e buscas)

def ler_data(mensagem):
    """Pede uma data até o usuário digitar uma válida (DD/MM/AAAA)."""
    data_valida = False
    while data_valida == False:
        texto = input(mensagem)
        try:
            data = datetime.strptime(texto, FORMATO_DATA).date()
            data_valida = True
        except ValueError:
            print("Data inválida! Use o formato DD/MM/AAAA (exemplo: 25/12/2026).")
    return data

def data_para_texto(data):
    return data.strftime(FORMATO_DATA)

def texto_para_data(texto):
    return datetime.strptime(texto, FORMATO_DATA).date()

def confirmar(mensagem):
    """Pergunta sim/não e devolve True se o usuário digitou s."""
    resposta = input(mensagem + " (s/n): ")
    return resposta.lower() == "s"

def procurar_posicao(lista, valor, indice):
    """Devolve a posição da primeira linha cujo campo [indice] é igual a valor,
    ou -1 se não achar."""
    posicao = -1
    for i in range(len(lista)):
        info = lista[i].split(";")
        if info[indice] == valor and posicao == -1:
            posicao = i
    return posicao

def buscar_cliente(lista_clientes, cpf):
    """Devolve os campos do cliente (lista) ou [] se ele não existir."""
    cliente = []
    for linha in lista_clientes:
        info = linha.split(";")
        if info[0] == cpf:
            cliente = info
    return cliente

def buscar_servico(lista_servicos, codigo):
    """Devolve os campos do serviço (lista) ou [] se ele não existir."""
    servico = []
    for linha in lista_servicos:
        info = linha.split(";")
        if info[0] == codigo:
            servico = info
    return servico

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
            if buscar_cliente(lista_clientes, cpf) != []:
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
        posicao = procurar_posicao(lista_clientes, cpf, 0)
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

def excluir_cliente(lista_clientes, lista_agendamentos):
    if lista_clientes == []:
        print("Não existe nenhum cliente cadastrado ainda!")
    else:
        cpf = input("Qual o CPF do cliente que deseja excluir o cadastro? ")
        posicao = procurar_posicao(lista_clientes, cpf, 0)
        if posicao == -1:
            print("Cliente não encontrado")
        elif procurar_posicao(lista_agendamentos, cpf, 0) != -1:
            # evita agendamentos ligados a um cliente que não existe mais
            print("Esse cliente tem agendamentos. Exclua os agendamentos antes de excluir o cadastro.")
        else:
            mostrar_cliente(lista_clientes[posicao].split(";"))
            if confirmar("Confirma a exclusão desse cliente?") == True:
                del lista_clientes[posicao]
                print("Cadastro excluído")
            else:
                print("Exclusão cancelada")

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
    if buscar_servico(lista_servicos, codigo) != []:
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
        posicao = procurar_posicao(lista_servicos, codigo, 0)
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

def excluir_servico(lista_servicos, lista_agendamentos):
    if lista_servicos == []:
        print("Não existe nenhum serviço cadastrado ainda!")
    else:
        print("Os serviços já cadastrados são:")
        listar(lista_servicos)
        codigo = input("Digite o código do serviço para excluí-lo: ")
        posicao = procurar_posicao(lista_servicos, codigo, 0)
        if posicao == -1:
            print("Serviço não encontrado")
        elif procurar_posicao(lista_agendamentos, codigo, 1) != -1:
            print("Esse serviço tem agendamentos. Exclua os agendamentos antes de excluir o serviço.")
        else:
            codigo_existe(lista_servicos, codigo)
            if confirmar("Confirma a exclusão desse serviço?") == True:
                del lista_servicos[posicao]
                print("Serviço excluído")
            else:
                print("Exclusão cancelada")

# Agendamentos (Cliente/Serviço)
def procurar_agendamento(lista_agendamentos, cpf, codigo, data_texto):
    """Devolve a posição do agendamento (cpf + código + data) ou -1."""
    posicao = -1
    for i in range(len(lista_agendamentos)):
        info = lista_agendamentos[i].split(";")
        if info[0] == cpf and info[1] == codigo and info[2] == data_texto:
            posicao = i
    return posicao

def mostrar_agendamento(linha, lista_clientes, lista_servicos):
    info = linha.split(";")
    cliente = buscar_cliente(lista_clientes, info[0])
    servico = buscar_servico(lista_servicos, info[1])
    nome_cliente = "?"
    nome_servico = "?"
    if cliente != []:
        nome_cliente = cliente[1]
    if servico != []:
        nome_servico = servico[1]
    print(f"Data: {info[2]} | Cliente: {nome_cliente} (CPF {info[0]}) | Serviço: {nome_servico} (cód. {info[1]})")

def imprimir_agendamentos(lista_agendamentos, lista_clientes, lista_servicos):
    if lista_agendamentos == []:
        print("Não há nenhum agendamento marcado!")
    else:
        for linha in lista_agendamentos:
            mostrar_agendamento(linha, lista_clientes, lista_servicos)

def pedir_dados_agendamento():
    """Pergunta o CPF, o código do serviço e a data. Devolve os três."""
    cpf = input("Qual o CPF do cliente que agendou o horário? ")
    codigo = input("Qual o código do serviço agendado? ")
    data = ler_data("Qual a data do agendamento (DD/MM/AAAA)? ")
    return cpf, codigo, data_para_texto(data)

def imprimir_um_agendamento(lista_agendamentos, lista_clientes, lista_servicos):
    cpf, codigo, data_texto = pedir_dados_agendamento()
    posicao = procurar_agendamento(lista_agendamentos, cpf, codigo, data_texto)
    if posicao == -1:
        print("Esse agendamento não existe")
    else:
        mostrar_agendamento(lista_agendamentos[posicao], lista_clientes, lista_servicos)

def incluir_agendamento(lista_agendamentos, lista_clientes, lista_servicos):
    quantos = int(input("Quantos agendamentos vão ser feitos? "))
    for i in range(quantos):
        #procura o cliente pelo CPF
        cpf = input("Qual o CPF do cliente que está agendando? ")
        cliente = buscar_cliente(lista_clientes, cpf)
        if cliente == []:
            print("Cliente não encontrado")
        else:
            #procura o serviço pelo código
            codigo = input(f"Qual é o código do serviço que {cliente[1]} quer agendar? ")
            if buscar_servico(lista_servicos, codigo) == []:
                print("Serviço não encontrado")
            else:
                #pede a data e confere se esse agendamento já existe
                data_texto = data_para_texto(ler_data("Qual a data do agendamento (DD/MM/AAAA)? "))
                if procurar_agendamento(lista_agendamentos, cpf, codigo, data_texto) != -1:
                    print("Esse agendamento já foi feito antes")
                else:
                    lista_agendamentos.append(cpf + ";" + codigo + ";" + data_texto + ";\n")
                    print("Agendamento incluído")

def alterar_agendamento(lista_agendamentos, lista_servicos):
    cpf, codigo, data_texto = pedir_dados_agendamento()
    posicao = procurar_agendamento(lista_agendamentos, cpf, codigo, data_texto)
    if posicao == -1:
        print("Agendamento não encontrado")
    else:
        opcao = input("1-Serviço\n2-Data\nQual você quer alterar? ")
        if opcao == "1":
            novo_codigo = input("Digite o código do novo serviço: ")
            if buscar_servico(lista_servicos, novo_codigo) == []:
                print("Serviço não encontrado")
            elif procurar_agendamento(lista_agendamentos, cpf, novo_codigo, data_texto) != -1:
                print("Esse agendamento já existe")
            else:
                lista_agendamentos[posicao] = cpf + ";" + novo_codigo + ";" + data_texto + ";\n"
                print("Alterado com sucesso")
        elif opcao == "2":
            nova_data = data_para_texto(ler_data("Digite a nova data (DD/MM/AAAA): "))
            if procurar_agendamento(lista_agendamentos, cpf, codigo, nova_data) != -1:
                print("Esse agendamento já existe")
            else:
                lista_agendamentos[posicao] = cpf + ";" + codigo + ";" + nova_data + ";\n"
                print("Alterado com sucesso")
        else:
            print("Não é uma escolha válida")

def excluir_agendamento(lista_agendamentos, lista_clientes, lista_servicos):
    cpf, codigo, data_texto = pedir_dados_agendamento()
    posicao = procurar_agendamento(lista_agendamentos, cpf, codigo, data_texto)
    if posicao == -1:
        print("Agendamento não encontrado")
    else:
        mostrar_agendamento(lista_agendamentos[posicao], lista_clientes, lista_servicos)
        if confirmar("Confirma a exclusão desse agendamento?") == True:
            del lista_agendamentos[posicao]
            print("Agendamento excluído")
        else:
            print("Exclusão cancelada")

# Relatórios
def salvar_relatorio(titulo, linhas, lista_relatorios):
    """Mostra o relatório na tela e guarda o texto dele na lista de relatórios
    (que é gravada em relatorios.txt quando o programa é encerrado)."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    cabecalho = f"{titulo} - gerado em {agora}\n"
    if linhas == []:
        linhas.append("Nenhum resultado encontrado.\n")
    print("\n" + cabecalho.strip())
    lista_relatorios.append(cabecalho)
    for linha in linhas:
        print(linha.strip())
        lista_relatorios.append(linha)
    lista_relatorios.append("\n")

def relatorio_clientes_do_servico(lista_agendamentos, lista_clientes, lista_servicos, lista_relatorios):
    """a) Nome e telefones dos clientes que contrataram um serviço no último mês
    (considerado como os últimos 30 dias, até hoje)."""
    codigo = input("Digite o código do serviço: ")
    servico = buscar_servico(lista_servicos, codigo)
    if servico == []:
        print("Serviço não encontrado")
    else:
        hoje = date.today()
        inicio = hoje - timedelta(days=30)
        linhas = []
        cpfs_ja_listados = []
        for linha in lista_agendamentos:
            info = linha.split(";")
            data = texto_para_data(info[2])
            if info[1] == codigo and data >= inicio and data <= hoje and info[0] not in cpfs_ja_listados:
                cliente = buscar_cliente(lista_clientes, info[0])
                if cliente != []:
                    cpfs_ja_listados.append(info[0])
                    linhas.append(f"Cliente: {cliente[1]} | Telefone fixo: {cliente[3]} | Celulares: {cliente[4].rstrip(',')}\n")
        titulo = (f"RELATÓRIO A - Clientes que contrataram o serviço {codigo} ({servico[1]}) "
                  f"entre {data_para_texto(inicio)} e {data_para_texto(hoje)}")
        salvar_relatorio(titulo, linhas, lista_relatorios)

def relatorio_servicos_da_data(lista_agendamentos, lista_clientes, lista_servicos, lista_relatorios):
    """b) Dados dos serviços realizados em uma data, com o nome do cliente."""
    data = ler_data("Digite a data (DD/MM/AAAA): ")
    data_texto = data_para_texto(data)
    linhas = []
    for linha in lista_agendamentos:
        info = linha.split(";")
        if info[2] == data_texto:
            cliente = buscar_cliente(lista_clientes, info[0])
            servico = buscar_servico(lista_servicos, info[1])
            if cliente != [] and servico != []:
                linhas.append(f"Serviço {servico[0]} - {servico[1]} - {servico[2]} - R$ {servico[3]} | Cliente: {cliente[1]}\n")
    salvar_relatorio(f"RELATÓRIO B - Serviços realizados em {data_texto}", linhas, lista_relatorios)

def relatorio_servicos_entre_datas(lista_agendamentos, lista_servicos, lista_relatorios):
    """c) Código, descrição e preço dos serviços realizados entre duas datas."""
    inicio = ler_data("Digite a data inicial X (DD/MM/AAAA): ")
    fim = ler_data("Digite a data final Y (DD/MM/AAAA): ")
    if inicio > fim:
        print("A data inicial não pode ser depois da data final")
    else:
        linhas = []
        for linha in lista_agendamentos:
            info = linha.split(";")
            data = texto_para_data(info[2])
            servico = buscar_servico(lista_servicos, info[1])
            if data >= inicio and data <= fim and servico != []:
                linhas.append(f"Data: {info[2]} | Serviço {servico[0]} - {servico[1]} - {servico[2]} - R$ {servico[3]}\n")
        titulo = f"RELATÓRIO C - Serviços realizados entre {data_para_texto(inicio)} e {data_para_texto(fim)}"
        salvar_relatorio(titulo, linhas, lista_relatorios)

def listar_relatorios_salvos(lista_relatorios):
    if lista_relatorios == []:
        print("Nenhum relatório foi gerado ainda!")
    else:
        for linha in lista_relatorios:
            print(linha.strip())

# Menus
def carregar_submenu1(lista_clientes, lista_agendamentos):
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
        excluir_cliente(lista_clientes, lista_agendamentos)
    else:
        print("Não existe essa opção")

def carregar_submenu2(lista_servicos, lista_agendamentos):
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
        excluir_servico(lista_servicos, lista_agendamentos)
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
        imprimir_agendamentos(lista_agendamentos, lista_clientes, lista_servicos)
    elif escolha == "2":
        imprimir_um_agendamento(lista_agendamentos, lista_clientes, lista_servicos)
    elif escolha == "3":
        incluir_agendamento(lista_agendamentos, lista_clientes, lista_servicos)
    elif escolha == "4":
        alterar_agendamento(lista_agendamentos, lista_servicos)
    elif escolha == "5":
        excluir_agendamento(lista_agendamentos, lista_clientes, lista_servicos)
    else:
        print("Não existe essa opção")

def carregar_submenu4(lista_agendamentos, lista_clientes, lista_servicos, lista_relatorios):
    print("1. Clientes que contrataram um serviço no último mês\n"
          "2. Serviços realizados em uma data\n"
          "3. Serviços realizados entre duas datas\n"
          "4. Ver relatórios já gerados")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        relatorio_clientes_do_servico(lista_agendamentos, lista_clientes, lista_servicos, lista_relatorios)
    elif escolha == "2":
        relatorio_servicos_da_data(lista_agendamentos, lista_clientes, lista_servicos, lista_relatorios)
    elif escolha == "3":
        relatorio_servicos_entre_datas(lista_agendamentos, lista_servicos, lista_relatorios)
    elif escolha == "4":
        listar_relatorios_salvos(lista_relatorios)
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
              "3. Submenu de Cliente/Serviço (agendamentos)\n"
              "4. Submenu de Relatórios\n"
              "5. Sair")
        opcao = input("Digite qual você quer escolher: ")
        if opcao == "1":
            carregar_submenu1(lista_clientes, lista_agendamentos)
        elif opcao == "2":
            carregar_submenu2(lista_servicos, lista_agendamentos)
        elif opcao == "3":
            carregar_submenu3(lista_agendamentos, lista_clientes, lista_servicos)
        elif opcao == "4":
            carregar_submenu4(lista_agendamentos, lista_clientes, lista_servicos, lista_relatorios)
        elif opcao == "5":
            # só grava nos arquivos ao sair
            incluir_no_arquivo(lista_clientes, lista_servicos, lista_agendamentos, lista_relatorios)
            print("Dados salvos. Até logo!")
            sair = True
        else:
            print("Não existe essa opção")

if __name__ == "__main__":
    main()
