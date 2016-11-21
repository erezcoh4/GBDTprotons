'''
    useful tools for GBDT analysis
'''
from uboone_tools import *
from ROOT import GBDTanalysis


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
                       'run','subrun','event','trackid'
                       ,'mscore_p'    ,'mscore_mu'  ,'mscore_pi'    ,'mscore_em'    ,'mscore_cos'
                       ,'mscore_max'
                       ]

features_scores_roi = [
                       'run','subrun','event','trackid'
                       ,'U_start_wire','U_start_time','U_end_wire','U_end_time'
                       ,'V_start_wire','V_start_time','V_end_wire','V_end_time'
                       ,'Y_start_wire','Y_start_time','Y_end_wire','Y_end_time'
                       ,'mscore_p'    ,'mscore_mu'  ,'mscore_pi'    ,'mscore_em'    ,'mscore_cos'
                       ,'mscore_max'
                       ]


features_multiscores_roi = [
                            'run'           ,'subrun'       ,'event'        ,'trackid'
                            ,'U_start_wire' ,'U_start_time' ,'U_end_wire'   ,'U_end_time'
                            ,'V_start_wire' ,'V_start_time' ,'V_end_wire'   ,'V_end_time'
                            ,'Y_start_wire' ,'Y_start_time' ,'Y_end_wire'   ,'Y_end_time'
                            ,'mscore_p'    ,'mscore_mu'  ,'mscore_pi'    ,'mscore_em'    ,'mscore_cos'
                            ,'mscore_max'
                            ]










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
def GBDTclassListName( GBDTmodelName, DataListName, maxscore='protons' , score=0 ,ListFeatures = 'rse'):
    
    classification_name = DataListName + "_" + GBDTmodelName
    classified_list_path = Classified_protons_path(GBDTmodelName)
    classified_list_name = "passedGBDT_" + classification_name + "_maxscored_" + maxscore
    
    if score == 0:
        classified_list_full_name = classified_list_name + "_allscores"
    else:
        classified_list_full_name = classified_list_name + "_score_%.2f"%score
    
    classified_list_full_name = classified_list_full_name + "_" + ListFeatures

    return classified_list_path + "/" + classified_list_full_name + ".csv"

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
    allfeatures_filename = GBDTprotonsListName( GBDTmodelName, TracksListName, 0,'features_and_scores')
    tracks_scores.to_csv( allfeatures_filename , header=True )
    print_filename( allfeatures_filename , "csv file of all features:" )




# -------------------------
def calc_all_gbdt_multiscores( TracksListName , GBDTmodelName ):
    if flags.verbose: print_important( 'calc all gbdt multiscores' )
    SampleFileName = FeaturesFileName( TracksListName )
    if flags.verbose: print_filename( SampleFileName , "loading data from" )
    
    # create a directory for the results of classifying from this GBDT model
    init.generate_directory( Classified_protons_path(GBDTmodelName) )
    tracks_data = pd.read_csv( SampleFileName )
    if flags.verbose: print "loaded %d tracks"%len(tracks_data)
    tracks_scores = predict_multi.predict_multiscore( tracks_data , GBDTtreeName( GBDTmodelName ) , feature_names )
    if flags.verbose: print "predicted on the %d tracks"%len(tracks_data)

    # stream into output files
    # all features + scores
    allfeatures_filename = GBDTprotonsListName( GBDTmodelName, TracksListName, 0 , 'features_and_scores' )
    tracks_scores.to_csv( allfeatures_filename , header=True )
    print_filename( allfeatures_filename , "wrote csv file of all features and scores:" )




# -------------------------
def select_gbdt_protons( TracksListName , GBDTmodelName , p_score = 0.99 ):


    tracks = pd.read_csv( GBDTprotonsListName( GBDTmodelName, TracksListName, 0,'features_and_scores') )
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





# -------------------------
def select_analysistrees_to_gbdt_class( TracksListName , GBDTmodelName ,
                                       maxscore = 'protons', score = 0.99 ):
    classified_dirname = Classified_protons_path( GBDTmodelName )
    
    allfeatures_filename = GBDTprotonsListName( GBDTmodelName, TracksListName, 0 , 'features_and_scores' )
    tracks = pd.read_csv( allfeatures_filename )
    if ('proton' in maxscore):
        classified_tracks = tracks[tracks.mscore_max == 0]
        classified_tracks = classified_tracks[classified_tracks.mscore_p > score ]
    elif ('muon' in maxscore):
        classified_tracks = tracks[tracks.mscore_max == 1]
        classified_tracks = classified_tracks[classified_tracks.mscore_mu > score ]
    elif ('pion' in maxscore):
        classified_tracks = tracks[tracks.mscore_max == 2]
        classified_tracks = classified_tracks[classified_tracks.mscore_pi > score ]
    elif ('em' in maxscore):
        classified_tracks = tracks[tracks.mscore_max == 3]
        classified_tracks = classified_tracks[classified_tracks.mscore_em > score ]
    elif ('cosmic' in maxscore):
        classified_tracks = tracks[tracks.mscore_max == 4]
        classified_tracks = classified_tracks[classified_tracks.mscore_cos > score ]

    print "read classified tracks max-scodes as ",maxscore
    PassedGBDTFileRSEName = GBDTclassListName( GBDTmodelName, TracksListName, maxscore , score ,'rse')
    PassedGBDTFileROIName = GBDTclassListName( GBDTmodelName, TracksListName, maxscore , score ,'roi')
    classified_tracks[ features_scores_rse ].to_csv( PassedGBDTFileRSEName , sep=' ' , header=False , index=False )
    classified_tracks[ features_scores_roi ].to_csv( PassedGBDTFileROIName , sep=' ' , header=True , index=False )
    print_filename( PassedGBDTFileRSEName , "only R/S/E & scores written to file" )
    print_filename( PassedGBDTFileROIName , "R/S/E, ROIs and scores written to file" )




# -------------------------
def find_rse( rse , EventsList ):
    print rse[0] , rse[1], rse[2]
    print EventsList['run'],EventsList['subrun'],EventsList['event']
    print zip(EventsList['run'],EventsList['subrun'],EventsList['event'])
    for r,s,e in zip(EventsList['run'],EventsList['subrun'],EventsList['event']):
        if r == rse[0] and s == rse[1] and e == rse[2]:
            return True
    return False








# -------------------------
def filter_analysistrees_to_gbdt_class( TracksListName , GBDTmodelName  , maxscore = 'protons', score = 0.99  ):
    '''
        This functionallity schemes (big) analysis trees
        and returns a tree containing only entries with a Run/Subrun/Event
        of a given list (RSE map)
        '''
    from ROOT import ImportantTools
    it = ImportantTools()
    
    # input: (1) analysis trees
    ana = TPlots( anafiles_path + "/Tracks_" + TracksListName + "_AnalysisTrees.root" , 'TracksTree' )
    all_tracks_tree = ana.GetTree()
    # input: (2) r/s/e list to filter the analysistree from
    gbdt_class_list_name = GBDTclassListName( GBDTmodelName, TracksListName, maxscore , score ,'rse')

    print_filename(gbdt_class_list_name , "rse list to scheme from: ")

    # output: schemed analysistree file
    out_file_name = anafiles_path + "/Tracks_" + TracksListName + "_AnalysisTrees_"  + GBDTmodelName + "_maxscore_" + maxscore + "_score_%.2f"%score + ".root"
    out_file = ROOT.TFile( out_file_name , "recreate" )
    out_tree = it.SchemeTreeRSEList( all_tracks_tree , gbdt_class_list_name , flags.verbose )
    
    if flags.verbose:
        print_filename(out_file_name , "wrote schemed analysistree file (%d events, %.2f MB):"%(out_tree.GetEntries(),float(os.path.getsize(out_file_name)/1048576.0)))
    
    out_tree.Write()
    out_file.Close()




