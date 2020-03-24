import random
import string
import datetime
from dateutil.parser import parse


class RandomUnits(object):

    @staticmethod
    def get_random_str(p_len: int
                       , p_allow_spec_symbols: bool = True
                       , p_allow_lowercase: bool = True
                       , p_allow_uppercase: bool = True
                       , p_allow_chars: bool = True
                       , p_allow_digits: bool = True
                       , p_allowed_spec_symbols: str = ''
                       , p_disabled_spec_symbols: str = ''
                       , p_is_min: bool = None
                       , p_is_max: bool = None):
        symbols = ''

        if p_allow_spec_symbols:
            # do not generate strings with double-quote due to possible quotation issues
            symbols = symbols + string.punctuation.replace('"', '')

            if len(p_allowed_spec_symbols) > 0:
                symbols = p_allowed_spec_symbols
            elif len(p_disabled_spec_symbols) > 0:
                for curr in p_disabled_spec_symbols:
                    symbols = symbols.replace(curr, '')
        if p_allow_digits:
            symbols = symbols + string.digits
        if p_allow_chars:
            if p_allow_lowercase:
                symbols = symbols + string.ascii_lowercase
            if p_allow_uppercase:
                symbols = symbols + string.ascii_uppercase

        if p_is_min and p_is_max:
            return random.choice(symbols)
        elif p_is_min:
            return random.choice(symbols)
        elif p_is_max:
            return ''.join(random.choice(symbols) for i in range(p_len))
        else:
            rand_len = random.randrange(p_len + 1) # +1 because randrange function does not consider the last item
            return ''.join(random.choice(symbols) for i in range(rand_len))

    @staticmethod
    def get_random_int(p_len: int, p_is_min: bool = None, p_is_max: bool = None):
        digits = string.digits

        if p_is_min and p_is_max:
            return random.choice(digits[1:10])
        elif p_is_min:
            return random.choice(digits[1:10])
        elif p_is_max:
            return random.choice(digits[1:10]) + ''.join(random.choice(digits) for i in range(p_len - 1))
        else:
            rand_len = random.randrange(p_len + 1) # +1 because randrange function does not consider the last item
            return random.choice(digits[1:10]) + ''.join(random.choice(digits) for i in range(rand_len - 1))

    @staticmethod
    def get_random_decimal(p_whole_len: int, p_decimal_len: int, p_is_min: bool = None, p_is_max: bool = None):
        digits = string.digits

        if p_is_min and p_is_max:
            return random.choice(digits) + '.' + random.choice(digits)
        elif p_is_min:
            return random.choice(digits) + '.' + random.choice(digits)
        elif p_is_max:
            return random.choice(digits[1:10]) + ''.join(random.choice(digits) for i in range(p_whole_len - 1)) \
                   + '.' + ''.join(random.choice(digits) for i in range(p_decimal_len))
        else:
            rand_whole_len = random.randrange(p_whole_len + 1)
            rand_decimal_len = random.randrange(p_decimal_len + 1)
            return random.choice(digits[1:10]) + ''.join(random.choice(digits) for i in range(rand_whole_len - 1)) \
                   + '.' + random.choice(digits) + ''.join(random.choice(digits) for i in range(rand_decimal_len - 1))

    @staticmethod
    def get_random_date(p_date_mask: str, p_date_from: str = '2000-01-01', p_date_to: str = '2020-01-01'):
        date_from = parse(p_date_from)
        date_to = parse(p_date_to)
        res = datetime.datetime.now()

        if date_from > date_to:
            return datetime.datetime.strftime(res, p_date_mask)

        date_diff_days = (date_to - date_from).days
        rand_day_int = random.randrange(date_diff_days + 1)
        rand_day_dt = date_from \
                      + datetime.timedelta(days=rand_day_int) \
                      + datetime.timedelta(hours=random.randrange(24)) \
                      + datetime.timedelta(minutes=random.randrange(60)) \
                      + datetime.timedelta(seconds=random.randrange(60)) \
                      + datetime.timedelta(milliseconds=random.randrange(997))

        return datetime.datetime.strftime(rand_day_dt, p_date_mask)

    # generates bits in string format by default (True/False)
    # if p_num_format = True then generates bits in numeric format (0/1)
    @staticmethod
    def get_random_bit(p_num_format: bool, p_is_min: bool = None, p_is_max: bool = None):
        if p_num_format:
            return random.randrange(2)
        else:
            return bool(random.randrange(2))