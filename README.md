# Semantic-Role-Labelling in Hindi/urdu

## Aim

Argument Identification and Semantic Role Labelling (as a classification task)

## Dataset

Hindi-Urdu PropBank (Bhatt et al., 2009)
Link: http://ltrc.iiit.ac.in/hutb_release/
<br>
News Artices manually annotated in SSF format.
*Total sentences = 6800*

## Running the project

Python version 3.6 or above is required

> Install requirements

```bash
pip install -r requirements.txt
```

> Parse the raw annotated data
```bash
python parse.py
```

> Install Jupyter Notebook and add the kernal to environment (if using virtual env)
```bash
pip install jupyter notebook
python -m ipykernel install --user --name=<venv name>
```

> Run the notebook 
```bash
jupyter notebook runner.py
```

## Results

### Model 1 summary
```
Model: "sequential_13"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
dense_25 (Dense)             (None, 10)                890       
_________________________________________________________________
dense_26 (Dense)             (None, 1)                 11        
=================================================================
Total params: 901
Trainable params: 901
Non-trainable params: 0
```

### Model 2 summary
```
Model: "sequential_9"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
dense_17 (Dense)             (None, 10)                1380      
_________________________________________________________________
dense_18 (Dense)             (None, 22)                242       
=================================================================
Total params: 1,622
Trainable params: 1,622
Non-trainable params: 0
```

### Final Scores
```
Accuracy: 0.829616129398346
Precision: 0.8437967300415039
Recall: 0.8199087977409363
F1-score: 0.8314988017082214
Loss: 0.5700723652665305
```

## Contributions

__Pranav Goyal__
- Parsing script
- Initial Model Setup
- Hyperparameter Tuning

__Akshat Chhajer__
- Parsing Refactoring
- Feature Engineering for models
- Confusion Matrix
- Final Scoring
- Documentation
