import ROOT ,os, sys , math
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/protonid')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/protonid')


import pylab
import numpy as np
import input_flags ; flags = input_flags.get_args()
import Initiation as init
from my_tools import *




# paths
# -------------------------
if flags.worker=="erez":
    
    main_path = "/Users/erezcohen/Desktop/uBoone/AnalysisTreesAna"
    lists_path = "/Users/erezcohen/Desktop/uBoone/Lists"
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import boost_cosmic
    import predict_cosmic

elif flags.worker=="uboone":
    
    main_path = "/uboone/app/users/ecohen/AnalysisTreesAna"
    lists_path = "uboone/app/users/ecohen/Lists"


anatrees_lists_path = "/pnfs/uboone/persistent/users/aschu/devel/v05_11_01/hadd"
anatrees_data_path = "/uboone/data/users/ecohen/AnalysisTreeData"