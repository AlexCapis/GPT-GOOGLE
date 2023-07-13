from flask import Flask, jsonify, render_template
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
import os
from flask import Flask, jsonify, request
import pymysql

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "6cdddecde869790ad6c4ed5c449addd08f39948071e3802d9bbe07e86bbcf276"

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def hello():
    return render_template('preguntas.html')


@app.route('/api/generar-respuesta', methods=['POST'])
def generar_respuesta():
    pregunta = input("Introduce tu consulta")

    print(pregunta)
    try:
        # Load the model
        llm = OpenAI()

        # Load in some tools to use
        tools = load_tools(["serpapi", "llm-math"], llm=llm)

        # Initialize the agent with the tools, language model, and agent type
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)

        # Use the agent to generate a response
        respuesta = agent.run(pregunta)

        # Conexión con AWS (esto habrá que borrarlo)
        username = "admin"
        password = "12345678"
        host = "database-1.c3d40xwrejy4.eu-west-3.rds.amazonaws.com" 
        port = 3306

        db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
        )

        # Acceso a la base de datos 
        cursor = db.cursor()
        cursor.connection.commit()
        use_db = ''' USE GPT'''
        cursor.execute(use_db)

        # Insertamos en la tabla elegida los datos obtenidos
        insert_data = '''INSERT INTO GPT (FECHA, PREGUNTAS, RESPUESTAS) 
        VALUES ('%s', '%s', '%s')''' % (pregunta, respuesta)
        cursor.execute(insert_data)

        # Guarda los cambios y cierra la conexión
        db.commit()
        db.close()

        # Devuelve la respuesta generada en formato JSON
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        return jsonify({'error': str(e)}), 50


app.run()
