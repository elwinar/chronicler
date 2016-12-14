from datetime import datetime
import math
import re


DateFormat = '%Y-%m-%d'


class Chronicle(object):
    def __init__(self, games):
        self.games = []
        for raw in games:
            self.games.append(Game(raw))

    def filter(self, filters):
        return list(filter(lambda g: all(f.match(g) for f in filters), self.games))


class Game(object):
    def __init__(self, raw):
        self.raw = raw
        self.date = datetime.strptime(raw['date'], DateFormat).date()

    def get(self, path):
        if path == 'date':
            return self.date.__str__()

        keys = path.split('.')
        if keys[0] == 'date':
            return self.date.strftime(keys[1])

        obj = self.raw
        for key in path.split('.'):
            obj = obj[key]
        return obj


class Filter(object):
    def __init__(self, raw):
            self.path, self.operator, self.value = re.findall(r"(.*)([=<>])(.*)", raw)[0]

    def match(self, game):
        if not self.path == 'date':
            return self.value.lower() == game.get(self.path).lower()
        else:
            value = game.get('date')
            if self.operator == '=':
                return value == self.value
            elif self.operator == '<':
                return value < self.value
            elif self.operator == '>':
                return value > self.value
            else:
                raise ValueError('unhandled operator '+self.operator)


class Groups(dict):
    def __init__(self, groups, games):
        self.group = groups.pop(0)

        for game in games:
            key = game.get(self.group)
            if not key in self:
                self[key] = []
            self[key].append(game)

    def compute(self, key):
        return len(self[key]), sum(1 for game in self[key] if game.get('result.victory'))
