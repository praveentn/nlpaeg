# variables


adj_tags = ['JJ', 'JJR', 'JJS']
noun_tags = ['NN', 'NNP', 'NNS', 'NNPS']
verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adverb_tags = ['RB', 'RBR', 'RBS']

# operations
operations = ["dict_replacement", "duplication",
              "punctuations", "punctuation_braces",  
              "random_removal", "split_words",
              "insert_determiner", "change_order",

             ]



# split words
splitters = {
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
    
}


# were -> where
# there -> they are

replacements = {
    
    "have": ["has"],
    "has": ["have"],
    "were": ["we are", "we're", "where",],
    "we're": ["were",],
    "where": ["were", "we're", "we are", ],
    "there": ["their", "they're", "they are"],
    "their": ["there", "they're", "they are"],
    "a": ["an", "as", "are", ],
    "an": ["a", "are", ],
    "its": ["it's", "it is"],
    "it's": ["its"],
    "to": ["too", "on",],
    "too": ["to",],
    "of": ["off",],
    "off": ["of",],
    "effect": ["affect",],
    "affect": ["effect",],
    "by": ["buy", "bye"],
    "buy": ["by", "bye"],
    "here": ["hear", ],
    "hear": ["here", ],
    
    
}




