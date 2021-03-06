'''
    useful tools for GBDT analysis
'''
from uboone_tools import *
from ROOT import GBDTanalysis



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



''' 
    how to run the GBDTs chain?
    -----------------------------
    (1) extract MC tracks information
    python $AnalysisTreesAna/mac/muon_proton_id.py  --option=extractMC
    python $AnalysisTreesAna/mac/muon_proton_id.py  --option=extract_CORSIKA
    
    (2) train
    
    (3) extract data tracks information
    python $AnalysisTreesAna/mac/muon_proton_id.py  --option=extractDATA
    
    (4) apply - predict
'''

def set_main_path( fmain_path ):
    main_path = fmain_path



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
def FullFeaturesFileName( FileType ):
    
    return main_path + "/FeaturesFiles/full_features_" + FileType + "_AnalysisTrees.csv"

# -------------------------
def TrainingSampleFileName( FileTypeToDivide , NumberOfEventsToTrain , main_path='/uboone/app/users/ecohen/AnalysisTreesAna'):
    
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
    
    data = pd.read_csv( FullFeaturesFileName( FileTypeToDivide ) )
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


# -------------------------------------------------------------------
def train_gbdt_MCBNB_and_CORSIKA( feature_names=None, feature_labels=None, model_name=None,
                                 data_type_arr=None , nevents_train_arr=None , parameters=None ,
                                 tracks_frac=1 , prompt_yesno=False , do_make_plots=False):
    
    '''
        Parameters: data_type_arr: ndarray
        array of data types to train on, MC-BNB and CORSIKA-MC
        
        nevents_train_arr: ndarray
        number of events to train form in each sample
        
        Returns:    bdt_model: xgb.train
        gdbt model
        '''
    
    model_path = GBDTmodels_path + '/' + model_name
    init.generate_directory(model_path)
    print 'generated a new directory: '+model_path
    model_suffix = '%s_%s_%s'%(model_name,data_type_arr[0],data_type_arr[1])
    
    outfile = open( model_path + '/xgb_%s.fmap'%model_suffix, 'wb')
    i = 0
    for feat in feature_labels:
        outfile.write('%d\t%s\tq\n'%(i, feat))
        i = i + 1
    outfile.close()
    print_filename( model_path + '/xgb_%s.fmap'%model_suffix , 'generated features map' )


    train_filename = []
    for data,nevnts in zip(data_type_arr,nevents_train_arr):
        train_filename.append(TrainingSampleFileName( data , nevnts , main_path=main_path))
        print_filename( train_filename[-1] , "input: traininig sample file" )

    


    # (A) load the data
    # ---------------------------------------
    data,label,weight = boost_multiscore.load_data( bnb_mc_filename=train_filename[0] ,
                                                   corsika_mc_filename=train_filename[1] ,
                                                   debug=parameters['debug'] ,
                                                   feature_names=feature_names ,
                                                   tracks_frac=parameters['evnts_frac'] )



    # (B) cross-validation step
    # ---------------------------------------
    do_cross_validation = yesno('cross validate?') if prompt_yesno else True
    if do_cross_validation:
        results = test_error,test_falsepos,test_falseneg,scores = boost_multiscore.run_cv( data , label , weight , parameters , Nskf=parameters['Nskf'] )
        
        if flags.verbose>2:
            print "test_error: \n",test_error
            print "test_falsepos: \n",test_falsepos
            print "test_falseneg: \n",test_falseneg
            print "scores: \n",scores

        # plot cross-validation results
        if do_make_plots:
            fig = plt.figure(figsize=(20,20))
            ax = fig.add_subplot(2,2,1)
            plt.hist(test_error)
            set_axes(ax,x_label='test error',y_label='counts',fontsize=20)

            ax = fig.add_subplot(2,2,2)
            h,bins,_=plt.hist([test_falsepos,test_falseneg],bins=np.linspace(0,0.03,30),label=['false positive','false negative']);
            set_axes(ax,x_label='fraction',y_label='counts',fontsize=25)
            ax.set_xlim(0,0.03)
            ax.set_ylim(0,1.1*np.max(h))
            plt.legend(fontsize=25,loc='best')

            ax = fig.add_subplot(2,1,2)
            plt.hist([scores[0],scores[1],scores[2],scores[3],scores[4]],
                     label=['$p$-score','$\\mu$-score','$\\pi$-score','$em$-score','$cosmic$-score'],
                     histtype='step',linewidth=2,bins=np.linspace(0,1,20));
            set_axes(ax,x_label='score',fontsize=25)
            plt.legend(fontsize=25,loc='best')
            plotfilename = model_path + '/cv_test_errors_scores_%s.pdf'%model_suffix
            plt.savefig( plotfilename )
            print_filename( plotfilename , 'plotted cross-validation results')


        resultsfilename = model_path + '/cv_test_errors_scores_%s.csv'%model_suffix
        writer = csv.writer(open(resultsfilename, 'wb'))
        writer.writerow( ['test_error','test_falsepos','test_falseneg'] )


        for i in range(parameters['Nskf']):
            if debug>2:
                print 'wriging test errors for skf ',i
                print [test_error[i],test_falsepos[i],test_falseneg[i]]
            writer.writerow( [test_error[i],test_falsepos[i],test_falseneg[i]] )

        print_filename( resultsfilename , 'saved cross-validation results')
        print "done cross-validation"


    # what does the parameter optimization stage do?? How can one use its output?
    do_optimize_paramters = yesno('optimize parameters?') if prompt_yesno else False
    if do_optimize_paramters:
        results_optimize = test_error,test_falsepos,test_falseneg,scores = boost_multiscore.parameter_opt( data , label , weight , parameters )
        resultsfilename = model_path + '/parameter_opt_scores_%s.csv'%model_suffix
        writer = csv.writer(open(resultsfilename, 'wb'))
        writer.writerow( ['test_error','test_falsepos','test_falseneg'] )
        for i in range(len(test_error)):
            writer.writerow( [test_error[i],test_falsepos[i],test_falseneg[i]] )
        print_filename( resultsfilename , 'saved optimize parameters results')
        print "done optimizing parameters"


    do_make_bdt = yesno('make bdt?') if prompt_yesno else True
    if do_make_bdt:
        bdt = boost_multiscore.make_bdt( data , label , weight , parameters)
        bdt.save_model( model_path + '/bst_model_%s.bst'%model_suffix)
        print_filename( model_path + '/bst_model_%s.bst'%model_suffix , 'bdt model')

        if do_make_plots:
            # plot importances with features names...
            importance = bdt.get_fscore(fmap = model_path + '/xgb_%s.fmap'%model_suffix)
            importance = sorted(importance.items(), key=operator.itemgetter(1))

            df = pd.DataFrame(importance, columns=['feature', 'fscore'])
            df['fscore'] = df['fscore'] / df['fscore'].sum()

            plt.figure()
            df.plot()
            df.plot(kind='barh', x='feature', y='fscore', legend=False, figsize=(10, 10))
            plt.title('XGBoost Feature Importance',fontsize=25)
            plt.xlabel('relative importance',fontsize=25)
            plt.gcf().tight_layout()
            plt.gcf().savefig( model_path + '/importances_model_%s.pdf'%model_suffix)
            print_filename( model_path + '/importances_model_%s.pdf'%model_suffix , 'bdt model importances')

    print "done building bst model"

    print 'done training, continue with predicting on tracks...'






# -------------------------
def calc_all_gbdt_scores( TracksListName , GBDTmodelName  ):
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
def calc_all_gbdt_multiscores( TracksListName , GBDTmodelName , TracksListPath=None ):
    if flags.verbose: print_important( 'compute all gbdt multiscores' )
    if TracksListPath is None:
        SampleFileName = FullFeaturesFileName( TracksListName )
    else:
        SampleFileName = TracksListPath + "/" + TracksListName + ".csv"
    if flags.verbose: print_filename( SampleFileName , "input tracks file" )
    
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
    print EventsList.run,EventsList.subrun,EventsList.event
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




