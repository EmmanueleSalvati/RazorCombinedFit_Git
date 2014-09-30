"""Get cross sections to scan from the asymptotic limit"""

import ROOT as rt
from array import array


def xsecs_to_scan(mglu, asymfile=None, refxsecfile=None):
    """For a given (mg, mchi) point, returns the xsecs to scan"""

    x_xsec = []
    xsec_range = []

    if asymfile is not None:
        model = 'T2tt'
        box = 'BJetHS'
        exp = asymfile.Get("xsecUL_Exp_%s_%s" % (model, box))
        exp_xsec = exp.GetBinContent(exp.FindBin(mglu))
        for i in range(-3, 4):
            for j in range(1, 10, 3):
                xsec_range.append(exp_xsec * pow(10, int(i)) * int(j))
                x_xsec.append(mglu)

    elif refxsecfile is not None:
        susy = refxsecfile.Get("stop")
        susy_xsec = susy.GetBinContent(susy.FindBin(mglu))
        for i in range(-2, 1):
            for j in [1] + range(2, 5, 2):
                if i == 1 and mglu >= 300.:
                    continue
                elif i == -2 and mglu >= 500.:
                    continue
                x_xsec.append(mglu)
                xsec_range.append(susy_xsec * pow(10, i) * j)

    else:
        xsec_range = [0, 1]
    return x_xsec, xsec_range


if __name__ == '__main__':
    ASYMPTOTIC = rt.TFile.Open("asymptoticFile_T2tt_BJetHS.root")
    SUSY_XSEC = rt.TFile.Open("stop.root")

    LIST_X = []
    LIST_XSEC = []

    for mass in range(150, 800, 25):
        # my_x, my_range = xsecs_to_scan(mass, ASYMPTOTIC)
        my_x, my_range = xsecs_to_scan(mass, None, SUSY_XSEC)
        LIST_X = LIST_X + my_x
        LIST_XSEC = LIST_XSEC + my_range

    print len(LIST_X)
    print len(LIST_XSEC)

    ARRAY_X = array("d", LIST_X)
    ARRAY_XSEC = array("d", LIST_XSEC)

    C1 = rt.TCanvas("WTF", "WTF", 200, 10, 700, 500)
    C1.SetLogy()
    GR = rt.TGraph(len(ARRAY_X), ARRAY_X, ARRAY_XSEC)
    GR.Draw("AC*")
    C1.Print("wtf.pdf")
    RF = rt.TFile.Open("wtf.root", "recreate")
    GR.Write()
    RF.Close()
