#!/usr/bin/env python
from gipsy import *

def runjob():
   if work:
      subset  = work.pop(0)             # get next subset to be processed
      job     = inactive.pop(0)         # obtain free job identifier ...
      active.append(job)                # ... and put it in the active list
      jobname = 'job%d' % job           # job name (and job keyword)
      KeyCallback(jobdone, jobname, subset=subset, job=job)
                                        # schedule task completion callback
      xeq('%s(think) inset=%s %d' % (jobname, inset, subset), jobname)
                                        # start task and continue

def jobdone(cb):
    active.remove(cb.job)               # move job identifier from active ...
    inactive.append(cb.job)             # ... to inactive list
    fate = userint(cb.key)              # read task's exit status ...
    if fate<0:                          # ... and in case of failure ...
       failed.append(cb.subset)         # ... register subset number
    runjob()                            # start next job
    cb.deschedule()                     # deschedule this job's callback

init()

inset  = usertext("INSET=", "Input set name")
work   = userint("SUBSETS=", "Subset numbers", nmax=1000)
npar   = userint("NPAR=", "Number of parallel jobs")

failed   = []                           # list of subsets which failed
active   = []                           # job identifiers in use
inactive = range(npar)                  # available job identifiers

while inactive:                         # start the first 'npar' jobs
   runjob()

mainloop()                              # event loop: returns when there ...
                                        # ... are no scheduled callbacks left
if failed:
   anyout("Subset(s) failed: %s" % repr(failed))

finis()   
