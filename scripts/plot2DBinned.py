"""Reproducing Javier's plots"""
import ROOT as rt
import os.path
import sys
from array import array


def get_refXsec(mglu, refxsecfile='stop.root'):
    """Return the SUSY xsec for a given mass point"""
    root_file = rt.TFile.Open(refxsecfile)
    susy = root_file.Get("stop")
    return susy.GetBinContent(susy.FindBin(mglu))


def get_binnings():
    """Return the bin arrays"""
    # 180 bins
    mr_bins = array('d', [450., 470., 490., 510., 530., 550., 600., 700.,
                          800., 1000., 4000.])
    rsq_bins = array('d', [0.10, 0.20, 0.30, 0.50, 0.70, 1.1, 1.5])

    # 72 bins
    # mr_bins = array('d', [450., 500., 550, 600., 800., 1000., 4000.])
    # rsq_bins = array('d', [0.10, 0.35, 0.70, 1.1, 1.5])

    # 672 bins
    # mr_bins = array('d', [450.0, 600.0, 750.0, 900.0, 1200.0, 1600.0, 4000.0])

    # rsq_bins = array('d', [0.1, 0.13, 0.2, 0.3, 0.41, 0.52, 0.64, 1.5])

    # mr_bins = array('d', [450., 470., 490., 510., 530., 550, 575., 600., 625.,
    #                       650., 700., 800., 900., 1000., 4000.])
    # rsq_bins = array('d', [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17,
    #                        0.20, 0.23, 0.26, 0.30, 0.35, 0.40, 0.50,
    #                        0.7, 1.0, 1.5])

    return mr_bins, rsq_bins


def get_coarse_binning(bin_array):
    """Return the coarse bin array"""
    coarse_bins = array('d')

    for i in bin_array:
        if bin_array.index(i) % 2 != 0 and\
           bin_array.index(i) != 0 and bin_array.index(i) != len(bin_array)-1:
            continue
        else:
            coarse_bins.append(i)
    return coarse_bins


def rebin3dCoarse(oldhisto, xCoarse, yCoarse, xFine, yFine):
    """Reproducing Javier's function"""

    z_array = array('d', [1., 2., 3., 4.])

    print xCoarse
    print xFine
    print yCoarse
    print yFine
    newhistoCoarse = rt.TH3D(oldhisto.GetName()+"_coarse",
                             oldhisto.GetTitle()+"_coarse",
                             len(xCoarse)-1, xCoarse,
                             len(yCoarse)-1, yCoarse,
                             len(z_array)-1, z_array)
    newhistoCounts = rt.TH3D(oldhisto.GetName()+"_counts",
                             oldhisto.GetTitle()+"_counts",
                             len(xCoarse)-1, xCoarse,
                             len(yCoarse)-1, yCoarse,
                             len(z_array)-1, z_array)
    newhisto = rt.TH3D(oldhisto.GetName()+"_fine",
                       oldhisto.GetTitle()+"_fine",
                       len(xFine)-1, xFine,
                       len(yFine)-1, yFine,
                       len(z_array)-1, z_array)

    for i in range(1, oldhisto.GetNbinsX()+1):
        for j in range(1, oldhisto.GetNbinsY()+1):
            for k in range(1, oldhisto.GetNbinsZ()+1):
                xold = oldhisto.GetXaxis().GetBinCenter(i)
                yold = oldhisto.GetYaxis().GetBinCenter(j)
                zold = oldhisto.GetZaxis().GetBinCenter(k)
                oldbincontent = oldhisto.GetBinContent(i, j, k)
                newhistoCoarse.Fill(xold, yold, zold, max(0., oldbincontent))
                newhistoCounts.Fill(xold, yold, zold)

    for i in range(1, newhisto.GetNbinsX()+1):
        for j in range(1, newhisto.GetNbinsY()+1):
            for k in range(1, newhisto.GetNbinsZ()+1):
                newhisto.SetBinContent(i, j, k, 0.)
                xnew = newhisto.GetXaxis().GetBinCenter(i)
                ynew = newhisto.GetYaxis().GetBinCenter(j)
                znew = newhisto.GetZaxis().GetBinCenter(k)
                newYield = newhistoCoarse.GetBinContent(newhistoCoarse.FindBin(
                    xnew, ynew, znew))
                numBins = newhistoCounts.GetBinContent(newhistoCounts.FindBin(
                    xnew, ynew, znew))
                newhisto.SetBinContent(i, j, k, newYield/numBins)

    print newhistoCoarse.Integral()
    print newhistoCounts.Integral()
    return newhisto, newhistoCoarse


def binnedHisto2D(tree, binsX, binsY, efficiency=1, mass=400):
    """Make histogram"""
    z_bins = array('d', [1., 2., 3., 4.])

    histo = rt.TH3D("histo", "histo",
                    len(binsX)-1, binsX, len(binsY)-1, binsY,
                    len(z_bins)-1, z_bins)

    for i_binx in range(0, len(binsX) - 1):
        for i_biny in range(0, len(binsY) - 1):
            for i_binz in range(0, len(z_bins) - 1):
                binx = binsX[i_binx]
                binx_p1 = binsX[i_binx+1]
                biny = binsY[i_biny]
                biny_p1 = binsY[i_biny+1]
                binz = z_bins[i_binz]
                binz_p1 = z_bins[i_binz+1]
                numEntries = (tree.reduce("MR > %s && MR < %s "
                                          "&& Rsq > %s && Rsq < %s "
                                          "&& nBtag >= %s && nBtag < %s" %
                                          (binx, binx_p1, biny, biny_p1,
                                           binz, binz_p1)).
                              numEntries())
                histo.Fill(binx, biny, binz, numEntries)
    histo.Scale(19300. * efficiency * get_refXsec(mass) / histo.Integral())
    return histo, histo.Project3D("yxe")


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    rt.gStyle.SetPaintTextFormat("5.2f")

    # ####### Get Arguments
    box = sys.argv[1]
    mLSP = int(sys.argv[2])
    directory = sys.argv[3]

    MRbins, Rsqbins = get_binnings()
    # Coarse_MR_bins = get_coarse_binning(MRbins)
    # Coarse_Rsq_bins = get_coarse_binning(Rsqbins)
    Coarse_MR_bins = array('d', [450., 490., 530., 600., 800., 4000.])
    Coarse_Rsq_bins = array('d', [0.10, 0.30, 0.70, 1.1, 1.5])

    # print MRbins, Rsqbins, Coarse_MR_bins, Coarse_Rsq_bins

    histoRsqs = {}
    histoMRs = {}
    files = {}
    trees = {}

    for mStop in range(450, 475, 25):  # 825, 25):
        filename = directory + 'SMS-T2tt_mStop-Combo_mLSP_' + str(mLSP) +\
            '.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_' +\
            'MR450.0_R0.316227766017_' +\
            str(mStop) + '.0_' + str(mLSP) + '.0_' + box + '.root'

        if not os.path.exists(filename):
            continue

        files[filename] = rt.TFile(filename)
        trees[filename] = files[filename].Get("RMRTree")
        wHisto = files[filename].Get("wHisto")
        eff = wHisto.Integral()
        print 'eff', eff

        # c = rt.TCanvas("2Dplots/RsqMR2D_mStop%s_mLSP%s_box%s.png" %
        #                (mStop, mLSP, box), "RsqMR2D_mStop%s_mLSP%s_box%s.png" %
        #                (mStop, mLSP, box))
        c = rt.TCanvas("RsqMR2D_mStop%s_mLSP%s_box%s" %
                       (mStop, mLSP, box), "RsqMR2D_mStop%s_mLSP%s_box%s" %
                       (mStop, mLSP, box))

        c.cd()
        c.SetLogx()
        c.SetLogy()
        histo3d, histo = binnedHisto2D(trees[filename], MRbins, Rsqbins, eff,
                                       mStop)
        histo.SetTitle("Rsq vs MR, mStop = %s, mLSP = %s, signal, %s box;"
                       "MR(GeV);Rsq" % (mStop, mLSP, box))
        histo.Draw("colzTEXT")

        c.Print(c.GetName() + '.pdf(')
        fine_histo, coarse_histo = rebin3dCoarse(
            histo3d, Coarse_MR_bins, Coarse_Rsq_bins, MRbins, Rsqbins)

        coarse_histo.Project3D("yxe").Draw("colzTEXT")
        c.Print(c.GetName() + '.pdf')

        fine_histo.Project3D("yxe").Draw("colzTEXT")
        c.Print(c.GetName() + '.pdf)')
