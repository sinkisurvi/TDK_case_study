from datetime import datetime
import util
import re
from pyspark.sql import functions as sf
from pyspark.sql import SparkSession


postgres_config = {
    "url": "jdbc:postgresql://postgres:5432/airflow",
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}

class TdkUseCae:
    def __init__(self, spark, filepath):
        self.spark = spark
        self.filepath = filepath
        self.df = spark.sparkContext.emptyRDD()

    def extract_fields(self):
        self.df = self.spark.read.csv(
            self.filepath, inferSchema=True, sep=" ", ignoreLeadingWhiteSpace=True
        )

        self.df = self.df.withColumn('request_time', sf.concat(sf.col('_c3'),sf.lit('Z'), sf.col('_c4')))\
                        .withColumn('request_time', sf.regexp_replace(sf.col("request_time"), "^\[|\]$", ""))\
                        .withColumn('request_time', sf.to_timestamp('request_time', "dd/MMM/yyyy:H:m:s'Z'Z"))

        split_col = sf.split(self.df['_c5'], ' ')
        self.df = self.df.withColumn('request_method', split_col.getItem(0))
        self.df = self.df.withColumn('request_path', split_col.getItem(1))
        self.df = self.df.withColumn('http_version', split_col.getItem(2))
        self.df = self.df.withColumnRenamed('_c0', 'remote_ip')\
                       .withColumnRenamed('_c1', 'rfc_1413')\
                       .withColumnRenamed('_c2', 'user_id')\
                       .withColumnRenamed('_c6', "response_code")\
                       .withColumnRenamed('_c7', "content_size")
        columns_to_drop = ['_c3', '_c4', '_c5']
        self.df = self.df.drop(*columns_to_drop)
        

    def show(self):
        self.df.show()

    def write_to_db(self):
        self.df.write \
        .format("jdbc") \
        .option("url", postgres_config["url"]) \
        .option("dbtable", "tdk.input_logs") \
        .option("user", postgres_config["user"]) \
        .option("password", postgres_config["password"]) \
        .option("driver", postgres_config["driver"]) \
        .mode("append") \
        .save()
        
if __name__ == "__main__":
    config = util.config()
    date_format = "%d-%m-%Y"
    current_date = datetime.today().strftime(date_format)
    log_file_path = config["log_path"]

    spark = SparkSession.builder.appName("TDK Use Case").getOrCreate()
    use_case = TdkUseCae(spark, f"{log_file_path}{current_date}.log")

    use_case.extract_fields()
    use_case.show()
    use_case.write_to_db()
    
    spark.stop()
