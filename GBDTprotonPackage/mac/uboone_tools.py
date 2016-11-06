import ROOT ,os, sys , math
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/uboone/app/users/ecohen/larlite/UserDev/protonid')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/protonid')


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pylab
import numpy as np
import input_flags
import boost_cosmic
import predict_cosmic
from my_tools import *


# paths
# -------------------------
if flags.worker=="erez":
    
    main_path           = "/Users/erezcohen/Desktop/uBoone/AnalysisTreesAna"
    import pandas as pd

elif flags.worker=="uboone":
    
    main_path           = "/uboone/app/users/ecohen/AnalysisTreesAna"

