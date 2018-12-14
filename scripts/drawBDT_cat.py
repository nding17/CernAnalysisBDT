import ROOT
from ROOT import TTree, TFile, TH1F, TLegend, TCanvas, gStyle, gPad, THStack
from ROOT import TLatex
import numpy as np
from array import array

##########################################################
# this script is to draw the BDT distribution histograms #
# in different categories. The categories in this task   #
# are 7j3b, 7j4b, 8j3b, 8j4b, 9j3b, 9j4b.                #
# It basically takes the same input file as that in      #
# drawBDT.py                                             #
##########################################################

dir_ = "/shome/nding/CMSSW_8_0_11/src/task2"

### _name_ = [ "qcd3", "qcd5", "qcd7", "qcd10", "qcd15", "qcd20", "ttbar", "tth" ]

_name_ = [ "qcd5", "qcd7", "qcd10", "qcd15", "qcd20", "ttbar", "tth" ]

nickname_bkg = "QCD MC"
nickname_ttbar = "t#bar{t}"

sclfac_ = { "tth" : 0.5085*0.577 / 3413232.0, 
            "qcd3" : 351300.0 / 38222596.0, 
	    "qcd5" : 31630.0 / 56596792.0, 
            "qcd7" : 6802.0 / 41236680.0, 
	    "qcd10" : 1206.0 / 10024439.0, 
            "qcd15" : 120.4 / 7479181.0, 
	    "qcd20" : 25.25 / 3951574.0, 
            "ttbar" : 831.76 / 76610800.0 }

f_in_ = {}

for _n_ in _name_:
    f_in_[ _n_ ] = TFile.Open( dir_ + "/backup/" + "all_new_inputs_update_BDT_" 
                               + _n_ + ".root", "READ" )

class histsAtt:
    """
    a constructor that contains all necessary styling
    attributes of a histogram
    """
    def __init__( self, sample, color, stroke ):
        self.sample = sample
        self.color = color
        self.stroke = stroke

def style_hist_( h_, att_ ):
    h_.SetLineColor( att_.color )
    h_.SetLineWidth( att_.stroke )

c1 = TCanvas( "c1", "c1" )
c2 = TCanvas( "c2", "c2" )
c3 = TCanvas( "c3", "c3" )
c4 = TCanvas( "c4", "c4" )
c5 = TCanvas( "c5", "c5" )
c6 = TCanvas( "c6", "c6" )

cs_ = [ c1, c2, c3, c4, c5, c6 ]

x = 0.42
y = 0.75

latex1 = TLatex( x, y, "7j, 3b" )
latex2 = TLatex( x, y, "7j, #geq4b" )
latex3 = TLatex( x, y, "8j, 3b" )
latex4 = TLatex( x, y, "8j, #geq4b" )
latex5 = TLatex( x, y, "9j, 3b" )
latex6 = TLatex( x, y, "9j, #geq4b" )

latex_ = [ latex1, latex2, latex3, latex4, latex5, latex6 ]

for i in range( len( latex_ ) ):
     latex_[ i ].SetTextAlign( 22 )
     latex_[ i ].SetNDC()
     latex_[ i ].SetTextFont( 43 )
     latex_[ i ].SetTextColor( ROOT.kBlack )
     latex_[ i ].SetTextSize( 27 )

lim_nj = [ 7, 8, 9 ]
lim_nbj = [ 3, 4 ]

histAttBkg = histsAtt( nickname_bkg, ROOT.kGreen+1, 4 )
histAttTTbar = histsAtt( "ttbar", ROOT.kRed, 4 )
histAttSig = histsAtt( "tth", ROOT.kBlue, 4 ) 

leg1 = ROOT.TLegend(  .74, .69, .89, .89, "" )

gStyle.SetOptStat(0)

sam_sig = histAttSig.sample
t_in_sig = f_in_[ "tth" ].Get( "tree" )

BDT_sig = array( 'd', [ 0 ] )
njets_sig = array( 'i', [ 0 ] )
nBCSVM_sig = array( 'i', [ 0 ] )

t_in_sig.SetBranchAddress( "BDT_tth_vs_qcds", BDT_sig )
t_in_sig.SetBranchAddress( "njets", njets_sig )
t_in_sig.SetBranchAddress( "nBCSVM", nBCSVM_sig )

hist_sig = TH1F( "sig", "BDT Distribution (training: ttH vs QCD MC);"\
                        "BDT Evaluation;normalized units", 22, -1.0, 1.2 )

hist_sig_ = []

for i in range( len( lim_nj )*len( lim_nbj ) ): 
    hist_sig_.append( hist_sig.Clone() )

for j in range( t_in_sig.GetEntries() ):
    t_in_sig.GetEntry( j )
    for k in range( len( lim_nj ) ):
        if njets_sig[ 0 ] == lim_nj[ k ] and nBCSVM_sig[ 0 ] == lim_nbj[ 0 ]: 
            hist_sig_[ k*2 ].Fill( BDT_sig[ 0 ], sclfac_[ "tth" ] )
        if njets_sig[ 0 ] == lim_nj[ k ] and nBCSVM_sig[ 0 ] >= lim_nbj[ 1 ]: 
            hist_sig_[ k*2+1 ].Fill( BDT_sig[ 0 ], sclfac_[ "tth" ] )

sam_ttbar = histAttTTbar.sample
t_in_ttbar = f_in_[ "ttbar" ].Get( "tree" )

BDT_ttbar = array( 'd', [ 0 ] )
njets_ttbar = array( 'i', [ 0 ] )
nBCSVM_ttbar = array( 'i', [ 0 ] )

t_in_ttbar.SetBranchAddress( "BDT_tth_vs_qcds", BDT_ttbar )
t_in_ttbar.SetBranchAddress( "njets", njets_ttbar )
t_in_ttbar.SetBranchAddress( "nBCSVM", nBCSVM_ttbar )

hist_ttbar = TH1F( "ttbar", "", 22, -1.0, 1.2 )

hist_ttbar_ = []

for i in range( len( lim_nj )*len( lim_nbj ) ):
    hist_ttbar_.append( hist_ttbar.Clone() )

for k in range( t_in_ttbar.GetEntries() ):
    t_in_ttbar.GetEntry( k )
    for n in range( len( lim_nj ) ): 
        if njets_ttbar[ 0 ] == lim_nj[ n ] and nBCSVM_ttbar[ 0 ] == lim_nbj[ 0 ]:
            hist_ttbar_[ n*2 ].Fill( BDT_ttbar[ 0 ], sclfac_[ "ttbar" ] )
        if njets_ttbar[ 0 ] == lim_nj[ n ] and nBCSVM_ttbar[ 0 ] >= lim_nbj[ 1 ]:
            hist_ttbar_[ n*2+1 ].Fill( BDT_ttbar[ 0 ], sclfac_[ "ttbar" ] )

hist_bkg = TH1F( "bkg", "", 22, -1.0, 1.2 )

hist_bkg_ = []

for i in range( len( lim_nj ) * len( lim_nbj ) ):
    hist_bkg_.append( hist_bkg.Clone() )

for nm in _name_:
    if 'q' in nm :
        t_in = f_in_[ nm ].Get( "tree" )
        BDT_bkg = array( 'd', [ 0 ] )
        njets_bkg = array( 'i', [ 0 ] )
        nBCSVM_bkg = array( 'i', [ 0 ] )

        t_in.SetBranchAddress( "BDT_tth_vs_qcds", BDT_bkg )
        t_in.SetBranchAddress( "njets", njets_bkg )
        t_in.SetBranchAddress( "nBCSVM", nBCSVM_bkg )

        for i in range( t_in.GetEntries() ):
            t_in.GetEntry( i )
            for k in range( len( lim_nj ) ):
                if njets_bkg[ 0 ] == lim_nj[ k ] and nBCSVM_bkg[ 0 ] == lim_nbj[ 0 ]: 
                    hist_bkg_[ k*2 ].Fill( BDT_bkg[ 0 ], sclfac_[ nm ] )
                if njets_bkg[ 0 ] == lim_nj[ k ] and nBCSVM_bkg[ 0 ] >= lim_nbj[ 1 ]:
                    hist_bkg_[ k*2+1 ].Fill( BDT_bkg[ 0 ], sclfac_[ nm ] )

leg1.AddEntry( hist_sig_[ 0 ], "ttH" )
leg1.AddEntry( hist_ttbar_[ 0 ], "t#bar{t}" )
leg1.AddEntry( hist_bkg_[ 0 ], "#splitline{QCD MC}{QCD300 excl.}" )

all_hists_ = [ hist_sig_, hist_ttbar_, hist_bkg_ ]
  
for i in range( len( lim_nj ) * len( lim_nbj ) ): 
    style_hist_( hist_bkg_[ i ], histAttBkg )
    style_hist_( hist_sig_[ i ], histAttSig )
    style_hist_( hist_ttbar_[ i ], histAttTTbar )

    sclfac_tth = hist_bkg_[ i ].Integral() / hist_sig_[ i ].Integral()
    sclfac_ttbar = hist_bkg_[ i ].Integral() / hist_ttbar_[ i ].Integral()

    hist_sig_[ i ].Scale( sclfac_tth )
    hist_ttbar_[ i ].Scale( sclfac_ttbar )

    cs_[ i ].cd()

    for k in range( len( all_hists_ ) ):
        all_hists_[ k ][ i ].SetMaximum( 1.35*max( hist_sig_[ i ].GetMaximum(), 
                                                  hist_ttbar_[ i ].GetMaximum(),
                                                  hist_bkg_[ i ].GetMaximum() ) )
        all_hists_[ k ][ i ].DrawNormalized( "histsame" )
        cs_[ i ].Update()

    latex_[ i ].Draw( 'same' )
    leg1.Draw()
    
    cs_[ i ].SaveAs( dir_ + "/dist/EVERYTHING/new_selection_update_" + str(i) + ".pdf" )
    cs_[ i ].SaveAs( dir_ + "/dist/EVERYTHING/new_selection_update_" + str(i) + ".png" )
    
raw_input( "<<<waiting" )
