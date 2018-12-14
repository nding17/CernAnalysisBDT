#!/usr/bin/env python
#from TTH.MEAnalysis.ParHadd import par_hadd
import ROOT
import glob
import sys
import os, fnmatch

#usage: python get_nGen.py /path/to/root/files

#recurse over the given path
for fname in os.listdir(sys.argv[1]):
    if(fname.find('.root')>0):
        file_ = ROOT.TFile(sys.argv[1]+"/"+fname)
        count = file_.Get("Count")
        half = fname.split("__")[1]
        name = half.split(".")[0]
        #print name,count.GetBinContent(1)

        if(name.find('ttHTobb')==0):
            print "double scalefacttH = 0.5085*0.577 /",count.GetBinContent(1),";"
        if(name.find('TT_Tune')==0):
            print "double scalefacTTbar = 831.76 /",count.GetBinContent(1),";"
        if(name.find('QCD_HT300')==0):
            print "double scalefacQCD3 = 351300.0 /",count.GetBinContent(1),";"    
        if(name.find('QCD_HT500')==0):
            print "double scalefacQCD5 = 31630.0 /",count.GetBinContent(1),";"
        if(name.find('QCD_HT700')==0):
            print "double scalefacQCD7 = 6802.0 /",count.GetBinContent(1),";"
        if(name.find('QCD_HT1000')==0):
            print "double scalefacQCD10 = 1206.0 /",count.GetBinContent(1),";"
        if(name.find('QCD_HT1500')==0):
            print "double scalefacQCD15 = 120.4 /",count.GetBinContent(1),";"
        if(name.find('QCD_HT2000')==0):
            print "double scalefacQCD20 = 25.25 /",count.GetBinContent(1),";"
