# LinguaF

![Version](https://img.shields.io/pypi/v/linguaf?logo=pypi)
![Downloads](https://img.shields.io/pypi/dm/linguaf)
![Repo size](https://img.shields.io/github/repo-size/perevalov/linguaf)

**LinguaF provides an easy access for researchers and developers to methods of quantitative language analysis, such as: readability, complexity, diversity, and other descriptive statistics.**

## Usage

```python
documents = [
    "Pain and suffering are always inevitable for a large intelligence and a deep heart. The really great men must, I think, have great sadness on earth.",
    "To go wrong in one's own way is better than to go right in someone else's.",
    "The darker the night, the brighter the stars, The deeper the grief, the closer is God!"
]
```

### Descriptive Statistics

The following descriptive statistics are supported (`descriptive_statistics.py` module):

* Number of characters `char_count`
* Number of letters `letter_count`
* Number of punctuation characters `punctuation_count`
* Number of digits `digit_count`
* Number of syllables `syllable_count`
* Number of sentences `sentence_count`
* Number of n-syllable words `number_of_n_syllable_words`
* Number of n-syllable words for all found syllables `number_of_n_syllable_words_all`
* Average syllables per word `avg_syllable_per_word`
* Average word length `avg_word_length`
* Average sentence length `avg_sentence_length`
* Average words per sentence `avg_words_per_sentence`

Additional methods:
* Get lexical items (nouns, adjectives, verbs, adverbs) `get_lexical_items`
* Get n-grams `get_ngrams`
* Get sentences `get_sentences`
* Get words `get_words`
* Tokenize `tokenize`
* Remove punctuation `remove_punctuation`
* Remove digits `remove_digits`

Example:

```python
from linguaf import descriptive_statistics as ds


ds.words_per_sentence(documents)
# Output: 15
```

### Syntactical Complexity

The following syntactical complexity metrics are supported (`syntactical_complexity.py` module): 
* Mean Dependency Distance (MDD) `mean_dependency_distance`

Example:

```python
from linguaf import syntactical_complexity as sc


sc.mean_dependency_distance(documents)
# Output: 2.307306255835668
```

### Lexical Diversity

The following lexical diversity metrics are supported (`lexical_diversity.py` module): 
* Lexical Density (LD) `lexical_density`
* Type Token Ratio (TTR) `type_token_ratio`
* Herdan's Constant or Log Type Token Ratio (LogTTR) `log_type_token_ratio`
* Summer's Index `summer_index`
* Root Type Token Ratio (RootTTR) `root_type_token_ratio`

Example:

```python
from linguaf import lexical_diversity as ld


ld.log_type_token_ratio(documents)
# Output: 94.03574963462502
```

### Readability

The following readability metrics are supported (`readability.py` module): 
* Flesch Reading Ease (FRE) `flesch_reading_ease`
* Flesch-Kincaid Grade (FKG) `flesch_kincaid_grade`
* Automated Readability Index (ARI) `automated_readability_index`
* Simple Automated Readability Index (sARI) `automated_readability_index_simple`
* Coleman's Readability Score `coleman_readability`
* Easy Listening Score `easy_listening`


Example:

```python
from linguaf import readability as r


r.flesch_kincaid_grade(documents)
# Output: 4.813333333333336
```

## Install

### Via PIP

```bash
pip install linguaf
```

### Latest version from GitHub

```bash
git clone https://github.com/Perevalov/LinguaF.git
cd LinguaF
pip install .
```

## Language Support

At the moment, library supports English and Russian languages for all the methods.

## Citation

TBD
