#Conectar Python y Spark
from pyspark import SparkConf,SparkContext
config = (SparkConf().setMaster("local").setAppName("estaciones").set("spark.executor.memory","1g"))

sc = SparkContext(conf = config)
#Crear Sesión en Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("estacionesClimaticas").config("spark.executor.memory","1g").getOrCreate()

#Creación de DF
noaaData = spark.read.json("datosNoa.json")
#noaaData.show()


# Filtrar los datos por país

def filtrarPorEstaciones(country):
	estacionesDelPais = noaaData.filter(noaaData.pais == country)
	return estacionesDelPais.show()
	

# Mostrar las estaciones filtradas
filtrarPorEstaciones("US")




