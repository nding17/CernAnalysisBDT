import ROOT
from ROOT import TTree, TFile, TH1F, TLegend, TCanvas, gStyle, gPad, TMath
from array import array

#######################################################
# this script is to draw various input variables      #
# you selected to train. It shows how those variables #
# in tth, QCD and ttbar are distributed differently,  #
# just so you could get an idea of which variables    #
# might help you with better training performance     #
#######################################################

dir_ = "/shome/nding/CMSSW_8_0_11/src/task2"

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
    h_.GetYaxis().SetTitleSize( 0.04 )

sclfac_ = { "tth" : 0.5085*0.577 / 3413232.0, 
            "qcd3" : 351300.0 / 38222596.0, 
	    "qcd5" : 31630.0 / 56596792.0, 
            "qcd7" : 6802.0 / 41236680.0, 
	    "qcd10" : 1206.0 / 10024439.0, 
            "qcd15" : 120.4 / 7479181.0, 
	    "qcd20" : 25.25 / 3951574.0, 
            "ttbar" : 831.76 / 76610800.0 }

leg1_ = TLegend( .74, .75, .89, .89, "" )

gStyle.SetOptStat( 0 )

input_nm = []
input_xaxis = []
input_lb = []
input_ub = []
input_nbins = []
c_nm = []

for i in range( 6 ):
    input_nm.append( "jet_pt[" + str(i) + "] Distribution;" )
    input_xaxis.append( "pT [GeV];" )
    input_nbins.append( 100 )
    c_nm.append( "jet" + str(i+1) + "_pt" )

input_lb.extend( [ 40, 40, 40, 40, 30, 30 ] )
input_ub.extend( [ 440, 340, 240, 140, 140, 100 ] )

for i in range( 6 ):
    input_nm.append( "jet_eta[" + str(i) + "] Distribution;" )
    input_xaxis.append( "#eta;" )
    input_lb.append( -3 )
    input_ub.append( 3 )
    input_nbins.append( 60 )
    c_nm.append( "jet" + str(i+1) + "_eta" )

for i in range( 6 ):
    input_nm.append( "jet_phi[" + str(i) + "] Distribution;" )
    input_xaxis.append( "#phi;" )
    input_lb.append( -4 )
    input_ub.append( 4 )
    input_nbins.append( 60 )
    c_nm.append( "jet" + str(i+1) + "_phi" )

for i in range( 6 ):
    input_nm.append( "jet_qgl[" + str(i) + "] Distribution;" )
    input_xaxis.append( "qgl;" )
    input_lb.append( -0.1 )
    input_ub.append( 1.1 )
    input_nbins.append( 60 )
    c_nm.append( "jet" + str(i+1) + "_qgl" )

input_nm.extend( [ 'isotropy Distribution;', 'sphericity Distribution;', 
                   'min_dr_btag Distribution;', 'aplanarity Distribution;', 
                   'nBCSVM Distribution;', 'njets Distribution;', 
                   'log_{10}(C) Distribution;', 'log_{10}(D) Distribution;',
                   'DD5j[12] Distribution;', 'DD3j4[12] Distribution;',
                   'Deta5j Distribution;', 'Deta3j4 Distribution;',
                   'Dphi5j Distribution;', 'Dphi4j5 Distribution;', 
                   'DR5j Distribution;', 'DR4j5 Distribution;',
                   'DW3j Distribution;', 'DW5j6 Distribution;' ] )

input_xaxis.extend( [ 'isotropy;', 'sphericity;', 'min_dr_btag;', 'aplanarity;', 'nBCSVM;',
                      'njets;', 'log_{10}(C);', 'log_{10}(D);', 'DD5j;', 'DD3j4;', 'Deta5j;',
                      'Deta3j4;', 'Dphi5j;', 'Dphi4j5;', 'DR5j;', 'DR4j5;', 'DW3j;', 'DW5j6;' ] )

c_nm.extend( [ 'isotropy', 'sphericity', 'min_dr_btag', 'aplanarity', 'nBCSVM',
               'njets', 'logC', 'logD', 'DD5j', 'DD3j4', 'Deta5j',
               'Deta3j4', 'Dphi5j', 'Dphi4j5', 'DR5j', 'DR4j5', 'DW3j', 'DW5j6' ] )
input_lb.extend( [ 0.1, 0, 0.3, 0, 0, 6, 2.5, 3.5, 0, 0, 0, 0, 1, 0.8, 1.5, 1, 0.5, 0.5 ] )
input_ub.extend( [ 1, 140, 2.5, 30, 7, 13, 5.5, 7.5, 5, 5, 4, 2.5, 3.5, 2.6, 4.5, 4, 2.5, 4 ] )
input_nbins.extend( [ 90, 70, 110, 150, 7, 7, 60, 80, 80, 80, 80, 80, 80, 60, 80, 80, 80, 80 ] )

hists = []
cs_ = []

for i in range( len( input_nm ) ):
    hists.append( {} )
    c_new = TCanvas("c" + str(i+1), "c" + str(i+1) )
    cs_.append( c_new )

f_in_ = {}
samples_ = [ "tth", "ttbar", "qcd3", "qcd5", "qcd7", "qcd10", "qcd15", "qcd20" ]
samples_overall = [ "qcd", "tth", "ttbar" ]
sam_nicknames ={ "tth" : "ttH", "qcd" : "QCD MC", "ttbar" : "t#bar{t}" }
hAtt = { "tth" : histsAtt( "tth", ROOT.kBlue, 3 ), 
         "qcd" : histsAtt( "qcd", ROOT.kGreen+1, 3 ),
         "ttbar" : histsAtt( "ttbar", ROOT.kRed, 3 ) }
 
for sALL in samples_overall:
    for i in range( len( input_nm ) ):
        hists[ i ][ sALL ] = TH1F("", input_nm[ i ] + input_xaxis[ i ] + "normalized units", 
                                  input_nbins[ i ], input_lb[ i ], input_ub[ i ] )

    """
    histogram filling processes happening here>>>
    fill() is based on the scale factor of each individual 
    check first if the sample belongs to a certain sample
    group, for example, all qcd's should be combined
    as one.
    """
    for sam in samples_:
        
        if sALL in sam: # check if this is one of the qcd samples     
            f_in_[ sam ] = ROOT.TFile.Open( dir_ + "/copied/cp_new_train/cp_train_" + 
                                            sam + ".root", "READ" )
            f_in_[ sam ].cd()
            t_in = f_in_[ sam ].Get( "tree" )
            print t_in.GetEntries()
            for i in range( t_in.GetEntries() ):
                t_in.GetEntry( i )
                for j in range( len( input_nm ) ):
                    if j < 6:
                        hists[ j ][ sALL ].Fill( t_in.jet_pt[ j ], sclfac_[ sam ] )
                    elif ( j >= 6 and j < 12 ):
                        hists[ j ][ sALL ].Fill( t_in.jet_eta[ j - 6 ], sclfac_[ sam ] )
                    elif ( j >= 12 and j < 18):
                        hists[ j ][ sALL ].Fill( t_in.jet_phi[ j - 12 ], sclfac_[ sam ] )
                    elif ( j >= 18 and j < 24 ):
                        hists[ j ][ sALL ].Fill( t_in.jet_qgl[ j - 18 ], sclfac_[ sam ] )

                hists[ 24 ][ sALL ].Fill( t_in.isotropy, sclfac_[ sam ] )
                hists[ 25 ][ sALL ].Fill( t_in.sphericity, sclfac_[ sam ] )
                hists[ 26 ][ sALL ].Fill( t_in.min_dr_btag, sclfac_[ sam ] )
                hists[ 27 ][ sALL ].Fill( t_in.aplanarity, sclfac_[ sam ] )
                hists[ 28 ][ sALL ].Fill( t_in.nBCSVM, sclfac_[ sam ] )
                hists[ 29 ][ sALL ].Fill( t_in.njets, sclfac_[ sam ] )
                hists[ 30 ][ sALL ].Fill( TMath.Log10( t_in.C ), sclfac_[ sam ] )
                hists[ 31 ][ sALL ].Fill( TMath.Log10( t_in.D ), sclfac_[ sam ] )
                hists[ 32 ][ sALL ].Fill( t_in.DD5j[12], sclfac_[ sam ] )
                hists[ 33 ][ sALL ].Fill( t_in.DD3j4[12], sclfac_[ sam ] )
                hists[ 34 ][ sALL ].Fill( t_in.Deta5j, sclfac_[ sam ] )
                hists[ 35 ][ sALL ].Fill( t_in.Deta3j4, sclfac_[ sam ] )
                hists[ 36 ][ sALL ].Fill( t_in.Dphi5j, sclfac_[ sam ] )
                hists[ 37 ][ sALL ].Fill( t_in.Dphi4j5, sclfac_[ sam ] )
                hists[ 38 ][ sALL ].Fill( t_in.DR5j, sclfac_[ sam ] )
                hists[ 39 ][ sALL ].Fill( t_in.DR4j5, sclfac_[ sam ] )
                hists[ 40 ][ sALL ].Fill( t_in.DW3j, sclfac_[ sam ] )
                hists[ 41 ][ sALL ].Fill( t_in.DW5j6, sclfac_[ sam ] )
             
    leg1_.AddEntry( hists[0][ sALL ], sam_nicknames[ sALL ] )

for sALL in samples_overall:
    for k in range( len( input_nm ) ):
        style_hist_( hists[k][sALL], hAtt[ sALL ] ) 
        cs_[k].cd()
        sclfac_tth = hists[k]['qcd'].Integral() / hists[k]['tth'].Integral()
        sclfac_ttbar = hists[k]['qcd'].Integral() / hists[k]['ttbar'].Integral()
        hists[k][sALL].SetMaximum( 1.3*max( hists[k]['qcd'].GetMaximum(), 
                                            sclfac_tth*hists[k]['tth'].GetMaximum(),
                                            sclfac_ttbar*hists[k]['ttbar'].GetMaximum() ) )
        hists[k][sALL].GetYaxis().SetTitleOffset( 1.3 )
        hists[k][sALL].DrawNormalized( "samehist" )
        cs_[k].Update()
    
for n in range( len( input_nm ) ):
    cs_[n].cd()
    leg1_.Draw()
    cs_[n].Update()
    cs_[n].SaveAs( dir_ + "/dist/EVERYTHING/" + c_nm[n] +'.pdf' )
    cs_[n].SaveAs( dir_ + "/dist/EVERYTHING/" + c_nm[n] +'.png' )

raw_input( "<<<waiting" )
