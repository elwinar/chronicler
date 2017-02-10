import re


class Filter(object):
    def __init__(self, raw):
            self.path, self.operator, self.value = re.findall(r"(.*)([=<>])(.*)", raw)[0]

    def match(self, game):
        value = game[self.path]
        if self.path == 'date':
            if self.operator == '=':
                return value == self.value
            elif self.operator == '<':
                return value < self.value
            elif self.operator == '>':
                return value > self.value
            else:
                raise ValueError('unhandled operator '+self.operator)
        else:
            if isinstance(value, bool):
                return toBool(self.value) == value
            else:
                return self.value.lower() == game[self.path].lower()

def toBool(value):
    return value in ['true', 'True', '1', 't', 'T', 'y', 'Y']
