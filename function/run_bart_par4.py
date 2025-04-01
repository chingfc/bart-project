#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from os.path import join
from hbayesdm.models import bart_par4
import os

base_dir = '/home/qiulab_DATA/chingfc/BART'

def save(obj, filename) -> None:
    """ save compiled models """
    with open(filename, "wb") as f:
        pickle.dump(obj, f)


bart_output_pred = bart_par4(data='~/chingfc/BART/code/bart_data.txt', niter=5000,nwarmup=2000, 
                        nchain=4, ncore=48, adapt_delta=0.99, 
                        inc_postpred=True,
                        inits=[0.01, 0.0029, 0.00048, 12], max_treedepth=100)
                      
fit = bart_output_pred.fit  
par_vals = bart_output_pred.par_vals
all_ind_pars = bart_output_pred.all_ind_pars


save_path = join(base_dir, 'code/model')
os.makedirs(save_path, exist_ok=True)


all_ind_pars.to_csv(join(save_path, 'bart_output_par4_pred_all_ind_pars.csv'))
save(fit, join(save_path, 'bart_output_par4_pred_fit.pkl'))
save(par_vals, join(save_path, 'bart_output_par4_pred_par_vals.pkl'))
save(bart_output_pred, join(save_path, 'bart_output_par4_pred.pkl'))
