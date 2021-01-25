# generator.py

# load libraries
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import chain
from numpy.random import choice
from collections import Counter
from lemminflect import isTagBaseForm
from lemminflect import getLemma, getAllLemmas, getInflection
from lemminflect import getAllInflections, getAllInflectionsOOV

'''
var= np.round(np.random.normal(distribution mean, 
standard deviation, number of samples), 
number of digits after the decimal point)


# .5 is prob dist of 0 and 1
label = np.random.choice([0, 1], size=7000, p=[.5, .5]) 


'''

class Variables():

    def __init__(self):

        # globals
        # variables
        self.adj_tags = ['JJ', 'JJR', 'JJS']
        self.noun_tags = ['NN', 'NNP', 'NNS', 'NNPS']
        self.verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.adverb_tags = ['RB', 'RBR', 'RBS']

        # operations
        self.operations = ["dict_replacement", "duplication",
                    "punctuations", "punctuation_braces",  
                    "random_removal", "split_words",
                    "insert_determiner", "change_order",

                    ]

        # determiners/propositions
        self.determiners = ['a', 'is', 'are', 'an', 'to', 'of', 'on', 'in', 'it',
                    'if', 'or', 'was', 'were', 'from', 
                    ]

        # split words
        self.splitters = {
            "healthcare": "health care",
            "trademark": "trade mark",
            "decision-making": "decision making",
            "health-related": "health related",
            "highlight": "high light",
            "endpoint": "end point",
            "biomarker": "bio marker",
            "without": "with out",
            "meta-analysis": "meta analysis",
            "non-alcoholic": "non alcoholic",
            "understand": "under stand",
            "understood": "under stood",
            "relationship": "relation ship",
            "hypersensitivity": "hyper sensitivity",
            "outcome": "out come",
            "inflammatory": "in flammatory",
            "questionable": "question able",
            "independent": "in dependent",
            "stakeholders": "stake holders",
            "injectable": "inject able",
            "outcomes": "out comes",
            "moderate": "mode rate",
        }

        # were -> where
        # there -> they are
        self.replacements = {
            "have": ["has"],
            "has": ["have"],
            "were": ["we are", "we're", "where",],
            "we're": ["were",],
            "where": ["were", "we're", "we are", ],
            "there": ["their", "they're", "they are"],
            "their": ["there", "they're", "they are"],
            "A": ["An", ],
            "An": ["A", ],
            "a": ["an", "as", "are", ],
            "an": ["a", "are", ],
            "its": ["it's", "it is"],
            "it's": ["its"],
            "to": ["too", "on",],
            "too": ["to",],
            "of": ["off",],
            "off": ["of",],
            "once": ["ones", "one's", ],
            "ones": ["once", ],
            "on": ["own", "one"],
            "own": ["on",],
            "effect": ["affect",],
            "affect": ["effect",],
            "effects": ["affects",],
            "affects": ["effects",],
            "by": ["buy", "bye"],
            "buy": ["by", "bye"],
            "here": ["hear", ],
            "hear": ["here", ],
            "this": ["these", ],
            "these": ["this", ],
            "This": ["These", ],
            "These": ["This", ],
            "There": ["Their", ],
            "week": ["weak", ],
            "weak": ["week", ],
            "adopt": ["adept", ],
            "adept": ["adopt", ],
            "except": ["accept", ],

        }

        self.rep_punctuations = [",", ":", ";", "\'", "-", " ,", " .",
                            " , ", " . ", ", ", ". ", ",.", "..",
                            "...", ".,", "?", " ?"
                    ]

        self.rep_punctuations_braces = [')', '(', ' )', ' (', '( ', ') ',
                            ' ( ', ' ) ', ']', '[', ' ]', ' [', '[ ', 
                            '] ', ' [ ', ' ] ', '}', '{', ' }', ' {', 
                            '{ ', '} ', ' { ', ' } ',
                            ]

        # split words
        self.splitter_keys = list(self.splitters.keys())

        # replacements
        self.replacement_keys = list(self.replacements.keys())

        self.noreplace = "No replacement found"

        self.common_error_function_map = {
                "punctuations": punctuations,
                "punctuation_braces": punctuation_braces,
                "duplication": duplication,
                "insert_determiner": insert_determiner,
                "dictionary_replacement": dictionary_replacement,
                "phrase_order_change": phrase_order_change,
                "remove_words": remove_words,
                "split_words": split_words,
                "verb_form_change": verb_form_change,
                "dictionary_replacement_verb_form_change": dictionary_replacement_verb_form_change,
                "dictionary_replacement_phrase_order_change": dictionary_replacement_phrase_order_change,
                "verb_form_change_insert_determiner": verb_form_change_insert_determiner,
                "verb_form_change_phrase_order_change": verb_form_change_phrase_order_change,
                "insert_determiner_verb_form_change": insert_determiner_verb_form_change,
                "spelling_errors": spelling_errors,
            }



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

## change the form of verbs
## uses lemminflect
def verb_form_change(v, l, n):
    
    variations = []
    for word in l:

        ifs = ''
        word_lemma = ''
        root_word = ''
                
        word_lemma = getAllLemmas(word, upos='VERB')
        
        if 'VERB' in word_lemma:
            root_word = word_lemma['VERB'][0]

        # only verb upos='VERB'
        ifs = getAllInflections(root_word, upos='VERB')        
        
        for k,v in ifs.items():
            for item in v:
                if (item not in variations) and (item != word):
                    variations.append(item)
    
        if variations:
            v = random.choice(variations)
            return [v if x == word else x for x in l]
            
    else:
        return l

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

                # convert tuple to list
                if i == 1:
                    req_one_ncom = [''.join(x for x in req_one_ncom)]
                else:
                    req_one_ncom = list(req_one_ncom)

                # [indx, ngram, sentence, replace/phrase]
                replacements.append([indx, i, sngs[0], req_one_ncom])
                found.append(indx)                    

    # replaced indices
    replaced_indices = list(set([x[0] for x in replacements]))

    # not found replacements
    unreplaced_indices = [x for x in range(len(sent_ngrams)) if x not in replaced_indices]

    for unreplaced_index in unreplaced_indices:
        replacements.append([unreplaced_index, 0, sent_ngrams[unreplaced_index], ''])

    return replacements

# remove a word randomly
def remove_words(v, l, n):

    choice = random.choice(l)
    r = [x for x in l if x != choice]

    return r

# insert a random determiner
def insert_determiner(v, l, n):
    
    # range of indices -> length of tokens
    insert_at = random.choice(list(range(len(l))))
    
    # insert at specific random index
    try:
        l.insert(insert_at, random.choice(v.determiners))
    except:
        return l

    return l

# replace based on dictionary
def dictionary_replacement(v, l, n):
    
    try:
        common = random.choice(list(set(v.replacement_keys).intersection(l)))    
    except:
        return l
    
    return [random.choice(v.replacements[w]) if w == common else w for w in l]

# change the order of phrases
def phrase_order_change(v, l, n):
    '''
    l, n = ["a", "went", "to", "the"], 4
    print(rearrange_words(s, 4))
    >>> ["went", "a", "to", "the"]
    '''

    a, b = (0,0)
    
    if n >= 5:
        a,b = random.choice([(0,1), (1,2), (2,3), (3,4)])
    elif n == 4:
        a,b = random.choice([(0,1), (1,2), (2,3)])
    elif n == 3:
        a,b = random.choice([(0,1), (1,2)])
    elif n == 2:
        a,b = (1,0)
    else:
        return l

    rl = l.copy()
    
    # swap positions
    rl[a] = l[b]
    rl[b] = l[a]

    return rl

def punctuations(v, l, n):
    # input: ['once', 'life']
    # return ['once.', 'life']

    w = random.choice(l)
    p = random.choice(v.rep_punctuations)
    x = w + p
    
    return [x if y==w else y for y in l]

def punctuation_braces(v, l, n):
    # input: ['once', 'life']
    # return ['once', '(life']

    w = random.choice(l)
    p = random.choice(v.rep_punctuations_braces)
    x = w + p
    
    return [x if y==w else y for y in l]

# duplicate a word
def duplication(v, l, n):
    # input: ['once', 'life']
    # return ['once', 'life life']

    w = random.choice(l)
    x = str(w) + ' ' + str(w)
    
    return [x if y==w else y for y in l]

# split known words into two or more
def split_words(v, l, n):

    x = ''
    for w in l:
        if w in v.splitter_keys:
            x = v.splitters[w]
            return [x if y==w else y for y in l]
    else:
        return l

def spelling_errors(v, l, n):

    return l

def dictionary_replacement_verb_form_change(v, l, n):

    r = dictionary_replacement(v, l,n)
    l = verb_form_change(v, r, n)    

    return l

def dictionary_replacement_phrase_order_change(v, l, n):

    r = dictionary_replacement(v, l,n)
    l = phrase_order_change(v, r, n)

    return l

def verb_form_change_insert_determiner(v, l, n):

    r = verb_form_change(v, l,n)
    l = dictionary_replacement(v, r, n)    

    return l

def insert_determiner_verb_form_change(v, l, n):

    r = insert_determiner(v, l, n)
    l = verb_form_change(v, r,n)

    return l

def verb_form_change_phrase_order_change(v, l, n):

    r = verb_form_change(v, l,n)
    l = phrase_order_change(v, r, n)

    return l


def create_error(x):

    v = Variables()
    v.__init__()

    # x -> # index, ngram, sentence, replace, error

    #print(common_error_function_map["remove_verbs"](['1', '2']))

    ng = x[1]
    sentence = x[2]
    ngs = list(x[3])
    error = x[4]

    if not ngs:
        dx = 1
        #print(ng, ngs)
    else:
        # call the function corresponding to the error
        rephrased = v.common_error_function_map[x[4]](v, ngs, ng)
        return rephrased


    return "foo"




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

            ngrams, sent_ngrams = create_sent_ngrams(self.ngram_order, self.ngram_cols,
                                                self.sentence_column, self.source_data[start:start+batchsize],
                                                self.n_ngrams,
                                                )

            print("sent_ngrams: ", len(sent_ngrams))

            replacements = random_most_common_ngram(sent_ngrams, self.ngram_cols, 
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
        sampled_replacements['replacement'] = sampled_replacements.apply(lambda x: create_error(x), axis=1)

        #print("No reps: ", len(sampled_replacements.loc[sampled_replacements.replacement == sampled_replacements.replace]))

        #print(sampled_replacements.loc[sampled_replacements.replacement == sampled_replacements.replace].error.value_counts())

        return sampled_replacements
