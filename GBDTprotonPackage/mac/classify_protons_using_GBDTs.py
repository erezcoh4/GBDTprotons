
from gbdt_tools import *
'''
    usage:
    --------
    python mac/classify_protons_using_GBDTs.py --option=divide
    
    options: 
        divide      { "divide training and testing samples" }
        train       { "train GBDTs cross validation" }
        scores      { "compute all GBDT p-scores" (for cosmic data) }
        multiscores { "compute all GBDT multiscores" }
        select      { "select GBDT protons" }
'''


TrainingDataType        = 'openCOSMIC_MC'                       # options: 'openCOSMIC_MC' , 'MC_BNB'
NumberOfTrainingEvents  = 200000                                # 'openCOSMIC_MC': 200000 , 'MC_BNB': 300000
TracksListName          = "BNB_5e19POT"
GBDTmodelName           = "multi_BNB_TrainedOn_MCBNB_MCCOSMIC"  # options: 'BNB_TrainedOn_only_MC_BNB'
score                   = 0.9                                   # p_score = 0.0 for cosmics
maxscore                = 'muons'

parameters = {  'debug':flags.verbose,
                'objective':'binary:logistic' ,
                'eta':0.025 ,
                'eval_metric':'error',
                'silent':1,
                'nthread':6,
                'min_child_weight':4,
                'max_depth':13,
                'gamma':0.7,
                'colsample_bytree':0.5,
                'subsample':0.8,
                'num_class':5,
                'Ntrees':500,
                'Nfolds':10,
#                'reg_alpha':1e-5
                }


# -------------------------------------------------------------------
if flags.option=="divide training and testing samples" or 'divide' in flags.option:

    divide_training_and_testing_samples( TrainingDataType , NumberOfTrainingEvents )


# -------------------------------------------------------------------
if flags.option=="train GBDTs cross validation" or 'train' in flags.option:
    
    #    train_gbdt_cross_validation( TrainingDataType , NumberOfTrainingEvents )
    train_gbdt_MCBNB_and_CORSIKA( data_type_arr=['MC_BNB','openCOSMIC_MC'] , nevents_train_arr=[300000,200000] , parameters=parameters )


# -------------------------------------------------------------------
if flags.option=="compute all GBDT p-scores" or 'p-scores' in flags.option:
    # for cosmic tracks classification - single-class classifier
    calc_all_gbdt_scores( TracksListName , GBDTmodelName )


# -------------------------------------------------------------------
if flags.option=="compute all GBDT multiscore" or 'multiscore' in flags.option:
    # for BNB tracks classification - multi-class classifier:  muon , pion , proton , em (electron/photon)
    calc_all_gbdt_multiscores( TracksListName , GBDTmodelName )


# -------------------------------------------------------------------
if flags.option=="select GBDT protons" or 'select' in flags.option:
    
    #    select_gbdt_protons( TracksListName , GBDTmodelName , p_score )
    select_analysistrees_to_gbdt_class( TracksListName , GBDTmodelName , maxscore=maxscore, score = score )



# -------------------------------------------------------------------
if flags.option=="filter AnalysisTrees data file to selected class" or 'filter' in flags.option:
    
    filter_analysistrees_to_gbdt_class( TracksListName , GBDTmodelName , maxscore=maxscore, score = score )















