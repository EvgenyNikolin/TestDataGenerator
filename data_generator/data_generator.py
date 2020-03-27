from data_generator.random_units import RandomUnits
from data_generator.schema_parser import SchemaParser
import pandas as pd
import re


class DataGenerator (object):
    def __init__(self, p_schema_obj: SchemaParser, p_scenarios: list = ['min', 'max', 'rand', 'null']):
        self.schema_obj = p_schema_obj
        self.data_generation_positive_scenarios = p_scenarios
        self.df = pd.DataFrame(columns=self.schema_obj.get_list_of_columns())

    def __insert_row_into_df(self, p_row: dict):
        self.df = self.df.append(p_row, ignore_index=True)

    def print_dataframe(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', 200)
        pd.set_option('display.width', 5000)
        print(self.df)

    def export_df_to_csv(self, p_save_dir: str):
        self.df.to_csv(p_save_dir, index=False, encoding='utf-8', doublequote=True)

    # supported positive scenarios:
    # 'rand' - random bit
    def __generate_bit_by_scenario(self, p_column_name: str, p_scenario_name: str):
        is_num_format = self.schema_obj.is_numeric_bit_format(p_column_name)

        if p_scenario_name == 'rand':
            return RandomUnits.get_random_bit(is_num_format)

    # supported positive scenarios:
    # 'rand' - random date
    def __generate_date_by_scenario(self, p_column_name: str, p_scenario_name: str):
        date_mask = self.schema_obj.get_column_property_by_name(p_column_name, 'Format')

        if p_scenario_name == 'rand':
            return RandomUnits.get_random_date(date_mask)

    # supported positive scenarios:
    # 'min' - minimum-length value (not the minimum number)
    # 'max' - maximum_length value (not the maximum number)
    # 'rand' - random-length value
    def __generate_decimal_by_scenario(self, p_column_name: str, p_scenario_name: str):
        whole_part_length = self.schema_obj.get_column_property_by_name(p_column_name, 'Length')[0]
        decimal_part_length = self.schema_obj.get_column_property_by_name(p_column_name, 'Length')[1]

        if decimal_part_length == 0:
            return self.__generate_int_by_scenario(p_column_name, p_scenario_name)
        else:
            if p_scenario_name == 'min':
                return RandomUnits.get_random_decimal(whole_part_length, decimal_part_length, p_is_min=True, p_is_max=False)
            elif p_scenario_name == 'max':
                return RandomUnits.get_random_decimal(whole_part_length, decimal_part_length, p_is_min=False, p_is_max=True)
            elif p_scenario_name == 'rand':
                return RandomUnits.get_random_decimal(whole_part_length, decimal_part_length, p_is_min=False, p_is_max=False)

    # supported positive scenarios:
    # 'min' - minimum-length value (not the minimum number)
    # 'max' - maximum_length value (not the maximum number)
    # 'rand' - random-length value
    def __generate_int_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_length = self.schema_obj.get_column_property_by_name(p_column_name, 'Length')[0]

        if p_scenario_name == 'min':
            return RandomUnits.get_random_int(column_length, p_is_min=True, p_is_max=False)
        elif p_scenario_name == 'max':
            return RandomUnits.get_random_int(column_length, p_is_min=False, p_is_max=True)
        elif p_scenario_name == 'rand':
            return RandomUnits.get_random_int(column_length, p_is_min=False, p_is_max=False)

    # supported positive scenarios:
    # 'min' - minimum-length value
    # 'max' - maximum_length value
    # 'rand' - random-length value
    def __generate_str_by_scenario(self, p_column_name: str, p_scenario_name: str):
        spec_symbols = self.schema_obj.get_column_property_by_name(p_column_name, 'Format')
        allowed_spec_symbols = ''
        disabled_spec_symbols = ''
        no_special_symbols = not self.schema_obj.no_special_symbols(p_column_name)
        no_lowercase = not self.schema_obj.no_lowercase(p_column_name)
        no_uppercase = not self.schema_obj.no_uppercase(p_column_name)
        no_characters = not self.schema_obj.no_characters(p_column_name)
        no_digits = not self.schema_obj.no_digits(p_column_name)
        not_null = not self.schema_obj.not_null(p_column_name)
        allow_spec_symbols_from_list = self.schema_obj.allow_spec_symbols_from_list(p_column_name)
        disable_spec_symbols_from_list = self.schema_obj.disable_spec_symbols_from_list(p_column_name)
        remove_length_limit = self.schema_obj.remove_length_limit(p_column_name)

        column_length = self.schema_obj.get_column_property_by_name(p_column_name, 'Length')[0]

        if not remove_length_limit:
            column_length = column_length if column_length <= 1000 else 1000
        if allow_spec_symbols_from_list:
            allowed_spec_symbols = spec_symbols
        if disable_spec_symbols_from_list:
            disabled_spec_symbols = spec_symbols

        if p_scenario_name == 'min':
            return RandomUnits.get_random_str(p_len=column_length
                                             , p_allow_spec_symbols=no_special_symbols
                                             , p_allow_lowercase=no_lowercase
                                             , p_allow_uppercase=no_uppercase
                                             , p_allow_chars=no_characters
                                             , p_allow_digits=no_digits
                                             , p_allow_nulls=not_null
                                             , p_allowed_spec_symbols=allowed_spec_symbols
                                             , p_disabled_spec_symbols=disabled_spec_symbols
                                             , p_is_min=True
                                             , p_is_max=False)
        elif p_scenario_name == 'max':
            return RandomUnits.get_random_str(p_len=column_length
                                             , p_allow_spec_symbols=no_special_symbols
                                             , p_allow_lowercase=no_lowercase
                                             , p_allow_uppercase=no_uppercase
                                             , p_allow_chars=no_characters
                                             , p_allow_digits=no_digits
                                             , p_allow_nulls=not_null
                                             , p_allowed_spec_symbols=allowed_spec_symbols
                                             , p_disabled_spec_symbols=disabled_spec_symbols
                                             , p_is_min=False
                                             , p_is_max=True)
        elif p_scenario_name == 'rand':
            return RandomUnits.get_random_str(p_len=column_length
                                             , p_allow_spec_symbols=no_special_symbols
                                             , p_allow_lowercase=no_lowercase
                                             , p_allow_uppercase=no_uppercase
                                             , p_allow_chars=no_characters
                                             , p_allow_digits=no_digits
                                             , p_allow_nulls=not_null
                                             , p_allowed_spec_symbols=allowed_spec_symbols
                                             , p_disabled_spec_symbols=disabled_spec_symbols
                                             , p_is_min=False
                                             , p_is_max=False)

    def __generate_data_by_scenario(self, p_column_name: str, p_scenario_name: str):
        column_type = self.schema_obj.get_column_property_by_name(p_column_name, 'Type')

        if p_scenario_name == 'null' and not self.schema_obj.not_null(p_column_name):
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
        for curr_col in self.schema_obj.get_list_of_columns():
            for scenario in self.data_generation_positive_scenarios:
                df_row = dict()
                for col in self.schema_obj.get_list_of_columns():
                    if curr_col == col:
                        df_row[col] = self.__generate_data_by_scenario(col, scenario)
                    else:
                        df_row[col] = self.__generate_data_by_scenario(col, 'rand')

                self.__insert_row_into_df(df_row)
