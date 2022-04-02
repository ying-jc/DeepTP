# DeepTP  
A deep learning-based tool for the prediction of transport proteins from sequence information

## Installation  
Clone DeepTP by  
```
$ git clone https://github.com/ying-jc/DeepTP.git
```  
or
Download DeepTP (ZIP file), move it to a directory where the user wants it installed, and uncompress it.

## Requirements  
DeepTP is an open-source Python-based tool, which operates depending on the Python environment (Python Version ≥ 3.0). Currently, DeepTP has only been tested on the Linux system. Before running DeepTP, the user should make sure all the following packages are installed in their Python environment: click, pandas, biopython, and torch. 
These packages can be easily installed using pip by
```
$ pip install -r requirements.txt
```  

## Usage  
### Options  
For details of all options, run:  
```
$ python DeepTP.py --help

Usage: DeepTP.py [OPTIONS]

  DeepTP: A deep learning-based tool for the prediction of transport proteins
  from sequence information

Options:  
  --seq TEXT                   Protein sequence file in fasta format. (Required)
  --terminal [True|False]      Output result to the terminal. [Default: True]
                               (Optional)
  --out TEXT                   The name of the output file in comma-delimited text
                               format. (Optional)
  --help                       Show this message and exit.
```  

### Notes  
#### Sequence of input
The input to DeepTP can be any number of protein sequences in FASTA format. The sequence must not contain the blurred disabilities (such as "X", "Z", "B", "J", "O", "U", and "*"), and the length must be no longer than 1000aa.

#### Result of output
DeepTP outputs the results to the terminal by default. The user can specify the name of the output file to save the results to a CSV file. In the results, the first column represents the sequence name, the second column represents the estimated probability of a transport protein for the corresponding sequence, and the third column represents the classification result.

## An example  
All files in the commands can be found in the directory of DeepTP.  
* Locate to the example folder:
```
$ cd DeepTP/example
```
* Run the following command to predict the sequences in the example with the default settings:
```
$ python ../Deep.py --seq example.fasta
```

## Citation  
Xu T, Wang Q, Ying J. Prediction of transport proteins from sequence information with the deep learning approach. (Under review).
