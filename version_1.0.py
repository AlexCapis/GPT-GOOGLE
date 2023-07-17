from flask import Flask, jsonify, render_template, request
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
import pymysql
import os
import datetime
from keys import *

os.environ["OPENAI_API_KEY"] = gpt
os.environ["SERPAPI_API_KEY"] = serpapi

app = Flask(__name__)
app.config['DEBUG'] = True
app.template_folder = 'src/templates'  # Ruta a la carpeta que contiene los archivos HTML

# Crear una conexión a la base de datos
def create_db_connection():
    return pymysql.connect(
        host='database-1.c3d40xwrejy4.eu-west-3.rds.amazonaws.com',
        user='admin',
        password='12345678',
        database='GPT'
    )

# Cerrar la conexión a la base de datos
def close_db_connection(connection):
    if connection is not None:
        connection.close()

@app.route("/", methods=['GET'])
def hello():
    return render_template('indexjavi.html')


@app.route('/api/generar-respuesta', methods=['GET', 'POST'])
def generar_respuesta():
    if request.method == 'POST':
        pregunta = request.form['pregunta']  # Obtener la pregunta del formulario

        try:
            # Cargamos el modelo
            llm = OpenAI()

            # Cargamos las herramientas que vamos a utilizar
            tools = load_tools(["serpapi", "llm-math"], llm=llm)

            # Inicializamos el agente con las herramientas, el modelo de lenguaje y el tipo de agente
            agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)

            # Utilizamos el agente para generar una respuesta
            respuesta = agent.run(pregunta)

            # Obtenemos la fecha actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Guardamos la fecha en la que hacemos la consulta, la pregunta y la respuesta en la base de datos
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO GPT (FECHA, PREGUNTAS, RESPUESTAS) VALUES (%s, %s, %s)", (fecha_actual, pregunta, respuesta))
            connection.commit()

            # Cerramos la conexión a la base de datos
            close_db_connection(connection)

            # Renderizamos el archivo HTML 'generar_respuesta_javi.html' pasando la respuesta generada como contexto
            return render_template('generar_respuesta_javi.html', respuesta=respuesta)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('formulario.html')

@app.route('/database', methods=['GET'])
def show_database():
    try:
        # Obtener los registros de la base de datos
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM GPT")
        rows = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        close_db_connection(connection)

        # Renderizar el archivo HTML 'database.html' pasando los registros como contexto
        return render_template('database.html', rows=rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
