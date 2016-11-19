/**
 * \file GBDTanalysis.h
 *
 * \ingroup GBDTprotonPackage
 *
 * \brief Class def header for a class GBDTanalysis
 *
 * @author erezcohen
 */

/** \addtogroup GBDTprotonPackage
 
 @{*/
#ifndef GBDTANALYSIS_H
#define GBDTANALYSIS_H

#include <iostream>
#include "../../mySoftware/MySoftwarePackage/myIncludes.h"

/**
 \class GBDTanalysis
 User defined class GBDTanalysis ... these comments are used to generate
 doxygen documentation!
 */
class GBDTanalysis{
    
public:
    
    /// Default constructor
    GBDTanalysis (TTree * fInTree, Int_t fdebug);
    ~GBDTanalysis(){}
    
    std::vector<Int_t> GetRSE (Int_t i);
    void        SetInTree (TTree * tree)    {InTree = tree;};
    void         SetDebug (int _debug)      {debug = _debug;};

    void    InitInputTree ();

    
    
    TTree * InTree;
    
    
    
    Int_t   run , subrun    , event;
    Int_t   debug;
};

#endif
/** @} */ // end of doxygen group

