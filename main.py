"""Usage: chronicler [-c CHRONICLE]

The Chronicler remembers…

Options:
    -c, --chronicle CHRONICLE   chronicle file to use [default: chronicle.txt]

"""
import docopt
import hjson

if __name__ == '__main__':
    options = docopt.docopt(__doc__)

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
    print(chronicle)
