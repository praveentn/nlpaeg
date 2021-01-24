# generator.py

# load libraries
import numpy as np
import pandas as pd
import helper_functions as hf
from tqdm import tqdm
from numpy.random import choice

'''
var= np.round(np.random.normal(distribution mean, 
standard deviation, number of samples), 
number of digits after the decimal point)


# .5 is prob dist of 0 and 1
label = np.random.choice([0, 1], size=7000, p=[.5, .5]) 


'''

class ErrorGenerator():

    def __init__(self):
        self.name = "nlpaeg"
        self.ngrams = 3
        self.ngram_weights = dict()
        self.n_ngrams = None
        self.ngram_order = None
        self.ngram_cols = None
        self.sentence_column = None
        self.source_data = pd.DataFrame()
        self.error_distribution = None
        self.error_distribution_unigram = None

    def get_aeg_data(self):
        '''
        input: dataframe with correct sentences
                - predefined parameters
                - name of sentence column
                - order of n-grams (upto 5)
                - 
        output: dataframe with 
                - actual sentences 
                - sentences with errors
                - type of errors
                - word/phrase for replacement
                - replacement word/phrase

        '''        

        # ngram order <= 5; >=1
        if not (self.ngram_order > 0 and self.ngram_order < 6):
            print("n-gram order should be between 0 and 6")
            raise

        # creates all n-grams for each sentence
        # [[3, "this is sent", ["this", "is", "sent"], ["this is", "is sent"], ["this is sent"]]]
        # memory intensive!!

        start = 0
        batchsize = 10000

        sampled_replacements = pd.DataFrame()

        # process in batches
        for i in tqdm(range(start, len(self.source_data), batchsize)):

            print("start: ", start, " | batchsize: ", batchsize)

            ngrams, sent_ngrams = hf.create_sent_ngrams(self.ngram_order, self.ngram_cols,
                                                self.sentence_column, self.source_data[start:start+batchsize],
                                                self.n_ngrams,
                                                )

            print("sent_ngrams: ", len(sent_ngrams))

            replacements = hf.random_most_common_ngram(sent_ngrams, self.ngram_cols, 
                                                        self.ngram_order, ngrams)

            print("replacements: ", len(replacements))

            tmp_df = pd.DataFrame(replacements, columns=["index", "ngram", "sentence", "replace"])

            tmp = dict()

            for i in range(0, self.ngram_order+1):
                tmp[i] = tmp_df.loc[tmp_df.ngram == i].sample(frac=self.ngram_weights[i])
                sampled_replacements = pd.concat([sampled_replacements, tmp[i]], ignore_index=True)

            print("sampled_replacements: ", len(sampled_replacements))

            start += batchsize

        #self.aeg_data = self.source_data.sample()

        error_mappings = choice(list(self.error_distribution.keys()), 
                                        len(sampled_replacements.loc[~(sampled_replacements.ngram == 1)]), 
                                        p=list(self.error_distribution.values()))

        sampled_replacements.loc[~(sampled_replacements.ngram == 1), 'error'] = error_mappings

        error_mappings_unigrams = choice(list(self.error_distribution_unigram.keys()), 
                                        len(sampled_replacements.loc[sampled_replacements.ngram == 1]), 
                                        p=list(self.error_distribution_unigram.values()))

        sampled_replacements.loc[sampled_replacements.ngram == 1, 'error'] = error_mappings_unigrams

        # sampled_replacements 
        # index, ngram, sentence, replace, error, replacement
        sampled_replacements['replacement'] = sampled_replacements.apply(lambda x: hf.create_error(x), axis=1)

        return sampled_replacements
