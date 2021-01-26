# __main__.py

import os
import sys
import pandas as pd
import error_generator as eg
from importlib import resources  # Python 3.7+

def main():
    """Begin here"""

    # instantiate the class
    g = eg.ErrorGenerator()

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

    # comment below to select entire dataset
    #g.source_data = g.source_data.sample(2000)

    # set sentence column name
    # default: sentences
    g.sentence_column = "sentences"

    # define n-gram order
    # 4 => quadgrams, trigrams, bigrams and unigrams
    # 3 => trigrams, bigrams and unigrams
    # 2 => bigrams and unigrams
    # default is 3; max is 5
    g.ngram_order = 4

    # name of columns -> predefined
    # max upto 5 -grams
    g.ngram_cols = {
        1: "unigrams", 2: "bigrams", 3: "trigrams", 
        4: "quadgrams", 5: "pentgrams"
    }

    # total samples
    g.total_samples = len(g.source_data)

    # selecting a proportion of most common n-grams
    # if there are 1000 sentences and 2000 unigrams
    # then we select only 30% of total unigrams
    # how many ngrams to consider
    # using most frequent ones
    # total unigrams -> 2000; take top 600
    g.n_ngrams = {
        1: int(g.total_samples * 0.3),
        2: int(g.total_samples * 0.2),
        3: int(g.total_samples * 0.15),
        4: int(g.total_samples * 0.1),
        5: int(g.total_samples * 0.05),
    }


    # define proportion of ngram matches to modify
    # for example, if there were 10 sentences in total
    # changes to unigrams -> 10
    # changes to bigrams -> 7
    # changes to trigrams -> 3
    # we'll need to use all three trigrams, most of bigrams
    # and half of unigrams
    # for sampling ngram changes
    g.ngram_weights = {
        0: 1,    # 100% of no grams
        1: 0.4, # 40% of unigram changes
        2: 0.6, # 60% of bigram changes
        3: 0.8, # 80% of trigram changes
        4: 0.95, # 95% of quadgram changes
        5: 1    # 100% of pentgram changes
    }



    # probability distribution of artificial errors
    # keys -> type of errors
    # values -> distribution %
    g.error_distribution = {
        "dictionary_replacement_phrase_order_change": 0.1,
        "verb_form_change_insert_determiner": 0.1,
        "verb_form_change_phrase_order_change": 0.1,
        "insert_determiner_verb_form_change": 0.1,
        "phrase_order_change": 0.1,
        "duplication": 0.1,
        "split_words": 0.1,
        "remove_words": 0.1,
        "spelling_errors": 0.1,
        "insert_determiner": 0.05,
        "punctuations": 0.04,
        "punctuation_braces": 0.01,
    }

    # not all errors are applicable to unigrams
    g.error_distribution_unigram = {
        "verb_form_change_insert_determiner": 0.15,
        "insert_determiner_verb_form_change": 0.15,
        "insert_determiner": 0.15,
        "duplication": 0.15,
        "split_words": 0.1,
        "remove_words": 0.1,
        "spelling_errors": 0.1,
        "punctuations": 0.05,
        "punctuation_braces": 0.05,
        
    }

    # call the method to create error data
    aeg_df = g.get_aeg_data()

    aeg_df.to_csv('sampled_replacements_min.csv', index=None)

    print(aeg_df.tail(5))

if __name__ == "__main__":
    main()