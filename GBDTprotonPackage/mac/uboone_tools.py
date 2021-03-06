import ROOT ,os, sys , math
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')


import input_flags ; flags = input_flags.get_args()
import Initiation as init
from ROOT import larlite
from larlite import *
from ROOT import TPlots
from my_tools import *

# --------------------------------------------------
#                       globals
# --------------------------------------------------
debug = flags.verbose
MCCversion = "MCC%d"%flags.MCCversion

# --------------------------------------------------
#                       paths
# --------------------------------------------------

# main paths
if "erez" in flags.worker or "helion" in flags.worker:

    import pylab , csv , numpy as np, pandas as pd
    import matplotlib.pyplot as plt, matplotlib.ticker as ticker
    import boost_cosmic , predict_cosmic, predict_multi , boost_multiscore
    from prompter import yesno
    from xgboost import plot_importance
    import operator
    import csv


if flags.worker=="erez":
    path = "/Users/erezcohen/Desktop/uBoone"
    main_path       = path + "/AnalysisTreesAna"
    lists_path      = path + "/Lists"
    data_files_path = path + "/DATA"
    ana_files_path  = path + "/analysis/AnaFiles"
    ccqe_candidates_path= path + "/analysis/ccqe_candidates"


elif flags.worker=="helion":
    app_path  = "/extra/Erez/uBoone"
    main_path       = app_path + "/AnalysisTreesAna"
    data_path = app_path
    lists_path      = data_path + "/Lists"
    data_files_path = data_path + "/DATA"
    ana_files_path  = data_path + "/analysis/AnaFiles"



elif flags.worker=="uboone":
    app_path  = "/uboone/app/users/ecohen"
    main_path       = app_path + "/AnalysisTreesAna"
    data_path = "/uboone/data/users/ecohen"
    lists_path      = data_path + "/Lists"
    data_files_path = data_path + "/DATA"
    ana_files_path  = data_path + "/analysis/AnaFiles"
    
    import csv




# analysis trees
anatrees_lists_path = "/pnfs/uboone/persistent/users/aschu/devel/v05_11_01/hadd"
anatrees_data_path  = "/uboone/data/users/ecohen/AnalysisTreeData"

# my analysis files
eventsfiles_path    = main_path + "/TracksAnaFiles"
featuresfiles_path  = main_path + "/FeaturesFiles"
rois_path           = main_path + "/ROIs"


# gdbts
GBDTmodels_path         = main_path + "/GBDTmodels"
GBDTprotonsLists_path   = main_path + "/PassedGBDTFiles"


def Classified_protons_path( GBDTmodelName ):
    return  GBDTprotonsLists_path + "/" + GBDTmodelName
# --------------------------------------------------



