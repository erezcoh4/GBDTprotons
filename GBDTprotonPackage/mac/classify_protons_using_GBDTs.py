
from gbdt_tools import *
from uboone_tools import *

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


TrainingDataType        = 'MC_BNB'                              # options: 'openCOSMIC_MC' , 'MC_BNB'
NumberOfTrainingEvents  = 300000                                # 'openCOSMIC_MC': 200000 , 'MC_BNB': 300000
TracksListName          = "BNB_5e19POT"
GBDTmodelName           = "multi_BNB_TrainedOn_MCBNB_MCCOSMIC"  # options: 'BNB_TrainedOn_only_MC_BNB'
score                   = 0.9                                   # p_score = 0.0 for cosmics
maxscore                = 'muons'


feature_names = [
                 # geometry
                 # ----------------------
                 'nhits','length', 'distlenratio'
                 ,'theta','phi' # to be removed in another model...
                 ,'starty','startz','endy','endz'# to be removed in another model...
                 # calorimetry
                 # ----------------------
                 ,'startdqdx','enddqdx','dqdxdiff','dqdxratio','totaldqdx','averagedqdx'
                 # uboonecode tagging and PID
                 # ----------------------
                 ,'cosmicscore','coscontscore','pidpida','pidchi'
                 # optical information - unused for open cosmic MC
                 # ----------------------
                 ,'cfdistance'
                 #  necessary just for training...
                 # ----------------------
                 ,'MCpdgCode' , 'truth_KE'
                 ]


parameters = dict({
                  'evnts_frac':0.001,# events fraction to process
                  'debug':2, # prints out information during the processes
                  'Nskf':2, # 100
                  'scale_pos_weight':2., # Balancing of positive and negative weights.
                  'objective':'multi:softprob', # Specify the learning task and the corresponding learning objective or a custom objective function to be used
                  #  in previous rounds was'objective':'binary:logistic'
                  'eta':0.025, # Boosting learning rate
                  'eval_metric':'merror', # a custom evaluation metric
                  'silent':True, # Whether to print messages while running boosting
                  'nthread':60, # Number of parallel threads used to run xgboost.
                  'min_child_weight':4, # Minimum sum of instance weight(hessian) needed in a child.
                  'max_depth':13,# Maximum tree depth for base learners
                  'gamma':0.7, # Minimum loss reduction required to make a further partition on a leaf node of the tree.
                  'colsample_bytree':0.5, # Subsample ratio of columns when constructing each tree
                  'subsample':0.8, # Subsample ratio of the training instance
                  'num_class':5, #  If early stopping occurs...
                  'Ntrees':500,
                  'Nfolds':10,
                  'num_round':200
                  #         'reg_alpha':1e-5 # L1 regularization term on weights
                  })
# [http://xgboost.readthedocs.io/en/latest/python/python_api.html]


# -------------------------------------------------------------------
if flags.option=="divide training and testing samples" or 'divide' in flags.option:

    divide_training_and_testing_samples( TrainingDataType , NumberOfTrainingEvents )


# -------------------------------------------------------------------
if flags.option=="train GBDTs cross validation" or 'train' in flags.option:
    
    #    train_gbdt_cross_validation( TrainingDataType , NumberOfTrainingEvents )
    train_gbdt_MCBNB_and_CORSIKA(
                                 model_name='all_features_possible' ,
                                 feature_names=feature_names,
                                 data_type_arr=['MC_BNB','openCOSMIC_MC'] , nevents_train_arr=[300000,200000] ,
                                 parameters=parameters ,
                                 prompt_yesno=False
                                 )


# -------------------------------------------------------------------
if flags.option=="compute all GBDT multiscore for test sample" or 'test' in flags.option:
    print_important("compute all GBDT multiscore for test sample")
    # for BNB tracks classification - multi-class classifier:  muon , pion , proton , em (electron/photon)
    calc_all_gbdt_multiscores( TracksListName='testsample_87789_tracks_MC_BNB' , GBDTmodelName=GBDTmodelName , TracksListPath=main_path+'/TestSamples' )


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















