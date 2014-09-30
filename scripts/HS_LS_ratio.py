"""Ratio of HS/LS expected UL limit"""

import sys
import ROOT as rt

if __name__ == '__main__':
    HSFILE = rt.TFile.Open(sys.argv[1])
    LSFILE = rt.TFile.Open(sys.argv[2])

    HS_HIST = HSFILE.Get("xsecUL_Exp_T2tt_BJetHS")
    LS_HIST = LSFILE.Get("xsecUL_Exp_T2tt_BJetLS")
    rt.gStyle.SetOptStat(0)

    C1 = rt.TCanvas()
    RATIO = HS_HIST.Clone()
    RATIO.Divide(LS_HIST)
    RATIO.SetTitleFont(42)
    RATIO.SetTitle("Ratio expected UL High Purity / Low Purity")
    RATIO.SetMinimum(-0.1)
    RATIO.GetXaxis().SetTitleFont(42)
    RATIO.GetYaxis().SetTitleFont(42)
    RATIO.GetXaxis().SetLabelFont(42)
    RATIO.GetYaxis().SetLabelFont(42)
    RATIO.GetXaxis().SetTitle("stop mass [GeV]")
    RATIO.GetYaxis().SetTitle("Limits ratio")
    RATIO.GetXaxis().CenterTitle()
    RATIO.GetYaxis().CenterTitle()
    RATIO.SetLineColor(1)
    RATIO.SetLineWidth(3)
    RATIO.Draw()
    HORIZONTAL = rt.TLine(150., 1., 800., 1.)
    HORIZONTAL.SetLineColor(2)
    HORIZONTAL.SetLineStyle(2)
    HORIZONTAL.SetLineWidth(3)
    HORIZONTAL.Draw("same")

    RATIO_FILE = rt.TFile.Open("Asymptotic_limit_ratio.root", 'RECREATE')
    RATIO.Write()
    RATIO_FILE.Close()

    C1.Print("ratio.pdf")
