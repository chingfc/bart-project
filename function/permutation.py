#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
import numpy as np
import pandas as pd

# system module
import sys
from os.path import join
##stats modules
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist

## fmri modules
from nltools.data import Brain_Data
from nltools.mask import expand_mask

# Arguments
metric_model = str(sys.argv[1])
n_permute = int(sys.argv[2])


rng = 123
base_dir = "/home/.admin/chingfc/BART"

subjects = np.loadtxt(join(base_dir, 'code', 'subject.csv'), skiprows=1, dtype=str)
model_df = pd.read_csv('model.csv', dtype={'subjid': str}).set_index('subjid')
model_df = model_df.loc[subjects]
model = model_df.loc[metric_model]

roi_mask = Brain_Data('http://neurovault.org/media/images/2099/Neurosynth%20Parcellation_2.nii.gz')
mask_x = expand_mask(roi_mask)



is_brain_data = []
for subj in subjects:
    brain_data = Brain_Data(f'../zmap/sub-{subj}_bart-explosion_derivative_zmap.nii.gz')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        is_brain_data.append(brain_data.apply_mask(mask_x[parcel]).data)
    
brain_vector = pdist(is_brain_data, metric='correlation')

para_vector =  pdist(metric_model.reshape(-1, 1), metric='euclidean')

brain_parcels[parcel] = brain_vector
model_para[parcel] = para_vector

isc_r[parcel], isc_p[parcel] = permutation(para_vector, brain_vector, n_permute)

def permutation(modelDist, brainDist_vec, n_permute):
    corr = spearmanr(modelDist,brainDist_vec)[0]
    perm = []
    for p in range(n_permute):
        perm.append(spearmanr(np.random.permutation(modelDist),brainDist_vec)[0])
    if corr>=0:
        perm_p = np.mean(perm>=corr)
    else:
        perm_p = np.mean(perm<=corr)
    pval = perm_p
    return corr, pval