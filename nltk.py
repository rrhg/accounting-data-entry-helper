# from nltk import word_tokenize
# last = s.split()[-1}
# tokens = word_tokenize(last)
# if len(tokens) = 1:
#     # last should not remain hyphenated


# from nltk.sentiment import sentimentintensityanalyzer
# sia = SentimentIntensityAnalyszer()
# sia.polarity_scores(...)
# # gives the %s of negative or positives

s = 'this a an english sentence'

# import nltk
# from nltk.corpora import udhr
from nltk import corpus
# from nltk.corpus import udhr
english_vocab = set(w.lower() for w in udhr.words.words())
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())
text_vocab = set(w.lower() for w in text if w.lower().isalpha())
unusual = text_vocab.difference(english_vocab) 
print(unusual)