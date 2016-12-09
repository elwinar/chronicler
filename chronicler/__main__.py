"""Usage: 
    ssc [-c CHRONICLE]
    ssc [-c CHRONICLE] -q QUESTION

The Chronicler remembers…

Options:
    -c --chronicle CHRONICLE     chronicle file to use [default: chronicle.hjson]
    -q --question QUESTION       question to answer [default: player.caster]

"""
import docopt
import hjson
import jsonschema
import tabulate


def main():
    try:
        options = docopt.docopt(__doc__)
    except docopt.DocoptLanguageError:
        print("Dumb chronicler. Contact Doomy.")
        exit(1)

    try:
        chronicle = open(options['--chronicle'])
    except FileNotFoundError:
        print("No chronicle to read.")
        exit(1)

    try:
        chronicle = hjson.load(chronicle)
    except hjson.HjsonDecodeError as e:
        print("This chronicle can't be deciphered.")
        print("L%d, C%d: %s" % (e.lineno, e.colno, e.msg))
        exit(1)

    try:
        jsonschema.validate(chronicle, schema)
    except jsonschema.ValidationError as e: 
        print("This chronicle isn't correctly engraved.")
        print("%s: %s" % (list(e.path), e.message))
        exit(1)

    question = options['--question'].split('.')
    answers = {}
    for game in chronicle:
        key = game
        for part in question:
            key = key[part]

        if not key in answers:
            answers[key] = {
                    'played': 0,
                    'won': 0
                }

        answers[key]['played'] += 1
        if game['result']['victory']:
            answers[key]['won'] += 1

    response = []
    headers = [options['--question'], 'played', 'won']
    for key in sorted(answers.keys()):
        response.append([key, answers[key]['played'], answers[key]['won']])

    print(tabulate.tabulate(response, headers, tablefmt='psql'))


schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "player": {
        "type": "object",
        "properties": {
          "faction": {
            "type": "string"
          },
          "caster": {
            "type": "string"
          }
        },
        "required": [
          "faction",
          "caster"
        ]
      },
      "opponent": {
        "type": "object",
        "properties": {
          "player": {
            "type": "string"
          },
          "faction": {
            "type": "string"
          },
          "caster": {
            "type": "string"
          }
        },
        "required": [
          "player",
          "faction",
          "caster"
        ]
      },
      "result": {
        "type": "object",
        "properties": {
          "victory": {
            "type": "boolean"
          },
          "type": {
            "type": "string"
          }
        },
        "required": [
          "victory",
          "type"
        ]
      }
    },
    "required": [
      "player",
      "opponent",
      "result"
    ]
  }
}

if __name__ == '__main__':
    main()
