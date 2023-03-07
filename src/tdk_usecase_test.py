import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
from pyspark.sql.readwriter import DataFrameWriter
from tdk_usecase import TdkUseCae


class MockDataFrameWriter(DataFrameWriter):
    def __init__(self, df):
        self.df = df
        self.format_options = {}
        self.save_options = {}

    def format(self, source):
        self.format_options['source'] = source
        return self

    def option(self, key, value):
        self.save_options[key] = value
        return self

    def mode(self, save_mode):
        self.save_options['mode'] = save_mode
        return self

    def save(self):
        pass

class TestTdkUseCase(unittest.TestCase):
    def setUp(self):
        self.spark = SparkSession.builder.master("local").appName("unit-testing").getOrCreate()

    def tearDown(self):
        self.spark.stop()

    def test_extract_fields(self):
        use_case = TdkUseCae(self.spark, "test.log")
        mock_read_csv = MagicMock()
        use_case.spark.read.csv = mock_read_csv
        use_case.extract_fields()


    def test_write_to_db(self):
        use_case = TdkUseCae(self.spark, "test.log")
        mock_write = MagicMock(spec=MockDataFrameWriter)
        use_case.df.write = mock_write

        use_case.write_to_db()


    def test_show(self):
        use_case = TdkUseCae(self.spark, "test.log")
        mock_show = MagicMock()
        use_case.df.show = mock_show

        use_case.show()

        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
