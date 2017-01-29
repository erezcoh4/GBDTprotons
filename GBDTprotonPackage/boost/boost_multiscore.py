#!/usr/bin/python
# this is the example script to use xgboost to train
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import StratifiedKFold

# -------------------------------------------------------------------
def load_data(  bnb_mc_filename, corsika_mc_filename
              , KE_min=0.04 #  take only protons with kinetic energy > 40 MeV (momentum 277 MeV/c); Katherine takes 40 MeV (277 MeV/c)
              , debug=0
              , feature_names=None
              , tracks_frac=1
              ):

    mc_bnb_tracks = pd.read_csv(bnb_mc_filename , usecols=feature_names)
    mc_bnb_tracks = mc_bnb_tracks[0:int(tracks_frac*len(mc_bnb_tracks))] # take only a fraction of the tracks for small-scale training on my machine
    
    mc_bnb_protons  = mc_bnb_tracks[(mc_bnb_tracks.MCpdgCode==2212) & (mc_bnb_tracks.truth_KE>=KE_min)][feature_names]
    mc_bnb_pions    = mc_bnb_tracks[(mc_bnb_tracks.MCpdgCode==211) | (mc_bnb_tracks.MCpdgCode==-211) | (mc_bnb_tracks.MCpdgCode==111)][feature_names]
    mc_bnb_em       = mc_bnb_tracks[(mc_bnb_tracks.MCpdgCode==11) | (mc_bnb_tracks.MCpdgCode==-11) | (mc_bnb_tracks.MCpdgCode==22)][feature_names]
    mc_bnb_muons    = mc_bnb_tracks[(mc_bnb_tracks.MCpdgCode==13) | (mc_bnb_tracks.MCpdgCode==-13)][feature_names]

    corsika_mc_tracks = pd.read_csv(corsika_mc_filename , usecols=feature_names)
    corsika_mc_tracks = corsika_mc_tracks[0:int(tracks_frac*len(corsika_mc_tracks))] # take only a fraction of the tracks for small-scale training on my machine
    
    corsika_mc_tracks = corsika_mc_tracks[feature_names]
    
    if debug>1:
        print 'took only a fraction of',tracks_frac,'of tracks from MC-BNB and CORSIKA samples:'
        print len(mc_bnb_protons),'protons,',len(mc_bnb_pions),'pions,',len(mc_bnb_muons),'muons,',len(mc_bnb_em),'em'
        print len(corsika_mc_tracks),'cosmic tracks'


    # make training array
    x_protons   = np.array(mc_bnb_protons)
    x_muons     = np.array(mc_bnb_muons)
    x_pions     = np.array(mc_bnb_pions)
    x_em        = np.array(mc_bnb_em)
    x_cosmic    = np.array(corsika_mc_tracks)
    data        = np.vstack([x_protons,x_muons,x_pions,x_em,x_cosmic])
    if debug>2: print 'data:',data


    # make class labels
    y_protons   = np.zeros(len(x_protons))
    y_muons     = np.ones(len(x_muons))
    y_pions     = np.ones(len(x_pions))*2
    y_em        = np.ones(len(x_em))*3
    y_cosmics   = np.ones(len(x_cosmic))*4
    label       = np.hstack([y_protons,y_muons,y_pions,y_em,y_cosmics])
    if debug>2: print 'label:',label


    # make weights
    w_protons   = np.ones(len(y_protons))   * 1.
    w_muons     = np.ones(len(y_muons))     * np.true_divide(len(y_protons),len(y_muons)) # true_divide Returns a true division of the inputs, element-wise.
    w_pions     = np.ones(len(y_pions))     * np.true_divide(len(y_protons),len(y_pions))
    w_em        = np.ones(len(y_em))        * np.true_divide(len(y_protons),len(y_em))
    w_cosmics   = np.ones(len(y_cosmics))   * np.true_divide(len(y_protons),len(y_cosmics))
    weight      = np.hstack([w_protons,w_muons,w_pions,w_em,w_cosmics])
    if debug>2: print 'weight:',weight

    return data,label,weight
# -------------------------------------------------------------------


# -------------------------------------------------------------------
def run_cv( data , label , weight , parameters , Nskf=10):
    
    # use logistic regression loss, use raw prediction before logistic transformation
    # since we only need the rank
    # cosmic data parameters
    parameters['objective']     = 'multi:softprob'
    parameters['eval_metric']   = 'merror'
    # you can directly throw param in, though we want to watch multiple metrics here
    plst  = list(parameters.items())+[('eval_metric', 'mlogloss')]
    
    test_error  , test_falsepos , test_falseneg = [] , [] , []
    scores      = np.zeros((6,len(label)))
    
    # get folds
    skf = StratifiedKFold(label, Nskf, shuffle=True)
    if parameters['debug']>1: print 'enumerate(skf):', enumerate(skf)
    
    for i, (train, test) in enumerate(skf):
        print 'On fold {}'.format(i)
        #print train, test
        Xtrain = data[train]
        ytrain = label[train]
        wtrain = label[train]
        Xtest  = data[test]
        ytest  = label[test]
        wtest  = label[test]
        # make dmatrices from xgboost
        dtrain = xgb.DMatrix( Xtrain, label=ytrain, weight=weight , missing=np.nan )
        dtest  = xgb.DMatrix( Xtest , missing=np.nan )
        
        bst   = xgb.train(plst, dtrain, parameters['num_round'])
        ypred = bst.predict(dtest)
        fold_error,fold_falsepos,fold_falseneg = compute_stats(ytest,ypred)
        test_error.append(fold_error)
        test_falsepos.append(fold_falsepos)
        test_falseneg.append(fold_falseneg)
        
        # 5 classes - 5 scores
        for i in range(5):
            scores[i,test] = ypred[:,i]
        scores[5,test] = ytest
    
    return test_error,test_falsepos,test_falseneg,scores
# -------------------------------------------------------------------




# -------------------------------------------------------------------
def parameter_opt( data , label , weight , parameters):

    dtrain = xgb.DMatrix(data,label=label,missing=np.nan)

    '''
    scale_pos_weights = [0.5,0.75,1.25]
    for spw in scale_pos_weights:
        param['scale_pos_weight'] = spw
        plst = list(param.items())+[('eval_metric', 'falsepos')]
        results = xgb.cv(param,dtrain,num_boost_round=num_round,nfold=10,stratified=True)
        print 'scale_pos_weight: ',spw,', test-error-mean: ',np.array(results['test-error-mean'])[-1],', test-error-std: ',np.array(results['test-error-std'])[-1]

    return
    '''
    results = xgb.cv( parameters , dtrain ,
                     num_boost_round=parameters['num_round'],
                     nfold=parameters['Nfolds'] ,
                     stratified=True )
    return results
# -------------------------------------------------------------------




# -------------------------------------------------------------------
def compute_stats(ytest,ypred):
  
    yscore        = ypred[:,0]
    fold_falsepos = float(len(np.where((yscore > 0.75) & (ytest != 0))[0]))/len(np.where(ytest != 0)[0])
    fold_falseneg = float(len(np.where((yscore < 0.75) & (ytest == 0))[0]))/len(np.where(ytest == 0)[0])
    fold_error    = float(fold_falsepos*len(np.where(ytest != 0)[0]) + fold_falseneg*len(np.where(ytest == 0)[0]))/len(ytest)

    return fold_error,fold_falsepos,fold_falseneg
# -------------------------------------------------------------------


# -------------------------------------------------------------------
def make_bdt( data , label , weight , parameters):

    # you can directly throw param in, though we want to watch multiple metrics here
    plst = list(parameters.items())+[('eval_metric', 'mlogloss')]

    # make dmatrices from xgboost
    dtrain = xgb.DMatrix( data, label=label, weight=weight , missing=np.nan)
    bst    = xgb.train(plst, dtrain, parameters['num_round'])
        
    return bst
# -------------------------------------------------------------------

