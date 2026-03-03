# Sistema de Automatização de Cálculo de Km

Sistema desenvolvido em Python com interface CustomTkinter para calcular automaticamente a quilometragem percorrida em viagens.

## Funcionalidades

- Registro de viagens com dados do motorista, setor, destino e veículo
- Cálculo automático da quilometragem percorrida
- Persistência de dados em arquivo JSON
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

1. Preencha todos os campos obrigatórios:
   - Nome do Motorista
   - Setor
   - Local de Destino
   - KM de Saída
   - KM de Chegada
   - Modelo do Carro

2. Clique em "Calcular e Registrar" para processar a viagem

3. Use "Limpar Campos" para resetar o formulário

## Dados salvos

As viagens são automaticamente salvas no banco de dados MySQL `sistema_km`.

## Estrutura do Banco

- **Tabela viagens**: Armazena todos os registros de viagem
  - id (chave primária)
  - data_hora
  - motorista
  - setor
  - destino
  - km_saida
  - km_chegada
  - km_percorrida
  - modelo_carro
  - created_at
