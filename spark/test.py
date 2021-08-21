from pyspark.context import SparkContext
from pyspark import SQLContext, SparkConf

sc_conf = SparkConf()
sc = SparkContext(conf=sc_conf)
print(sc.version)


from pyspark.sql.fuctions import size, split, max, col
#
# textFile = spark.read.text("README.md")
# textFile.select(size(split(textFile.value, "\s+")).name("numWords")).agg(max(col("numWords"))).collect()