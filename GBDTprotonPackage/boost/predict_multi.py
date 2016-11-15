#!/usr/bin/python
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import StratifiedKFold

def predict_multiscore( data , model_file_name , feature_names ):
    
    d_feat = data[feature_names]

    dpred = xgb.DMatrix(d_feat, missing=np.nan)

    # load in bdt
    bdt_cosmic = xgb.Booster(model_file=model_file_name)
    print "loaded model: ",model_file_name

    # score dataset
    m_preds  = bdt_cosmic.predict(dpred)
    max_pred = np.argmax(m_preds,axis=1) # maximal score
    print "created scores data-sets"

    # save scores
    data['mscore_p']   = m_preds[:,0]
    data['mscore_mu']  = m_preds[:,1]
    data['mscore_pi']  = m_preds[:,2]
    data['mscore_em']  = m_preds[:,3]
    data['mscore_cos'] = m_preds[:,4]
    data['mscore_max'] = max_pred
    print "done predicting"
    
    return data




