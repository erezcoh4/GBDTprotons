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

features_scores_rse = [
                        'run','subrun','event','trackid','p_score'
                        ]

features_scores_roi = [
                       'run','subrun','event','trackid'
                       ,'U_start_wire','U_start_time','U_end_wire','U_end_time'
                       ,'V_start_wire','V_start_time','V_end_wire','V_end_time'
                       ,'Y_start_wire','Y_start_time','Y_end_wire','Y_end_time'
                       ,'p_score'
                       ]






# paths
# -------------------------
GBDTmodels_path         = main_path + "/GBDTmodels"
GBDTprotonsLists_path   = main_path + "/PassedGBDTFiles"
def Classified_protons_path( GBDTmodelName ):
    return  GBDTprotonsLists_path + "/" + GBDTmodelName










# lists and names
# -------------------------
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



# -------------------------
def FeaturesFileName( FileType ):
    
    return main_path + "/FeaturesFiles/features_" + FileType + "_AnalysisTrees.csv"


# -------------------------
def TrainingSampleFileName( FileTypeToDivide , NumberOfEventsToTrain ):
    
    return main_path + "/TrainingSamples/trainsample_%d_tracks_"%NumberOfEventsToTrain + FileTypeToDivide + ".csv"

# -------------------------
def TestSampleFileName( FileTypeToDivide , NumberOfEventsToTest ):
    
    return main_path + "/TestSamples/testsample_%d_tracks_"%NumberOfEventsToTest + FileTypeToDivide + ".csv"


# -------------------------
def GBDTtreeName( GBDTmodelName ):
    return GBDTmodels_path + "/" + GBDTmodelName + ".bst"


# methods
# -------------------------
def divide_training_and_testing_samples( FileTypeToDivide , NumberOfEventsToTrain ):
    # FileTypeToDivide: MC_BNB , openCOSMIC_MC
    import random
    
    data = pd.read_csv( FeaturesFileName( FileTypeToDivide ) )
    Total = len(data)
    TrainFileName = TrainingSampleFileName( FileTypeToDivide , NumberOfEventsToTrain )
    TestFileName = TestSampleFileName( FileTypeToDivide , Total - NumberOfEventsToTrain )

    rows         = random.sample( data.index, NumberOfEventsToTrain )
    data_train   = data.ix[rows]
    data_test    = data.drop(rows)

    data_train.to_csv( TrainFileName , index=False )
    data_test.to_csv( TestFileName , index=False )
    
    if (flags.verbose):
        print_filename( TrainFileName , "divided into training sample with %d tracks:"%NumberOfEventsToTrain)
        print_filename( TestFileName , "test sample with %d tracks:"%(Total - NumberOfEventsToTrain))





# -------------------------
def train_gbdt_cross_validation( FileTypeToDivide , NumberOfEventsToTrain ):
    
    #ToDo: This needs work! i stopped working on this since i have to move to muon-proton vertex...
    
    import boost_cosmic
    import predict_cosmic

    TrainFileName = TrainingSampleFileName( FileTypeToDivide , NumberOfEventsToTrain )

    param = {}
    param['debug']              = flags.verbose     # just for monitoring....
    '''
    use logistic regression loss, use raw prediction before logistic transformation
    since we only need the rank cosmic data parameters
    '''
    param['objective']          = 'binary:logistic'
    param['eta']                = 0.025
    param['eval_metric']        = 'error'
    param['silent']             = 1
    param['nthread']            = 6
    param['min_child_weight']   = 4
    param['max_depth']          = 13
    param['gamma']              = 0.7
    param['colsample_bytree']   = 0.5    # Kat: 0.5
    param['subsample']          = 0.8
    param['Ntrees']             = 500    # Kat: 500
    param['Nfolds']             = 10     # Kat: 10
    #param['reg_alpha']         = 1e-5

    DoCrossValidation = yesno('cross validate?')


    # (A) load the data
    # ---------------------------------------
    data,label,weight = boost_cosmic.load_data( TrainingSampleName , feature_names )


    if flags.verbose:
        print "data: \n",data
        print "label: \n",label
        print "weight: \n",weight



    # (B) cross-validation step
    # ---------------------------------------
    if DoCrossValidation:
        test_error,test_falsepos,test_falseneg,scores = boost_cosmic.run_cv( data , label , weight , param )
        
        if flags.verbose:
            print "test_error: \n",test_error
            print "test_falsepos: \n",test_falsepos
            print "test_falseneg: \n",test_falseneg
            print "scores: \n",scores

        # (C) check if errors are stable
        # ---------------------------------------
        plt.figure()
        plt.hist( test_error )
        plt.title("test errors")
        plt.xlabel("error")
        plt.ylabel("Frequency")
        plt.savefig( model_path + "/test_errors_" + ModelName + ".pdf" )
        plt.show()

        DoContinue = yesno('build model?')

    if DoCrossValidation == False: DoContinue = True
    # (D) build the GBDTs which is training on the entire
    # training sample, with no boot-strapping
    # ---------------------------------------
    if DoContinue:
    
        BoostedTree = boost_cosmic.make_bdt( data , label , weight , param )
        BoostedTree.save_model( model_path + "/" + ModelName + ".bst")
    
        if flags.verbose:
            print "done"
            print "BoostedTree: \n",BoostedTree
            print "now use the test sample and test this"




    # plot the importances...
    importances_fig = boost_cosmic.plot_importances(BoostedTree).figure
    importances_fig.savefig( model_path + "/importances_" + ModelName + ".pdf" )
    importances_fig.show()



    file = open ( model_path + "/README_" + ModelName   , "wb" )

    string = "\nGBDT modeling \n--------------------- \n"
    string+= ("built the model to \n " + model_path + "/" + ModelName + ".bst") if DoContinue else "did not built the model..."
    string+= "\n%4d-%02d-%02d"       %time.localtime()[0:3]
    string+= "\n--------------------- \n"
    string+= "\nmodel: "             +ModelName
    string+= "\nobjective: "         +param['objective']
    string+= "\neta: "               +str(param['eta'])
    string+= "\neval_metric: "       +str(param['eval_metric'])
    string+= "\nsilent: "            +str(param['silent'])
    string+= "\nnthread: "           +str(param['nthread'])
    string+= "\nmin_child_weight: "  +str(param['min_child_weight'])
    string+= "\nmax_depth: "         +str(param['max_depth'])
    string+= "\ngamma: "             +str(param['gamma'])
    string+= "\ncolsample_bytree: "  +str(param['colsample_bytree'])
    string+= "\nsubsample: "         +str(param['subsample'])
    string+= "\nNtrees: "            +str(param['Ntrees'])
    string+= "\nNfolds: "            +str(param['Nfolds'])
    string+= "\n--------------------- \n"
    if DoCrossValidation:
        string+= "\terrors:\n"
        string+= str(test_error[:])
        string+= "\n--------------------- \n"
        string+= "false-positive: \n"
        string+=  str(test_falsepos[:])
        string+= "\n--------------------- \n"
        string+= "false-negative: \n"
        string+=  str(test_falseneg[:])
    string+= "\n--------------------- \n"

    file.write(string)

    print "done,"

    if DoContinue:
        print "built the model to \n" + model_path + "/" + ModelName + ".bst"
    else:
        print "did not built the model"

    print "see \n" + model_path + "/README_" + ModelName
    print "and \n" + model_path + "/importances_" + ModelName + ".pdf"




# -------------------------
def calc_all_gbdt_scores( TracksListName , GBDTmodelName ):
    SampleFileName = FeaturesFileName( TracksListName )
    if flags.verbose: print_filename( SampleFileName , "loading data from" )

    # create a directory for the BDT model
    init.generate_directory( Classified_protons_path(GBDTmodelName) )
    tracks_data = pd.read_csv( SampleFileName )
    if flags.verbose: print "loaded %d tracks"%len(tracks_data)
    tracks_scores = predict_cosmic.predict_data( tracks_data , GBDTtreeName( GBDTmodelName ) , feature_names )

    # stream into output files
    # all features + scores
    allfeatures_filename = GBDTprotonsListName( GBDTmodelName, TracksListName, 0,'features')
    tracks_scores.to_csv( allfeatures_filename , header=True )
    print_filename( allfeatures_filename , "csv file of all features:" )





# -------------------------
def select_gbdt_protons( TracksListName , GBDTmodelName , p_score = 0.99 ):


    tracks = pd.read_csv( GBDTprotonsListName( GBDTmodelName, TracksListName, 0,'features') )
    if flags.verbose: print "loaded %d tracks "%len(tracks)
    
    PassedGBDTFileRSEName = GBDTprotonsListName( GBDTmodelName, TracksListName, p_score ,'rse')
    PassedGBDTFileROIName = GBDTprotonsListName( GBDTmodelName, TracksListName, p_score ,'ROIs')


    tracks_selected = tracks[ tracks.p_score > p_score ]
    purity = float( len( tracks_selected ) )/len( tracks )
    if flags.verbose: print "purity for score %.2f is %.4f (left w/ %d tracks out of %d)"%(p_score,purity,len(tracks_selected),len(tracks))


    # now dump the run and event number to csv to use as input to larsoft filter
    # use only the relevant variables (the ones that we actually need for later)
    tracks_selected[ features_scores_rse ].to_csv( PassedGBDTFileRSEName , sep=' ' , header=False , index=False )
    tracks_selected[ features_scores_roi ].to_csv( PassedGBDTFileROIName , sep=' ' , header=True , index=False )
    print_filename( PassedGBDTFileRSEName , "only R/S/E & scores written to file" )
    print_filename( PassedGBDTFileROIName , "R/S/E, ROIs and scores written to file" )





