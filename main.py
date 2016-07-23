"""Usage: chronicler [-c CHRONICLE]

The Chronicler remembers…

Options:
    -c, --chronicle CHRONICLE   chronicle file to use [default: chronicle.hjson]

"""
import docopt
import hjson
import jsonschema
import chronicle


def main():
    options = docopt.docopt(__doc__)

    try:
        c = open(options['--chronicle'])
    except FileNotFoundError:
        print("No chronicle to read.")
        exit(1)

    try:
        c = hjson.load(c)
    except hjson.HjsonDecodeError as e:
        print("This chronicle can't be deciphered.")
        print("L%d, C%d: %s" % (e.lineno, e.colno, e.msg))
        exit(1)

    try:
        jsonschema.validate(c, chronicle.schema)
    except jsonschema.ValidationError as e: 
        print("This chronicle can't be deciphered.")
        print("%s: %s" % (list(e.path), e.message))
        exit(1)

    print("Behold my story:")

    played = 0
    won = 0
    for h in c:
        for a in h['against']:
            played += 1
            if a['result']['victory'] == True:
                won += 1

    print("victories: %d/%d" % (won, played))



if __name__ == '__main__':
    main()
