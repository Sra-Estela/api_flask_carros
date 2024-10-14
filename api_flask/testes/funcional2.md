## Estrutura de Pastas:
```
|api_flask_exemplo/
│  ├──templates/
|  │  ├──adicionado.html
|  │  ├──body.html
|  │  ├──carros.html
|  │  └──index.html
│  ├──testes/
│  ├──venv/
├──banco.sql
├──main.py
└──requeriments.txt
```

---

## Arquivo `adicionado.html`:
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carro Adicionado</title>
</head>
<body>
    <h1>Carro Adicionado com Sucesso!</h1>
    <p>Detalhes do carro:</p>
    <ul>
        <li>ID: {{ carro.id }}</li>
        <li>Marca: {{ carro.marca }}</li>
        <li>Modelo: {{ carro.modelo }}</li>
        <li>Ano: {{ carro.ano }}</li>
    </ul>
    <a href="{{ url_for('pagina_inicial') }}">Voltar à Página Inicial</a>
</body>
</html>
```

---

## Arquivo `body.html`:
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página 2</title>
</head>
<body>
    <form action="{{ url_for('create_carro') }}" method="POST">
        <label for="carro">Informações do carro (Formato: marca,modelo,ano):</label>
        <input type="text" name="carro" id="carro" placeholder="Fiat,Elba,1997">
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
```

---

## Arquivo `carros.html`:
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Carros</title>
</head>
<body>
    <h1>Carros Registrados</h1>
    <ul>
        {% for carro in carros %}
        <li>
            ID: {{ carro.id }} - Marca: {{ carro.marca }} - Modelo: {{ carro.modelo }} - Ano: {{ carro.ano }}
        </li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('pagina_inicial') }}">Voltar à Página Inicial</a>
</body>
</html>
```

---

## Arquivo `index.html`:
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pagina 1</title>
</head>
<body>
    <a href="{{ url_for('get_carros') }}">Carros</a>
    <a href="{{ url_for('body') }}">Página 2</a>
</body>
</html>
```

---

## Arquivo `banco.sql`:
```sql
CREATE DATABASE `db_banco_py`;

USE `db_banco_py`;

CREATE TABLE `tb_carros` (
	`id` int primary key not null auto_increment,
    `marca` varchar(100) not null,
    `modelo` varchar(100) not null,
    `ano` int not null
);

INSERT INTO `tb_carros` VALUES 
(1, 'Fiat', 'Marea', 1999), 
(2, 'Fiat', 'Uno', 1992), 
(3, 'Ford', 'Escort', 1985), 
(4, 'Chevrolet', 'Chevette', 1978), 
(5, 'Volkswagen', 'Fusca', 1962);

SELECT * FROM `tb_carros`; 
```

---

## Arquivo `main.py`:
```python
from flask import Flask, make_response, jsonify, request, url_for, render_template
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'db_banco_py'

def get_db_connection():
    return mysql.connector.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        password = app.config['MYSQL_PASSWORD'],
        database = app.config['MYSQL_DB']
    )

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/body')
def body():
    return render_template('body.html')

@app.route('/carros', methods=['GET'])
def get_carros():
    db = get_db_connection()
    cursor = db.cursor(dictionary = True)
    cursor.execute('SELECT * FROM tb_carros')
    carros = cursor.fetchall()
    
    for carro in carros:
        print(carro)
    
    cursor.close()
    db.close()
    return render_template('carros.html', carros=carros)

@app.route('/carros', methods=['POST'])
def create_carro():
    carro_dados = request.form['carro'].split(',')
    if len(carro_dados) != 3:
        return make_response(jsonify({'error': 'Formato inválido. Use: marca,modelo,ano'}), 400)

    marca, modelo, ano = carro_dados
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO tb_carros (marca, modelo, ano) VALUES (%s, %s, %s)', (marca.strip(), modelo.strip(), int(ano.strip())))
    db.commit()

    novo_id = cursor.lastrowid
    cursor.close()
    db.close()

    novo_carro = {
        'id': novo_id, 
        'marca': marca.strip(),
        'modelo': modelo.strip(),
        'ano': int(ano.strip())
    }

    return render_template('adicionado.html', carro=novo_carro)

# carro = {
#     'id': 6,
#     'marca': 'Fiat',
#     'modelo': 'Elba',
#     'ano': 1997
# }

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Arquivo `requeriments.txt`:
```txt
blinker==1.8.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
flask-mysql-connector==1.1.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
mysql-connector-python==9.0.0
numpy==2.1.2
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2024.2
six==1.16.0
tzdata==2024.2
Werkzeug==3.0.4
```

---

Aqui vai uma explicação detalhada do código e da estrutura do projeto:

# Estrutura do Projeto

O projeto é uma API simples usando Flask que interage com um banco de dados MySQL. Ele permite adicionar e listar carros, além de visualizar uma confirmação quando um carro é adicionado.

## Estrutura de Pastas
- **api_flask_exemplo/**: Pasta raiz do projeto.
  - **templates/**: Contém os templates HTML usados pelo Flask.
    - **adicionado.html**: Página de confirmação quando um carro é adicionado.
    - **body.html**: Página com um formulário para adicionar um carro.
    - **carros.html**: Página que exibe a lista de carros cadastrados.
    - **index.html**: Página inicial com links para outras páginas.
  - **testes/**: Provavelmente reservada para testes (não está utilizada).
  - **venv/**: Ambiente virtual Python.
- **banco.sql**: Script SQL para criação do banco de dados e tabela `tb_carros`.
- **main.py**: O código principal da API Flask.
- **requeriments.txt**: Lista de dependências necessárias para rodar o projeto.

# Arquivos HTML

### `adicionado.html`
Essa página é exibida quando um carro é adicionado com sucesso. Usa **placeholders** do Jinja2 (`{{ carro.id }}`, etc.) para exibir as informações do carro recém-adicionado.
```html
<ul>
    <li>ID: {{ carro.id }}</li>
    <li>Marca: {{ carro.marca }}</li>
    <li>Modelo: {{ carro.modelo }}</li>
    <li>Ano: {{ carro.ano }}</li>
</ul>
```
- A função `url_for('pagina_inicial')` gera um link para a rota principal.

### `body.html`
Contém um formulário simples para adicionar um carro, onde os dados são enviados via método **POST** para a rota `create_carro`.
```html
<form action="{{ url_for('create_carro') }}" method="POST">
    <input type="text" name="carro" placeholder="Fiat,Elba,1997">
    <input type="submit" value="Enviar">
</form>
```
- `url_for('create_carro')` cria um link dinâmico para a rota de criação de um carro.

### `carros.html`
Página que lista os carros cadastrados no banco de dados.
```html
{% for carro in carros %}
    <li>ID: {{ carro.id }} - Marca: {{ carro.marca }} - Modelo: {{ carro.modelo }} - Ano: {{ carro.ano }}</li>
{% endfor %}
```
- O loop **for** itera sobre uma lista de carros e exibe seus detalhes.

### `index.html`
Página inicial com links para a lista de carros e para a página de adição de carros.
```html
<a href="{{ url_for('get_carros') }}">Carros</a>
<a href="{{ url_for('body') }}">Página 2</a>
```

# Arquivo SQL: `banco.sql`
Este arquivo cria o banco de dados `db_banco_py`, define a tabela `tb_carros` e insere alguns registros iniciais. Ao final, há uma consulta para selecionar todos os registros da tabela.
```sql
CREATE DATABASE `db_banco_py`;
USE `db_banco_py`;
CREATE TABLE `tb_carros` (
    `id` int primary key not null auto_increment,
    `marca` varchar(100) not null,
    `modelo` varchar(100) not null,
    `ano` int not null
);
```
- **auto_increment**: O campo `id` é gerado automaticamente.
- **INSERT**: São inseridos 5 carros no banco.
- **SELECT**: Consulta todos os registros.

# Arquivo `main.py`

### Imports e Configurações
```python
from flask import Flask, make_response, jsonify, request, url_for, render_template
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'db_banco_py'
```
- **Flask** é o framework usado.
- **mysql.connector** é o módulo que permite conectar ao MySQL.
- O bloco de configuração define os parâmetros da conexão com o banco de dados.

### Função `get_db_connection`
Cria uma conexão com o banco de dados MySQL.
```python
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
```

### Rota `/` (Página Inicial)
```python
@app.route('/')
def pagina_inicial():
    return render_template('index.html')
```
- Renderiza o arquivo **index.html**.

### Rota `/body` (Formulário)
```python
@app.route('/body')
def body():
    return render_template('body.html')
```
- Renderiza o arquivo **body.html**, que contém o formulário para adicionar carros.

### Rota `/carros` (GET)
```python
@app.route('/carros', methods=['GET'])
def get_carros():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tb_carros')
    carros = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template('carros.html', carros=carros)
```
- **GET**: Recupera os dados de todos os carros do banco de dados.
- O método `cursor.fetchall()` retorna todos os registros e os passa para o template `carros.html`.

### Rota `/carros` (POST)
```python
@app.route('/carros', methods=['POST'])
def create_carro():
    carro_dados = request.form['carro'].split(',')
    if len(carro_dados) != 3:
        return make_response(jsonify({'error': 'Formato inválido. Use: marca,modelo,ano'}), 400)

    marca, modelo, ano = carro_dados
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO tb_carros (marca, modelo, ano) VALUES (%s, %s, %s)', (marca.strip(), modelo.strip(), int(ano.strip())))
    db.commit()

    novo_id = cursor.lastrowid
    cursor.close()
    db.close()

    novo_carro = {
        'id': novo_id,
        'marca': marca.strip(),
        'modelo': modelo.strip(),
        'ano': int(ano.strip())
    }

    return render_template('adicionado.html', carro=novo_carro)
```
- **POST**: Adiciona um novo carro ao banco de dados. A função `request.form['carro']` recebe os dados do formulário e os insere na tabela `tb_carros`.
- Após o carro ser adicionado, o ID do novo registro é recuperado (`cursor.lastrowid`) e o template `adicionado.html` é renderizado com os dados do carro adicionado.

# Arquivo `requeriments.txt`
Lista as dependências necessárias para o projeto, como Flask, MySQL Connector, e outras bibliotecas Python.

---

Essa é uma visão geral e explicação detalhada do projeto. Se precisar de mais detalhes ou tiver dúvidas sobre algo específico, é só avisar!