from flask import Flask, render_template, request, jsonify
import mysql.connector

cnx = mysql.connector.connect(user='root', password='12345678',
                               host='127.0.0.1',
                              )

cursor  = cnx.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS clinica")

cnx = mysql.connector.connect(user='root', password='12345678',
                               host='127.0.0.1',
                               database = "clinica"
                              )

cursor  = cnx.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS pacientes (
                id INT AUTO_INCREMENT,
                documento INT,
                nombres VARCHAR(255),
                apellidos VARCHAR(255),
                edad INT,
                direccion VARCHAR(255),
                sexo VARCHAR(1), 
                peso FLOAT(10, 4),
                estatura FLOAT(10, 4),
                fumador BOOLEAN,
                tiempo_fumando INT,
                dieta BOOLEAN,
                atendido BOOLEAN,
                PRIMARY KEY (id)
            ); """)





app = Flask(__name__)




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/saludo', methods=['POST'])
def saludo():
    print("Data")
    documento = request.form.get('documento')
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    edad = request.form.get('edad')
    direccion = request.form.get('direccion') or ""
    sexo = request.form.get('sexo') or ""
    if sexo == "option1":
        sexo = "M"
    else:
        sexo = "F"
    
    peso_kilogramos = request.form.get('peso_kilogramos')
    estatura = request.form.get('estatura')
    fumador = request.form.get('fumador')
    if fumador == "option1":
        fumador = "true"
    else:
        fumador = "false"
        
        
        
    tiempo_fumando = request.form.get('tiempo_fumando') or 0
    dieta = request.form.get('dieta')
    if dieta == "option1":
        dieta = "true"
    else:
        dieta = "false"
    
    cursor.execute(f"""INSERT INTO pacientes (documento,   nombres,    apellidos,     edad,  direccion,    sexo,    peso,    estatura,     fumador,    tiempo_fumando,    dieta, atendido) 
                  VALUES                     ({(documento)}, "{nombres}","{apellidos}", {(edad)},"{direccion}", "{sexo}", {(peso_kilogramos)}, {(estatura)}, {fumador}, {tiempo_fumando}, {dieta}, false);
               """)
    
    cnx.commit()
    cursor.execute("SELECT * FROM pacientes")
    result = cursor.fetchall()

    for x in result:
        print(x)


    return render_template('index.html')

@app.route('/pacientes', methods=['GET'])
def pacientes():
    cursor.execute("SELECT * FROM pacientes WHERE atendido=0")
    result = cursor.fetchall()

    return jsonify(result)


@app.route('/tablas')
def tablas():
    return render_template('tabla.html')


@app.route('/atender/<id>')
def atender(id):
    print(id)
    cursor.execute(f"""UPDATE pacientes
                    SET 
                        atendido = true
                    WHERE
                         id = {id};
                   """)
    cnx.commit()
    return render_template('tabla.html')

if __name__ == '__main__':
    app.run()
