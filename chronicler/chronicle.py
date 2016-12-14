from datetime import datetime


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

    def __getitem__(self, key):
        if not isinstance(key, list):
            return self.get(key)

        return [self.get(k) for k in key]


