# generator.py

# load libraries
import numpy as np
import pandas as pd
import helper_functions as hf


'''
var= np.round(np.random.normal(distribution mean, 
standard deviation, number of samples), 
number of digits after the decimal point)


# .5 is prob dist of 0 and 1
label = np.random.choice([0, 1], size=7000, p=[.5, .5]) 


'''

class Generator():
    def __init__(self):
        self.name = "nlpaeg"
        self.source_data = pd.DataFrame()
        self.aeg_data = pd.DataFrame()

        self.total_samples = len(self.source_data)

        # how many ngrams to consider
        # using most frequent ones
        # total unigrams -> 1000; take top 300
        self.n_ngrams = {
            1: int(self.total_samples * 0.3),
            2: int(self.total_samples * 0.2),
            3: int(self.total_samples * 0.15),
            4: int(self.total_samples * 0.1),
            5: int(self.total_samples * 0.05),
        }

        # for sampling ngram changes
        self.ngram_weights = {
            1: 0.4, # 40% of unigram changes
            2: 0.6, # 60% of bigram changes
            3: 0.8, # 80% of trigram changes
            4: 0.95, # 95% of quadgram changes
            5: 1    # 100% of pentgram changes
        }

        self.sentence_column = "sentences"


        # ngram_order: 1 to 5
        self.ngram_order = 3
        self.ngram_cols = {
            1: "unigrams", 2: "bigrams", 3: "trigrams", 
            4: "quadgrams", 5: "pentgrams"
        }

        self.error_distribution = {

        }


    

    def get_aeg_data(self):
        '''

        '''        


        self.total_samples = len(self.source_data)
        self.n_ngrams = {
            1: int(self.total_samples * 0.3),
            2: int(self.total_samples * 0.2),
            3: int(self.total_samples * 0.15),
            4: int(self.total_samples * 0.1),
            5: int(self.total_samples * 0.05),
        }

        # ngram order <= 5; >=1
        if not (self.ngram_order > 0 and self.ngram_order < 6):
            print("n-gram order should be between 0 and 6")
            raise

        
        ngrams, sent_ngrams = hf.create_sent_ngrams(self.ngram_order, self.ngram_cols,
                                            self.sentence_column, self.source_data,
                                            self.n_ngrams,
                                            )
    
        replacements = hf.random_most_common_ngram(sent_ngrams[:100], self.ngram_cols, 
                                                    self.ngram_order, ngrams)

        tmp_df = pd.DataFrame(replacements, columns=["index", "ngram", "sentence", "replace"])

        sampled_replacements = pd.DataFrame()
        tmp = dict()

        for i in range(1, self.ngram_order+1):
            tmp[i] = tmp_df.loc[tmp_df.ngram == i].sample(frac=self.ngram_weights[i])
            sampled_replacements = pd.concat([sampled_replacements, tmp[i]], ignore_index=True)


        #self.aeg_data = self.source_data.sample()

        return sampled_replacements
