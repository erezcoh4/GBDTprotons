'''
    useful tools for GBDT analysis
'''
from uboone_tools import *


# The features that we want to use for the GBDT
# -------------------------
feature_names = [ # geometry
                 'nhits','length','starty','startz','endy','endz','theta','phi', 'distlenratio'
                 # calorimetry
                 ,'startdqdx','enddqdx','dqdxdiff','dqdxratio','totaldqdx','averagedqdx'
                 # uboonecode tagging and PID
                 ,'cosmicscore','coscontscore','pidpida','pidchi'
                 # optical information - unused for open cosmic MC
                 ,'cfdistance'
                 ]

features_scores_roi = [
                       'run','subrun','event','trackid'
                       ,'U_start_wire','U_start_time','U_end_wire','U_end_time'
                       ,'V_start_wire','V_start_time','V_end_wire','V_end_time'
                       ,'Y_start_wire','Y_start_time','Y_end_wire','Y_end_time'
                       ,'p_score'
                       ]

features_only_scores = [
                        'run','subrun','event','trackid','p_score'
                        ]



# paths
# -------------------------
GBDTmodels_path         = main_path + "/GBDTmodels"
GBDTprotonsLists_path   = main_path + "/PassedGBDTFiles"







# lists and names
# -------------------------
def GBDTprotonsRSElistName( DataListName , GBDTmodelName , p_score ):
    
    classification_name = DataListName + "_" + GBDTmodelName
    classified_protons_list_path = GBDTprotonsLists_path + "/" + classification_name
    classified_protons_list_name = "passedGBDT_" + classification_name + "_score_%.2f_just_events.csv"%p_score
    return classified_protons_list_path + "/" + classified_protons_list_name




