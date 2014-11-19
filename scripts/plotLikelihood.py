"""Script to plot the profile likelihood w.r.t one parameter"""
import ROOT as rt
from optparse import OptionParser

if __name__ == '__main__':
    usage = ('\n\npython scripts/%prog inputFile parameter\nwhere inputFile '
             'is the root '
             'fit results file,\nand parameter is the parameter to profile '
             'the likelihood in')
    PARSER = OptionParser(usage=usage)
    (OPTIONS, ARGS) = PARSER.parse_args()

    rt.gSystem.Load("../lib/libRazor.so")
    my_file = rt.TFile.Open(ARGS[0])
    box_name = ARGS[0][:-5].split('_')[-1]
    my_wspace = my_file.Get(box_name + '/Box' + box_name + '_workspace')

    n_TTj2b = my_wspace.var("n_TTj2b")
    nll = my_wspace.pdf("fitmodel").createNLL(my_wspace.data("RMRTree"),
                                              rt.RooFit.NumCPU(2))
    rt.RooMinuit(nll).migrad()
    c = rt.TCanvas()
    nframe = n_TTj2b.frame(100., 120.)
    nll.plotOn(nframe)
    nframe.Draw()
    # pnll = nll.createProfile(rt.RooArgSet(n_TTj2b))
    # pnll.plotOn(nframe, rt.RooFit.LineColor(rt.kRed))
    # nframe.Draw()
    c.SaveAs("wtfdoiknow.png")
