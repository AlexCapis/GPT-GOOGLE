# Para que nuestra imagen se base en python (falta poner la versión, seria interesante poner alpine, ya que es el más usado de LINUX y el más liviano)
From python:

# Creación de una carpeta donde meter el código fuente de nuestra aplicación. Esta carpeta no hace referencia a la maquina física, sino es en base al contenedor.
RUN mkdir -p /home/app

# Indicar al contenedor de donde va a extraer el código
COPY . /home/app

# El puerto
EXPOSE

# Para que corra la aplicación. Indicamos el comando ("python"), la ruta ("/home/app") y el argumento ("prueba3.py")
CMD ["python", "/home/app/prueba3.py"]
