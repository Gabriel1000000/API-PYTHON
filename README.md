# API-PYTHON
 
 Desenvolvi esta API de e-commerce com Flask, permitindo o cadastro e autenticação de usuários, além da gestão de produtos e do carrinho de compras.

## 🚀 Tecnologias Utilizadas
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-CORS
- SQLite

## 📌 Instalação e Configuração


### Criar um Ambiente Virtual

```bash
python -m venv venv
```

Ativar o ambiente virtual:

Linux/macOS (Terminal)

```bash
source venv/bin/activate 
```

Usando o Windows (CMD)

```bash
venv\Scripts\activate  
```

Windows (PowerShell)

```bash
.\venv\Scripts\activate
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Configurar o Banco de Dados
Abra o terminal no diretorio do seu projeto e ative a venv caso esteja usando ela para guardar as libs que você está utilizando.

Enseguida escreva o nome do seu arquivo principal na variavel "FLASK_APP=":

Usando o Windows (CMD)

```bash
set FLASK_APP=api.py
```

Windows (PowerShell)

```bash
$env:FLASK_APP="api.py"
```

Linux/macOS (Terminal)

```bash
export FLASK_APP=api.py
```

### Criando o Banco de Dados

É de extrema importância que tenha feito a devida configuração do [Bandco de Dados](#configurar-o-banco-de-dados)

Digite o seguinte comando no terminal:

```bash
flask shell
```
Agora, use este comando para criar o banco de dados:

```bash
db.create_all()
```

Para confirmar a criação, execute:

```bash
db.session.commit()
```

Se precisar apagar o banco de dados já criado, repita os passos anteriores e digite:

```bash
 db.drop_all()
```

Para sair do shell do Flask, use:

```bash
>exit()
```

### Executar a API

É de extrema importância que tenha feito a devida configuração do [Bandco de Dados](#configurar-o-banco-de-dados)

```bash
python api.py
```


A API estará disponível em `http://127.0.0.1:5000/`.

## 🔑 Autenticação e Autorização
A API usa `Flask-Login` para autenticação de usuários. Algumas rotas requerem autenticação e privilégios de administrador.

- Usuários comuns podem se cadastrar e gerenciar seu carrinho de compras.
- Apenas administradores podem adicionar, editar e remover produtos.

## 📡 Endpoints

### 🛠️ Autenticação
- `POST /registration` → Cadastro de usuário
- `POST /registration-admin` → Cadastro de administrador
- `POST /login` → Login do usuário
- `POST /logout` → Logout do usuário

### 📦 Produtos
- `POST /api/products/add` → Adicionar produto *(Admin)*
- `DELETE /api/products/delete/<product_id>` → Remover produto *(Admin)*
- `PUT /api/products/update/<product_id>` → Atualizar produto *(Admin)*
- `GET /api/products` → Listar todos os produtos
- `GET /api/products/<product_id>` → Detalhes de um produto

### 🛒 Carrinho de Compras
- `POST /api/cart/add/<product_id>` → Adicionar item ao carrinho
- `DELETE /api/cart/remove/<product_id>` → Remover item do carrinho
- `GET /api/cart` → Listar itens do carrinho
- `POST /api/cart/checkout` → Finalizar compra

## 🏗️ Estrutura do Projeto
```
📂 API-PYTHON/
├── api.py            # Arquivo principal da API
├── db.py             # Configuração do banco de dados
├── config.py         # Configuração do Flask
├── decorators.py     # Decoradores para autenticação
├── Methods.py        # Métodos de lógica da API
├── User.py           # Modelo de usuário
├── Product.py        # Modelo de produto
├── CartIntem.py      # Modelo de item do carrinho
├── requirements.txt  # Dependências
└── README.md         # Documentação
```

## 🛠️ Melhorias Futuras
- Implementação de testes automatizados
- Integração com um gateway de pagamento
- Melhorias na segurança da API

## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para utilizá-lo e contribuir! 🚀
