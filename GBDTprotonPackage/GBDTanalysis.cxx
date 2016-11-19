#ifndef GBDTANALYSIS_CXX
#define GBDTANALYSIS_CXX

#include "GBDTanalysis.h"


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
GBDTanalysis::GBDTanalysis(TTree * fInTree, Int_t fdebug){
    SetInTree(fInTree);
    SetDebug(fdebug);
    InitInputTree();
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GBDTanalysis::InitInputTree(){
    if (debug > 2) InTree -> Print();
    InTree -> SetBranchAddress("run"    , &run);
    InTree -> SetBranchAddress("subrun" , &subrun);
    InTree -> SetBranchAddress("event"  , &event);
    if (debug > 2) Printf("GBDTanalysis::InitInputTree() completed");
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
std::vector<Int_t> GBDTanalysis::GetRSE (Int_t i){
    InTree -> GetEntry(i);
    std::vector<Int_t> RSE = {run , subrun , event};
    if (debug > 2) {
        SHOW3(run,subrun,event);
    }
    return RSE;
}


#endif
