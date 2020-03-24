from data_generator.random_units import RandomUnits as units
from data_generator.data_generator import DataGenerator
from data_generator.schema_parser import SchemaParser as parser

# supported constraints:
# NOT NULL
# NO LOWER
# NO UPPER
# NO CHARS
# NO DIGITS
# NO SPEC SYMBOLS
# DISABLE SPEC SYMBOLS [] --> TBD
# ALLOW SPEC SYMBOLS [] --> TBD

# bit values generation formats:
# numeric
# string
tbl_schema = {
    'Id': {'Type': 'INT', 'Length': [10], 'Constraints': 'NOT NULL, UNIQUE'}
    , 'Name': {'Type': 'VARCHAR', 'Length': [50], 'Constraints': 'NO UPPER, NO SPEC SYMBOLS'}
    , 'Salary': {'Type': 'NUMBER', 'Length': [15, 4]}
    , 'Hire_date': {'Type': 'DATETIME', 'Format': '%Y-%m-%d'}
    , 'Is_active': {'Type': 'BIT', 'Format': 'numeric', 'Constraints': 'NOT NULL'}
}

# print(units.get_random_date('%Y-%m-%d %H:%M:%S', '2018-01-01 23:00:01', '2019-05-01 15:00:59'))
data_obj = DataGenerator(tbl_schema)

print(data_obj.table_schema)
print('\n')
data_obj.generate_test_data()
data_obj.print_dataframe()