# NLP Tool Kit
My minimal natural language processing tools used in BioCreative Contest IV.

# Installation 
    pip install nlptoolkit

# Functions
## sent_tokenize(text)
A rule based sentence tokenizer desiged for biomedical papers. It will not cut the text in paired symbols such as '(', ')' and '[', ']'. 

    >>> from nlptoolkit import nlp
    >>> text = """A rule based sentence tokenizer desiged for biomedical papers. (Fig. 1a, we did a good job in this. The accuracy is about 0.9431.)"""
    >>> nlp.sent_tokenize(text)
    ['A rule based sentence tokenizer desiged for biomedical papers.', '(Fig. 1a, we did a good job on this. The accuracy is about 0.94.)']
    
- input: text containing multi-sentences
- output: a list of sentences

## sent_count(text)
Segment the give text by sent_tokenzie, and then return its length

    >>> nlp.sent_count(text)
    2

## clause_tokenize(sentence)
Split on comma or parenthesis, if there are more then three words for each clause

    >>> nlp.clause_tokenize(sentence)



## word_tokenize(sentence)
Cut the sentence in into tokens without deleting anything

## slim_stem(token)
A very simple stemmer, for entity of GO stemming

## powerset(iterable)
powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)

## ngram(n, iter_tokens)
Return a generator of n-gram from an iterable
    z = len(iter_tokens)
    return (iter_tokens[i:i+n] for i in xrange(z-n+1))

## power_ngram(iter_tokens)
Generate unigram, bigram, trigram ... and the max-gram, different from powerset(), this function will not generate skipped combinations such as (1,3)

