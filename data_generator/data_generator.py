from data_generator.random_units import RandomUnits as rand_units
from data_generator.schema_parser import SchemaParser as parser
import pandas as pd
import re


class DataGenerator (object):
    def __init__(self, p_tbl_schema: dict):
        self.table_schema = parser.parse_table_schema(p_tbl_schema)
        self.df = pd.DataFrame(columns = list(self.table_schema['Name']))

    def __get_column_property_by_name(self, p_col_name: str, p_property_name: str):
        return self.table_schema.query('Name == \'' + p_col_name + '\'')[p_property_name].values[0]

    # supported positive scenarios:
    # 'rand' - random bit
    def __generate_bit_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_constraints = self.__get_column_property_by_name(p_column_name, 'Format').upper()
        is_str_format = False if re.match('[a-zA-Z0-9,; \[\]\-.]*STRING[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        is_num_format = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NUMERIC[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True

        if p_scenario_name == 'rand':
            return rand_units.get_random_bit(is_str_format, is_num_format)

    # supported positive scenarios:
    # 'rand' - random date
    def __generate_date_by_scenario(self, p_column_name: str, p_scenario_name: str):
        date_mask = self.__get_column_property_by_name(p_column_name, 'Format')

        if p_scenario_name == 'rand':
            return rand_units.get_random_date(date_mask)

    # supported positive scenarios:
    # 'min' - minimum-length value (not the minimum number)
    # 'max' - maximum_length value (not the maximum number)
    # 'rand' - random-length value
    def __generate_decimal_by_scenario(self, p_column_name: str, p_scenario_name: str):
        whole_part_length = self.__get_column_property_by_name(p_column_name, 'Length')[0]
        decimal_part_length = self.__get_column_property_by_name(p_column_name, 'Length')[1]

        if decimal_part_length == 0:
            return self.__generate_int_by_scenario(p_column_name, p_scenario_name)
        else:
            if p_scenario_name == 'min':
                return rand_units.get_random_decimal(whole_part_length, decimal_part_length, p_is_min = True, p_is_max = False)
            elif p_scenario_name == 'max':
                return rand_units.get_random_decimal(whole_part_length, decimal_part_length, p_is_min = False, p_is_max = True)
            elif p_scenario_name == 'rand':
                return rand_units.get_random_decimal(whole_part_length, decimal_part_length, p_is_min = False, p_is_max = False)

    # supported positive scenarios:
    # 'min' - minimum-length value (not the minimum number)
    # 'max' - maximum_length value (not the maximum number)
    # 'rand' - random-length value
    def __generate_int_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_length = self.__get_column_property_by_name(p_column_name, 'Length')[0]

        if p_scenario_name == 'min':
            return rand_units.get_random_int(column_length, p_is_min = True, p_is_max = False)
        elif p_scenario_name == 'max':
            return rand_units.get_random_int(column_length, p_is_min = False, p_is_max = True)
        elif p_scenario_name == 'rand':
            return rand_units.get_random_int(column_length, p_is_min = False, p_is_max = False)

    # supported positive scenarios:
    # 'min' - minimum-length value
    # 'max' - maximum_length value
    # 'rand' - random-length value
    def __generate_str_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_constraints = self.__get_column_property_by_name(p_column_name, 'Constraints').upper()
        allow_spec_symbols = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO SPEC SYMBOLS[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_lowercase = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO LOWER[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_uppercase = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO UPPER[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_chars = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO CHARS[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_digits = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO DIGITS[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True

        column_length = self.__get_column_property_by_name(p_column_name, 'Length')[0]

        if p_scenario_name == 'min':
            return rand_units.get_random_str(column_length
                                             , allow_spec_symbols
                                             , allow_lowercase
                                             , allow_uppercase
                                             , allow_chars
                                             , allow_digits
                                             , p_is_min = True
                                             , p_is_max = False)
        elif p_scenario_name == 'max':
            return rand_units.get_random_str(column_length
                                             , allow_spec_symbols
                                             , allow_lowercase
                                             , allow_uppercase
                                             , allow_chars
                                             , allow_digits
                                             , p_is_min = False
                                             , p_is_max = True)
        elif p_scenario_name == 'rand':
            return rand_units.get_random_str(column_length
                                             , allow_spec_symbols
                                             , allow_lowercase
                                             , allow_uppercase
                                             , allow_chars
                                             , allow_digits
                                             , p_is_min = False
                                             , p_is_max = False)

    def __generate_data_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_type = self.__get_column_property_by_name(p_column_name, 'Type')

        if column_type == 'INT':
            return self.__generate_int_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'DECIMAL':
            return self.__generate_decimal_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'DATETIME':
            return self.__generate_date_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'BIT':
            return self.__generate_bit_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'STRING':
            return self.__generate_str_by_scenario(p_column_name, p_scenario_name)

    def generate_test_data(self):
        for curr_col in self.table_schema['Name']:
            print(self.__generate_data_by_scenario(curr_col, 'rand'))
