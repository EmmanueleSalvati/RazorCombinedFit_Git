"""Make 2D histgram of data and of background PDF"""
import ROOT as rt
import sys
from array import array
from math import sqrt


def getBinning():
    """binning for the smoothening and for combine"""
    # 180 bins
    # MRbins = [470., 480., 490., 510., 530., 550., 600., 700., 800., 1000.,
    #           4000.]
    # Rsqbins = [0.11, 0.12, 0.13, 0.16, 0.20, 0.30, 0.50, 0.70, 1.1, 1.5]

    MRbins = [450, 600, 750, 900, 1200, 1600, 4000]
    Rsqbins = [0.10, 0.13, 0.20, 0.30, 0.41, 0.52, 0.64, 1.5]

    nBtagbins = [1, 2, 3, 4]
    return MRbins, Rsqbins, nBtagbins


def setCanvasStyle(c):
    """Canvas margins"""
    c.SetRightMargin(0.15)
    c.SetBottomMargin(0.15)


def binnedHisto2D(tree, binsX, binsY, label=''):
    """Make histogram from the binning
    !!!Currently not using this function!!!"""
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


def fillHistFromToy(histos, myTree):
    """Fills the 2D histo with the content of the bins in myTree
    !!!Currently unused!!!"""
    for nb in range(0, len(histos)):
        histos[nb].Reset()
        for mr in range(0, histos[nb].GetNbinsX()-1):
            for rsq in range(0, histos[nb].GetNbinsY() - 1):
                myTree.Draw("b%s_%s_%s" % (mr, rsq, nb+1))
                htemp = rt.gPad.GetPrimitive('htemp')
                mean = htemp.GetMean()
                rms = htemp.GetRMS()
                print mean, rms
                histos[nb].SetBinContent(mr+1, rsq+1, mean)
                histos[nb].SetBinError(mr+1, rsq+1, rms)


def make2DProjection(histo, nb=None):
    """Project the 3D into 2D; if nb is given, consider only that b-tag,
    otherwise simply Project3D"""

    if nb is None:
        histo_2d = histo.Project3D('yxe')
        histo_2d.SetName(histo.GetName() + '_2D')
        histo_2d.SetTitle(histo.GetTitle() + '_2D')
    else:
        x = array('d', getBinning()[0])
        y = array('d', getBinning()[1])
        histo_2d = rt.TH2D(histo.GetName() + '_2D',
                           histo.GetTitle() + '_2D',
                           len(x)-1, x, len(y)-1, y)
        for i in range(1, len(x)):
            for j in range(1, len(y)):
                histo_2d.SetBinContent(i, j, histo.GetBinContent(i, j, nb))
    return histo_2d


def significanceHist(data, bkg, signal=None):
    """Given two (or three) histograms, return a significance histogram"""
    sign_hist = data.Clone("sig_hist")
    sign_hist.Reset()
    if signal is None:
        for mr in range(1, sign_hist.GetNbinsX() + 1):
            for rsq in range(1, sign_hist.GetNbinsY() + 1):
                obs = data.GetBinContent(mr, rsq)
                exp = bkg.GetBinContent(mr, rsq)
                if obs > 0:
                    sign_hist.SetBinContent(mr, rsq, (obs - exp) / sqrt(obs))
    else:
        for mr in range(1, sign_hist.GetNbinsX() + 1):
            for rsq in range(1, sign_hist.GetNbinsY() + 1):
                obs = data.GetBinContent(mr, rsq)
                exp = bkg.GetBinContent(mr, rsq)
                sig = signal.GetBinContent(mr, rsq)
                if obs > 0:
                    sign_hist.SetBinContent(mr, rsq,
                                            (obs - sig - exp) / sqrt(obs))

    hist_max = sign_hist.GetBinContent(sign_hist.GetMaximumBin())
    hist_min = sign_hist.GetBinContent(sign_hist.GetMinimumBin())
    if abs(hist_min) > hist_max:
        sign_hist.SetMaximum(-1 * hist_min)
    else:
        sign_hist.SetMinimum(-1 * hist_max)
    return sign_hist


def setHistRange(histo):
    """set min and max of a histogram according to which is bigger
    !!!Currently unused!!!"""

    minH = histo.GetMinimum()
    maxH = histo.GetMaximum()
    if abs(minH) > maxH:
        histo.SetMaximum(abs(minH))
    else:
        histo.SetMinimum(-1 * maxH)


def writeBinCount(histo_2d):
    """Write the numbers on the 2D histogram"""

    tlatexList = []
    for iBinX in range(1, histo_2d.GetNbinsX() + 1):
        for iBinY in range(1, histo_2d.GetNbinsY() + 1):
            binCount = histo_2d.GetBinContent(iBinX, iBinY)
            if binCount == -999 or abs(binCount) < 0.1:
                continue
            elif binCount >= 0:
                xBin = histo_2d.GetXaxis().GetBinLowEdge(iBinX) +\
                    0.25 * histo_2d.GetXaxis().GetBinWidth(iBinX)
                yBin = histo_2d.GetYaxis().GetBinLowEdge(iBinY) + \
                    0.30 * histo_2d.GetYaxis().GetBinWidth(iBinY)
            elif binCount < 0:
                xBin = histo_2d.GetXaxis().GetBinLowEdge(iBinX) + \
                    0.1 * histo_2d.GetXaxis().GetBinWidth(iBinX)
                yBin = histo_2d.GetYaxis().GetBinLowEdge(iBinY) + \
                    0.3 * histo_2d.GetYaxis().GetBinWidth(iBinY)
            if abs(binCount) < 0.1:
                tlatex = rt.TLatex(xBin, yBin, "%1.3f" % binCount)
            elif binCount < 10:
                tlatex = rt.TLatex(xBin, yBin, "%2.1f" % binCount)
            else:
                tlatex = rt.TLatex(xBin, yBin, "%i" % binCount)
            tlatex.SetTextSize(0.03)
            tlatex.SetTextFont(42)
            tlatexList.append(tlatex)

    return tlatexList


if __name__ == '__main__':
    rt.gStyle.SetOptStat(0)
    rt.gSystem.Load("../lib/libRazor.so")

    inFile = rt.TFile.Open(sys.argv[1], 'READ')
    box = (sys.argv[1].split('_')[-1])[:-5]

    # Signal pdf
    if len(sys.argv) > 3:
        refXsecFile = "./gluino.root"
        stopFile = rt.TFile.Open(refXsecFile, "READ")
        stopHistName = refXsecFile.split("/")[-1].split(".")[0]
        stopHist = stopFile.Get(stopHistName)
        refXsec = 1.e3 * stopHist.GetBinContent(stopHist.FindBin(875.))

        sigFile = rt.TFile.Open(sys.argv[3], 'READ')
        signal_all = sigFile.Get('wHisto')
        sigNorm = signal_all.Integral()
        sigEvents = sigNorm * 19.3 * refXsec
        print 'INFO: now multiplying efficiency * lumi * refXsec = ',\
            '%f * %f * %f = %f events' % (sigNorm, 19.3, refXsec, sigEvents)
        signal_all.Scale(sigEvents / signal_all.Integral())
        signal = [make2DProjection(signal_all, i) for i in range(1, 4)]
        signal_all_2d = make2DProjection(signal_all)
        signal_all_2d.SetName('signal')
        signal_all_2d.SetTitle('All b-tag bins')
        [signal[i].SetName('signal') for i in range(3)]
        [signal[i].SetTitle('nb=%i' % (i+1)) for i in range(3)]

    # Background pdf
    bkg_pdf_all = inFile.Get('BJetLS/histo3DToy_MRRsqBtag_FULL_ALLCOMPONENTS')
    bkg_pdf = [make2DProjection(bkg_pdf_all, i) for i in range(1, 4)]
    bkg_pdf_2d = make2DProjection(bkg_pdf_all)
    [bkg_pdf[i].SetName('background') for i in range(3)]
    [bkg_pdf[i].SetTitle('nb=%i' % (i+1)) for i in range(3)]

    # Get pdf values from toy file
    toyFile = rt.TFile.Open(sys.argv[2], 'READ')
    toyTree = toyFile.Get("myTree")
    # fillHistFromToy(bkg_pdf, toyTree)

    blatexList = [writeBinCount(bkg_pdf[i]) for i in range(3)]
    c = rt.TCanvas("2Dplots/bkg_%s" % box, "bkg_%s" % box, 5)
    c.Divide(2, 2)
    for i in range(3):
        c.cd(i+1)
        rt.gPad.SetRightMargin(0.15)
        rt.gPad.SetBottomMargin(0.15)
        rt.gPad.SetLogx()
        rt.gPad.SetLogy()
        bkg_pdf[i].Draw("colz")
        for tlatex in blatexList[i]:
            tlatex.Draw()
    c.SaveAs(c.GetName() + ".pdf")

    # Data set
    data_all = inFile.Get('BJetLS/histo3DData_MRRsqBtag_FULL_ALLCOMPONENTS')
    data_obs = [make2DProjection(data_all, i) for i in range(1, 4)]
    data_all_2d = make2DProjection(data_all)
    [data_obs[i].SetName('data_obs') for i in range(3)]
    [data_obs[i].SetTitle('nb=%i' % (i+1)) for i in range(3)]

    latexList = [writeBinCount(data_obs[i]) for i in range(3)]

    c1 = rt.TCanvas("2Dplots/data_%s" % box,
                    "data_%s" % box, 5)
    c1.Divide(2, 2)
    for i in range(3):
        c1.cd(i+1)
        rt.gPad.SetRightMargin(0.15)
        rt.gPad.SetBottomMargin(0.15)
        rt.gPad.SetLogx()
        rt.gPad.SetLogy()
        data_obs[i].Draw("colz")
        for tlatex in latexList[i]:
            tlatex.Draw()

    c1.SaveAs(c1.GetName() + ".pdf")

    if len(sys.argv) > 3:
        siglatexList = [writeBinCount(signal[i]) for i in range(3)]

        sigPad = rt.TCanvas("2Dplots/signal_%s" % box,
                            "signal_%s" % box)
        setCanvasStyle(sigPad)
        sigPad.Divide(2, 2)
        for i in range(3):
            sigPad.cd(i+1)
            rt.gPad.SetRightMargin(0.15)
            rt.gPad.SetBottomMargin(0.15)
            rt.gPad.SetLogx()
            rt.gPad.SetLogy()
            signal[i].Draw('colz')
            for siglatex in siglatexList[i]:
                siglatex.Draw()
        siglatexList_all = writeBinCount(signal_all_2d)
        sigPad.cd(4)
        rt.gPad.SetRightMargin(0.15)
        rt.gPad.SetBottomMargin(0.15)
        rt.gPad.SetLogx()
        rt.gPad.SetLogy()
        signal_all_2d.Draw('colz')
        for siglatex_2d in siglatexList_all:
            siglatex_2d.Draw()
        sigPad.SaveAs(sigPad.GetName() + ".pdf")
        diff_all = significanceHist(data_all_2d, bkg_pdf_2d, signal_all_2d)
        diff_all.SetTitle("(data - (sig + bkg)) / sqrt(data), all b-tag bins")
        diff = [significanceHist(data_obs[i], bkg_pdf[i], signal[i])
                for i in range(3)]
        [diff[i].SetTitle("(data - (sig + bkg)) / sqrt(data), nb=%i" % (i+1))
            for i in range(3)]
        d = rt.TCanvas("2Dplots/difference_withSig_%s" % box,
                       "difference_withSig_%s" % box)

    else:
        diff_all = significanceHist(data_all_2d, bkg_pdf_2d)
        diff_all.SetTitle('(data - bkg) / sqrt(data), all b-tag bins')
        diff = [significanceHist(data_obs[i], bkg_pdf[i]) for i in range(3)]
        [diff[i].SetTitle("(data - bkg) / sqrt(data), nb=%i" % (i+1))
            for i in range(3)]
        d = rt.TCanvas("2Dplots/difference_%s" % box, "difference_%s" % box)

    d.Divide(2, 2)
    latexList = [writeBinCount(diff[i]) for i in range(3)]

    Red = array('d', [0.00, 0.70, 0.90, 1.00, 1.00, 1.00, 1.00])
    Green = array('d', [0.00, 0.70, 0.90, 1.00, 0.90, 0.70, 0.00])
    Blue = array('d', [1.00, 1.00, 1.00, 1.00, 0.90, 0.70, 0.00])
    # colors get darker faster at 4sigma
    Length = array('d', [0.00, 0.20, 0.35, 0.50, 0.65, 0.8, 1.00])
    rt.TColor.CreateGradientColorTable(7, Length, Red, Green, Blue, 999)

    for i in range(3):
        d.cd(i+1)
        rt.gPad.SetRightMargin(0.15)
        rt.gPad.SetBottomMargin(0.15)
        rt.gPad.SetLogx()
        rt.gPad.SetLogy()
        diff[i].Draw("colz")
        for tlatex in latexList[i]:
            tlatex.Draw()
    d.cd(4)
    rt.gPad.SetRightMargin(0.15)
    rt.gPad.SetBottomMargin(0.15)
    rt.gPad.SetLogx()
    rt.gPad.SetLogy()
    difflatex_all = writeBinCount(diff_all)
    diff_all.Draw('colz')
    for dlatex in difflatex_all:
        dlatex.Draw()
    d.SaveAs(d.GetName() + ".pdf")

    outFile = rt.TFile.Open("2Dplots/wtf.root", "RECREATE")
    [data_obs[i].Write() for i in range(3)]
    [bkg_pdf[i].Write() for i in range(3)]
    outFile.Close()
