#include <vector>
 
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TFrame.h"
#include "TH1F.h"
#include "TBenchmark.h"
#include "TRandom.h"
#include "TSystem.h"

//Originally authored by the ROOT Team: https://root.cern/doc/master/hvector_8C.html


void write(int N=1e8, int autoflush=-30000000, int vecsize=50) // that is the default autoflush value 
{
 
   TFile *f = TFile::Open(Form("hvector_%d_%d_%d.root",N,autoflush,vecsize), "RECREATE");
 
   if (!f) { return; }
 
   std::vector<float> vpx;
   std::vector<float> vpy;
   std::vector<float> vpz;
   std::vector<float> vpt;   
   std::vector<int> vint;
 
   // Create a TTree
   TTree *t = new TTree("tvec","Tree with vectors");
   t->SetAutoFlush(autoflush);
   t->Branch("vpx",&vpx);
   t->Branch("vpy",&vpy);
   t->Branch("vpz",&vpz);   
   t->Branch("vpt",&vpt);
   t->Branch("vint",&vint);   
 
   gRandom->SetSeed();
   for (Int_t i = 0; i < N; i++) {
      Int_t npx = (Int_t)(gRandom->Rndm(1)*vecsize);
 
      vpx.clear();
      vpy.clear();
      vpz.clear();
      vpt.clear();
      vint.clear();            
 
      for (Int_t j = 0; j < npx; ++j) {
 
         Float_t px,py,pz,pt;
         Int_t integer;
         gRandom->Rannor(px,py);
         pt = sqrt(px*px + py*py);
         pz = gRandom->Rndm(1);
         integer = (int)(gRandom->Rndm(1)*npx + npx);
 
         vpx.emplace_back(px);
         vpy.emplace_back(py);
         vpz.emplace_back(pz);
         
         /// this gets pushed back twice on purpose
         vpt.emplace_back(pt);
         vpt.emplace_back(pt);         
         vint.emplace_back(integer);         
 
      }
      t->Fill();
   }
   
   t->Print();
   f->Write();
   
   delete f;
}
 
 
 
int main()
{
   int N = 1e7;
   int vecsize=50;
   std::vector<int> flushes;
   flushes.emplace_back(0);
   flushes.emplace_back(-30000000);
   flushes.emplace_back(-1000000);
   flushes.emplace_back(1e4);
   flushes.emplace_back(1e2);   

   // Timed write()
   for (auto flush : flushes) {
      std::cerr << "JAA doing flush = " << flush << " and N = " << N << " and vec size = " << vecsize << std::endl;
      gBenchmark = new TBenchmark();
      gBenchmark->Start(Form("write_hvector_%d_%d_%d",N,flush,vecsize));
      write(N, flush);  
      delete gBenchmark;
   }

   return 0;
}
