#!/usr/bin/python
# this is the example script to use xgboost to train
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import StratifiedKFold

def predict_data( data , model_file_name , feature_names ):
    
    d_feat = data[feature_names]

    dpred = xgb.DMatrix(d_feat, missing=np.nan)

    # load in bdt
    bdt_cosmic = xgb.Booster(model_file=model_file_name)
    print "loaded model: ",model_file_name

    # score dataset
    m_preds  = bdt_cosmic.predict(dpred)

    # save (only one) score for how likely is it to be a cosmic
    data['p_score']   = m_preds

    return data



# unused....
#
#def score_cut(data, pcut):
#    
#    # get passing samples
#    data_pass = data[data.p_score > pcut]
#
#    return data_pass
