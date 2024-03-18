# Finance Management API

A Finance Management API é uma solução back-end desenvolvida para gerenciar transações financeiras e resumos de assessores financeiros. Esta API permite criar, atualizar, visualizar e deletar informações de clientes e transações, além de fornecer um resumo das operações financeiras.

## Tecnologias Utilizadas

- **Django REST Framework**: Um poderoso e flexível framework para construir APIs web.
- **SQLite**: Banco de dados utilizado para desenvolvimento e testes.

### Instalação

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Realize as migrações do banco de dados:
   ```bash
   -python manage.py migrate
   -python manage.py makemigrations
   ```
5. Inicie o servidor:
   ```bash
   python manage.py runserver 8080
   ```
   O servidor estará rodando em `http://localhost:8080/`.

## Endpoints

### Clientes

- **Listar Clientes** `GET /clients/`
- **Criar Cliente** `POST /clients/`
  - Parâmetros: `name`, `broker`
- **Detalhes do Cliente** `GET /clients/{client_id}/`
- **Atualizar Cliente** `PUT /clients/{client_id}/`
- **Deletar Cliente** `DELETE /clients/{client_id}/`

### Transações

- **Listar Transações de um Cliente** `GET /clients/{client_id}/transactions/`
- **Criar Transação** `POST /clients/{client_id}/transactions/`
  - Parâmetros: `date`, `value`, `transaction_type` ("Aporte" ou "Resgate")
- **Detalhes da Transação** `GET /transactions/{transaction_id}/`
- **Atualizar Transação** `PUT /transactions/{transaction_id}/`
- **Deletar Transação** `DELETE /transactions/{transaction_id}/`

### Resumo do Assessor

- **Visualizar Resumo** `GET /advisor_summary/`

## Como Criar Usuário

Para criar um usuário e começar a utilizar a API, você pode utilizar o painel administrativo do Django:

1. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```
2. Siga as instruções no terminal para completar a criação do usuário.
3. Acesse `http://localhost:8080/admin/` no seu navegador e faça login com o usuário criado.

## Testes

Para executar os testes, use o seguinte comando:
```bash
python manage.py test
```