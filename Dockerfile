# Para que nuestra imagen se base en python 
FROM python:3.11.4

# Creación de una carpeta donde meter el código fuente de nuestra aplicación. Esta carpeta no hace referencia a la maquina física, sino es en base al contenedor.
WORKDIR /app

# Indicar al contenedor de donde va a extraer el código
COPY . /app

RUN pip install -r requirements.txt

# El puerto
EXPOSE 5000

# Para que corra la aplicación.
CMD ["python", "/app/version_1.0.py"]
