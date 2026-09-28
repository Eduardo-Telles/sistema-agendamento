# Sistema de Agendamento

Projeto desenvolvido na faculdade no 1º semestre em Python. É um programa de terminal para gerenciar clientes, serviços e agendamentos de um pequeno negócio, guardando os dados em arquivos '.txt'.

# Funcionalidades

- **Clientes:** listar, buscar, incluir, alterar e excluir (com validação de CPF de 11 dígitos e CPF único)
- **Serviços:** listar, buscar, incluir, alterar e excluir (código único)
- **Agendamentos:** listar, buscar, incluir, alterar (serviço ou data) e excluir, sempre conferindo se o cliente e o serviço existem
- **Relatórios:** menu criado, funcionalidade ainda em desenvolvimento

# Como rodar

Você só precisa do Python 3 instalado.
bash
git clone https://github.com/Eduardo-Telles/sistema-agendamento.git
cd sistema-agendamento
python main.py


Os arquivos de dados ('clientes.txt', 'servicos.txt', etc.) são criados automaticamente na primeira execução. **Os dados só são gravados quando você escolhe "Sair" no menu principal.**

# Como os dados são guardados

Cada linha do arquivo é um registro, com os campos separados por ';':

clientes.txt      cpf;nome;endereço;telefone fixo;celulares;nascimento;
servicos.txt      codigo;nome;descrição;preço;
agendamentos.txt  cpf;nome do cliente;nome do serviço;codigo do serviço;data;

# O que pratiquei neste projeto

- Funções e organização do código
- Leitura e escrita de arquivos
- Listas, strings ('split') e laços de repetição
- Validação de entradas do usuário
- Menus e submenus no terminal

# Melhorias futuras

- [ ] Implementar o módulo de relatórios
- [ ] Tratar entradas inválidas (por exemplo, letras onde se espera número)
- [ ] Salvar os dados automaticamente a cada alteração
- [ ] Excluir também os agendamentos de um cliente ou serviço removido
- [ ] Separar o código em módulos (clientes, serviços, agendamentos)
- [ ] Trocar os arquivos '.txt' por JSON ou banco de dados (SQLite)
