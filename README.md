# 🍕 Sistema de Autenticação e Gerenciamento - API

Uma API completa para gerenciamento de restaurantes, fornecedores, produtos e pagamentos com autenticação JWT.

## 📋 Sobre o Projeto

Este projeto é uma **API REST** desenvolvida com **FastAPI** que fornece funcionalidades para:
- 🏪 **Autenticação de Restaurantes** - Cadastro, login e gerenciamento de perfil
- 👨‍🍳 **Autenticação de Fornecedores** - Cadastro, login e gerenciamento de perfil
- 📦 **Gerenciamento de Produtos** - CRUD completo de produtos
- 💳 **Sistema de Pagamento** - Integração com Stripe
- 🔐 **Segurança** - Autenticação JWT e hash de senhas com bcrypt

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|-----------|--------|-----------|
| **FastAPI** | ≥0.104.0 | Framework web moderno e rápido |
| **Uvicorn** | ≥0.24.0 | Servidor ASGI |
| **Pydantic** | ≥2.0.0 | Validação de dados |
| **TinyDB** | ≥4.8.0 | Banco de dados NoSQL (JSON) |
| **python-jose** | ≥3.3.0 | Suporte a JWT |
| **Bcrypt** | ≥4.0.0 | Hash de senhas |
| **Passlib** | ≥1.7.4 | Gerenciamento de senhas |
| **Stripe** | ≥14.0.0 | Processamento de pagamentos |

---

## 📁 Estrutura do Projeto

```
repo_temp_api_adm/
├── main.py                    # Arquivo principal da aplicação
├── requirements.txt           # Dependências do projeto
├── data/
│   └── database.json         # Banco de dados TinyDB
├── app/
│   ├── __init__.py
│   ├── config.py             # Configurações da aplicação
│   ├── models/               # Schemas Pydantic
│   │   ├── usuario_restaurante.py
│   │   ├── usuario_fornecedor.py
│   │   ├── produto.py
│   │   └── payment.py
│   ├── rotas/                # Endpoints da API
│   │   ├── restaurante_routes.py
│   │   ├── fornecedor_routes.py
│   │   ├── produto_routes.py
│   │   └── payment_routes.py
│   └── services/             # Lógica de negócio
│       ├── database.py       # Funções de banco de dados
│       └── security.py       # Autenticação e segurança
└── venv/                     # Ambiente virtual Python
```

---

## 🚀 Como Começar

### 1️⃣ Pré-requisitos

- Python 3.13+
- pip (gerenciador de pacotes Python)

### 2️⃣ Instalação

**Clone ou copie o projeto para sua máquina**

```bash
cd repo_temp_api_adm
```

**Crie e ative um ambiente virtual (opcional, mas recomendado)**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

**Instale as dependências**

```bash
pip install -r requirements.txt
```

### 3️⃣ Configuração

**Crie um arquivo `.env` na raiz do projeto:**

```env
SECRET_KEY="sua_chave_secreta_aqui"
STRIPE_API_KEY="sk_test_sua_chave_stripe"
```

> **Nota:** As chaves padrão estão em `app/config.py`. Use valores reais em produção!

### 4️⃣ Rodando o Servidor

```bash
# Com hot-reload (desenvolvimento)
python -m uvicorn main:app --reload

# Sem hot-reload (produção)
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://127.0.0.1:8000`

**Documentação interativa (Swagger UI):** `http://127.0.0.1:8000/docs`

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação.

### Fluxo de Autenticação:

1. **Login** - Envie email e senha para receber um token
2. **Token** - Use o token nos headers para acessar rotas protegidas
3. **Header** - Adicione: `Authorization: Bearer {token}`

### Exemplo:
```bash
curl -X POST "http://127.0.0.1:8000/restaurantes/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"restaurante@email.com", "senha":"senha123"}'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 📚 Endpoints da API

### 🍽️ **RESTAURANTES**

| Método | Rota | Descrição | Autenticado |
|--------|------|-----------|------------|
| POST | `/restaurantes/register` | Cadastrar restaurante | ❌ |
| POST | `/restaurantes/login` | Fazer login | ❌ |
| POST | `/restaurantes/forgot-password` | Recuperar senha | ❌ |
| POST | `/restaurantes/reset-password` | Resetar senha | ❌ |
| PUT | `/restaurantes/perfil` | Editar perfil | ✅ |
| DELETE | `/restaurantes/perfil` | Deletar perfil | ✅ |
| POST | `/restaurantes/metodos-pagamento` | Adicionar método de pagamento | ✅ |
| GET | `/restaurantes/historico-compras` | Obter histórico de compras | ✅ |

### 👨‍🍳 **FORNECEDORES**

| Método | Rota | Descrição | Autenticado |
|--------|------|-----------|------------|
| POST | `/fornecedores/register` | Cadastrar fornecedor | ❌ |
| POST | `/fornecedores/login` | Fazer login | ❌ |
| POST | `/fornecedores/forgot-password` | Recuperar senha | ❌ |
| POST | `/fornecedores/reset-password` | Resetar senha | ❌ |
| PUT | `/fornecedores/perfil` | Editar perfil | ✅ |
| DELETE | `/fornecedores/perfil` | Deletar perfil | ✅ |
| POST | `/fornecedores/metodos-pagamento` | Adicionar método de pagamento | ✅ |
| GET | `/fornecedores/metodos-pagamento` | Listar métodos de pagamento | ✅ |
| PUT | `/fornecedores/metodos-pagamento/{id}` | Editar método de pagamento | ✅ |
| DELETE | `/fornecedores/metodos-pagamento/{id}` | Remover método de pagamento | ✅ |
| GET | `/fornecedores/historico-vendas` | Obter histórico de vendas | ✅ |

### 📦 **PRODUTOS**

| Método | Rota | Descrição | Autenticado |
|--------|------|-----------|------------|
| POST | `/produtos/` | Criar produto | ❌ |
| GET | `/produtos/` | Listar todos os produtos | ❌ |
| GET | `/produtos/{id}` | Obter produto por ID | ❌ |
| PUT | `/produtos/{id}` | Atualizar produto | ❌ |
| DELETE | `/produtos/{id}` | Deletar produto | ❌ |

### 💳 **PAGAMENTO**

| Método | Rota | Descrição | Autenticado |
|--------|------|-----------|------------|
| POST | `/pagamento/checkout` | Criar sessão de checkout (Stripe) | ❌ |
| POST | `/pagamento/webhooks` | Receber webhooks do Stripe | ❌ |

---

## 📝 Exemplos de Uso

### 1. Registrar um Restaurante

```bash
curl -X POST "http://127.0.0.1:8000/restaurantes/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Pizza Gourmet",
    "email": "contato@pizzagourmet.com",
    "senha": "senha123",
    "numero": "123456789",
    "cnpj": "12.345.678/0001-90"
  }'
```

Resposta:
```json
{
  "mensagem": "Restaurante cadastrado com sucesso."
}
```

### 2. Fazer Login

```bash
curl -X POST "http://127.0.0.1:8000/restaurantes/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "contato@pizzagourmet.com",
    "senha": "senha123"
  }'
```

### 3. Editar Perfil (com autenticação)

```bash
curl -X PUT "http://127.0.0.1:8000/restaurantes/perfil" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {seu_token}" \
  -d '{
    "nome": "Pizza Gourmet Premium",
    "endereco": "Rua Principal, 123",
    "cidade": "São Paulo",
    "estado": "SP"
  }'
```

### 4. Criar um Produto

```bash
curl -X POST "http://127.0.0.1:8000/produtos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_produto": "Pizza Margherita",
    "categoria": "Pizzas",
    "preco_unitario": 45.50,
    "estoque_inicial": 100,
    "fornecedor": "Fornecedor XYZ",
    "prazo_medio": "2-3"
  }'
```

### 5. Criar Sessão de Pagamento (Stripe)

```bash
curl -X POST "http://127.0.0.1:8000/pagamento/checkout" \
  -H "Content-Type: application/json" \
  -d '{
    "itens": [
      {
        "nome": "Pizza Margherita",
        "preco_unitario": 45.50,
        "quantidade": 2
      }
    ]
  }'
```

---

## 🗄️ Banco de Dados

A aplicação usa **TinyDB**, um banco de dados NoSQL baseado em arquivos JSON.

### Tabelas:
- `restaurantes` - Dados dos restaurantes
- `fornecedores` - Dados dos fornecedores
- `produtos` - Catálogo de produtos
- `pedidos` - Histórico de pedidos/pagamentos
- `metodos_pagamento` - Métodos de pagamento dos fornecedores

O arquivo do banco está em: `data/database.json`

---

## ⚙️ Configuração

Edit `app/config.py` para customizar:

```python
class Settings(BaseModel):
    secret_key: str = "CHANGE_ME_SUPER_KEY_FOR_CLASSROOM"
    stripe_api_key: str = "sk_test_placeholder"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_path: str = "data/database.json"
    debug_password_reset_token: bool = True
```

---

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env`:

```env
# Chave secreta para JWT (mude em produção!)
SECRET_KEY=sua_chave_super_secreta_aqui

# Chave da API Stripe (modo teste)
STRIPE_API_KEY=sk_test_sua_chave_aqui

# Caminho do banco de dados
DATABASE_PATH=data/database.json
```

---

## 🛡️ Segurança

✅ **Implementado:**
- Hash de senhas com Bcrypt
- Autenticação JWT com expiração
- Validação de email com Pydantic
- CORS configurável
- Proteção de dados sensíveis

⚠️ **Para Produção:**
- Altere `SECRET_KEY` para uma chave forte
- Use `STRIPE_API_KEY` real
- Configure HTTPS
- Implemente rate limiting
- Use banco de dados robusto (MongoDB, PostgreSQL, etc)

---

## 📊 Modelos de Dados

### Restaurante
```json
{
  "nome": "string",
  "email": "email@example.com",
  "senha": "hashed_password",
  "numero": "number",
  "cnpj": "string",
  "foto_perfil": "url",
  "endereco": "string",
  "cidade": "string",
  "estado": "string"
}
```

### Fornecedor
```json
{
  "nome": "string",
  "email": "email@example.com",
  "senha": "hashed_password",
  "numero": "number",
  "cnpj": "string",
  "foto_perfil": "url",
  "endereco": "string",
  "cidade": "string",
  "estado": "string"
}
```

### Produto
```json
{
  "nome_produto": "string",
  "categoria": "string",
  "preco_unitario": "number",
  "estoque_inicial": "integer",
  "fornecedor": "string",
  "prazo_medio": "string"
}
```

---

## 🐛 Troubleshooting

### Erro: "uvicorn: comando não encontrado"
```bash
python -m uvicorn main:app --reload
```

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "Campo não encontrado"
Verifique se a chave secreta está configurada:
```bash
export SECRET_KEY="sua_chave_aqui"
```

---

## 📖 Documentação

**Swagger UI (Documentação Interativa):**
- URL: `http://127.0.0.1:8000/docs`

**ReDoc (Documentação Alternativa):**
- URL: `http://127.0.0.1:8000/redoc`

---

## 🤝 Contribuindo

Sinta-se livre para fazer melhorias, reportar bugs ou adicionar novas funcionalidades!

---

## 📄 Licença

Este projeto é open source e pode ser usado livremente.

---

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. A documentação em `/docs`
2. Os comentários no código
3. Os exemplos de uso acima

---

**Desenvolvido com ❤️ usando FastAPI**
