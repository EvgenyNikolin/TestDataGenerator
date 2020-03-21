import pandas as pd
import re


class SchemaParser(object):
    @staticmethod
    def parse_column_type(p_non_parsed_column_type: str):
        type_associations = {
            'INT': ['INTEGER', 'INT', 'BIGINT', 'TINYINT']
            ,'DECIMAL': ['NUMBER', 'DECIMAL', 'FLOAT', 'NUMERIC', 'DOUBLE', 'REAL']
            ,'DATETIME': ['DATE', 'TIME', 'DATETIME', 'TIMESTAMP']
            ,'BIT': ['BIT', 'BOOLEAN', 'BOOL']
            ,'STRING': ['VARCHAR', 'NVARCHAR', 'STR', 'STRING', 'CHAR', 'CHARACTER', 'TEXT']
        }

        for column_type in type_associations:
            for synonym in type_associations[column_type]:
                if re.match('^' + synonym + '[a-zA-Z ]*$', p_non_parsed_column_type):
                    return column_type

    @staticmethod
    def parse_table_schema(p_table_schema: dict):
        columns_list = ['Name', 'Type', 'Length', 'Format', 'Constraints']
        df = pd.DataFrame(columns = columns_list)

        for col in p_table_schema:
            row = {
                'Name': col
                , 'Type': SchemaParser.parse_column_type(p_table_schema.get(col).get('Type'))
                , 'Length': p_table_schema.get(col).get('Length')
                , 'Format': p_table_schema.get(col).get('Format')
                , 'Constraints': p_table_schema.get(col).get('Constraints')
            }
            df = df.append(row, ignore_index = True)

        return df
