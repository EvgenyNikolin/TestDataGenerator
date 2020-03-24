from data_generator.data_generator import DataGenerator
from data_generator.schema_parser import SchemaParser

# supported constraints:
# for all data types:
# NOT NULL
# for strings:
# NO LOWER
# NO UPPER
# NO CHARS
# NO DIGITS
# NO SPEC SYMBOLS
# DISABLE SPEC SYMBOLS FROM LIST
# ALLOW SPEC SYMBOLS FROM LIST
# REMOVE LENGTH LIMIT

# bit values generation formats:
# numeric
# string
tbl_schema = {
    'Id': {'Type': 'INT', 'Length': [10], 'Constraints': 'NOT NULL, UNIQUE'}
    , 'Name': {'Type': 'VARCHAR', 'Length': [50], 'Format': '+,-./:;<=>?@', 'Constraints': 'DISABLE SPEC SYMBOLS FROM LIST'}
    , 'Salary': {'Type': 'NUMBER', 'Length': [15, 4]}
    , 'Hire_date': {'Type': 'DATETIME', 'Format': '%Y-%m-%d'}
    , 'Is_active': {'Type': 'BIT', 'Format': 'numeric', 'Constraints': 'NOT NULL'}
}

# print('\n')
# data_obj.generate_test_data()
# data_obj.print_dataframe()
# data_obj.export_df_to_csv('C:\\Users\\Yevhen_Nikolin\\Desktop\\test.csv')

schema_obj = SchemaParser(tbl_schema)
schema_obj.print_table_schema()
print('\n')
print(schema_obj.get_list_of_columns())
data_obj = DataGenerator(schema_obj)
data_obj.generate_test_data()
data_obj.print_dataframe()