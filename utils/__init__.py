from datetime import date, datetime
import dataclasses
import json
import logging

# Look at all of these beautiful docstrings! Guess who didn't eat their TDD Wheaties!


logger = logging.getLogger('discord')


@dataclasses.dataclass
class Birthday:
    birthday: date
    member_id: int

class BirthdayJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        json_dict = super().decode(s)
        output_dict = {}
        for month_day, birthdays_list in json_dict.items():
            output_dict[month_day] = [
                Birthday(datetime.strptime(birthday_dict['birthday'], '%Y-%m-%d').date(),
                                           birthday_dict['member_id'])
                for birthday_dict in json_dict[month_day]
            ]
        return output_dict

class birthdayJSONEncoder(json.JSONEncoder):
    """https://stackoverflow.com/a/51286749/1779707
    """

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        return super().default(o)


def num_to_ith(num):
    """1 becomes 1st, 2 becomes 2nd, etc.
    https://stackoverflow.com/a/37343184/1779707
    """
    value             = str(num)
    before_last_digit = value[-2]
    last_digit        = value[-1]
    if len(value) > 1 and before_last_digit == '1': return value +'th'
    if last_digit == '1': return value + 'st'
    if last_digit == '2': return value + 'nd'
    if last_digit == '3': return value + 'rd'
    return value + 'th'

def init_logger():
    logger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='a')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)