#! /usr/bin/env python
"""To submit toy jobs on the PBS queues"""

from optparse import OptionParser

import ROOT as rt
import RootTools
from RazorCombinedFit.Framework import Config
import os.path
import sys
import time
import glob

def writeBashScript(box, sideband, fitmode, nToys, nToysPerJob, t,\
                    doToys, doConvertToRoot, doFinalJob):
    pwd = os.environ['PWD']

    fit_results_dir = "fit_results/"
    config = "config/RazorMultiJet2013_3D_FULL.config"

    submit_dir = "submit"

    fit_result_map = {'TTJets': fit_results_dir+'razor_TTJets3D_%s_FULL.root'\
                      %(box),\
                      'BJetHS_Sideband': fit_results_dir +\
                      'fit_result_Sideband_' + box + '.root',
                      'BJetHS_FULL': fit_results_dir +\
                      'fit_result_FULL_' + box + '.root',
                      'BJetLS_FULL': fit_results_dir +\
                      'fit_result_FULL_' + box + '.root',
                      'BJetLS_Sideband': fit_results_dir +\
                      'fit_result_Sideband_' + box + '.root'}

    mr_min = 350.0
    r_min = 0.282842712475

    # label = "MR"+str(mr_min)+"_R"+str(r_min)
    dataset_map = {'TTJets':('Datasets/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-'
                             'madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7C'
                             '-v1-SUSY_MR%s_R%s_gt4jets_BTAG_%s.root') %\
                            (mr_min, r_min, box),
                   'BJetHS_Sideband': 'Datasets/Parked_' + box + '.root',
                   'BJetHS_FULL': 'Datasets/Parked_' + box + '.root',
                   'BJetLS_Sideband': 'Datasets/Parked_' + box + '.root',
                   'BJetLS_FULL': 'Datasets/Parked_' + box + '.root'
                  }
    # print dataset_map
    results_dir = "./toys_files_%s" % datasetName
    toy_dir = results_dir+"/%s_%s" % (sideband, box)
    ffDir = toy_dir+"_FF"

    tagFR = "--"+sideband
    tag3D = "--"+fitmode

    tagPrintPlots = "--printPlots"

    os.system("mkdir -p %s"%(submit_dir))

    output_file = submit_dir + "/submit_" + datasetName +\
                  "_" + box + "_" + str(t) + ".sh"
    outputfile = open(output_file, 'w')
    outputfile.write('#$ -S /bin/sh\n')
    outputfile.write('#$ -l arch=lx24-amd64\n')
    outputfile.write('#$ -m ea\n')
    outputfile.write('#$ -l mem_total=2G\n')
    outputfile.write('#$ -j oe\n\n')

    outputfile.write('export SCRAM_ARCH=slc5_amd64_gcc462\n')
    outputfile.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n\n')
    outputfile.write('cd /home/uscms208/cms/CMGTools/CMSSW_5_3_14/src/\n')
    outputfile.write('eval `scramv1 runtime -sh` \n')
    outputfile.write('cd /home/uscms208/cms/RazorCombinedFit_Git\n')

    outputfile.write("source setup.sh\n\n")
    outputfile.write("mkdir -p %s\n" % results_dir)
    outputfile.write("mkdir -p %s \n" % toy_dir)
    outputfile.write("mkdir -p %s \n\n" % ffDir)
    if True:  # doToys:
        outputfile.write(('python scripts/runAnalysis.py -a SingleBoxFit '
                          '-c %s %s --fit-region %s -i %s --save-toys-from-fit '
                          '%s -t %i --toy-offset %i -b --fitmode %s\n\n') %\
                          (config, dataset_map[datasetName], sideband,\
                          fit_result_map[datasetName], toy_dir,\
                          int(nToysPerJob), int(t*nToysPerJob), fitmode))
    if doConvertToRoot:
        outputfile.write(('python scripts/convertToyToROOT.py %s/frtoydata_%s '
                          '--start=%i --end=%i -b \n') %(toy_dir, box,\
                          int(t*nToysPerJob), int(t*nToysPerJob)+nToysPerJob))
    if True:  # doFinalJob:
        outputfile.write("rm -f %s.txt \n" %(toy_dir))
        outputfile.write("ls %s/frtoydata*.root > %s.txt \n\n" %\
                         (toy_dir, toy_dir))
        outputfile.write(('# python scripts/expectedYield_sigbin.py 1 '
                          '%s/expected_sigbin_%s.root %s %s.txt %s %s -b \n\n')\
                         % (ffDir, box, box, toy_dir, tagFR, tag3D))
        outputfile.write(('# python scripts/makeToyPVALUE_sigbin.py %s '
                          '%s/expected_sigbin_%s.root %s %s %s %s %s -b \n\n')\
                          %(box, ffDir, box, fit_result_map[datasetName],\
                            ffDir, tagFR, tag3D, tagPrintPlots))
        if datasetName.find("Run") != -1:
            outputfile.write(('# python scripts/make1DProj.py %s'
                              '%s/expected_sigbin_%s.root %s %s %s %s %s'
                              '-Label=%s_%s_%s -b \n') % (box, ffDir, box,\
                             fit_result_map[datasetName], ffDir, tagFR, tag3D,\
                             tagPrintPlots, datasetName, sideband, box))
        else:
            outputfile.write(('# python scripts/make1DProj.py %s '
                              '%s/expected_sigbin_%s.root %s %s -MC=%s %s %s %s'
                              ' -Label=%s_%s_%s -b \n') % (box, ffDir, box,\
                              fit_result_map[datasetName], ffDir, datasetName,\
                              tagFR, tag3D, tagPrintPlots, datasetName,\
                              sideband, box))

    outputfile.close

    return output_file, ffDir, pwd

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "\nRun the script as follows:\n"
        print "python scripts/runToys DatasetName BoxName FitRegion"
        print "with:"
        print (" DatasetName = name of the sample (TTJets, WJets, SMCocktail,"
               "MuHad-Run2012ABCD, Parked_3Comps, etc)")
        print " BoxName = name of the Box (MuMu, MuEle, etc, or All)"
        print " FitRegion = name of the fit region (FULL, Sideband, or All)"
        print ""
        print "After the inputs you can specify the following options"
        print "--t=number of toys"
        sys.exit()

    datasetName = sys.argv[1]
    box = sys.argv[2]
    sideband = sys.argv[3]
    # fitmode = sys.argv[4]
    fitmode = '3D'
    nToys = 1000
    nJobs = 1

    for i in range(4, len(sys.argv)):
        if sys.argv[i].find("--t=") != -1:
            nToys = int(sys.argv[i].replace("--t=", ""))
        if sys.argv[i].find("--j=") != -1:
            nJobs = int(sys.argv[i].replace("--j=", ""))

    boxNames = [sys.argv[2]]

    if sys.argv[3] == 'All':
        sidebandNames = ['Sideband', 'FULL']
    else:
        sidebandNames = [sys.argv[3]]

    nToysPerJob = int(nToys/nJobs)
    totalJobs = 0
    nJobsByBox = {}
    for box in boxNames:
        for sideband in sidebandNames:
            results_dir = "./toys_files_%s"\
                        % datasetName
            toy_dir = results_dir+"/%s_%s"%(sideband, box)
            ffDir = toy_dir+"_FF"
            fullSetToys = ["%s/frtoydata_%s_%i.txt"%(toy_dir, box, i)\
                           for i in xrange(0, nToys)]
            fullSetRoot = ["%s/frtoydata_%s_%i.root"%(toy_dir, box, i)\
                           for i in xrange(0, nToys)]

            allToys = glob.glob("%s/*.txt"%(toy_dir))
            allRoot = glob.glob("%s/*.root"%(toy_dir))
            doFinalJob = (len(allToys) == nToys and len(allRoot) == nToys)
            doFinalJob = False

            nJobsByBox[(box, sideband)] = nJobs
            if doFinalJob:
                nJobsByBox[(box, sideband)] = 1
                missingToys = set([])
                missingRoot = set([])
            else:
                missingToys = set(fullSetToys) - set(allToys)
                missingRoot = set(fullSetRoot) - set(allRoot)

            if glob.glob("%s/expected_sigbin_%s.root"%(ffDir, box)):
                doFinalJob = False

            for t in xrange(0, nJobsByBox[(box, sideband)]):
                doToys = False
                doConvertToRoot = False
                for i in xrange(int(t*nToysPerJob), int((t+1)*nToysPerJob)):
                    if "%s/frtoydata_%s_%i.txt"%(toy_dir, box, i)\
                        in missingToys:
                        doToys = True
                    if "%s/frtoydata_%s_%i.root"%(toy_dir, box, i)\
                        in missingRoot:
                        doConvertToRoot = True

                if True:  # doFinalJob or doToys or doConvertToRoot:
                    output_name, ffDir, pwd = writeBashScript(box, sideband,\
                        fitmode, nToys, nToysPerJob, t, doToys,\
                        doConvertToRoot, doFinalJob)
                    totalJobs += 1
                    #time.sleep(3)
                    os.system("echo qsub " + pwd + "/" + output_name + " -o " +\
                        pwd + "/" + ffDir + "/log_"+str(t)+".log")
                    # os.system("qsub -o "+pwd+"/"+ffDir+"/log_"+str(t)+\
                    #           ".log source "+pwd+"/"+output_name)

    print "TOTAL JOBS IS %i" % totalJobs
