#!/usr/bin/python
# this is the example script to use xgboost to train
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import StratifiedKFold

def load_data( TrainingSampleName , feature_names ):
    
    # (1) use pandas to import csvs
    # ---------------------------------------
    data_c1 = pd.read_csv( TrainingSampleName )
    data_p1 = data_c1[data_c1.MCpdgCode == 2212] # all protons
    data_b1 = data_c1[data_c1.MCpdgCode != 2212] # everything else - to be labeled as 'bad'
    
    
    
    
    # (2) pull out features we want to use
    # ---------------------------------------
    data_mc_protons     = data_p1[feature_names]    # only protons
    data_mc_non_protons = data_b1[feature_names]    # everything else
    
    # change the format to match the GBT package req.
    Xprotons        = np.array( data_mc_protons )
    Xnon_protons    = np.array( data_mc_non_protons )
    data = np.vstack( [ Xprotons , Xnon_protons ] )
                            





    # (3) label 'good' = 1, and 'bad' = 0
    # ---------------------------------------
    Yprotons        = np.ones( len(Xprotons) )
    Ynon_protons    = np.zeros( len(Xnon_protons) )
    label = np.hstack( [ Yprotons , Ynon_protons ] )






    # (4) weight everything so that the
    # sum of all of the negative sample equals
    # the sum of all of the positive sample
    # ---------------------------------------
    Wprotons        = np.ones( len(Xprotons) )
    Wnon_protons    = np.ones( len(Xnon_protons) ) * np.true_divide( len(Xprotons) ,len(Xnon_protons) )
    weight = np.hstack( [ Wprotons , Wnon_protons ] )
    
    return data,label,weight


# these following line are to be used in load_data() if we want to train also on (extBNB) cosmic data:
# ------------------------------------------------------------------------------------------------------------
#   data_d1 = pd.read_csv('data/goodruns/features_extBNB_AnalysisTrees_train.csv') # 20k extBNB data tracks
#   data_d = data_d1[feature_names]
#   X3 = np.array(data_d)
#   data = np.vstack([X1,X2,X3])
#   y2 = np.zeros(len(X2) + len(X3))
#   w3 = np.ones(len(X3))*np.true_divide(len(X1),len(X3))
#   weight = np.hstack([w1,w2,w3])
#   weight = np.ones(len(data))








def run_cv( data , label , weight , param ):
    '''
    cross-validation stage, to see how things behave
    '''
    
    # you can directly throw param in, though we want to watch multiple metrics here
    plst = list(param.items())
    
    test_error    = []
    test_falsepos = []
    test_falseneg = []
    scores        = np.zeros((2,len(label)))
    
    # get folds
    # we now make Nfolds fold cross-validation
    skf = StratifiedKFold(label, param['Nfolds'] , shuffle=True) # breakes the cross-validation sample to XX parts
    # break-up into different samples during the cross-validation stage
    for i, (train, test) in enumerate(skf):
        
        if param['debug']>0: print 'running fold {}'.format(i)
        if param['debug']>2: print train, test
        
        Xtrain = data[train]
        ytrain = label[train]
        wtrain = weight[train]
        Xtest  = data[test]
        ytest  = label[test]
        wtest  = weight[test]
        # make dmatrices from xgboost
        dtrain = xgb.DMatrix( Xtrain, label=ytrain, weight=wtrain , missing=np.nan)
        dtest  = xgb.DMatrix( Xtest, label=ytest, weight=wtest , missing=np.nan)
        #watchlist = [ (dtrain,'train') ]
        
        bst   = xgb.train(plst, dtrain, param['Ntrees'])
        ypred = bst.predict(dtest)
        fold_error,fold_falsepos,fold_falseneg = compute_stats(ytest,ypred)
        test_error.append(fold_error)
        test_falsepos.append(fold_falsepos)
        test_falseneg.append(fold_falseneg)
        scores[0,test] = ypred
        scores[1,test] = ytest
        
        if param['debug']>1: print 'test error: {}'.format(fold_error)
    
    return test_error,test_falsepos,test_falseneg,scores


def compute_stats(ytest,ypred):
    
    ydiff         = ypred - ytest
    fold_falsepos = float(len(np.where(ydiff > 0.75)[0]))/len(np.where(ytest == 0)[0])
    fold_falseneg = float(len(np.where(ydiff < -0.25)[0]))/len(np.where(ytest == 1)[0])
    fold_error    = float(len(np.where(ydiff > 0.75)[0])+len(np.where(ydiff < -0.25)[0]))/len(ytest)
    
    return fold_error,fold_falsepos,fold_falseneg







def make_bdt( data , label , weight , param ):
    
    # print weight statistics
    #print ('weight statistics: wpos=%g, wneg=%g, ratio=%g' % ( sum_wpos, sum_wneg, sum_wpos/sum_wneg))
    wp = len(np.where(label == 1)[0])
    wd = len(np.where(label == 0)[0])
    
    # you can directly throw param in, though we want to watch multiple metrics here
    #plst = list(param.items())+[('eval_metric', 'falsepos')]
    plst = list(param.items())
    
    # make dmatrices from xgboost
    dtrain = xgb.DMatrix( data, label=label, weight=weight , missing=np.nan )
    bst    = xgb.train(plst, dtrain, param['Ntrees'] )
    
    return bst





def plot_importances(Booster):
    
    importances = xgb.plot_importance(Booster)
    
    return importances
















