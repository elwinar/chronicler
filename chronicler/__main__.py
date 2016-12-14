'''Usage: ssc FILE [-g GROUP] [-f FILTERS]


Options:
    -g --groups GROUPS     comma-separated groups to display [default: player.caster]
    -f --filters FILTERS   comma-separated filters to apply


Description:

ssc is a game tracker for Warmachine/Horde. It displays statistics about a set of games, eventually filtering them using the filter syntax.

Games are grouped using a comma-separated list of item, each item bescribed as `<path>`. The statistics of each group will be computed and displayed as result.

Filters are a comma-separated list of items, each item described as `<path>=<value>`. Games included in the result set must match all filters.

Special cases are handled for dates:
    - Dates are added virtual attributes corresponding to the format to represent the date with, following the python strftime format (see http://strftime.org),
    - Date filters can be compared using '<' and '>' operators in addition of '=';


File format:

    [
        {
            player: {
                faction: FACTION
                caster: CASTER
            }
            opponent: {
                player: PLAYER
                faction: FACTION
                caster: CASTER
            }
            date: %Y-%m-%d
            result: {
                victory: true|false
                type: TYPE
            }
        }
    ]


Examples:

`ssc chronicle.hjson -g "player.caster"` will display the statistics for each caster played (its the default command).

`ssc chronicle.hjson -g "player.caster" -f player.faction=Trollbloods"` will display the statistics for each caster for games where the player played a Trollbloods list.

`ssc chronicle.hjson -g "opponent.faction"` will display the statistics for each faction played against.

`ssc chronicle.hjson -g "result.type"` will display the statistics for each victory condition.

`ssc chronicle.hjson -g "date.%Y-%m"` will display the statistics for each month.

`ssc chronicle.hjson -f "date>2016-10-15,date<2016-11-15"` will display the statistics for games that occured between 2016-10-15 and 2016-11-15.

`ssc chronicle.hjson -f "date.%Y-%m=2016-11"` will display games played in 2016-11.


'''
import docopt
import hjson
import jsonschema
import math
import tabulate
import unicodedata
import itertools
import operator

from chronicler.chronicle import Chronicle, Game
from chronicler.filter import Filter
from chronicler.schema import schema

def main():

    # Parse the command-line options.
    try:
        options = docopt.docopt(__doc__)
    except docopt.DocoptLanguageError:
        print('Dumb chronicler. Contact Doomy.')
        exit(1)

    # Load the chronicle file.
    try:
        raw = hjson.load(open(options['FILE']))
        jsonschema.validate(raw, schema)
        chronicle = Chronicle(raw)
    except FileNotFoundError:
        print('No chronicle to read.')
        exit(1)
    except hjson.HjsonDecodeError as e:
        print('This chronicle can\'t be deciphered.')
        print('L%d, C%d: %s' % (e.lineno, e.colno, e.msg))
        exit(1)
    except jsonschema.ValidationError as e: 
        print('This chronicle isn\'t correctly engraved.')
        print('%s: %s' % (list(e.path), e.message))
        exit(1)

    # Get the filters to apply.
    filters = []
    if options['--filters'] != None:
        for raw in options['--filters'].split(','):
            filters.append(Filter(raw))

    # Get the games matching the filters.
    games = chronicle.filter(filters)

    # Early exit if there is no game.
    if len(games) == 0:
        print('There is no battle like this.')
        exit(0)

    # Aggregate the games in groups.
    groups = options['--groups'].split(',')
    grouper = operator.itemgetter(groups)
    results = []
    totalPlayed = 0
    totalWon = 0
    for key, games in itertools.groupby(sorted(games, key=grouper), grouper):
        played = 0
        won = 0
        for game in games:
            played += 1
            totalPlayed += 1
            won += int(game['result.victory'])
            totalWon += int(game['result.victory'])
        results.append(key + [played, won, math.trunc(won/played*100)])
    results.append(['TOTAL'] + ['' for i in groups[1:]] + [totalPlayed, totalWon, math.trunc(totalWon/totalPlayed*100)])

    # Print the results.
    headers = groups + ['played', 'won', '%']
    print(tabulate.tabulate(results, headers, tablefmt='psql'))


def normalize(str):
    return unicodedata.normalize('NFKD', str).encode('ASCII', 'ignore')


if __name__ == '__main__':
    main()
