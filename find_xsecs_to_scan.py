"""Find 6 xsec values to scan based on Asym.root"""
import sys
import ROOT as rt

if __name__ == '__main__':
    ASYM_NAME = sys.argv[1]
    ASYM_FILE = rt.TFile.Open(ASYM_NAME)
    MODEL = 'T2tt'
    BOX = 'BJetHS'
    NXSEC = 5

    EXPMINUS2 = ASYM_FILE.Get("xsecUL_ExpMinus2_%s_%s" % (MODEL, BOX))
    EXPPLUS2 = ASYM_FILE.Get("xsecUL_ExpPlus2_%s_%s" % (MODEL, BOX))
    EXPMINUS1 = ASYM_FILE.Get("xsecUL_ExpMinus_%s_%s" % (MODEL, BOX))
    EXPPLUS1 = ASYM_FILE.Get("xsecUL_ExpPlus_%s_%s" %(MODEL, BOX))
    EXP = ASYM_FILE.Get("xsecUL_Exp_%s_%s" % (MODEL, BOX))

    print "expPlus2  = %f " % (EXPPLUS2.GetBinContent(EXPPLUS2.\
                               FindBin(700, 25)))
    print "expPlus   = %f " % (EXPPLUS1.GetBinContent(EXPPLUS1.\
                               FindBin(700, 25)))
    print "exp       = %f " %(EXP.GetBinContent(EXP.FindBin(700, 25)))
    print "expMinus  = %f " %(EXPMINUS1.GetBinContent(EXPMINUS1.\
                              FindBin(700, 25)))
    print "expMinus2 = %f " %(EXPMINUS2.GetBinContent(EXPMINUS2.\
                              FindBin(700, 25)))

    MINXSEC = EXPPLUS2.GetBinContent(EXPPLUS2.FindBin(700, 25))
    MAXXSEC = EXPMINUS2.GetBinContent(EXPMINUS2.FindBin(700, 25))

    XSECRANGE = [round(MAXXSEC - (MAXXSEC-MINXSEC)*float(i)/float(NXSEC-1), 6)\
    for i in range(-5, NXSEC+5) if round(MAXXSEC - (MAXXSEC-MINXSEC)*float(i)/\
                                         float(NXSEC-1), 6) > 0]
    print 'MINXSEC', MINXSEC, 'MAXXSEC', MAXXSEC
    print XSECRANGE
