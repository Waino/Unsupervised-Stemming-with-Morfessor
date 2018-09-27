# Unsupervised-morphological-segmentation-with-Morfessor

This stemmer uses Morfessor 2.0 (Virpioja,et al. 2013) and Morfessor FlatCat 1.0 (Grönroos, et al. 2014).
* Stemming_unsupervised.py is the code for unsupervised stemming.
* The sample data to be stemmed is in raw/en/ and raw/tr/.
* The output will be stored in segmented/en/ and segmented/tr/ respectively.
* In this example, the model is trained on the data to be stemmed. In practice you may want to train on larger data.

## Setup
Before running the code, please install Morfessor 2.0 (http://morfessor.readthedocs.io/en/latest/installation.html) and Morfessor FlatCat 1.0.5 (http://morfessor-flatcat.readthedocs.io/en/latest/installation.html#installation-instructions).

## Unsupervised Example
Here we set the corpus weight parameter to 1.0. 
The optimal value depends on the data set.
`$ python Stemming_unsupervised.py 1.0 raw/en/ segmented/en/`

## Auto-tuning Example
Here we use auto-tuning of the corpus weight parameter.
The tuning parameter is the average length of morphs (all morphs including affixes, not just stems).
In the example we set this to 3.5 characters.
`$ python Stemming_autotune.py 3.5 raw/en/ segmented/en/`
