# generator.py

# load libraries
import numpy as np
import pandas as pd
import helper_functions as hf
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
        self.source_data = None
        self.error_distribution = None
        self.error_distribution_unigram = None

    def get_aeg_data(self):
        '''

        '''        

        # ngram order <= 5; >=1
        if not (self.ngram_order > 0 and self.ngram_order < 6):
            print("n-gram order should be between 0 and 6")
            raise

        
        ngrams, sent_ngrams = hf.create_sent_ngrams(self.ngram_order, self.ngram_cols,
                                            self.sentence_column, self.source_data,
                                            self.n_ngrams,
                                            )
    
        replacements = hf.random_most_common_ngram(sent_ngrams, self.ngram_cols, 
                                                    self.ngram_order, ngrams)

        
        tmp_df = pd.DataFrame(replacements, columns=["index", "ngram", "sentence", "replace"])

        sampled_replacements = pd.DataFrame()
        tmp = dict()

        for i in range(0, self.ngram_order+1):
            tmp[i] = tmp_df.loc[tmp_df.ngram == i].sample(frac=self.ngram_weights[i])
            sampled_replacements = pd.concat([sampled_replacements, tmp[i]], ignore_index=True)


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
