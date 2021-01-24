# Generata - Generate Data

A Python package for Artificial Error Generation!

## <i> work-in-progress

## About

Approach:


Data Description:

Abstracts and Titles are extracted from PubMed. NLTK Sentence Tokenizer (PunktSentenceTokenizer) is used to create sentences. Some post-processing is done on top of sentence tokenization.

No. of samples: 100,000
No. of sentences from abstracts: ~89,000
No. of titles: ~11,000




Model Analysis Dataset: The Corpus of Linguistic Acceptability (CoLA) in its full form consists of 10657 sentences from 23 linguistics publications, expertly annotated for acceptability (grammaticality) by their original authors. The public version provided here contains 9594 sentences belonging to training and development sets, and excludes 1063 sentences belonging to a held out test set. Contact alexwarstadt [at] gmail [dot] com with any questions or issues. Read the paper or check out the source code for baselines.

Paper 

Read the paper at https://arxiv.org/abs/1805.12471

https://nyu-mll.github.io/CoLA/


### Dependencies:

+ Python (3.8+)


Install `nlpaeg` on your system using:

```
pip install nlpaeg
```


### Usage:

Importing the library: 

```
import nlpaeg
from nlpaeg import error_generator as eg
```


Instantiate the class:

```
g = eg.ErrorGenerator()
```


Initialize the parameters:

```
params = {

       }
```

Set config params
```
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
"dictionary_replacement_verb_form_change": 0.1,
"dictionary_replacement_word_order_change": 0.1,
"verb_form_change_order_change": 0.1,
"insert_determiner": 0.1,
"punctuation_braces": 0.05,
"punctuations": 0.05,
"duplication": 0.1,
"split_words": 0.1,
"remove_words": 0.05,


}






```

Create your dataframe:

```

# call the method to create error data
aeg_df = g.get_aeg_data()

aeg_df.to_csv('sampled_replacements_1.csv', index=None)

```


