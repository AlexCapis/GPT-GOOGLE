from flask import Flask, jsonify, render_template, request
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
import os
from datetime import datetime
import pymysql

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "6cdddecde869790ad6c4ed5c449addd08f39948071e3802d9bbe07e86bbcf276"
# api_key_path = os.path.join(os.path.dirname(__file__), "api_key.txt")

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

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/api/generar-respuesta', methods=['POST'])
def generar_respuesta():
    try:
        # api_key = request.form['api_key']
        # openai.api_key = api_key
        pregunta = request.form.get('pregunta')

        # Load the model
        llm = OpenAI()

        # Load in some tools to use
        tools = load_tools(["serpapi", "llm-math"], llm=llm)

        # Initialize the agent with the tools, language model, and agent type
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)

        # Use the agent to generate a response
        respuesta = agent.run(pregunta)

         # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar la pregunta y la respuesta en la base de datos
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO GPT (FECHA, PREGUNTAS, RESPUESTAS) VALUES (%s, %s, %s)", (fecha_actual, pregunta, respuesta))
        connection.commit()

        # Cerrar la conexión a la base de datos
        close_db_connection(connection)


        # Devuelve la respuesta generada en formato JSON
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


app.run()