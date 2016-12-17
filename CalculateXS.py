#!/usr/bin/env python
from ROOT import TSpectrum,TCanvas,TH1D,TFile,TLine
from scipy.constants import N_A
#Number of triggers=>integrated flux. Should be obtained from unsubtracted histogram
flux=(60+5)*60/20*5e8
rho=2.2 #g/cm3 carbon density => to be verified
Mmol=12.011 #g/mol cargon molar mass
d=1 #cm target thickness
Nt=rho*N_A/12.011*d
#solid angle of one detector elements
dOmega=0.8997975532e-3
#histo name prefix
#pre=hAmplitude
pre="hAmpl0Sub"
def getEvents(histo,thresh=0.9,niter=20):
    pf=TSpectrum(100)    
    pf.Clear()
    pf.Search(histo,10,"",0.3)
    peakX,peakY=pf.GetPositionX(),pf.GetPositionY()
    pos=[]
    for i in range(pf.GetNPeaks()):
        pos.append(peakX[i])
    pos.sort()
    lowEdge=histo.GetXaxis().FindBin(thresh*pos[-1])
    sum=0
    for iBin in range(lowEdge,histo.GetNbinsX()):
        sum+=histo.GetBinContent(iBin)
    return sum

def main():
    sigma=0
    for dir in ["Left","Righ"]:
        infile=TFile(dir+"_Det.root")
        canvas=infile.Get(dir+"_Det")
        suf=[]
        if dir=="Left":
            suf=range(1,7)+range(25,31)
        else:
            suf=range(9,15)+range(17,23)
        outfile=TFile(dir+"_out.root","RECREATE")
        outfile.cd()
        for s in suf:
            hAmp=canvas.FindObject("hAmpl0Sub"+str(s))
            #flux+=hAmp.GetEntries()
            hAmp.SetDirectory(outfile)
            n=getEvents(hAmp)
            sigma+=n/(Nt*flux*dOmega)*10**27
            print pre+str(s)+": {:2f} mb".format(n/(Nt*flux*dOmega)*10**27)
            hAmp.Write()
    print "sigma_tot={:2f} mb".format(sigma) 
if __name__=="__main__":
    main()
   
   
