# Importamos las librerías necesarias
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import json

# Creamos una nueva sesión de Spark con el nombre "LeyendoArchivoTxt"
spark = SparkSession.builder.appName("LeyendoArchivoTxt").getOrCreate()

# Creamos una nueva aplicación Flask
app = Flask(__name__)

# Habilitamos CORS para nuestra aplicación Flask
CORS(app)

# Definimos una nueva ruta '/filtrar_por_pais' para nuestra aplicación Flask
@app.route('/filtrar_por_pais')
def filtrar_por_pais():
    # Leemos un archivo JSON y creamos un DataFrame de Spark a partir de él
    dfDatosNoa = spark.read.json("./datosNoa.json")

    # Obtenemos el parámetro 'pais' de la URL de la solicitud HTTP
    pais = request.args.get('pais')

    # Filtramos el DataFrame por la columna 'pais' y mantenemos solo las filas donde 'pais' es igual al parámetro 'pais'
    df_filtrado = dfDatosNoa.filter(dfDatosNoa["pais"] == pais)

    # Recogemos los datos filtrados del DataFrame y los almacenamos en una lista de filas
    json = df_filtrado.collect()

    # Convertimos la lista de filas en una respuesta JSON y la retornamos
    return jsonify(json)

# Si el script se ejecuta directamente (en lugar de ser importado), iniciamos la aplicación Flask
if __name__ == '__main__':
    app.run()
