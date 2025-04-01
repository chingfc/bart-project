#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import warnings

import numpy as np
import pandas as pd

# system module
import sys
from os.path import join
## fmri modules
from nltools.data import Brain_Data
from nltools.mask import expand_mask

# Arguments
parcel = int(sys.argv[1])
cond = str(sys.argv[2])

base_dir = "/home/.admin/chingfc/BART"


subjects = np.loadtxt(join(base_dir, 'code', 'subject.csv'), skiprows=1, dtype=str)


roi_mask = Brain_Data(join(base_dir, 'code', 'Neurosynth Parcellation_2.nii.gz'))
mask_x = expand_mask(roi_mask)

parcel_data = {}
for subj in subjects:
    brain_data = Brain_Data(join(base_dir, 'zmap', f'sub-{subj}_bart-{cond}_zmap.nii.gz'))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        parcel_data[subj]= brain_data.apply_mask(mask_x[parcel]).data

parcel_data = pd.DataFrame.from_dict(parcel_data)
parcel_data.T.to_csv(join(base_dir, '200parcels', cond, f'task-bart_parcel-{parcel}_{cond}.csv'))


