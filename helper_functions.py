import random
import pandas as pd
import helper_variables as hv
from tqdm import tqdm
from itertools import chain
from collections import Counter
from lemminflect import isTagBaseForm
from lemminflect import getLemma, getAllLemmas, getInflection
from lemminflect import getAllInflections, getAllInflectionsOOV

# globals

# split words
splitter_keys = list(hv.splitters.keys())

# replacements
replacement_keys = list(hv.replacements.keys())

# operations
operations = hv.operations



## change the form of verbs
## uses lemminflect
def verb_form_change(l, n):
    
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
        return "No replacement found"


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
def remove_words(l, n):

    choice = random.choice(l)
    r = [x for x in l if x != choice]

    return r

# insert a random determiner
def insert_determiner(l, n):
    
    # range of indices -> length of tokens
    insert_at = random.choice(list(range(len(l))))
    
    # insert at specific random index
    try:
        l.insert(insert_at, random.choice(hv.determiners))
    except:
        return "No replacement found"

    return l

# replace based on dictionary
def dictionary_replacement(l, n):
    
    common = random.choice(list(set(hv.replacement_keys).intersection(l)))    
    
    if common:
        return [random.choice(hv.replacements[w]) if w == common else w for w in l]
    else:
        return "No replacement found"

# change the order of phrases
def phrase_order_change(l, n):
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
        return "No replacement found"

    rl = l.copy()
    
    # swap positions
    rl[a] = l[b]
    rl[b] = l[a]

    return rl

def punctuations(l, n):
    # input: ['once', 'life']
    # return ['once.', 'life']

    w = random.choice(l)
    p = random.choice(hv.punctuations)
    x = w + p
    
    return [x if y==w else y for y in l]

def punctuation_braces(l, n):
    # input: ['once', 'life']
    # return ['once', '(life']

    w = random.choice(l)
    p = random.choice(hv.punctuation_braces)
    x = w + p
    
    return [x if y==w else y for y in l]


# duplicate a word
def duplication(l, n):
    # input: ['once', 'life']
    # return ['once', 'life life']

    w = random.choice(l)
    x = str(w) + ' ' + str(w)
    
    return [x if y==w else y for y in l]

# split known words into two or more
def split_words(l, n):

    x = ''
    for w in l:
        if w in splitter_keys:
            x = hv.splitters[w]
            return [x if y==w else y for y in l]
    else:
        return "No replacement found"

def spelling_errors(l, n):

    return l

def dictionary_replacement_verb_form_change(l, n):

    try:
        l = dictionary_replacement(l,n)
        l = verb_form_change(l, n)
    except:
        return "No replacement found"

    return l

def dictionary_replacement_phrase_order_change(l, n):

    try:
        l = dictionary_replacement(l,n)
        l = phrase_order_change(l, n)
    except:
        return "No replacement found"

    return l

def verb_form_change_insert_determiner(l, n):

    try:
        l = verb_form_change(l,n)
        l = insert_determiner(l, n)
    except:
        return "No replacement found"

    return l

def verb_form_change_phrase_order_change(l, n):

    try:
        l = verb_form_change(l,n)
        l = phrase_order_change(l, n)
    except:
        return "No replacement found"

    return l

def random_pick(l, n):

    pick = random.choice(list(common_error_function_map.keys()))

    try:
        l = pick(l, n)
        l = pick(l, n)
    except:
        return "No replacement found"

    return l


common_error_function_map = {
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
    "spelling_errors": spelling_errors,
    "random_pick": random_pick,


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
            dx = 1
            #print(ng, ngs)
        else:
            # call the function corresponding to the error
            rephrased = common_error_function_map[x[4]](ngs, ng)
            return rephrased


    return "foo"