# Sistema de Automatização de Cálculo de Km

Sistema desenvolvido em Python com interface CustomTkinter para calcular automaticamente a quilometragem percorrida em viagens.

## Funcionalidades

- Registro de viagens com mês de referência
- Registro de dados do motorista, setor, destino e veículo
- Cálculo automático da quilometragem percorrida
- Exclusão de registros de viagens
- Relatórios de quilometragem por modelo de carro e mês
- Relatórios agrupados por setor com totalizações
- Persistência de dados em banco MySQL
- Interface moderna e intuitiva

## Instalação

1. Execute o script SQL no MySQL Workbench:
   - Abra o arquivo `create_database.sql`
   - Execute no MySQL Workbench

2. Configure a senha do MySQL:
   - Edite o arquivo `database.py`
   - Altere a linha `'password': ''` com sua senha do MySQL

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o sistema:
```bash
python main.py
```

## Como usar

### Registrar uma viagem:

1. Preencha todos os campos obrigatórios:
   - Mês de Referência (formato MM/AAAA, ex: 01/2024)
   - Nome do Motorista
   - Setor
   - Local de Destino
   - KM de Saída
   - KM de Chegada
   - Modelo do Carro

2. Clique em "Calcular e Registrar" para processar a viagem

3. Use "Limpar Campos" para resetar o formulário

### Excluir uma viagem:

1. Clique em "Excluir Viagem"
2. Selecione a viagem desejada na lista
3. Clique no botão "Excluir" ao lado da viagem

### Gerar relatórios:

1. Clique em "Gerar Relatórios"
2. Selecione o mês de referência desejado
3. Selecione o modelo do carro
4. Visualize o relatório com:
   - Total geral de quilometragem e viagens
   - Quilometragem por setor (ordenado do maior para o menor)
   - Número de viagens por setor

## Dados salvos

As viagens são automaticamente salvas no banco de dados MySQL `sistema_km`.

## Estrutura do Banco

- **Tabela viagens**: Armazena todos os registros de viagem
  - id (chave primária)
  - mes_referencia (formato MM/AAAA)
  - data_hora
  - motorista
  - setor
  - destino
  - km_saida
  - km_chegada
  - km_percorrida
  - modelo_carro
  - created_at

## Tecnologias Utilizadas

- Python 3.x
- CustomTkinter (Interface gráfica moderna)
- MySQL (Banco de dados)
- mysql-connector-python (Conexão com MySQL)
