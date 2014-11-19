"""Plot run B, C and D separately"""
import ROOT as rt
import RootTools
import sys


def run_color(run):
    """Giving a run, it returns the color of the histogram"""
    color = {dsB: rt.RooFit.kGreen, dsC: rt.RooFit.kRed,
             dsD: rt.RooFit.kBlack}
    return color[run]


def get_pads():
    """Return two pads for the current canvas"""
    Tpad1 = rt.TPad("pad1", "pad1", 0, 0.35, 1, 1)
    Tpad2 = rt.TPad("pad2", "pad2", 0, 0, 1, 0.35)
    Tpad1.Range(-213.4588, -0.3237935, 4222.803, 5.412602)
    Tpad2.Range(-213.4588, -5.206896, 4222.803, 3.241379)
    Tpad1.SetLeftMargin(0.15)
    Tpad2.SetLeftMargin(0.15)
    Tpad1.SetRightMargin(0.05)
    Tpad2.SetRightMargin(0.05)
    Tpad1.SetTopMargin(0.05)
    Tpad2.SetTopMargin(0.)
    Tpad1.SetBottomMargin(0.)
    Tpad2.SetBottomMargin(0.27)

    return (Tpad1, Tpad2)


def make_histogram(var, run):
    """Make histogram from RooRealVar for RooDataSet run"""

    my_histo = var.createHistogram("", "Events")
    # my_histo.SetTitle(var.GetTitle())
    my_histo.SetTitle("")
    run.fillHistogram(my_histo, rt.RooArgList(var))
    my_histo.Scale(1./my_histo.Integral())
    my_histo.SetMarkerStyle(20)
    my_histo.SetMarkerSize(0.7)
    my_histo.SetMarkerColor(run_color(run))
    my_histo.SetLineColor(run_color(run))
    return my_histo


def make_ratio_hist(run1, run2):
    """Given two hists, it returns their ratio"""
    ratio = run1.Clone()
    ratio.GetXaxis().SetTitleSize(0.13)
    ratio.GetXaxis().SetLabelSize(0.13)
    ratio.GetYaxis().SetTitleSize(0.13)
    ratio.GetYaxis().SetLabelSize(0.09)
    ratio.SetTitle("")
    ratio.Divide(run2)
    ratio.SetMaximum(5)

    return ratio


def add_legend(run1, run2):
    """Create a TLegend"""

    title = {dsB_MR: "Run B", dsB_Rsq: "Run B",
             dsC_MR: "Run C", dsC_Rsq: "Run C",
             dsD_MR: "Run D", dsD_Rsq: "Run D"}

    leg = rt.TLegend(0.7, 0.5, 0.93, 0.93)
    leg.AddEntry(run1, title[run1])
    leg.AddEntry(run2, title[run2])

    return leg

if __name__ == '__main__':

    rt.gStyle.SetOptStat(0)
    dsB = RootTools.getDataSet(sys.argv[1], 'RMRTree')
    dsC = RootTools.getDataSet(sys.argv[2], 'RMRTree')
    dsD = RootTools.getDataSet(sys.argv[3], 'RMRTree')

    MR = rt.RooRealVar("MR", "MR", 400., 2000.)
    Rsq = rt.RooRealVar("Rsq", "Rsq", 0.08, 1.)
    nBtag = rt.RooRealVar("nBtag", "nBtag", 1.0, 5.0)

    dsB_MR = make_histogram(MR, dsB)
    dsC_MR = make_histogram(MR, dsC)
    dsD_MR = make_histogram(MR, dsD)
    dsB_Rsq = make_histogram(Rsq, dsB)
    dsC_Rsq = make_histogram(Rsq, dsC)
    dsD_Rsq = make_histogram(Rsq, dsD)

    # RunD V RunB
    mr_canvas = rt.TCanvas("mr_canvas", "mr_canvas")
    (pad1, pad2) = get_pads()
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    rt.gPad.SetLogy()
    dsD_MR.Draw("E1")
    dsB_MR.Draw("E1 SAME")
    leg = add_legend(dsB_MR, dsD_MR)
    leg.Draw()

    pad2.cd()
    dsB_dsD = make_ratio_hist(dsB_MR, dsD_MR)
    dsB_dsD.Draw()
    line = rt.TLine(400., 1., 2000, 1.)
    line.SetLineColor(rt.RooFit.kBlack)
    line.Draw()
    mr_canvas.SaveAs("MR_RunBD.pdf")
    del mr_canvas, pad1, pad2, dsB_dsD

    rsq_canvas = rt.TCanvas("rsq_canvas", "rsq_canvas")
    (pad1, pad2) = get_pads()
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    rt.gPad.SetLogy()
    dsD_Rsq.Draw("E1")
    dsB_Rsq.Draw("E1 SAME")
    leg.Draw()

    pad2.cd()
    dsB_dsD = make_ratio_hist(dsB_Rsq, dsD_Rsq)
    dsB_dsD.Draw()
    line = rt.TLine(0.08, 1., 1., 1.)
    line.SetLineColor(rt.RooFit.kBlack)
    line.Draw()
    rsq_canvas.SaveAs("Rsq_RunBD.pdf")
    del rsq_canvas, pad1, pad2, dsB_dsD, leg

    # RunD V RunC
    mr_canvas = rt.TCanvas("mr_canvas", "mr_canvas")
    (pad1, pad2) = get_pads()
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    rt.gPad.SetLogy()
    dsD_MR.Draw("E1")
    dsC_MR.Draw("E1 SAME")
    leg = add_legend(dsC_MR, dsD_MR)
    leg.Draw()

    pad2.cd()
    dsC_dsD = make_ratio_hist(dsC_MR, dsD_MR)
    dsC_dsD.Draw()
    line = rt.TLine(400., 1., 2000, 1.)
    line.SetLineColor(rt.RooFit.kBlack)
    line.Draw()
    mr_canvas.SaveAs("MR_RunCD.pdf")
    del mr_canvas, pad1, pad2

    rsq_canvas = rt.TCanvas("rsq_canvas", "rsq_canvas")
    (pad1, pad2) = get_pads()
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    rt.gPad.SetLogy()
    dsD_Rsq.Draw("E1")
    dsC_Rsq.Draw("E1 SAME")
    leg.Draw()

    pad2.cd()
    dsC_dsD = make_ratio_hist(dsC_Rsq, dsD_Rsq)
    dsC_dsD.Draw()
    line = rt.TLine(0.08, 1., 1., 1.)
    line.SetLineColor(rt.RooFit.kBlack)
    line.Draw()
    rsq_canvas.SaveAs("Rsq_RunCD.pdf")
    del rsq_canvas, pad1, pad2, dsC_dsD
