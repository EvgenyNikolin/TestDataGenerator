import pandas as pd
import re


class SchemaParser(object):
    def __init__(self, p_tbl_schema: dict):
        self.table_schema = self.__parse_table_schema(p_tbl_schema)

    def print_table_schema(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', 200)
        pd.set_option('display.width', 5000)
        print(self.table_schema)

    def get_column_property_by_name(self, p_col_name: str, p_property_name: str):
        value = self.table_schema.query('Name == \'' + p_col_name + '\'')[p_property_name].values[0]
        return '' if value is None else value

    def get_list_of_columns(self):
        return list(self.table_schema['Name'])

    # general method for validating column constraints
    # returns True if given column contains the given constraint, otherwise returns False
    def parse_column_constraints(self, p_column_name: str, p_constraint_name: str):
        column_constraints = self.get_column_property_by_name(p_column_name, 'Constraints').upper()
        pattern = '[a-zA-Z0-9,; \[\]\-.]*' + p_constraint_name + '[a-zA-Z0-9,; \[\]\-.]*'

        return True if re.match(pattern, column_constraints) else False

    # below is the list of methods that identify the properties of some specific data types or applicable to any data type

    # all data types:
    # NOT NULL

    def not_null(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'NOT NULL')

    # string properties:
    # NO LOWER
    # NO UPPER
    # NO CHARS
    # NO DIGITS
    # NO SPEC SYMBOLS
    # DISABLE SPEC SYMBOLS FROM LIST
    # ALLOW SPEC SYMBOLS FROM LIST
    # REMOVE LENGTH LIMIT

    def no_lowercase(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'NO LOWER')

    def no_uppercase(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'NO UPPER')

    def no_characters(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'NO CHARS')

    def no_digits(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'NO DIGITS')

    def no_special_symbols(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'NO SPEC SYMBOLS')

    def allow_spec_symbols_from_list(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'ALLOW SPEC SYMBOLS FROM LIST')

    def disable_spec_symbols_from_list(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'DISABLE SPEC SYMBOLS FROM LIST')

    def remove_length_limit(self, p_column_name: str):
        return self.parse_column_constraints(p_column_name, 'REMOVE LENGTH LIMIT')

    def is_numeric_bit_format(self, p_column_name: str):
        column_format = self.get_column_property_by_name(p_column_name, 'Format').upper()
        pattern = '[a-zA-Z0-9,; \[\]\-.]*NUMERIC[a-zA-Z0-9,; \[\]\-.]*'

        return True if re.match(pattern, column_format) else False

    def __parse_column_type(self, p_non_parsed_column_type: str):
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

    def __parse_table_schema(self, p_table_schema: dict):
        columns_list = ['Name', 'Type', 'Length', 'Format', 'Constraints']
        df = pd.DataFrame(columns = columns_list)

        for col in p_table_schema:
            row = {
                'Name': col
                , 'Type': self.__parse_column_type(p_table_schema.get(col).get('Type'))
                , 'Length': p_table_schema.get(col).get('Length')
                , 'Format': p_table_schema.get(col).get('Format')
                , 'Constraints': p_table_schema.get(col).get('Constraints')
            }
            df = df.append(row, ignore_index = True)

        return df
