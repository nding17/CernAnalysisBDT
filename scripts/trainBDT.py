import ROOT
import sys

ROOT.TMVA.Tools.Instance()

##########################################################
# this script is for the BDT training,               
# it trains tth against multiple weighted QCD
# samples, and as an output, a .xml weights file
# will be generated for evaluation.
# In this training, I've chosen some specific
# variables, summing up 40 in total.
# you could of course replace them with
# other variables that fit the purpose of your tasks.
# All of the training settings could be modified
# in MVAsettings
##########################################################

MVAtype = "BDT"
MVAname = "myBDT"
MVAsettings = "!H:!V:NTrees=300:MinNodeSize=5%:MaxDepth=2:" \
    "BoostType=AdaBoost:AdaBoostBeta=0.1:" \
    "SeparationType=MisClassificationError:" \
    "nCuts=25:PruneMethod=NoPruning"

weights = "puWeight"

variables = [] # variables that are used for training
for i in range(0, 6):
    variables.append( "Alt$(jet_pt[" + str(i) + "],0)" )
    variables.append( "Alt$(jet_eta[" + str(i) + "],0)" )
    variables.append( "Alt$(jet_phi[" + str(i) + "],0)" )
    variables.append( "Alt$(jet_qgl[" + str(i) + "],0)"  ) 
 
variables.append( "max( 0, isotropy )" )
variables.append( "max( 0, sphericity )" )

variables.append( "max( 0, aplanarity )" )
variables.append( "max( 0, min_dr_btag )" )

variables.append( "max( 1, log10(C) )" )
variables.append( "max( 1, log10(D) )" )

variables.extend( [ "Alt$(DD5j[12],0)", "Alt$(DD3j4[12],0)",
                    "Deta5j", "Deta3j4", "Dphi5j", "Dphi4j5",
                    "DR5j", "DR4j5", "DW3j", "DW5j6" ] )

def file_check_ ( f_ ):
    """
    check files to avoid zombies
    """
    if(f_.IsZombie()):
        print "invalid file"
        sys.exit(1)

### Nelson's task2(data training) directory
dir_ = "/shome/nding/CMSSW_8_0_11/src/task2"

f_in_ = {}

samples_ = [ "qcd3", "qcd5", "qcd7",  "qcd10", "qcd15", "qcd20" ]

sclfac_ = { "tth" : 0.5085*0.577 / 3413232.0, 
            "qcd3" : 351300.0 / 38222596.0, 
	    "qcd5" : 31630.0 / 56596792.0, 
            "qcd7" : 6802.0 / 41236680.0, 
	    "qcd10" : 1206.0 / 10024439.0, 
            "qcd15" : 120.4 / 7479181.0, 
	    "qcd20" : 25.25 / 3951574.0, 
            "ttbar" : 831.76 / 76610800.0 }
 
f_in_sig = ROOT.TFile( dir_ + "/copied/cp_new_train/cp_train_tth.root", "READ" )
file_check_( f_in_sig )

f_in_sig.cd()
sigTree = f_in_sig.Get( "tree" ).Clone( "sigTree" )

f_out = ROOT.TFile( dir_ + "/backup/f_out_new_vars_update.root", "RECREATE"  )
file_check_( f_out )

f_out.cd()
sigTreeTrain = sigTree.CopyTree( "evt%5 != 0" )
sigTreeTest = sigTree.CopyTree( "evt%5 == 0" )

sigTreeTrain.Write( "", ROOT.TObject.kOverwrite )
sigTreeTest.Write( "", ROOT.TObject.kOverwrite )

factory = ROOT.TMVA.Factory( "TMVAClassification_new_vars_update", f_out, 
                             "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:"\
                                 "AnalysisType=Classification" )

for var in variables:
	factory.AddVariable( var, 'D' )

factory.AddSignalTree( sigTreeTrain, sclfac_[ "tth" ], ROOT.TMVA.Types.kTraining )
factory.AddSignalTree( sigTreeTest, sclfac_[ "tth" ], ROOT.TMVA.Types.kTesting )

factory.SetSignalWeightExpression( weights )

for sam in samples_:
    
    f_in_[ sam ] = ROOT.TFile( dir_ + "/copied/cp_new_train/cp_train_" + sam + ".root", "READ" )
    file_check_( f_in_[ sam ] )
       
    f_in_[ sam ].cd()
    bkgTree = f_in_[ sam ].Get(  "tree" ).Clone( "bkgTree_" + sam  )
    
    """ 
    80% sample for trainging 
    20% for testing
    """
    f_out.cd()

    bkgTreeTrain = bkgTree.CopyTree( "evt%5 != 0" )
    bkgTreeTest = bkgTree.CopyTree( "evt%5 == 0" )

    bkgTreeTrain.Write( "", ROOT.TObject.kOverwrite )
    bkgTreeTest.Write( "", ROOT.TObject.kOverwrite )

    factory.AddBackgroundTree( bkgTreeTrain, sclfac_[ sam ], ROOT.TMVA.Types.kTraining )
    factory.AddBackgroundTree( bkgTreeTest, sclfac_[ sam ], ROOT.TMVA.Types.kTesting )

    factory.SetBackgroundWeightExpression( weights )
    
factory.Verbose()

my_methodBase_bdt = factory.BookMethod( MVAtype, MVAname, MVAsettings )
my_methodBase_bdt.TrainMethod()

factory.TestAllMethods()
factory.EvaluateAllMethods()

f_out.Write()
f_out.Close()
