from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import json
spark = SparkSession.builder.appName("LeyendoArchivoTxt").getOrCreate()
app = Flask(__name__)
CORS(app)


with open('./isd-history.txt','r') as archivo:
   lineas=archivo.readlines()

listaEstaciones = []
encabezado = ["USAF", "WBAN", "STATION NAME", "CTRY", "ST", "CALL", "LAT", "LON", "ELEV(M)", "BEGIN", "END"]
read = False
for linea in lineas:
   if read == False:
      primeraPalabra = linea.split()
      if len(linea.split()):
         if linea.split()[0] == encabezado[0] and linea.split()[1] == encabezado[1] and linea.split()[1] == encabezado[1]:
            read = True
   else:
      nombre = linea[13:43]
      pais = linea[43:45]
      lat = linea[57:64]
      lon = linea[65:72]
      if len(pais.replace(" ","")) !=0:
         if len(nombre.replace(" ","")) == 0:
            nombre = "NA"
         else:
            nombre =  nombre.strip()
         if len(lat.replace(" ","")) !=0 and len(lon.replace(" ","")) !=0:
            if lat != "+00.000" and lon != "+000.000":
               estacion = {"nombre":nombre,"pais":pais,"lat":float(lat),"lon":float(lon)}
               listaEstaciones.append(estacion)
    
@app.route('/filtrar_por_pais')
def filtrar_por_pais():
   #dfDatosNoa = spark.read.json("./datos.json")
   pais = request.args.get('pais')
   dfDatosNoa = spark.createDataFrame(listaEstaciones)
   df_filtrado = dfDatosNoa.filter(dfDatosNoa["pais"] == pais)
   json = df_filtrado.collect()
   return jsonify(json)


if __name__ == '__main__':
    app.run()