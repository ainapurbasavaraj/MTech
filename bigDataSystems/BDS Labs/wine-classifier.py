import operator
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.mllib.clustering import KMeans
from numpy import array
from math import sqrt
import matplotlib.pyplot as plt

# data load

datafile = "./wine.csv"
sc = SparkContext("local", "wine app")
sqlContext = SQLContext(sc)

df = sqlContext.read.format("csv").options(header="true", inferschema="true").load(datafile)
df.show(n=2)
df.printSchema()

# data prep
from pyspark.ml.feature import VectorAssembler
vectorAssembler = VectorAssembler(inputCols = ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol"], outputCol = 'features')

df2 = vectorAssembler.transform(df)
df2 = df2.select(['features', 'quality'])
df2.show(3)

train, test = df2.randomSplit([0.7, 0.3], seed = 2018)

# train on 70% of the data
from pyspark.ml.classification import DecisionTreeClassifier
dt = DecisionTreeClassifier(featuresCol = 'features', labelCol = 'quality', maxDepth = 3)
dtModel = dt.fit(train)

# test classifier with 30% of the data
predictions = dtModel.transform(test)
predictions.select("features", "quality", "prediction").show(20)



