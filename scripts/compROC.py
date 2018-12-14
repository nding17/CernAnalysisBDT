import ROOT
from ROOT import TTree, TFile, TH1F, TLegend, TCanvas, gStyle, gPad, TLatex
import numpy as np
from array import array

##################################################################
# this script is useful when you want to compare the ROC curves  #
# in two different trainings but the difference is too slight to #
# tell.                                                          #
##################################################################

# set up directory path and files' name
dir_ = "/shome/nding/CMSSW_8_0_11/src/task2"

samples_ = [  'tth', 'ttbar', 'qcd3', 'qcd5', 'qcd7', 'qcd10', 'qcd15', 'qcd20' ]

f_in_ = {}
f_in_prev_ = {}
for sam in samples_ :
    f_in_[ sam ] = TFile.Open( dir_ + "/backup/all_new_inputs_final_update_BDT_" + 
                               sam + ".root", "READ"  )
    f_in_prev_[ sam ] = TFile.Open( dir_ + "/backup/all_new_inputs_update_BDT_" + 
                                    sam + ".root", "READ" ) 

bdt_qcds_train = {} 
bdt_qcds_train_prev = {}

for sam in samples_ :
    bdt_qcds_train[ sam ] = array( 'd', [ 0 ] ) 
    bdt_qcds_train_prev[ sam ] = array( 'd', [ 0 ] )

bdt_ = {}
tr_ = {}

bdt_prev_ = {}
tr_prev_ = {}

for sam in samples_ :
    bdt_[ sam ] = array( 'd', [ 0 ] )
    bdt_prev_[ sam ] = array( 'd', [ 0 ] )

    tr_[ sam ] = f_in_[ sam ].Get( "tree" ) 
    tr_[ sam ].SetBranchAddress( "BDT_tth_vs_qcds", bdt_[ sam ] )
    
    tr_prev_[ sam ] = f_in_prev_[ sam ].Get( 'tree' )
    tr_prev_[ sam ].SetBranchAddress( 'BDT_tth_vs_qcds', bdt_prev_[ sam ] )

trs_ = [ tr_, tr_prev_ ]
bdts_ = [ bdt_, bdt_prev_ ]
  
sclfac_ = { "tth" : 0.5085*0.577 / 3413232.0, 
            "qcd3" : 351300.0 / 38222596.0, 
	    "qcd5" : 31630.0 / 56596792.0, 
            "qcd7" : 6802.0 / 41236680.0, 
	    "qcd10" : 1206.0 / 10024439.0, 
            "qcd15" : 120.4 / 7479181.0, 
	    "qcd20" : 25.25 / 3951574.0, 
            "ttbar" : 831.76 / 76610800.0 }

ylds_ = { 'tth' : [], 'ttbar' : [], 'qcds' : [] }
ylds_prev = { 'tth' : [], 'ttbar' : [], 'qcds' : [] }

ylds_all_ = [ ylds_, ylds_prev ]

cuts = []
for i in range( 21 ):
    cuts.append( i * 0.1 + ( -1.0 ) )

for c in cuts:

    total_ = { 'tth' : 0.0, 'ttbar' : 0.0, 'qcds' : 0.0 }
    total_prev = { 'tth' : 0.0, 'ttbar' : 0.0, 'qcds' : 0.0 }

    ttl_ = [ total_, total_prev ]

    for k in range( len( trs_ ) ):
        for sam in samples_:
            for i in range( trs_[ k ][ sam ].GetEntries() ):
                # if i > 3000: break
                trs_[ k ][ sam ].GetEntry( i )
                if bdts_[ k ][ sam ][ 0 ] >= c:
                    if 'q' in sam:
                        ttl_[ k ][ 'qcds' ] = ttl_[ k ][ 'qcds' ] + sclfac_[ sam ]
                    else:
                        ttl_[ k ][ sam ] = ttl_[ k ][ sam ] + sclfac_[ sam ]
             
        print ">= " + str( c )
        print "tth ttl ylds: " +  str( total_[ 'tth' ] )
        print "ttbar ttl ylds: " + str( total_[ 'ttbar' ] )
        print "qcds ttl ylds: " + str( total_[ 'qcds' ] )
        print '\n'
        ylds_all_[ k ][ 'tth' ].append( ttl_[ k ][ 'tth' ] )
        ylds_all_[ k ][ 'ttbar' ].append( ttl_[ k ][ 'ttbar' ] )
        ylds_all_[ k ][ 'qcds' ].append( ttl_[ k ][ 'qcds' ] )

tth_eff_ = [ array( 'd', [] ),  array( 'd', [] ) ]
ttbar_eff_ = [ array( 'd', [] ), array( 'd', [] ) ]
qcds_eff_ = [ array( 'd', [] ), array( 'd', [] ) ]

for k in range( len( tth_eff_ ) ) :
    for nct in range( len( cuts ) ) :
        tth_eff_[ k ].append( ylds_all_[ k ][ 'tth' ][ nct ] / ylds_all_[ k ][ 'tth' ][ 0 ] )
        ttbar_eff_[ k ].append( ylds_all_[ k ][ 'ttbar' ][ nct ] / ylds_all_[ k ][ 'ttbar' ][ 0 ] )
        qcds_eff_[ k ].append( ylds_all_[ k ][ 'qcds' ][ nct ] / ylds_all_[ k ][ 'qcds' ][ 0 ] )

# all of the styling attributes of the ROC curves
color_ = { "tthvsttbar" : ROOT.kRed, "tthvsqcds" : ROOT.kGreen + 1 }
roc_nickname = { "tthvsttbar" : "eff. : ttH vs t#bar{t} ", "tthvsqcds" :  "eff. : ttH vs QCD " }

roc_baseline = ROOT.TMultiGraph() # ROC curves without doing any combinations
leg_baseline = TLegend( 0.13, 0.88, 0.47, 0.77 )

roc_tth_vs_ttbar = []
roc_tth_vs_qcds = []

for i in range( len( tth_eff_ ) ):
    roc1 = ROOT.TGraph( len( tth_eff_[i] ), tth_eff_[i], ttbar_eff_[i] )
    roc2 = ROOT.TGraph( len( tth_eff_[i] ), tth_eff_[i], qcds_eff_[i] )
    roc_tth_vs_ttbar.append( roc1 )
    roc_tth_vs_qcds.append( roc2 )

roc_ = { "tthvsttbar" : roc_tth_vs_ttbar, 'tthvsqcds' : roc_tth_vs_qcds }

options_ = [ "tthvsttbar", "tthvsqcds" ]

wid_ = [ 1, 2 ]
sty_ = [ 2, 1 ]
tra_ = [ '( BDT4 )', '( BDT3 )' ]

for opt in options_ :
    for i in range( len( wid_ ) ):
        roc_[ opt ][ i ].SetLineColor( color_[ opt ] )
        roc_[ opt ][ i ].SetLineWidth( wid_[ i ] )
        roc_[ opt ][ i ].SetLineStyle( sty_[ i ] )
        roc_[ opt ][ i ].SetFillStyle( 0 )

        leg_baseline.AddEntry( roc_[ opt ][ i ], roc_nickname[ opt ] + tra_[ i ] )
        roc_baseline.Add( roc_[opt][ i ] )

ref_pts = array( 'd', [ 0.0, 1.0 ] )
ref = ROOT.TGraph( 2, ref_pts, ref_pts ) # draw a diagonal line for reference
ref.SetLineColor( ROOT.kBlack )
ref.SetLineWidth( 1 )

x = 0.35
y = 0.65
latex_ = TLatex( x, y, "" )

c1 = TCanvas( "c1", "c1" )
c1.cd()
roc_baseline.Add( ref )

roc_baseline.Draw( 'ACP' )
roc_baseline.SetTitle( "ROC Curve for BDT Evaluation" )
roc_baseline.GetXaxis().SetTitle( "Signal Efficiency" )
roc_baseline.GetYaxis().SetTitle( "Background Efficiency" )
leg_baseline.Draw( "same" )
latex_.Draw( "same" )

gPad.Modified()
roc_baseline.GetXaxis().SetLimits( 0.0, 1.0 )
roc_baseline.SetMinimum( 0.0 )
roc_baseline.SetMaximum( 1.0 )

c1.Update()
c1.SaveAs( dir_ + "/dist/EVERYTHING/ROC_new_vars_comp_" + str(i) + ".pdf" )
c1.SaveAs( dir_ + "/dist/EVERYTHING/ROC_new_vars_comp_" + str(i) + ".png" )
    
raw_input( "<<<waiting" )
