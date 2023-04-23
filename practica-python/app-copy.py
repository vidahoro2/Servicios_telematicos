from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import json

# Crear una instancia de SparkSession  
spark = SparkSession.builder.appName("LeyendoArchivoTxt").getOrCreate()

app = Flask(__name__)
CORS(app)

# Definir la ruta /filtrar_por_pais
@app.route('/filtrar_por_pais')
def filtrar_por_pais():
    
    return jsonify("json")


if __name__ == '__main__':
    app.run()