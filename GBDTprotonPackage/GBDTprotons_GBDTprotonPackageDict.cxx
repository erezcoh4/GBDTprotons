// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME GBDTprotons_GBDTprotonPackageDict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments

// Header files passed via #pragma extra_include

namespace {
  void TriggerDictionaryInitialization_libGBDTprotons_GBDTprotonPackage_Impl() {
    static const char* headers[] = {
0
    };
    static const char* includePaths[] = {
"/Users/erezcohen/root6/root-6.04.10/include",
"/Users/erezcohen/larlite/UserDev/GBDTprotons/GBDTprotonPackage/",
0
    };
    static const char* fwdDeclCode = 
R"DICTFWDDCLS(
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libGBDTprotons_GBDTprotonPackage",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libGBDTprotons_GBDTprotonPackage_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libGBDTprotons_GBDTprotonPackage_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libGBDTprotons_GBDTprotonPackage() {
  TriggerDictionaryInitialization_libGBDTprotons_GBDTprotonPackage_Impl();
}
