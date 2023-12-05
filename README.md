# Medical Privace Protection  
  
## Environments  
  
### Using conda ( Recommended )  

#### Using environment.yml
Create a conda environment using `environment.yml`  
```  
conda env create -f /path/to/environment.yml  
```  

#### Create environment manually
1. Create a conda env
```
conda create -p ./env python=3.11
```
2. Install with pip
```
pip install -r requirements.txt
```

  
### Using Pip   
1. Create a virtaul environment with venv  
```  
python -m venv venv  
```  
2. Pip install with requirments.txt  
```  
pip install -r requirements.txt  
```  

## Running   

### Subtask 1  
  
Run `Medical_Privacy_Protection.ipynb` to generate answer.txt subminssion without TIME, DATE, DURATION, and SET field.  
Hyperparameter can be set in Hyperparameter part.  

### Subtask 2

Run `run_phase2.py --file /path/to/answer.txt` to generate answer_result_sorted.txt.  

## Files  

```
Medical_Privacy_Protection.ipynb  --- for all the impliment of task1
run_phase2.py                     --- for the main read file logic for task2.
parsers/                          --- all the parsers used in task2
    |- basic_parser.py            --- basic parser class for extends
    |- time_parser.py             --- parser for time
    |- date_parser.py             --- parser for date
    |- set_parser.py              --- parser for set
    |- duration_parser.py         --- parser for duration
    |- __init__.py                --- make class warpped all the parsers
dataset/                          --- store all the datasets
submissions/                      --- store generated answer.txt

```