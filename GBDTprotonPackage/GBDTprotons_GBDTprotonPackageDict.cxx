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
#include "GBDTanalysis.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *GBDTanalysis_Dictionary();
   static void GBDTanalysis_TClassManip(TClass*);
   static void delete_GBDTanalysis(void *p);
   static void deleteArray_GBDTanalysis(void *p);
   static void destruct_GBDTanalysis(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::GBDTanalysis*)
   {
      ::GBDTanalysis *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::GBDTanalysis));
      static ::ROOT::TGenericClassInfo 
         instance("GBDTanalysis", "GBDTanalysis.h", 25,
                  typeid(::GBDTanalysis), DefineBehavior(ptr, ptr),
                  &GBDTanalysis_Dictionary, isa_proxy, 4,
                  sizeof(::GBDTanalysis) );
      instance.SetDelete(&delete_GBDTanalysis);
      instance.SetDeleteArray(&deleteArray_GBDTanalysis);
      instance.SetDestructor(&destruct_GBDTanalysis);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::GBDTanalysis*)
   {
      return GenerateInitInstanceLocal((::GBDTanalysis*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::GBDTanalysis*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *GBDTanalysis_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::GBDTanalysis*)0x0)->GetClass();
      GBDTanalysis_TClassManip(theClass);
   return theClass;
   }

   static void GBDTanalysis_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrapper around operator delete
   static void delete_GBDTanalysis(void *p) {
      delete ((::GBDTanalysis*)p);
   }
   static void deleteArray_GBDTanalysis(void *p) {
      delete [] ((::GBDTanalysis*)p);
   }
   static void destruct_GBDTanalysis(void *p) {
      typedef ::GBDTanalysis current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::GBDTanalysis

namespace {
  void TriggerDictionaryInitialization_libGBDTprotons_GBDTprotonPackage_Impl() {
    static const char* headers[] = {
"GBDTanalysis.h",
0
    };
    static const char* includePaths[] = {
"/home/erez/larlite/UserDev/mySoftware",
"/home/erez/larlite/UserDev/MyLarLite/MyPackage",
"/home/erez/larlite/UserDev/AnalysisTreesInformation/AnaTreesPackage",
"/home/erez/larlite/core",
"/usr/local/root/include/root",
"/home/erez/larlite/UserDev/GBDTprotons/GBDTprotonPackage/",
0
    };
    static const char* fwdDeclCode = 
R"DICTFWDDCLS(
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$GBDTanalysis.h")))  GBDTanalysis;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "GBDTanalysis.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"GBDTanalysis", payloadCode, "@",
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
