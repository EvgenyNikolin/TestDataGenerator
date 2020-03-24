from data_generator.random_units import RandomUnits as rand_units
from data_generator.schema_parser import SchemaParser as parser
import pandas as pd
import re


class DataGenerator (object):
    def __init__(self, p_tbl_schema: dict, p_scenarios: list = ['min', 'max', 'rand', 'null']):
        self.table_schema = parser.parse_table_schema(p_tbl_schema)
        self.df = pd.DataFrame(columns = list(self.table_schema['Name']))
        self.data_generation_positive_scenarios = p_scenarios

    def __get_column_property_by_name(self, p_col_name: str, p_property_name: str):
        return self.table_schema.query('Name == \'' + p_col_name + '\'')[p_property_name].values[0]

    def __insert_row_into_df(self, p_row: dict):
        self.df = self.df.append(p_row, ignore_index = True)

    def print_dataframe(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', 200)
        pd.set_option('display.width', 5000)
        print(self.df)

    def export_df_to_csv(self, p_save_dir: str):
        self.df.to_csv(p_save_dir, index = False, encoding = 'utf-8', doublequote = True)

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
        spec_symbols = self.__get_column_property_by_name(p_column_name, 'Format')
        allowed_spec_symbols = ''
        disabled_spec_symbols = ''
        allow_spec_symbols = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO SPEC SYMBOLS[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_lowercase = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO LOWER[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_uppercase = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO UPPER[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_chars = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO CHARS[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_digits = False if re.match('[a-zA-Z0-9,; \[\]\-.]*NO DIGITS[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else True
        allow_spec_symbols_from_list = True if re.match('[a-zA-Z0-9,; \[\]\-.]*ALLOW SPEC SYMBOLS FROM LIST[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else False
        disable_spec_symbols_from_list = True if re.match('[a-zA-Z0-9,; \[\]\-.]*DISABLE SPEC SYMBOLS FROM LIST[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else False
        remove_length_limit = True if re.match('[a-zA-Z0-9,; \[\]\-.]*REMOVE LENGTH LIMIT[a-zA-Z0-9,; \[\]\-.]*', column_constraints) else False

        column_length = self.__get_column_property_by_name(p_column_name, 'Length')[0]

        if not remove_length_limit:
            column_length = column_length if column_length <= 1000 else 1000
        if allow_spec_symbols_from_list:
            allowed_spec_symbols = spec_symbols
        if disable_spec_symbols_from_list:
            disabled_spec_symbols = spec_symbols

        if p_scenario_name == 'min':
            return rand_units.get_random_str(p_len = column_length
                                             , p_allow_spec_symbols = allow_spec_symbols
                                             , p_allow_lowercase = allow_lowercase
                                             , p_allow_uppercase = allow_uppercase
                                             , p_allow_chars = allow_chars
                                             , p_allow_digits = allow_digits
                                             , p_allowed_spec_symbols = allowed_spec_symbols
                                             , p_disabled_spec_symbols = disabled_spec_symbols
                                             , p_is_min = True
                                             , p_is_max = False)
        elif p_scenario_name == 'max':
            return rand_units.get_random_str(p_len = column_length
                                             , p_allow_spec_symbols = allow_spec_symbols
                                             , p_allow_lowercase = allow_lowercase
                                             , p_allow_uppercase = allow_uppercase
                                             , p_allow_chars = allow_chars
                                             , p_allow_digits = allow_digits
                                             , p_allowed_spec_symbols = allowed_spec_symbols
                                             , p_disabled_spec_symbols = disabled_spec_symbols
                                             , p_is_min = False
                                             , p_is_max = True)
        elif p_scenario_name == 'rand':
            return rand_units.get_random_str(p_len = column_length
                                             , p_allow_spec_symbols = allow_spec_symbols
                                             , p_allow_lowercase = allow_lowercase
                                             , p_allow_uppercase = allow_uppercase
                                             , p_allow_chars = allow_chars
                                             , p_allow_digits = allow_digits
                                             , p_allowed_spec_symbols = allowed_spec_symbols
                                             , p_disabled_spec_symbols = disabled_spec_symbols
                                             , p_is_min = False
                                             , p_is_max = False)

    def __generate_data_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_type = self.__get_column_property_by_name(p_column_name, 'Type')

        if p_scenario_name == 'null':
            return ''
        elif column_type == 'INT':
            return self.__generate_int_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'DECIMAL':
            return self.__generate_decimal_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'DATETIME':
            # currently only 'rand' scenario is supported
            return self.__generate_date_by_scenario(p_column_name, 'rand')
        elif column_type == 'BIT':
            return self.__generate_bit_by_scenario(p_column_name, p_scenario_name)
        elif column_type == 'STRING':
            return self.__generate_str_by_scenario(p_column_name, p_scenario_name)

    def generate_test_data(self):
        for curr_col in self.table_schema['Name']:
            for scenario in self.data_generation_positive_scenarios:
                df_row = dict()
                for col in self.table_schema['Name']:
                    if curr_col == col:
                        df_row[col] = self.__generate_data_by_scenario(col, scenario)
                    else:
                        df_row[col] = self.__generate_data_by_scenario(col, 'rand')

                self.__insert_row_into_df(df_row)
