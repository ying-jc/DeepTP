from dataset_processing import Processing
import numpy as np
from torch.utils.data import DataLoader
import torch.nn as nn
import torch
import pandas as pd
from Bio import SeqIO
import sys

def mod_predict(seq,terminal,out):
    
    print('\nPerforming data processing ......')
    pseqs, pseq_ids = read_fasta(seq)
    pseq_labels = np.zeros(len(pseqs))
    pseqDataset = Processing(pseqs, pseq_labels)
    pseqDataloader = DataLoader(pseqDataset, batch_size=32, shuffle=False)

    print('\nPerforming protein prediction ......')
    m = torch.load(sys.path[0]+'/CNN.pkl')
    y_pred = torch.zeros([0, 1])
    with torch.no_grad():
        m.eval()
        for x, _ in pseqDataloader:
            x = x.type(torch.FloatTensor)
            pre0 = m(x)
            y_pred = torch.cat([y_pred,pre0],dim=0)
    pre_scores = y_pred[:,0]    
    preds = [0 if p < 0.5 else 1 for p in pre_scores]
    df = pd.DataFrame({'SeqID':pseq_ids,'Probability of TP':pre_scores,'Prediction of TP':preds})
    df = df.set_index('SeqID')
    
    if terminal == 'True':
        print('\n'.join(['','Result of prediction:\n']))
        print(df)
        
    if out != None:        
        df.to_csv(out)
        print('\nThe result of prediction has been saved to '+out+'!')


def read_fasta(fasta_file, len_criteria=1000):
    result = []
    seq_ids = []
    fp = open(fasta_file)
    for seq_record in SeqIO.parse(fp, 'fasta'):
        seq = seq_record.seq.upper()
        seq_id = seq_record.id
        if len(seq) <= len_criteria:
            seq += '_' * (len_criteria-len(seq))
            result.append(str(seq))
            seq_ids.append(seq_id)
    fp.close()
    return result, seq_ids
