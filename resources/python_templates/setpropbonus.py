   n = s.ndims( subset=True )
   anyout( "dimension of the subsets is: %s" % n )

   # use the axis permutation 'k' to get the axis name
   for k in s.axperm('inside'):
      anyout("subset axis name         : %s" % str(s.axname(k)))
   for k in s.axperm('outside'):
      anyout("repeat axis name         : %s" % str(s.axname(k)))
