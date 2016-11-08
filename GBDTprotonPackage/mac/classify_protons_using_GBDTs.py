from gbdt_tools import *
'''
    usage:
    --------
    python mac/classify_protons_using_GBDTs.py --option=divide
    
    options: 
        divide      { "divide training and testing samples" }
        train       { "train GBDTs cross validation" }
        scores      { "compute all GBDT p-scores" }
        select      { "select GBDT protons" }
'''


TrainingDataType        = "MC_BNB"
NumberOfTrainingEvents  = 300000
TracksListName          = "BNB_5e19POT"
GBDTmodelName           = "BNB_TrainedOn_only_MC_BNB"
p_score                 = 0.99





# -------------------------------------------------------------------
if flags.option=="divide training and testing samples" or 'divide' in flags.option:

    divide_training_and_testing_samples( TrainingDataType , NumberOfTrainingEvents )


# -------------------------------------------------------------------
if flags.option=="train GBDTs cross validation" or 'train' in flags.option:
    
    train_gbdt_cross_validation( TrainingDataType , NumberOfTrainingEvents )


# -------------------------------------------------------------------
if flags.option=="compute all GBDT p-scores" or 'scores' in flags.option:

    calc_all_gbdt_scores( TracksListName , GBDTmodelName )



# -------------------------------------------------------------------
if flags.option=="select GBDT protons" or 'select' in flags.option:
    
    select_gbdt_protons( TracksListName , GBDTmodelName , p_score )

