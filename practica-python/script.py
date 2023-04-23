from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import json
import webbrowser
# Crear una instancia de SparkSession  
spark = SparkSession.builder.appName("LeyendoArchivoTxt").getOrCreate()


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
#print(listaEstaciones)
listaEstaciones.pop(0)
with open("./datos.json", "w") as archivo:
    json.dump(listaEstaciones, archivo)


def filtrar_por_valor(dataFrame: DataFrame, pais: str) -> DataFrame:
    df_filtrado = dataFrame.filter(dataFrame["pais"] == pais)
    return df_filtrado

def jsonConv(pais: str) -> any:
   dfDatosNoa = spark.read.json("./datos.json")
   dfDatosNoaFiltrado = filtrar_por_valor(dfDatosNoa,pais)
   json = dfDatosNoaFiltrado.toJSON().collect()
   return json
# Mostrar los datos
#jsonData = jsonConv("SV")
#print(jsonData)

#url = 'http://127.0.0.1:5500/index.html'
#webbrowser.open_new_tab(url)


