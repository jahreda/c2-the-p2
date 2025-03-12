#include <vector>
#include <cstdio> 
#include <iostream> 

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TFrame.h"
#include "TH1F.h"
#include "TBenchmark.h"
#include "TRandom.h"
#include "TSystem.h"
#include "TTreePerfStats.h"

//Originally authored by the ROOT Team: https://root.cern/doc/master/hvector_8C.html

int ntodo = 10;

void read(char *fin, char *fout)
{

   TH1F *hdisk = new TH1F("hdisk","hdisk",500,0,100);   

   for (int iter = 0; iter < ntodo; iter++) {
      TFile *f = TFile::Open(fin,"READ");
      if (!f) { return; }
     

      TTree *t; f->GetObject("tvec",t);
      int N = t->GetEntries();
      
      std::vector<float> *vpx = 0;
      std::vector<float> *vpy = 0;
      std::vector<float> *vpz = 0;
      std::vector<float> *vpt = 0;
      std::vector<float> *vint = 0;      
      
      TTreePerfStats* myIOStats = new TTreePerfStats("IOPerfStats", t);
      
      TBranch *bvpx = 0;
      t->SetBranchAddress("vpx",&vpx,&bvpx);
      
      TBranch *bvpy = 0;
      t->SetBranchAddress("vpy",&vpy,&bvpy);
      
      TBranch *bvpz = 0;
      t->SetBranchAddress("vpz",&vpz,&bvpz);
      
      TBranch *bvpt = 0;
      t->SetBranchAddress("vpt",&vpt,&bvpt);
      
      TBranch *bvint = 0;
      t->SetBranchAddress("vint",&vint,&bvint);
      
      
      for (Int_t i = 0; i < N; i++) {
         Long64_t tentry = t->LoadTree(i);
         bvpx->GetEntry(tentry);
         bvpy->GetEntry(tentry);
         bvpz->GetEntry(tentry);
         bvpt->GetEntry(tentry);
         bvint->GetEntry(tentry);            
      
	 // Monitor Progress
	 if(i%10000==0 & iter > 0) {
	     std::cerr << "\rLOOP [read()] iter = " << iter <<", i = " << i << " / " << N << std::flush;
	 }
      }

      hdisk->Fill(myIOStats->GetDiskTime());
      // Since we passed the address of a local variable we need
      // to remove it.
      t->ResetBranchAddresses();
      if (iter == 0) { 
	      std::cerr << std::endl;
	      myIOStats->SaveAs(fout); // save only once
      }
      f->Close();
   }
   std::cerr << std::endl;
   std::cerr << "Disk Mean = " << hdisk->GetMean() << " and RMS/sqrt(N) = " << hdisk->GetRMS()/sqrt(ntodo) << std::endl;   
   delete hdisk;
}
 
 
int main()
{
   int N = 1e8; // match this with N in writeROOTFile.cpp
   std::vector<int> flushes;
   flushes.emplace_back(0);
   flushes.emplace_back(-30000000);
   flushes.emplace_back(-1000000);
   flushes.emplace_back(1e4);
   flushes.emplace_back(1e2);   
   for (auto flush : flushes) {
   
      gBenchmark = new TBenchmark();
      // Timed read()
      gBenchmark->Start("read_hvector");
      std::cerr << std::endl;
      std::cerr << "<==== Flush Setting: @ " << flush << "====>" << std::endl;
      char *fname_in=Form("hvector_%d_%d_50.root",N,flush);
      char *fname_out=Form("stats_%d_%d_50.root",N,flush);            
      read(fname_in,fname_out);
      gBenchmark->Show("read_hvector");
      delete gBenchmark;
   }
   
   return 0;
}
