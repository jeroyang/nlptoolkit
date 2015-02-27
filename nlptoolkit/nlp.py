# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import re
from itertools import chain, combinations

def sent_tokenize(context):
    paired_symbols = [("(", ")"),
                  ("[", "]"),
                  ("{", "}")]
    paired_patterns = ["%s.*?%s" % (re.escape(lt), re.escape(rt)) for lt, rt in paired_symbols]
    number_pattern = ['\d+\.\d+']
    arr_pattern = ['(?: \w\.){2,3}|(?:\A|\s)(?:\w\.){2,3}|[A-Z]\. [a-z]|\svs\. |et al\.|Fig\. \d|approx\.|(?:Prof|Dr)\. (?:[A-Z]\.)?']
    escape_re = re.compile("|".join(paired_patterns + number_pattern + arr_pattern))
    escapes = escape_re.findall(context)
    escaped_stem = escape_re.sub('{}', context)
    escaped_escaped_stem = escaped_stem.replace('{','{{').replace('}', '}}')
    sent_re = re.compile(r'([A-Z0-9]..+?(?:[.!?]\s|[\n$]))')
    sent_stem = sent_re.sub(r'\1###linebreak###', escaped_escaped_stem)
    recovered_sent_stem = sent_stem.replace('{{}}', '{}')
    result = recovered_sent_stem.format(*escapes)
    return [r.strip() for r in result.split('###linebreak###') if r != '']

def sent_count(context):
    return len(sent_tokenize(context))

def clause_tokenize(sentence):
    """Split on comma or parenthesis, if there are more then three words for each clause"""
    clause_re = re.compile(r'((?:\S+\s){2,}\S+,|(?:\S+\s){3,}(?=\((?:\S+\s){2,}\S+\)))')
    clause_stem = clause_re.sub(r'\1###clausebreak###', sentence)
    return [c for c in clause_stem.split('###clausebreak###') if c!='']

def word_tokenize(sentence):
    """Cut the sentence in into tokens without deleting anything"""
    number_pattern = ['\d+\.\d+']
    arr_pattern = ['(?: \w\.){2,3}|(?:\A|\s)(?:\w\.){2,3}|[A-Z]\. [a-z]']
    escape_re = re.compile("|".join(number_pattern + arr_pattern))
    escapes = escape_re.findall(sentence)
    escaped_stem = escape_re.sub('protectprotectprotect', sentence)
    word_stem = re.sub("([%s])" % re.escape('!"#$%&()*,./:;<=>?@[\]^_`{|}~'), r' \1 ', escaped_stem)
    escaped_word_stem = word_stem.replace('{','{{').replace('}', '}}')
    result = escaped_word_stem.replace('protectprotectprotect', '{}').format(*escapes)
    return [r.strip() for r in result.split(' ') if r != '']

def slim_stem(token):
    """A very simple stemmer, for entity of GO stemming"""
    target_subfixs = ['ic', 'tic', 'e', 'ive', 'ing', 'ical', 'nal', 'al', 'ism', 'ion', 'ation', 'ar', 'sis', 'us', 'ment']
    for subfix in sorted(target_subfixs, key=len, reverse=True):
        idx = token.find(subfix)
        if idx != -1 and idx == len(token)-len(subfix):
            return token[0:-len(subfix)]
    return token  

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def ngram(n, iter_tokens):
    """Return a generator of n-gram from an iterable"""
    z = len(iter_tokens)
    return (iter_tokens[i:i+n] for i in xrange(z-n+1))

def power_ngram(iter_tokens):
    """Generate unigram, bigram, trigram ... and the max-gram,
     different from powerset(), this function will not generate skipped combinations such as (1,3)"""
    return chain.from_iterable(ngram(j, iter_tokens) for j in xrange(1, len(iter_tokens)))

