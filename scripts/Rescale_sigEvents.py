"""Rescale signal histogram to number of events"""

import ROOT as rt
import sys


def get_xsec(stop_file, mglu):
    """return the cross section to normalize to"""
    susy = stop_file.Get("stop")
    return susy.GetBinContent(susy.FindBin(mglu))


if __name__ == '__main__':
    sig_file = sys.argv[1]
    stop_root = rt.TFile.Open("stop.root")
    LUMI = 19300
    XSEC = get_xsec(stop_root, 400)

    root_file = rt.TFile.Open(sig_file)
    efficiency = root_file.Get("wHisto").Integral()
    sigEvents = efficiency * LUMI * XSEC

    before = root_file.Get("wHisto")
    before.SetTitle("Before rebinning")
    before.Scale(sigEvents / efficiency)

    out_file = rt.TFile.Open("signal_files.root", 'RECREATE')
    before.Write()
    out_file.Close()
