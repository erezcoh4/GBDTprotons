
import sys, pandas as pd, numpy as np, matplotlib.pyplot as plt, ast
import matplotlib.pyplot as plt, matplotlib as mpl , seaborn as sns; sns.set(style="white", color_codes=True , font_scale=1)
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
from prompter import yesno


sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/mac')

sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/GBDTprotons/GBDTprotonPackage/boost')
sys.path.insert(0, '/home/erez/larlite/UserDev/GBDTprotons/GBDTprotonPackage/mac')



import GeneralPlot as gp , Initiation as init
import predict_multi
from plot_tools import *
from my_tools import *
from calc_tools import *
import boost_multiscore
#from uboone_tools import *

from matplotlib.colors import LogNorm

generic = lambda x: ast.literal_eval(x)

path = "/Users/erezcohen/Desktop/uBoone"
main_path       = path + "/AnalysisTreesAna"
lists_path      = path + "/Lists"
data_files_path = path + "/DATA"
ana_files_path  = path + "/analysis/AnaFiles"
GBDTprotonsLists_path = main_path + "/PassedGBDTFiles"
features_path         = main_path + "/FeaturesFiles/"

# ----------------------------------------------------------------------
def Classified_protons_path( GBDTmodelName ):
    return  GBDTprotonsLists_path + "/" + GBDTmodelName
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
def GBDTprotonsListName( GBDTmodelName , DataListName , p_score = 0 , ListFeatures = 'rse' ):
    
    classification_name = DataListName + "_" + GBDTmodelName
    classified_protons_list_path = Classified_protons_path(GBDTmodelName)
    classified_protons_list_name = "passedGBDT_" + classification_name
    
    if p_score == 0:
        classified_protons_list_full_name = classified_protons_list_name + "_allscores"
    else:
        classified_protons_list_full_name = classified_protons_list_name + "_pscore_%.2f"%p_score
    
    classified_protons_list_full_name = classified_protons_list_full_name + "_" + ListFeatures

    return classified_protons_list_path + "/" + classified_protons_list_full_name + ".csv"
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
def efficiency_1d(gen_protons=None,
                  rec_protons=None,
                  x_label='momentum [GeV/c]',
                  bins=np.linspace(0,2,30) ,
                  figsize=(10,10),
                  fontsize=20,
                  legend_loc='best'):
    
    if gen_protons is None or rec_protons is None:
        print 'I need to get gen_protons and rec_protons (pandas.DataFrame[var])'
        print "for instance gen_protons=MC_gen_protons['P'], rec_protons=MC_rec_protons['truth_P']"
        print 'exiting...'
        exit(0)
    
    x = [bins[i] for i in range(len(bins)-1)]
    
    fig = plt.figure(figsize=figsize)
    ax=fig.add_subplot(211)
    h_gen,edges=np.histogram(gen_protons,bins=bins)
    h_gen_err = np.sqrt(h_gen)
    h_rec,edges=np.histogram(rec_protons,bins=bins)
    h_rec_err = np.sqrt(h_rec)
    plt.errorbar(x, h_gen, yerr=h_gen_err, fmt='o',markersize=4,label='generated')
    plt.errorbar(x, h_rec, yerr=h_rec_err, fmt='s',markersize=4,label='reconstructed')
    
    plt.legend(fontsize=fontsize,loc=legend_loc)
    set_axes(ax,'','')
    ax.xaxis.set_major_formatter( NullFormatter() )
    acceptance = [float(h_rec[i])/h_gen[i] if h_gen[i]>0 else 0 for i in range(len(h_gen))]
    acceptance_err = [sqrt(1./h_rec[i]+1./h_gen[i]) if h_gen[i]>50 and h_rec[i]>50 else 0 for i in range(len(h_gen))]
    
    ax=fig.add_subplot(212)
    plt.errorbar(x, acceptance, yerr=acceptance_err, fmt='o',label='Reconstructed proton tracks')
    plt.plot(x,acceptance,color='r',marker='s')
    ax.set_ylim(0,np.max([1.,1.2*np.max(acceptance+acceptance_err)]))
    set_axes(ax,x_label,'fraction of generated protons')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    return ax , x, acceptance , acceptance_err
# ----------------------------------------------------------------------

## ----------------------------------------------------------------------
#def acceptace_2d( vx='theta' , vy='phi',
#                 x_label='$\\theta$ [rad.]',y_label='$\\phi$ [rad.]',
#                 binsx=np.linspace(0,3.4,30) , binsy=np.linspace(-3.4,3.4,30),
#                 figsize=(10,10),fontsize=20,
#                 legend_loc='lower left',
#                 norm=LogNorm()):
#    x = [binsx[i] for i in range(len(binsx)-1)]
#    y = [binsy[i] for i in range(len(binsy)-1)]
#    
#    fig = plt.figure(figsize=(12,4))
#    ax = fig.add_subplot(131)
#    h_gen,xedges,yedges = np.histogram2d(MC_gen_protons[vx],MC_gen_protons[vy],bins=[binsx,binsy])
#    h_rec,xedges,yedges = np.histogram2d(MC_rec_protons['truth_'+vx],MC_rec_protons['truth_'+vy],bins=[binsx,binsy])
#    plt.scatter(MC_gen_protons[vx],MC_gen_protons[vy],s=7,color='black',label='generated')
#    plt.scatter(MC_rec_protons['truth_'+vx],MC_rec_protons['truth_'+vy],s=4,color='green',label='reconstructed')
#    ax = fig.add_subplot(132)
#    plt.hist2d(MC_gen_protons[vx],MC_gen_protons[vy],bins=[binsx,binsy],cmap='gray_r')
#    ax.set_title('generated')
#    plt.colorbar()
#    ax = fig.add_subplot(133)
#    plt.hist2d(MC_rec_protons['truth_'+vx],MC_rec_protons['truth_'+vy],bins=[binsx,binsy],cmap='Greens')
#    ax.set_title('reconstructed')
#    plt.colorbar()
# ----------------------------------------------------------------------

