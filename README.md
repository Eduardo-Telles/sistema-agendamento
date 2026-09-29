# Sistema de Agendamento

Projeto desenvolvido na faculdade 1º semestre em Python. É um programa de terminal para gerenciar clientes, serviços e agendamentos de um pequeno negócio, guardando os dados em arquivos `.txt`.

# Funcionalidades

- **Clientes:** listar, buscar, incluir, alterar e excluir (com validação de CPF de 11 dígitos e CPF único)
- **Serviços:** listar, buscar, incluir, alterar e excluir (código único)
- **Agendamentos (Cliente/Serviço):** listar, buscar, incluir, alterar (serviço ou data) e excluir, sempre conferindo se o cliente e o serviço existem e validando a data (DD/MM/AAAA)
- **Exclusão com confirmação:** o programa mostra os dados e pede confirmação antes de excluir, e não deixa excluir um cliente ou serviço que já tenha agendamentos
- **Relatórios:**
  - clientes (nome e telefones) que contrataram um serviço nos últimos 30 dias
  - serviços realizados em uma data, com o nome do cliente
  - serviços realizados entre duas datas
  - os relatórios gerados ficam salvos em `relatorios.txt`

# Como rodar

Você só precisa do Python 3 instalado.

```bash
git clone https://github.com/SEU-USUARIO/sistema-agendamento.git
cd sistema-agendamento
python main.py
```

Os arquivos de dados (`clientes.txt`, `servicos.txt`, etc.) são criados automaticamente na primeira execução. **Os dados só são gravados quando você escolhe "Sair" no menu principal.**

# Como os dados são guardados

Cada linha do arquivo é um registro, com os campos separados por `;`:

```
clientes.txt      cpf;nome;endereço;telefone fixo;celulares;nascimento;
servicos.txt      codigo;nome;descrição;preço;
agendamentos.txt  cpf;codigo do serviço;data (DD/MM/AAAA);
relatorios.txt    texto dos relatórios já gerados
```

# O que pratiquei neste projeto

- Funções e organização do código
- Leitura e escrita de arquivos
- Listas, strings (`split`) e laços de repetição
- Validação de entradas do usuário
- Manipulação de datas com o módulo `datetime`
- Menus e submenus no terminal

# Melhorias futuras

- [ ] Tratar entradas inválidas (por exemplo, letras onde se espera número)
- [ ] Salvar os dados automaticamente a cada alteração
- [ ] Separar o código em módulos (clientes, serviços, agendamentos)
- [ ] Trocar os arquivos `.txt` por JSON ou banco de dados (SQLite)
