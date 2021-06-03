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

```python
from linguaf import descriptive_statistics as ds


ds.words_per_sentence(documents)
# Output: 15
```

### Syntactical Complexity

```python
from linguaf import syntactical_complexity as sc


sc.mean_dependency_distance(documents)
# Output: 2.307306255835668
```

### Lexical Diversity

```python
from linguaf import lexical_diversity as ld


ld.log_type_token_ratio(documents)
# Output: 94.03574963462502
```

### Readability

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

## Open API

The Swagger UI of the API is located here: http://webengineering.ins.hs-anhalt.de:41008/docs

There is currently a request limit set up for 50 requests per minute. If you are beyond the limit, requests are moved to the queue.

## Citation

TBD
