#!/usr/bin/env python
from gipsy import *

init()

s = Set(usertext("SET=", "Set, subset"), write=True)
anyout("blo= %s, bhi= %s" % (s.blo, s.bhi))

while True:
   b = usertext("BOX=", "Give box", defval='', default=1)
   cancel("BOX=")
   s.setbox(b)
   i = s.subimage(s.subsets[0])
   anyout(str(i.shape))
   anyout("blo= %s, bhi= %s" % (s.blo, s.bhi))
   v = userreal("VALUE=", "Give value")
   i[:] = v

finis()
