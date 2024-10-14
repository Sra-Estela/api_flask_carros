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