# __main__.py

import os
import sys
import pandas as pd
import generator
from importlib import resources  # Python 3.7+

def main():
    """Begin here"""

    # instantiate the class
    g = generator.Generator()

    # data directory
    data_dir = os.path.join(os.getcwd(), "data")
    
    # filename sentences without errors
    train_data = "nlpaeg_pubmed_data_min.csv"
    train_data_file_path = os.path.join(data_dir, train_data)

    # read as dataframe
    #df = pd.read_csv(train_data_file_path, sep="\t", header=None)
    #df.columns = ["source", "valid", "note", "sentence"]

    # set source data
    g.source_data = pd.read_csv(train_data_file_path)
    g.source_data = g.source_data.sample(1000)

    # set sentence column name
    # default: sentences
    g.sentence_column = "sentences"

    # define n-gram order
    # 4 => quadgrams, trigrams, bigrams and unigrams
    # 3 => trigrams, bigrams and unigrams
    # 2 => bigrams and unigrams
    # default is 3; max is 5
    g.ngram_order = 4

    # define proportion of ngram matches to modify
    # for example, if there were 10 sentences in total
    # changes to unigrams -> 10
    # changes to bigrams -> 7
    # changes to trigrams -> 3
    # we'll need to use all three trigrams, most of bigrams
    # and half of unigrams
    g.ngram_weights = {
        1: 0.4, 2: 0.6, 3: 0.8, 4: 0.95, 5: 1
    }


    # call the method to create error data
    aeg_df = g.get_aeg_data()

    print(aeg_df.head(2))

if __name__ == "__main__":
    main()