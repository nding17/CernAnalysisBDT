import ROOT
import numpy as n
import sys
from array import array

##################################################
# this script is for BDT evaluation. Taken all   #
# the input variables from the training, it      #
# implements a TMVA reader to read the BDT       #
# scores extracted from the .xml file.           #
# It would then make a tree, first of all, it    #
# copies all the input variables to the tree,    #
# and after that the tree will stretch a new     #
# branch to store the BDT results as a variable  #
##################################################


dir2_ = "/shome/nding/CMSSW_8_0_11/src/task2"

def fill_tree_ (tree,  sample_, f_, sam_name):
    """
    functions for filling up the histograms of the BDT distributions
    since in the training, even entries are picked up to do the job
    we will be interested in odd events for evaluation
    """
    
    """ initiate the first six variables and their readable names """
    variables = [ ]

    for i in range(0, 6):
        variables.append( "Alt$(jet_pt[" + str(i) + "],0)" )
        variables.append( "Alt$(jet_eta[" + str(i) + "],0)" )
        variables.append( "Alt$(jet_phi[" + str(i) + "],0)" )
        variables.append( "Alt$(jet_qgl[" + str(i) + "],0)" )

    variables.append( "max(0, isotropy)" )
    variables.append( "max(0, sphericity)" )
    
    variables.append( "max(0, aplanarity)" )
    variables.append( "max(0, min_dr_btag)" )
    
    variables.append( "max( 1, log10(C) )" )
    variables.append( "max( 1, log10(D) )" )

    variables.extend( [ "Alt$(DD5j[12],0)", "Alt$(DD3j4[12],0)",
                    "Deta5j", "Deta3j4", "Dphi5j", "Dphi4j5",
                    "DR5j", "DR4j5", "DW3j", "DW5j6" ] )
       
    buffer_  = {}
    formula_ = {}

    reader = ROOT.TMVA.Reader( "!Color:!Silent" )
    sam_cnt_ = n.zeros(1, dtype = float) # set up the branch variable for BDT measurement   
    tree_ = ROOT.TTree( "tree", "tree" )
    tree_.Branch( "BDT_tth_vs" + sample_, sam_cnt_, "BDT_tth_vs_qcds/D") # connect the branch with its tree
    
    ### all input and relevant variables are 
    ### incorporated into the root file that 
    ### used to store BDT results
    njets       = array( 'i', [ 0 ] )
    nBCSVM      = array( 'i', [ 0 ] )
    evt         = array( 'i', [ 0 ] )
    puWeight    = array( 'd', [ 0 ] )
    isotropy    = array( 'd', [ 0 ] )
    sphericity  = array( 'd', [ 0 ] )
    aplanarity  = array( 'd', [ 0 ] )
    min_dr_btag = array( 'd', [ 0 ] )
    C           = array( 'd', [ 0 ] )
    D           = array( 'd', [ 0 ] )
    Deta5j      = array( 'd', [ 0 ] )
    Deta3j4     = array( 'd', [ 0 ] )
    Dphi5j      = array( 'd', [ 0 ] )
    Dphi4j5     = array( 'd', [ 0 ] )
    DR5j        = array( 'd', [ 0 ] )
    DR4j5       = array( 'd', [ 0 ] )
    DW3j        = array( 'd', [ 0 ] )
    DW5j6       = array( 'd', [ 0 ] )

    mxn  = 20
    mxn2 = 12
    jet_pt  = array( 'd', mxn*[ 0 ] )
    jet_eta = array( 'd', mxn*[ 0 ] )
    jet_phi = array( 'd', mxn*[ 0 ] )
    jet_qgl = array( 'd', mxn*[ 0 ] )
    DD5j    = array( 'd', mxn2*[ 0 ] )
    DD3j4   = array( 'd', mxn2*[ 0 ] )

    ### C equivalent pointers translated into python
    input_vars_ = [ njets, jet_pt, jet_eta, jet_phi, jet_qgl, nBCSVM, evt, puWeight, isotropy,
                   min_dr_btag, aplanarity, C, D, sphericity ]
    ### corresponding names for all copied input variables
    input_nm_ = [ 'njets', 'jet_pt', 'jet_eta', 'jet_phi', 'jet_qgl', 'nBCSVM', 'evt', 'puWeight',
                 'isotropy', 'min_dr_btag', 'aplanarity', 'C', 'D', 'sphericity' ]
    ### corresponding types for those input variables
    input_typ_ = [ '/I', '[njets]/D', '[njets]/D', '[njets]/D', '[njets]/D', '/I', '/I', '/D', 
                   '/D', '/D', '/D', '/D', '/D', '/D' ]

    ### connect the output trees with all the branches, 
    ### each with corresponding name and type 
    for k in range( len( input_vars_ ) ): 
        tree_.Branch( input_nm_[ k ], input_vars_[ k ], input_nm_[ k ] + input_typ_[ k ] )

    for var in variables:
        buffer_[var] = array( 'f', [ 0 ] )
        formula_[var] = ROOT.TTreeFormula( "myFormula", var, tree )
        reader.AddVariable( var, buffer_[ var ] )
    
    reader.BookMVA( "myBDT","weights/TMVAClassification_new_vars_update_myBDT.weights.xml" )

    for i in range( tree.GetEntries() ):
        """
        only looking for odd inputs for testing to avoid biased results
        since even events are taken to do the training
        """
        # if i > 5000: break
        tree.GetEntry( i )  
        for var in variables:
            formula_[ var ].GetNdata()
            buffer_[ var ][ 0 ] = formula_[ var ].EvalInstance()
                
        sam_cnt_[ 0 ] = reader.EvaluateMVA( "myBDT" )
        njets[ 0 ] = tree.njets
        
        for j in range( len( tree.jet_pt ) ) : 
            jet_pt[ j ]  = tree.jet_pt[ j ]
            jet_eta[ j ] = tree.jet_eta[ j ]
            jet_phi[ j ] = tree.jet_phi[ j ]
            jet_qgl[ j ] = tree.jet_qgl[ j ]

            if j < mxn2:
                DD5j[ j ]    = tree.DD5j[ j ]
                DD3j4[ j ]   = tree.DD3j4[ j ]

        nBCSVM[ 0 ]      = tree.nBCSVM
        evt[ 0 ]         = tree.evt
        puWeight[ 0 ]    = tree.puWeight
        isotropy[ 0 ]    = tree.isotropy
        aplanarity[ 0 ]  = tree.aplanarity
        sphericity[ 0 ]  = tree.sphericity
        min_dr_btag[ 0 ] = tree.min_dr_btag
        C[ 0 ]           = tree.C
        D[ 0 ]           = tree.D
        Deta5j[ 0 ]      = tree.Deta5j
        Deta3j4[ 0 ]     = tree.Deta3j4
        Dphi5j[ 0 ]      = tree.Dphi5j
        Dphi4j5[ 0 ]     = tree.Dphi4j5
        DR5j[ 0 ]        = tree.DR5j
        DR4j5[ 0 ]       = tree.DR4j5
        DW3j[ 0 ]        = tree.DW3j
        DW5j6[ 0 ]       = tree.DW5j6
             
        tree_.Fill()
                
    tree_.Print()
    tree_.Write( "", ROOT.TObject.kOverwrite )
    f_.Write()
                   
def file_check_ ( f_ ):
    """
    check files to avoid zombies
    """
    if( f_.IsZombie() ):
        print "invalid file"
        sys.exit(1)

### identifier for all of the input samples
samples_ = [ "qcd3", "qcd5", "qcd7",  "qcd10", "qcd15", "qcd20", "tth", "ttbar" ]

"""
define dictionaries for bkg histograms, 
trees, files and even legends
"""
tree_ = {}
f_in_ = {}
f_out_ = {}
   
for sam in samples_:
    f_in_[ sam ] = ROOT.TFile( dir2_ + "/copied/cp_new_eval/cp_eval_" + sam + ".root", "READ" )
    file_check_( f_in_[ sam ] )
    f_in_[ sam ].cd()
    tree_[ sam ] = f_in_[ sam ].Get( "tree" ) # get all the background trees

    f_out_[ sam ] = ROOT.TFile.Open( dir2_ + "/backup/" + "all_new_inputs_update_BDT_" 
                                     + sam  + ".root", "RECREATE" )
    
    f_out_[ sam ].cd() # update to the current location
    fill_tree_( tree_[ sam ],  "_qcds", f_out_[ sam ], sam )
    f_out_[ sam ].Close() # finish writing, close the root file

