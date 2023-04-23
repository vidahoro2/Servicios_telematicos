from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import json
spark = SparkSession.builder.appName("LeyendoArchivoTxt").getOrCreate()
app = Flask(__name__)
CORS(app)
    
@app.route('/filtrar_por_pais')
def filtrar_por_pais():
   dfDatosNoa = spark.read.json("./datos.json")
   pais = request.args.get('pais')
   df_filtrado = dfDatosNoa.filter(dfDatosNoa["pais"] == pais)
   json = df_filtrado.collect()
   return jsonify(json)


if __name__ == '__main__':
    app.run()