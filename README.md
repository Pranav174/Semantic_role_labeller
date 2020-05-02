# Semantic-Role-Labelling in Hindi/urdu

## Aim

Argument Identification and Semantic Role Labelling (as a classification task)

## Dataset

Hindi-Urdu PropBank (Bhatt et al., 2009)
Link: http://ltrc.iiit.ac.in/hutb_release/
<br>
News Artices manually annotated in SSF format.
*Total sentences = 6800*

# How to run

Python version 3.6 or above is required

Use parse.py to first process the raw annotated data

```
pip install -r requirements.txt

python parse.py

```

Then checkout the jupyter notebook `runner.ipynb`