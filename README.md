# FastAPI JWT - Sistema de Gerenciamento de Artigos

Este projeto foi desenvolvido com fins didáticos, focado na implementação de autenticação assíncrona utilizando **FastAPI** e **JSON Web Tokens (JWT)**.  
Ele permite o gerenciamento de usuários e artigos, garantindo que operações sensíveis exijam autenticação.

---

## 🚀 Objetivo do Projeto

O sistema foi criado para demonstrar a integração de tecnologias modernas de back-end em Python, incluindo:

- **Autenticação JWT**: Geração e validação de tokens para acesso seguro a rotas.
- **Segurança**: Armazenamento seguro de senhas utilizando hash duplo (SHA256 + Bcrypt).
- **Programação Assíncrona**: Uso de SQLAlchemy com `asyncio` e `asyncpg` para alta performance em operações de banco de dados.
- **Padronização de Dados**: Uso de Pydantic para validação de esquemas e tipos.

---

## 🛠️ Tecnologias Utilizadas

- **Framework**: FastAPI  
- **Banco de Dados**: PostgreSQL (via asyncpg)  
- **ORM**: SQLAlchemy 2.0 (Assíncrono)  
- **Segurança**: Python-Jose (JWT) e Passlib (Bcrypt)  
- **Servidor**: Uvicorn  

---

## 📋 Funcionalidades

- **Usuários**:  
  - Cadastro  
  - Login (geração de token)  
  - Consulta de perfil  
  - Listagem  

- **Artigos**:  
  - Criação (vinculada ao usuário logado)  
  - Edição  
  - Exclusão  
  - Listagem  

- **Segurança**:  
  - Proteção de rotas através de dependências que validam o token no cabeçalho `Authorization`.

---

## 🔧 Como Utilizar

### 1. Pré-requisitos

- Python 3.10+  
- PostgreSQL instalado e rodando  

---

### 2. Configuração do Ambiente

Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

---

### 3. Configuração do Banco de Dados

No arquivo `core/configs.py`, ajuste a constante `DB_URL` com as suas credenciais do PostgreSQL:

```python
DB_URL: str = "postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco"
```

---

### 4. Inicialização do Banco de Dados

Execute o script para criar as tabelas automaticamente:

```bash
python creat-table.py
```

---

### 5. Executando a API

Inicie o servidor de desenvolvimento:

```bash
python main.py
```

A documentação interativa estará disponível em:  
👉 http://localhost:8000/docs

---

## 📌 Endpoints Principais

- `POST /api/v1/users/signup`  
  Cadastro de novo usuário.

- `POST /api/v1/users/login`  
  Login para obtenção do **Access Token**.

- `GET /api/v1/articles`  
  Listagem de todos os artigos cadastrados.

- `POST /api/v1/articles`  
  Criação de artigo (**Requer Token Bearer**).

---

#### Usado para desenvolvimento:
- pip install aiosqlite

#### Principais Libs:
- fastapi
- psycopg2-binary
- sqlalchemy
- asyncpg
- uvicorn
- python-jose[cryptography]
- pytz
- passlib==1.7.4
- python-multipart
- pydantic-settings
- pydantic[email]
- bcrypt==4.0.1