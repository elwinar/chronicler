"""Usage: chronicler [-c CHRONICLE]

The Chronicler remembers…

Options:
    -c, --chronicle CHRONICLE   chronicle file to use [default: chronicle.txt]

"""
from docopt import docopt
import hjson

if __name__ == '__main__':
    options = docopt(__doc__)

    try:
        chronicle = open(options['--chronicle'])
    except FileNotFoundError:
        print("No chronicle to read.")
        exit(1)

    try:
        chronicle = hjson.load(chronicle)
    except HjsonDecodeError:
        print("This chronicle can't be deciphered.")
    print(chronicle)
