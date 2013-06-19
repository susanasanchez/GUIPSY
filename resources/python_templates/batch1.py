#!/usr/bin/env python
from gipsy import *

init()

inset  = usertext("INSET=", "Input set name")
work   = userint("SUBSETS=", "Subset numbers", nmax=1000)

failed = []                           # list of subsets which failed

for subset in work:
   try:
      xeq('think inset=%s %d' % (inset, subset)) # start and wait for completion
   except:                                       # in case of failure ...
      failed.append(subset)                      # ... register subset number

if failed:
   anyout("Subset(s) failed: %s" % repr(failed))

finis()   
