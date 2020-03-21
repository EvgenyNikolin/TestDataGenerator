from data_generator.random_units import RandomUnits as rand_units
from data_generator.schema_parser import SchemaParser as parser
import pandas as pd


class DataGenerator (object):
    def __init__(self, p_tbl_schema: dict):
        self.table_schema = parser.parse_table_schema(p_tbl_schema)


