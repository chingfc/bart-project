#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join
import sys
from hbayesdm.models import bart_ewmv
import arviz as az


id = str(sys.argv[1]) # get the id of the simulation

base_dir = "/home/.admin/chingfc/BART/code/simulations"

file = join(base_dir, f'estimated_values_{id}.txt')




bart_ewmv_pred = bart_ewmv(data=file, niter=1000,nwarmup=500, 
        nchain=4, ncore=10, adapt_delta=0.99, 
        inc_postpred=True,
        inits=([0.01,0.0029,-0.00048,12,1.9]), max_treedepth=10000)

                      
fit = bart_ewmv_pred.fit  
all_ind_pars = bart_ewmv_pred.all_ind_pars

idata = az.from_pystan(fit, log_likelihood='log_lik', posterior_predictive='y_pred')

idata.to_netcdf(join(base_dir, f'models/bart_ewmv_estimated_values{id}.nc'))

all_ind_pars.to_csv(join(base_dir, f'models/bart_ewmv_inv_paras_estimated{id}.csv'))