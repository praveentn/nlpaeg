import random
import pandas as pd
import helper_variables as hv
from itertools import chain
from collections import Counter

# globals

# split words
splitter_keys = list(hv.splitters.keys())

# replacements
replacement_keys = list(hv.replacements.keys())

# operations
operations = hv.operations





# create n-grams
def create_ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))
    

# return sentences

def create_sent_ngrams(ngram_order, ngram_cols, sentence_column, source_data, n_ngrams):
    # dictionary of most common n n-grams
    ngrams = {}

    df = pd.DataFrame()
    df[sentence_column] = source_data[sentence_column]

    # iterate over ngram order to create df columns
    # with names from the dict ngram_cols
    for n in range(1, ngram_order+1):
        df[ngram_cols[n]] = source_data[sentence_column].map(lambda x: create_ngrams(x.split(" "), n))
        grams = df[ngram_cols[n]].tolist()
        grams = list(chain(*grams))
        grams = [x for x in grams]
        grams_counter = Counter(grams)
        ngrams[ngram_cols[n]] = grams_counter.most_common(n_ngrams[n])
        ngrams[ngram_cols[n]] = [ng for ng, count in ngrams[ngram_cols[n]]]

    # combine sentences with ngrams
    # select random most common ngram for each sentence
    ncols = df.columns
    sent_ngrams = list(df[ncols].values)

    return ngrams, sent_ngrams


# sent list of sentences and its ngrams
# return randomly chosen most common ngram in the sentence

def random_most_common_ngram(sent_ngrams, ngram_cols, ngram_order, ngrams):
    
    # required output
    # [ngram matched, sentence, replacement words]
    replacements = []

    # sent_ngrams = [sentence, [1-gm], [2-gms], [3-gms], [4-gms], [5-gms]]
    # return replacements = [ngram matched, sentence, replacement words]
    # found replacements
    found = []

    for indx, sngs in enumerate(sent_ngrams):

        for i in range(ngram_order, 0, -1):
            ngs = sngs[i]
            ncom = list(set(ngrams[ngram_cols[i]]).intersection(ngs))

            #if indx not in found:
            if ncom:
                req_one_ncom = random.choice(ncom)
                replacements.append([indx, i, sngs[0], req_one_ncom])
                found.append(indx)                    
        #else:
            #    continue


    return replacements

#sent_ngrams = list(df[["sentences", "quadgrams", "trigrams", "bigrams", "unigrams"]].values)
#random_most_common_ngram(sent_ngrams[35:43])




