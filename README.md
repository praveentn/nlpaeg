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
from nlpaeg import generator as gr
```


Instantiate the class:

```
g = gr.Generator()
```


Initialize the parameters:

```
params = {

       }
```

Set config params
```
    # data directory
    data_dir = os.path.join(os.getcwd(), "data")
    
    # filename sentences without errors
    train_data = "nlpaeg_pubmed_data_min.csv"
    train_data_file_path = os.path.join(data_dir, train_data)

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



```

Create your dataframe:

```
df = g.get_aeg_data()
```


