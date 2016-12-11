from datetime import datetime

class Chronicle(object):

    def __init__(self, games):
        self.games = []
        for raw in games:
            self.games.append(Game(raw))

    def filter(self, filters):
        return filter(lambda g: all(f.match(g) for f in filters), self.games)


class Game(object):

    def __init__(self, raw):
        self.raw = raw

    def get(self, path):
        obj = self.raw
        for key in path.split('.'):
            obj = obj[key]
        return obj


class Filter(object):
    DateFormat = '%Y-%m-%d'

    def __init__(self, raw):
        if not raw.startswith('date'):
            self.path, self.operator, self.value = raw.partition('=')
        else:
            self.path = 'date'
            self.operator = raw[len('date'):len('date')+1]
            self.value = datetime.strptime(raw[len('date')+1:], self.DateFormat).date()

    def match(self, game):
        if not self.path == 'date':
            return self.value == game.get(self.path)
        else:
            value = datetime.strptime(game.get('date'), self.DateFormat).date()
            if self.operator == '=':
                return value == self.value
            elif self.operator == '<':
                return value < self.value
            elif self.operator == '>':
                return value > self.value
            else:
                raise ValueError('unhandled operator '+self.operator)

