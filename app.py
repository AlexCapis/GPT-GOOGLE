
from flask import Flask, jsonify
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a la API del proyecto GPTGoogler"

@app.route('/api/generar-respuesta', methods=['POST'])
def generar_respuesta():
    pregunta = request.json['pregunta']

    try:
        # Configura las claves de API
        os.environ["OPENAI_API_KEY"] = "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"
        os.environ["SERPAPI_API_KEY"] = "6cdddecde869790ad6c4ed5c449addd08f39948071e3802d9bbe07e86bbcf276"

        # Load the model
        llm = OpenAI()

        # Load in some tools to use
        tools = load_tools(["serpapi", "llm-math"], llm=llm)

        # Initialize the agent with the tools, language model, and agent type
        agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

        # Use the agent to generate a response
        respuesta = agent.run(pregunta)

        # Devuelve la respuesta generada en formato JSON
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

