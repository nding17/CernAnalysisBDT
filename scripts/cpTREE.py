import ROOT
import sys
import numpy as n

######################################################
# the purpose of this script is to help improve the  #
# speed of BDT training and evaluating:              #
#                                                    #
# copy only the variables that are relevant to the   #
# training and evaluation process. Make new trees    #
# to store these variables, each tree takes half     #
# of the events in each sample.                      #
######################################################


dir_ = "/mnt/t3nfs01/data01/shome/dsalerno/TTH_2016/"\
    "TTH_80X_test2/mini_trees/v2/" # Daniel's directory
dir2_ = "/shome/nding/CMSSW_8_0_11/src/task2/copied" # Nelson's directory

""" 
set up all datasets files 
"""
with open( dir2_ + "/" + "new_samples.txt" ) as sample_f:
    pre_ = sample_f.read().strip().split( ';' )

prefix_ = { "ttbar": pre_[0], "qcd3": pre_[1], "qcd5": pre_[2],
           "qcd7": pre_[3], "qcd10": pre_[4], "qcd15": pre_[5],
           "qcd20": pre_[6], "tth": pre_[7] } # a collection of all filenames


def file_check_ ( f_ ):
    """
    check files to avoid zombies
    """
    if( f_.IsZombie() ):
        print "invalid file"
        sys.exit(1)

f_in_ = {}
t_in_ = {}

f_out_train_ = {}
f_out_test_ = {}
t_out_train_ = {}
t_out_test_ = {}

# nickname for all the samples
samples_ = [ "ttbar", "qcd3", "qcd5", "qcd7", "qcd10", "qcd15", "qcd20", "tth" ]

# all of the relevant variables that's going to 
# be implemented in the training algorithm
variables_ = [ "njets", "evt", "puWeight", "jet_pt", "jet_eta", "jet_phi", "jet_qgl", "min_dr_btag", 
               "isotropy", "aplanarity", "sphericity", "C", "D", "nBCSVM", "DD5j", "DD3j4", "Deta5j", 
               "Deta3j4", 'Dphi5j', 'Dphi4j5', 'DR5j', 'DR4j5', 'DW3j', 'DW5j6' ]
for sam in samples_:
    f_out_train_[ sam ] = ROOT.TFile.Open( dir2_ + "/cp_new_train/cp_train_" + sam + ".root", "RECREATE" )
    f_out_test_[ sam ] = ROOT.TFile.Open( dir2_ + "/cp_new_eval/cp_eval_" + sam + ".root", "RECREATE" )

    f_in_[ sam ] = ROOT.TFile.Open( dir_ + prefix_[ sam ], "READ" )
    t_in_[ sam ] = f_in_[ sam ].Get( "tree" )

    t_in_[ sam ].SetBranchStatus( "*", False )
    
    for var in variables_:
        t_in_[ sam ].SetBranchStatus( var, True )

    # half of each sample for training
    f_out_train_[ sam ].cd()
    t_out_train_[ sam ] = t_in_[ sam ].CopyTree( "evt%2 == 0" )
    t_out_train_[ sam ].Write( "", ROOT.TObject.kOverwrite )
    f_out_train_[ sam ].Write()
    f_out_train_[ sam ].Close()

    # half of each sample for evaluation
    f_out_test_[ sam ].cd()
    t_out_test_[ sam ] = t_in_[ sam ].CopyTree( "evt%2 == 1")
    t_out_test_[ sam ].Write( "", ROOT.TObject.kOverwrite )
    f_out_test_[ sam ].Write()
    f_out_test_[ sam ].Close()

    
