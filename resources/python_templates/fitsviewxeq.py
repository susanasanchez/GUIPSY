#!/usr/bin/env python
from gipsy import *

init()

fitsfile = "file000001.mt"             # Set a default name for an fits file
fitsfile = usertext("FITSFILE=",
                    "Enter name of fits file:  [%s]" % fitsfile, defval=fitsfile)

# If the fits file you entered does not exist, then ens this program 
# in the GIPSY way e.g. call the 'finis' function
if not os.path.exists(fitsfile):
   anyout(">>>>>>> WARNING: Cannot find %s <<<<<<<<" % fitsfile)
   finis()


# Get a name for a GIPSY set to store the fits data in gds format
outputset = "gipsyset"
outputset = usertext("GIPSYSET=",
                     "Enter name of output set: [%s]" % outputset, 1, outputset)
try:
   s = Set(outputset)
except:
   pass
else:
   s.delete()
   del s


xeq("RFITS AUTO=Y FITSFILE=%s; INFILES=0; OUTSET=%s" % (fitsfile, outputset) )
xeq("VIEW INSET=%s CLIP=" % outputset)

finis()
