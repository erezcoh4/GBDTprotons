import ROOT ,os, sys , math
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')


import input_flags ; flags = input_flags.get_args()
import Initiation as init
from ROOT import larlite
from larlite import *
from ROOT import TPlots
from my_tools import *



# --------------------------------------------------
#                       paths
# --------------------------------------------------

# main paths
if flags.worker=="erez":
    
    main_path = "/Users/erezcohen/Desktop/uBoone/AnalysisTreesAna"
    lists_path = "/Users/erezcohen/Desktop/uBoone/Lists"
    import pylab
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import boost_cosmic , predict_cosmic
    import predict_multi

elif flags.worker=="uboone":
    import csv
    main_path = "/uboone/app/users/ecohen/AnalysisTreesAna"
    lists_path = "/uboone/data/users/ecohen/Lists"


# larlite files
data_files_path = "/uboone/data/users/ecohen/DATA"

# analysis trees
anatrees_lists_path = "/pnfs/uboone/persistent/users/aschu/devel/v05_11_01/hadd"
anatrees_data_path  = "/uboone/data/users/ecohen/AnalysisTreeData"

# my analysis files
anafiles_path       = main_path + "/TracksAnaFiles"
featuresfiles_path  = main_path + "/FeaturesFiles"
rois_path           = main_path + "/ROIs"

# gdbts
GBDTmodels_path         = main_path + "/GBDTmodels"
GBDTprotonsLists_path   = main_path + "/PassedGBDTFiles"


def Classified_protons_path( GBDTmodelName ):
    return  GBDTprotonsLists_path + "/" + GBDTmodelName
# --------------------------------------------------



