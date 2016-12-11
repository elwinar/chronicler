'''Usage: 
    ssc [-c CHRONICLE] [-q QUESTION] [-f FILTERS]

The Chronicler remembers…

Options:
    -c --chronicle CHRONICLE     chronicle file to use [default: chronicle.hjson]
    -q --question QUESTION       question to answer [default: player.caster]
    -f --filters FILTERS         comma-separated filters to apply

'''
import docopt
import hjson
import jsonschema
import math
import tabulate
import unicodedata

from chronicle import Chronicle, Game, Filter
from schema import schema

def main():

    # Parse the command-line options.
    try:
        options = docopt.docopt(__doc__)
    except docopt.DocoptLanguageError:
        print('Dumb chronicler. Contact Doomy.')
        exit(1)

    # Load the chronicle file.
    try:
        raw = hjson.load(open(options['--chronicle']))
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

    # Get the question to answer and the filters to apply.
    question = options['--question']

    filters = []
    if options['--filters'] != None:
        for raw in options['--filters'].split(','):
            filters.append(Filter(raw))

    # Get the games matching the filters.
    answers = {}
    for game in chronicle.filter(filters):
        key = game.get(question)
        if not key in answers:
            answers[key] = {
                    'played': 0,
                    'won': 0
                }
        answers[key]['played'] += 1
        if game.get('result.victory'):
            answers[key]['won'] += 1

    # Early exit if there is no game.
    if len(answers) == 0:
        print('There is no battle like this.')
        exit(0)

    # Compute the response.
    response = []
    headers = [options['--question'], 'played', 'won', '%']
    totals = ['TOTAL', 0, 0, 0]
    for key in sorted(answers.keys(), key=normalize):
        answer = answers[key]
        played = answer['played']
        won = answer['won']
        response.append([key, played, won, math.trunc(won / played * 100)])
        totals[1] += played
        totals[2] += won
    totals[3] = math.trunc(totals[2]/totals[1]*100)
    response.append(totals)

    # Print the response.
    print(tabulate.tabulate(response, headers, tablefmt='psql'))


def normalize(str):
    return unicodedata.normalize('NFKD', str).encode('ASCII', 'ignore')


if __name__ == '__main__':
    main()
