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
    
    # sent_ngrams = [sentence, [1-gm], [2-gms], [3-gms], [4-gms], [5-gms]]
    # ngram_cols = {1: "unigrams", 2: "bigrams", 3: "trigrams", }
    # self.ngram_order = 3 -> trigrams; 2-> bigrams
    # ngrams -> top most common ngrams dictionary
    # return replacements = [ngram matched, sentence, replacement words]

    # required output
    # [ngram matched, sentence, replacement words]
    # found replacements
    replacements = []
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

    # replaced indices
    replaced_indices = list(set([x[0] for x in replacements]))

    # not found replacements
    unreplaced_indices = [x for x in range(len(sent_ngrams)) if x not in replaced_indices]

    for unreplaced_index in unreplaced_indices:
        replacements.append([unreplaced_index, 0, sent_ngrams[unreplaced_index], ''])

    return replacements


def remove_verbs(l):

    choice = random.choice(l)
    r = [x for x in l if x != choice]    
    return r


common_error_function_map = {
    "remove_verbs": remove_verbs
}



def create_error(x):

    # x -> # index, ngram, sentence, replace, error

    #print(common_error_function_map["remove_verbs"](['1', '2']))

    ng = x[1]
    sentence = x[2]
    ngs = list(x[3])
    error = x[4]

    if ng == 1:
        pass
    else:
        if not ngs:
            print(ng, ngs)
        else:
            rephrased = common_error_function_map["remove_verbs"](ngs)
            return rephrased


    return "foo"