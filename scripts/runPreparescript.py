"""This module is to prepare the input script to combine"""
import os
from optparse import OptionParser


if __name__ == '__main__':

    PARSER = OptionParser()
    PARSER.add_option('-c', '--config', dest='config', type='string',
                      default=None, help='Name of the config file to use')
    PARSER.add_option('-i', '--input', dest='input', metavar='FILE',
                      default=None, help='Input fit results file to read\
                      results and workspace from')
    PARSER.add_option('-b', '--box', dest='box', default='Ele', type='string',
                      help='Specify the box')
    PARSER.add_option('-s', '--signal-file', dest='signal_file', default=None,
                      metavar='FILE', help="SMS input dataset")

    (OPTIONS, ARGS) = parser.parse_args()

    strengthMod = ''
    NJETS = '4jets'
    BOX = OPTIONS.box
    name = 'Ele_4jets'
    FIT_RES = OPTIONS.input
    SIG_FILE = OPTIONS.signal_file
    CFG = OPTIONS.config

    SUSY_XSEC = {150: 80.268,
                 175: 36.7994,
                 200: 18.5245,
                 225: 9.90959,
                 250: 5.57596,
                 275: 3.2781,
                 300: 1.99608,
                 325: 1.25277,
                 350: 0.807323,
                 375: 0.531443,
                 400: 0.35683,
                 425: 0.243755,
                 450: 0.169688,
                 475: 0.119275,
                 500: 0.0855847,
                 525: 0.0618641,
                 550: 0.0452067,
                 575: 0.0333988,
                 600: 0.0248009,
                 625: 0.0185257,
                 650: 0.0139566,
                 675: 0.0106123,
                 700: 0.0081141,
                 725: 0.00623244,
                 750: 0.00480639,
                 775: 0.00372717}

    for mass in range(150, 800, 25):

        #SUSY_XSEC[mass]  = 100.
        SUSY_XSEC[mass] *= 1000.
        # os.system("python prepareCombineWorkspace.py --box %s\
        #   -i /home/uscms208/cms/RazorCombinedFit_Git/fit_results/razor_Single%s3D_%s_%s_FULL.root --xsec %s\
        #   -c /home/uscms208/cms/RazorCombinedFit_Git/config/RazorMultiJet2013_3D_hybrid.config\
        #   /home/uscms208/cms/RazorCombinedFit_Git/Datasets/T2tt%s%s/mLSP25/SMS-T2tt_mStop-Combo_mLSP_25.0_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_MR350.0_R0.282842712475_%s.0_25.0_%s.root"\
        #   % (name, BOX, NJETS, BOX, str(SUSY_XSEC[mass]), BOX, NJETS, mass, BOX))
        os.system("python prepareCombineWorkspace.py --box %s\
                  -i %s --xsec %s -c %s -s %s"\
                  % (BOX, FIT_RES, str(SUSY_XSEC[mass]), CFG, SIG_FILE))
        os.system("combine -M Asymptotic razor_combine_%s_%s_T2tt_%s.0_25.0.txt\
                  -n T2tt_%s_25_%s_%s"\
                  % (BOX, NJETS, mass, mass, BOX, NJETS))
        os.system("mkdir -p combine_files_%s_%s" % (NJETS, BOX))
        os.system("mv razor_combine* combine_files_%s_%s" % (NJETS, BOX))
        os.system("mv higgsCombine* combine_files_%s_%s" % (NJETS, BOX))
        os.system("rm roostats*")
