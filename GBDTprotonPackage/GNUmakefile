# GBDTprotonPackage

# specific names for this package
DICT  = GBDTprotons_GBDTprotonPackageDict
SHLIB = libGBDTprotons_GBDTprotonPackage.so
SOURCES = $(filter-out $(DICT).cxx, $(wildcard *.cxx))
FMWK_HEADERS = LinkDef.h $(DICT).h
HEADERS = $(filter-out $(FMWK_HEADERS), $(wildcard *.h))
OBJECTS = $(SOURCES:.cxx=.o)

# include options for this package
INCFLAGS  = -I.                       #Include itself
INCFLAGS += -I$(LARLITE_USERDEVDIR)/mySoftware
INCFLAGS += -I$(LARLITE_USERDEVDIR)/MyLarLite/MyPackage
INCFLAGS += -I$(LARLITE_USERDEVDIR)/AnalysisTreesInformation/AnaTreesPackage
INCFLAGS += $(shell larlite-config --includes)

# platform-specific options
OSNAME          = $(shell uname -s)
HOST            = $(shell uname -n)
OSNAMEMODE      = $(OSNAME)

# call kernel specific compiler setup
include $(LARLITE_BASEDIR)/Makefile/Makefile.${OSNAME}

# call the common GNUmakefile
LDFLAGS += $(shell larlite-config --libs)
LDFLAGS += -L$(LARLITE_LIBDIR) -lAnalysisTreesInformation_AnaTreesPackage
include $(LARLITE_BASEDIR)/Makefile/GNUmakefile.CORE
