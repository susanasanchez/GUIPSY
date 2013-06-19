#!/usr/bin/env python
from gipsy import *

init()

s = Set(usertext("INSET=", "Set,subset(s): "))

for subset in s.subsets:
   anyout( "mean of subset" + " = " + str(s.subimage(subset).mean()) )

finis()
