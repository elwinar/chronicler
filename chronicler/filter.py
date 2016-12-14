import re


class Filter(object):
    def __init__(self, raw):
            self.path, self.operator, self.value = re.findall(r"(.*)([=<>])(.*)", raw)[0]

    def match(self, game):
        if not self.path == 'date':
            return self.value.lower() == game[self.path].lower()
        else:
            value = game['date']
            if self.operator == '=':
                return value == self.value
            elif self.operator == '<':
                return value < self.value
            elif self.operator == '>':
                return value > self.value
            else:
                raise ValueError('unhandled operator '+self.operator)
