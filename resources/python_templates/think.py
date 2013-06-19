#!/usr/bin/env python

from gipsy import *
import time, random

init()
inset = usertext('inset=')
delay = 2.0*random.random()+1.0
anyout('Start thinking about set "%s".' % inset)
time.sleep(delay)                                # simulate processing
if random.random()<0.1:                          # simulate 10% failure
   error(4, 'couldn\'t think about set "%s" anymore' % inset)
anyout('%s thought about set "%s" during %g seconds.'
        % (myname(), inset, delay))
finis()
