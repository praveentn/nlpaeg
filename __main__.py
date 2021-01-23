# __main__.py

import sys
import generator
from importlib import resources  # Python 3.7+

def main():
    """Begin here"""

    # instantiate the class
    g = generator.Generator()

    # data definition
    datag = {
    }

    df = g.get_dataframe(datag)

    print(df)

if __name__ == "__main__":
    main()