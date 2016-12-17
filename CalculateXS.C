#include "TFile.h"
#include "TH1D.h"
#include "TSpectrum.h"
#include "TCanvas.h"
#include <iostream>

void CalculateEventNumber(){
  //TFile rightFile("Right_Det.root");
  TFile* leftFile=TFile::Open("Left_Det.root");
  TFile* outFile=TFile::Open("out.root","RECREATE");
  TSpectrum peakfinder(10);
  outFile->cd();
  auto Left_Det=(TCanvas*)leftFile->Get("Left_Det");
  auto hAmpl0Sub3=(TH1D*)Left_Det->FindObject("hAmpl0Sub3")->Clone();
  peakfinder.Search(hAmpl0Sub3,2,"",0.10);
  Double_t peakX=peakfinder.GetPositionX()[0];
  Double_t peakY=peakfinder.GetPositionY()[0];
  Int_t lowBin=hAmpl0Sub3->GetXaxis()->FindBin(peakX*0.9);
  Int_t sum=0;
  //TF1* fitfunc=new TF1("gaus","gaus",0.95*peakX,1.05*peakX);
  for(Int_t iBin=lowBin;iBin<hAmpl0Sub3->GetNbinsX();iBin++){
    sum+=hAmpl0Sub3->GetBinContent(iBin);
  }
  //fitfunc->SetParameter(0,peakY);
  //fitfunc->FixParameter(1,peakX);
  //fitfunc->SetParameter(2,10);
  //hAmpl0Sub3->Fit(fitfunc,"RM");
  std::cout<<peakX<<" "<<hAmpl0Sub3->GetEntries()<<" "<<sum<<"\n";
  hAmpl0Sub3->Draw();
}
