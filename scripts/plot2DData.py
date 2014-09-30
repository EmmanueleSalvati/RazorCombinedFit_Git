"""Make 2D histgram of data"""
import ROOT as rt
import sys
from array import array


def binnedHisto2D(tree, binsX, binsY, label=''):
    """Make histogram from the binning"""
    histo = rt.TH2F("histo"+label, "histo"+label, len(binsX)-1, binsX,
                    len(binsY)-1, binsY)

    for i_binx in range(0, len(binsX) - 1):
        for i_biny in range(0, len(binsY) - 1):

            binx = binsX[i_binx]
            binx_p1 = binsX[i_binx+1]
            biny = binsY[i_biny]
            biny_p1 = binsY[i_biny+1]

            numEntries = (tree.reduce("MR > %s && MR < %s && Rsq > %s "
                                      "&& Rsq < %s && nBtag < 2" %
                                      (binx, binx_p1, biny, biny_p1)).
                          numEntries())
            histo.Fill(binx, biny, numEntries)

    return histo


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)

    box = sys.argv[1]

    MRbins = array('d', [450., 470., 490., 510., 530., 550, 575., 600., 625.,
                         650., 700., 800., 900., 1000., 4000.])
    Rsqbins = array('d', [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17,
                          0.20, 0.23, 0.26, 0.30, 0.35, 0.40, 0.50,
                          0.7, 1.0, 1.5])

    filename = 'Datasets/Parked_%s.root' % box

    file = rt.TFile(filename)
    tree = file.Get("RMRTree")

    c = rt.TCanvas("2Dplots/RsqMR2D_%s.png" % box, "RsqMR2D_%s.png" % box)

    c.cd()
    c.SetLogx()
    c.SetLogy()
    histo = binnedHisto2D(tree, MRbins, Rsqbins, '')
    histo.SetTitle("Rsq vs MR, %s box;MR(GeV);Rsq" % (box))
    histo.Draw("colz")
    c.SaveAs(c.GetName())
