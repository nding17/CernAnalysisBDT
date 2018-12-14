import ROOT
from ROOT import TTree, TFile, TH1F, TLegend, TCanvas, gStyle, gPad, THStack
import numpy as np
from array import array

########################################################
# this script is to draw the BDT distribution for tth, #
# ttbar and QCD without any selections.                #
########################################################

dir_ = "/shome/nding/CMSSW_8_0_11/src/task2"

_name_ = [ "qcd3", "qcd5", "qcd7", "qcd10", "qcd15", "qcd20", "ttbar", "tth" ]

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

histAttBkg = histsAtt( nickname_bkg, ROOT.kGreen+1, 4 )
histAttTTbar = histsAtt( "ttbar", ROOT.kRed, 4 )
histAttSig = histsAtt( "tth", ROOT.kBlue, 4 ) 

leg1_ = ROOT.TLegend(  .74, .69, .89, .89, "" )
frame_ = ROOT.TH1F( "frame", "BDT Distribution (training: ttH vs QCD MC);"\
                        "BDT Evaluation;normalized units", 22, -1.0, 1.2 )
frame_.SetMaximum( 0.20 )
frame_.Draw()

sam_sig = histAttSig.sample
t_in_sig = f_in_[ "tth" ].Get( "tree" )
BDT_sig = array( 'd', [ 0 ] )
t_in_sig.SetBranchAddress( "BDT_tth_vs_qcds", BDT_sig )

hist_sig = TH1F( "sig", "", 22, -1.0, 1.2 )

for j in range( t_in_sig.GetEntries() ):
    t_in_sig.GetEntry( j )
    hist_sig.Fill( BDT_sig[ 0 ], sclfac_[ "tth" ] )

style_hist_( hist_sig, histAttSig )

c1.cd()
hist_sig.DrawNormalized( "samehist" )
leg1_.AddEntry( hist_sig, "ttH" )
c1.Update()

sam_ttbar = histAttTTbar.sample
t_in_ttbar = f_in_[ "ttbar" ].Get( "tree" )
BDT_ttbar = array( 'd', [ 0 ] )
t_in_ttbar.SetBranchAddress( "BDT_tth_vs_qcds", BDT_ttbar )

hist_ttbar = TH1F( "ttbar", "", 22, -1.0, 1.2 )

for k in range( t_in_ttbar.GetEntries() ):
    t_in_ttbar.GetEntry( k )
    hist_ttbar.Fill( BDT_ttbar[ 0 ], sclfac_[ "ttbar" ] )

style_hist_( hist_ttbar, histAttTTbar )

c1.cd()
hist_ttbar.DrawNormalized( "samehist" )
leg1_.AddEntry( hist_ttbar, nickname_ttbar )
c1.Update()
 
hist_bkg = TH1F( "bkg", "", 22, -1.0, 1.2 )

for nm in _name_:
    if 'q' in nm:
        t_in = f_in_[ nm ].Get( "tree" )
        BDT_bkg = array( 'd', [ 0 ] )
        t_in.SetBranchAddress( "BDT_tth_vs_qcds", BDT_bkg )

        for i in range( t_in.GetEntries() ):
            t_in.GetEntry( i )
            hist_bkg.Fill( BDT_bkg[ 0 ], sclfac_[ nm ] )

style_hist_( hist_bkg, histAttBkg )
leg1_.AddEntry( hist_bkg, "QCD MC" )

c1.cd()
hist_bkg.DrawNormalized( "samehist" )
c1.Update()

gStyle.SetOptStat( 0 )
c1.cd()
leg1_.Draw( "same")
c1.Update()
c1.SaveAs( dir_ + "/dist/EVERYTHING/BDT_tth_vs_qcds_new_vars_update.pdf" )
c1.SaveAs( dir_ + "/dist/EVERYTHING/BDT_tth_vs_qcds_new_vars_update.png" )

raw_input( "<<<waiting" )
