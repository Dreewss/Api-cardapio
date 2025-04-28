### API RESTful para Cardápio de Restaurante

## Visão Geral

Esta API RESTful foi desenvolvida para gerenciar um cardápio de restaurante, permitindo operações CRUD (Create, Read, Update, Delete) para categorias, ingredientes, itens do menu e pedidos. A API foi construída usando Python com FastAPI e PostgreSQL como banco de dados.

## Estrutura do Banco de Dados

O banco de dados consiste nas seguintes tabelas:

- **categories**: Categorias do cardápio (ex: Entradas, Pratos Principais, Sobremesas)
- **ingredients**: Ingredientes utilizados nos pratos
- **menu_items**: Itens do cardápio
- **menu_item_ingredients**: Tabela de associação entre itens do menu e ingredientes
- **orders**: Pedidos dos clientes
- **order_items**: Itens incluídos em cada pedido


## Configuração e Instalação

### Pré-requisitos

- Python 3.8+
- PostgreSQL 
- pip (gerenciador de pacotes Python)


### Instalação

1. Clone o repositório:


```shellscript
git clone https://github.com/Dreewss/Api-cardapio.git
cd api-cardapio
```

2. Instale as dependências:


```shellscript
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:


```shellscript
# .env
DATABASE_URL=postgresql://usuario:senha@seu-host-neon.com/api-cardapio
```

4. Execute a aplicação:


```shellscript
uvicorn app.main:app --reload
```

## Criando Itens no Cardápio

Para criar itens no cardápio, você precisa seguir uma sequência lógica:

1. Criar categorias
2. Criar ingredientes
3. Criar itens do menu (associando-os a categorias e ingredientes)


### 1. Criando Categorias

#### Exemplo de requisição:

```shellscript
curl -X 'POST' \
  'http://localhost:8000/categories/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Entradas",
  "description": "Pratos para começar sua refeição"
}'
```

#### Resposta:

```json
{
  "id": 1,
  "name": "Entradas",
  "description": "Pratos para começar sua refeição"
}
```

### 2. Criando Ingredientes

#### Exemplo de requisição:

```shellscript
curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Tomate",
  "is_allergen": false
}'
```

#### Resposta:

```json
{
  "id": 1,
  "name": "Tomate",
  "is_allergen": false
}
```

### 3. Criando Itens do Menu

#### Exemplo de requisição:

```shellscript
curl -X 'POST' \
  'http://localhost:8000/menu-items/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Bruschetta",
  "description": "Pão italiano com tomate, manjericão e azeite",
  "price": 15.90,
  "image_url": "https://example.com/images/bruschetta.jpg",
  "is_available": true,
  "category_id": 1,
  "ingredient_ids": [1, 2, 3]
}'
```

#### Resposta:

```json
{
  "id": 1,
  "name": "Bruschetta",
  "description": "Pão italiano com tomate, manjericão e azeite",
  "price": 15.9,
  "image_url": "https://example.com/images/bruschetta.jpg",
  "is_available": true,
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Entradas",
    "description": "Pratos para começar sua refeição"
  },
  "ingredients": [
    {
      "id": 1,
      "name": "Tomate",
      "is_allergen": false
    },
    {
      "id": 2,
      "name": "Manjericão",
      "is_allergen": false
    },
    {
      "id": 3,
      "name": "Azeite",
      "is_allergen": false
    }
  ]
}
```

## Exemplos Completos para Criar um Cardápio

Aqui está um script completo para criar um cardápio básico:

### 1. Criar Categorias

```shellscript
# Criar categoria de Entradas
curl -X 'POST' \
  'http://localhost:8000/categories/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Entradas",
  "description": "Pratos para começar sua refeição"
}'

# Criar categoria de Pratos Principais
curl -X 'POST' \
  'http://localhost:8000/categories/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Pratos Principais",
  "description": "Pratos principais do nosso cardápio"
}'

# Criar categoria de Sobremesas
curl -X 'POST' \
  'http://localhost:8000/categories/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Sobremesas",
  "description": "Doces para finalizar sua refeição"
}'

# Criar categoria de Bebidas
curl -X 'POST' \
  'http://localhost:8000/categories/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Bebidas",
  "description": "Bebidas para acompanhar sua refeição"
}'
```

### 2. Criar Ingredientes

```shellscript
# Criar ingredientes comuns
curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Tomate",
  "is_allergen": false
}'

curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Manjericão",
  "is_allergen": false
}'

curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Azeite",
  "is_allergen": false
}'

curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Queijo",
  "is_allergen": true
}'

curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Carne",
  "is_allergen": false
}'

curl -X 'POST' \
  'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Chocolate",
  "is_allergen": true
}'
```

### 3. Criar Itens do Menu

```shellscript
# Criar uma entrada
curl -X 'POST' \
  'http://localhost:8000/menu-items/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Bruschetta",
  "description": "Pão italiano com tomate, manjericão e azeite",
  "price": 15.90,
  "image_url": "https://example.com/images/bruschetta.jpg",
  "is_available": true,
  "category_id": 1,
  "ingredient_ids": [1, 2, 3]
}'

# Criar um prato principal
curl -X 'POST' \
  'http://localhost:8000/menu-items/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Filé Mignon",
  "description": "Filé mignon grelhado com molho de vinho tinto e batatas",
  "price": 59.90,
  "image_url": "https://example.com/images/filet.jpg",
  "is_available": true,
  "category_id": 2,
  "ingredient_ids": [3, 5]
}'

# Criar uma sobremesa
curl -X 'POST' \
  'http://localhost:8000/menu-items/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Mousse de Chocolate",
  "description": "Mousse de chocolate belga com calda de frutas vermelhas",
  "price": 18.90,
  "image_url": "https://example.com/images/mousse.jpg",
  "is_available": true,
  "category_id": 3,
  "ingredient_ids": [6]
}'

# Criar uma bebida
curl -X 'POST' \
  'http://localhost:8000/menu-items/' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Suco de Laranja",
  "description": "Suco de laranja natural",
  "price": 8.90,
  "image_url": "https://example.com/images/orange-juice.jpg",
  "is_available": true,
  "category_id": 4,
  "ingredient_ids": []
}'
```

## Documentação da API

A documentação completa da API está disponível em:

```plaintext
http://localhost:8000/docs
```

### Endpoints Principais

#### Categorias

- `GET /categories/` - Listar todas as categorias
- `POST /categories/` - Criar uma nova categoria
- `GET /categories/{category_id}` - Obter detalhes de uma categoria
- `PUT /categories/{category_id}` - Atualizar uma categoria
- `DELETE /categories/{category_id}` - Excluir uma categoria


#### Ingredientes

- `GET /ingredients/` - Listar todos os ingredientes
- `POST /ingredients/` - Criar um novo ingrediente
- `GET /ingredients/{ingredient_id}` - Obter detalhes de um ingrediente
- `PUT /ingredients/{ingredient_id}` - Atualizar um ingrediente
- `DELETE /ingredients/{ingredient_id}` - Excluir um ingrediente


#### Itens do Menu

- `GET /menu-items/` - Listar todos os itens do menu
- `POST /menu-items/` - Criar um novo item do menu
- `GET /menu-items/{menu_item_id}` - Obter detalhes de um item do menu
- `PUT /menu-items/{menu_item_id}` - Atualizar um item do menu
- `DELETE /menu-items/{menu_item_id}` - Excluir um item do menu


#### Pedidos

- `GET /orders/` - Listar todos os pedidos
- `POST /orders/` - Criar um novo pedido
- `GET /orders/{order_id}` - Obter detalhes de um pedido
- `PUT /orders/{order_id}` - Atualizar um pedido
- `DELETE /orders/{order_id}` - Excluir um pedido


## Parâmetros de Consulta

### Filtragem de Itens do Menu

Você pode filtrar itens do menu por categoria e disponibilidade:

```plaintext
GET /menu-items/?category_id=1&available_only=true
```

### Filtragem de Pedidos

Você pode filtrar pedidos por status:

```plaintext
GET /orders/?status=pending
```

## Considerações Finais

Esta API foi projetada para ser fácil de usar e extensível. Você pode expandir suas funcionalidades adicionando:

- Autenticação e autorização
- Upload de imagens para os itens do menu
- Sistema de avaliações de clientes
- Relatórios de vendas e estatísticas
- Integração com sistemas de pagamento
