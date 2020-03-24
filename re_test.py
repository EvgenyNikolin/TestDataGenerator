import re

pattern = ''
expr = ''

# if re.match(pattern, expr):
#     print('success')
# else:
#     print('fail')

str1 = 'abcdef'
str2 = 'bcde'

for curr in str2:
    str1 = str1.replace(curr, '')

print(str1)