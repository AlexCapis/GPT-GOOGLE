from flask import Flask, jsonify
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import pymysql
import os
import datetime

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "6cdddecde869790ad6c4ed5c449addd08f39948071e3802d9bbe07e86bbcf276"

app = Flask(__name__)
app.config['DEBUG'] = True

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
    return "Bienvenido a la API del proyecto GPTGoogler"


@app.route('/api/generar-respuesta', methods=['POST'])
def generar_respuesta():
    pregunta = input("Introduce tu consulta: ")

    try:
        # Cargamos el modelos
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

        # Devuelve la respuesta generada en formato JSON
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


app.run()